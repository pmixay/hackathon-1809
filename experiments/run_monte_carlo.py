"""EXP-10: seeded, conditional Monte Carlo of fixed P3 protections (no re-planning).

Common random numbers compare three plans in MANDATORY_STRESS. The independent
model and the comonotonic demand/ISRU diagnostic are reported separately.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
import random
from collections import Counter
from dataclasses import asdict
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from statistics import NormalDist

from common import ASSUMPTIONS, CASE_DIR, PLANS, RESULTS, ROOT, load_all, scenario
from run_protection_measures import early_zbo_plan, inventory_plan
from run_reverse_stress import SERVICE_RULES, YEARS, failure_violations, shocked_scenario
from terraplan import __version__
from terraplan.engine import EPS, TOL_T, simulate
from terraplan.plan import load_plan
from terraplan.scenario import scenario_from_dict

DEFAULT_N = 10_000
DEFAULT_SEED = 203510
MODES = ("independent", "comonotonic_demand_isru")
METRICS = ("shortage_t", "critical_shortage_t", "min_service_total", "min_service_critical",
           "max_reserve_gap_t", "pv_cost_mln", "delta_pv_mln")


def sample_factors(n, seed, assumptions):
    """Three random() calls per realization: demand, ISRU, price, in that order.

    The diagnostic reuses demand's uniform for ISRU; it consumes no extra draws.
    Store both latent uniforms and physical factors at full float precision.
    """
    if isinstance(n, bool) or not isinstance(n, int) or n < 1:
        raise ValueError("n must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("seed must be a nonnegative integer")
    for key in ("exp10_demand_max", "exp10_isru_reduction_max", "exp10_price_half_range"):
        value = assumptions.get(key)
        if not isinstance(value, (float, int)) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError(f"{key} must be finite and in [0, 1]")
    rng = random.Random(seed)
    rows = []
    for i in range(1, n + 1):
        u, v, w = rng.random(), rng.random(), rng.random()
        rows.append(dict(sample_id=i, u_demand=u, u_isru=v, u_price=w,
                         demand_increase=u * assumptions.exp10_demand_max,
                         isru_reduction=v * assumptions.exp10_isru_reduction_max,
                         coupled_isru_reduction=u * assumptions.exp10_isru_reduction_max,
                         price_deviation=(2 * w - 1) * assumptions.exp10_price_half_range))
    return rows


def sample_scenario(stress, case, sample, mode):
    if mode not in MODES:
        raise ValueError(f"unknown dependence mode: {mode}")
    reduction = sample["isru_reduction" if mode == "independent" else "coupled_isru_reduction"]
    data = shocked_scenario(stress, case, sample["demand_increase"], reduction).to_dict()
    p = sample["price_deviation"]
    if not math.isfinite(p) or p < -1:
        raise ValueError("price_deviation must be finite and >= -1")
    data.update(scenario_id=f"TEAM_MC_{mode}_{sample['sample_id']:05d}",
                label=f"EXP-10 / {mode} / sample {sample['sample_id']}")
    data["variable_price_multiplier"] = {
        sid: {y: stress.price_mult(source, y) * (1 + p if sid in ("A", "B") and y in (2038, 2039) else 1)
              for y in case.years} for sid, source in case.sources.items()}
    data["changes"][-1].update(experiment="EXP-10", dependence=mode,
                               price_deviation=p, price_sources=["A", "B"], price_years=[2038, 2039])
    return scenario_from_dict(data)


def protection_plans(case):
    original = load_plan(PLANS / "P3_isru_zbo_adapted.json", case)
    return dict(without_measure=original,
                physical_stock=inventory_plan(original, case, 8.6),
                early_zbo_plus_stock=inventory_plan(early_zbo_plan(original, 18), case, 0.1))


def result_row(result, mode, sample_id, variant):
    failures = failure_violations(result)
    # Use the EXP-07 convention: undated first, annual checks in December.
    date = lambda v: (v.year or 0, v.month or 12)
    first = [v for v in failures if date(v) == date(failures[0])] if failures else []
    rules = {v.rule_id for v in failures}
    return dict(mode=mode, sample_id=sample_id, variant=variant, failed=bool(failures),
                reserve_failed="RESERVE_45D" in rules, service_failed=bool(rules & SERVICE_RULES),
                shortage_occurred=result.kpi["shortage_total_t"] > TOL_T,
                failure_rules=";".join(sorted(rules)),
                first_year=date(first[0])[0] if first else None,
                first_month=date(first[0])[1] if first else None,
                first_rules=";".join(sorted({v.rule_id for v in first})),
                first_violations=json.dumps([asdict(v) for v in first], ensure_ascii=False, sort_keys=True),
                shortage_t=result.kpi["shortage_total_t"],
                critical_shortage_t=result.kpi["shortage_critical_t"],
                min_service_total=result.kpi["min_service_level_total"],
                min_service_critical=result.kpi["min_service_level_critical"],
                max_reserve_gap_t=max(max(0.0, y.reserve_required_t - y.opening_t) for y in result.years),
                pv_cost_mln=result.kpi["pv_cost_mln"])


def wilson_interval(k, n):
    """Two-sided 95% Wilson score interval, including k=0 and k=n."""
    if n < 1 or not 0 <= k <= n:
        raise ValueError("Wilson interval requires n > 0 and 0 <= k <= n")
    z = NormalDist().inv_cdf(0.975)
    p, z2 = k / n, z * z
    center = (p + z2 / (2 * n)) / (1 + z2 / n)
    half = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / (1 + z2 / n)
    return [max(0.0, center - half), min(1.0, center + half)]


def metric_summary(values):
    """Quantiles use linear interpolation at (n-1)*q (Hyndman-Fan type 7)."""
    values = sorted(values)
    def quantile(q):
        idx = (len(values) - 1) * q
        lo, hi = math.floor(idx), math.ceil(idx)
        return values[lo] + (values[hi] - values[lo]) * (idx - lo)
    return dict(mean=math.fsum(values) / len(values), min=values[0], max=values[-1],
                p05=quantile(0.05), p50=quantile(0.5), p95=quantile(0.95))


def summarize(rows):
    summaries = []
    for mode in MODES:
        baseline = {r["sample_id"]: r for r in rows if r["mode"] == mode and r["variant"] == "without_measure"}
        for variant in ("without_measure", "physical_stock", "early_zbo_plus_stock"):
            group = [r for r in rows if r["mode"] == mode and r["variant"] == variant]
            n = len(group)
            count = sum(r["failed"] for r in group)
            eliminated = sum(baseline[r["sample_id"]]["failed"] and not r["failed"] for r in group)
            introduced = sum(not baseline[r["sample_id"]]["failed"] and r["failed"] for r in group)
            first_counts = Counter((r["first_year"], r["first_month"], r["first_rules"]) for r in group if r["failed"])
            summaries.append(dict(
                mode=mode, variant=variant, n=n, failures=count, failure_frequency=count / n,
                failure_wilson95=wilson_interval(count, n),
                reserve_failure_frequency=sum(r["reserve_failed"] for r in group) / n,
                service_failure_frequency=sum(r["service_failed"] for r in group) / n,
                shortage_frequency=sum(r["shortage_occurred"] for r in group) / n,
                failure_rule_counts=dict(sorted(Counter(rule for r in group for rule in r["failure_rules"].split(";") if rule).items())),
                first_failure_counts=[dict(year=y, month=m, rules=rules, count=c)
                                      for (y, m, rules), c in sorted(first_counts.items())],
                eliminated_failures=eliminated, introduced_failures=introduced,
                eliminated_frequency=eliminated / n,
                failure_reduction_pp=100 * (eliminated - introduced) / n,
                metrics={key: metric_summary([r[key] for r in group]) for key in METRICS}))
    return summaries


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def package_versions():
    versions = {}
    for name in ("PyYAML", "openpyxl", "pytest"):
        try:
            versions[name] = version(name)
        except PackageNotFoundError:
            versions[name] = None
    return versions


def analyze(n=DEFAULT_N, seed=DEFAULT_SEED, replay_samples=None):
    case, assumptions = load_all()
    stress = scenario("MANDATORY_STRESS")
    plans = protection_plans(case)
    samples = sample_factors(n, seed, assumptions)
    if replay_samples is not None:
        with Path(replay_samples).open(encoding="utf-8", newline="") as f:
            replay = [{k: int(v) if k == "sample_id" else float(v) for k, v in row.items()}
                      for row in csv.DictReader(f)]
        if replay != samples:
            raise ValueError("replay samples do not match n, seed and current factor assumptions")
        samples = replay
    reference = []
    for name, plan in plans.items():
        row = result_row(simulate(case, plan, stress, assumptions), "reference", 0, name)
        if row["failed"]:
            raise ValueError(f"reference plan {name} fails before additional shocks")
        row["delta_pv_mln"] = row["pv_cost_mln"] - (reference[0]["pv_cost_mln"] if reference else row["pv_cost_mln"])
        reference.append(row)
    rows = []
    for mode in MODES:
        for sample in samples:
            sc = sample_scenario(stress, case, sample, mode)
            baseline_pv = None
            for name, plan in plans.items():
                row = result_row(simulate(case, plan, sc, assumptions), mode, sample["sample_id"], name)
                if baseline_pv is None:
                    baseline_pv = row["pv_cost_mln"]
                row["delta_pv_mln"] = row["pv_cost_mln"] - baseline_pv
                rows.append(row)
    method = dict(
        status="TEAM_ASSUMPTION", reference="MANDATORY_STRESS", n_per_mode=n, random_seed=seed,
        generator="random.Random / MT19937; random() float draws",
        draw_order="sample_id 1..N; u_demand, u_isru, u_price; diagnostic uses u_demand for ISRU",
        demand=dict(distribution="uniform", bounds=[0, assumptions.exp10_demand_max], years=list(YEARS),
                    operation="stress total AND critical demand *= 1+d"),
        isru=dict(distribution="uniform", bounds=[0, assumptions.exp10_isru_reduction_max], years=list(YEARS),
                  operation="stress actual delivery share D *= 1-s; no extra reliability factor"),
        prices=dict(distribution="uniform", bounds=[-assumptions.exp10_price_half_range, assumptions.exp10_price_half_range],
                    years=[2038, 2039], sources=["A", "B"], operation="stress variable price *= 1+p"),
        dependence=dict(independent="d,s,p independent; each persists over its entire period; A/B share p",
                        comonotonic_demand_isru="same uniform for d and s; price independent; separate diagnostic, not pooled"),
        rationale="physical 0..2% brackets the EXP-08 1% target; price +/-10% illustrative; no organizer probability data",
        fixed="all orders, reservations, investments and opening stock; common samples for all three plans",
        excluded="no stochastic Core capacity availability, delays, reaction policy or geopolitics",
        failure="any hard violation OR total/critical service guideline below 97%/99%; warnings excluded",
        first_failure="earliest year/month; annual checks at December, undated year=0; ALL simultaneous causes retained",
        physical_tolerance_t=TOL_T, service_tolerance=EPS, shortage_frequency_threshold_t=TOL_T,
        confidence_interval="two-sided 95% Wilson score for each binomial failure frequency; sampling error only",
        quantiles="linear interpolation at (n-1)*q, Hyndman-Fan type 7",
        costs="engine PV in mln constant-2035 units; paired deltas vs unprotected plan on same realization; no damage valuation",
        limitations="conditional frequencies, not real-world risk probabilities; no proof of robustness in BASE; ZBO lag remains zero")
    paths = [ASSUMPTIONS, PLANS / "P3_isru_zbo_adapted.json", Path(stress.source_file), Path(__file__),
             ROOT / "experiments/common.py", ROOT / "experiments/run_reverse_stress.py",
             ROOT / "experiments/run_protection_measures.py", ROOT / "experiments/run_all.py",
             ROOT / "requirements.txt"]
    paths += sorted(CASE_DIR.glob("*.csv")) + sorted((ROOT / "src/terraplan").glob("*.py"))
    manifest = dict(experiment_id="EXP-10", schema_version=1, method=method,
                    python=platform.python_version(), python_implementation=platform.python_implementation(),
                    terraplan_version=__version__, packages=package_versions(),
                    input_sha256={p.relative_to(ROOT).as_posix(): sha256(p) for p in paths},
                    assumptions=assumptions.entries, reference_scenario=stress.to_dict(),
                    plans={name: plan.to_dict() for name, plan in plans.items()},
                    reproduction=f"python experiments/run_monte_carlo.py --n {n} --seed {seed} --out results/monte_carlo",
                    replay="add --replay-samples <original>/samples.csv --out <other-dir> --compare <original>; compare is byte-for-byte")
    return dict(manifest=manifest, samples=samples, runs=rows,
                report=dict(experiment_id="EXP-10", method=method, reference=reference, comparison=summarize(rows)))


def summary_text(report):
    method = report["method"]
    lines = ["# EXP-10 Conditional Monte Carlo: fixed P3 protections", "",
             f"N={method['n_per_mode']} per dependence model; seed={method['random_seed']}; random.Random / MT19937.",
             f"Background: MANDATORY_STRESS. Demand U(0, {method['demand']['bounds'][1]:.2%}), ISRU reduction U(0, {method['isru']['bounds'][1]:.2%}) in 2038-2040; "
             f"Core/Flex prices +/-{method['prices']['bounds'][1]:.2%} in 2038-2039.",
             "TEAM_ASSUMPTION distributions, not calibrated probabilities. All three plans use the same sample.", "",
             "## No-additional-shock control", "",
             "| Variant | PV, mln | Extra PV, mln | Passes |", "|---|---:|---:|---|"]
    for row in report["reference"]:
        lines.append(f"| {row['variant']} | {row['pv_cost_mln']:.6f} | {row['delta_pv_mln']:.6f} | {not row['failed']} |")
    for mode in MODES:
        group = [s for s in report["comparison"] if s["mode"] == mode]
        lines += ["", f"## {mode}", "",
                  "| Variant | Failures / N | Failure % (95% Wilson) | Reduction, pp | Mean extra PV, mln | Mean PV | PV P5 / P50 / P95 |",
                  "|---|---:|---:|---:|---:|---:|---|"]
        for s in group:
            lo, hi = s["failure_wilson95"]
            pv = s["metrics"]["pv_cost_mln"]
            lines.append(f"| {s['variant']} | {s['failures']} / {s['n']} | {s['failure_frequency']:.2%} ({lo:.2%}, {hi:.2%}) | "
                         f"{s['failure_reduction_pp']:.2f} | {s['metrics']['delta_pv_mln']['mean']:.6f} | {pv['mean']:.6f} | "
                         f"{pv['p05']:.3f} / {pv['p50']:.3f} / {pv['p95']:.3f} |")
        lines += ["", "| Variant | Reserve failure % | Service failure % | Shortage % | Max shortage, t | Worst annual total / critical service | Max reserve gap, t |",
                  "|---|---:|---:|---:|---:|---|---:|"]
        for s in group:
            m = s["metrics"]
            lines.append(f"| {s['variant']} | {s['reserve_failure_frequency']:.2%} | {s['service_failure_frequency']:.2%} | "
                         f"{s['shortage_frequency']:.2%} | {m['shortage_t']['max']:.6f} | "
                         f"{m['min_service_total']['min']:.6%} / {m['min_service_critical']['min']:.6%} | {m['max_reserve_gap_t']['max']:.6f} |")
        lines += ["", "First failure (simultaneous causes kept together):", ""]
        for s in group:
            for first in s["first_failure_counts"]:
                lines.append(f"- {s['variant']}: {first['rules']} @ {first['year']}-{first['month']:02d}: {first['count']} realizations.")
    lines += ["", "## Interpretation and limits", "",
              "- Failure includes reserve compliance, not just unserved demand. Service guidelines count even if Result.feasible is true.",
              "- Physical shocks are persistent, not independent monthly noise. The comonotonic diagnostic is not pooled with the primary independent model.",
              "- Zero/all observed failures do not establish a true probability of zero/one: use the Wilson interval. It excludes model/distribution uncertainty.",
              "- The protections target a 1% uncertainty square, while this experiment samples up to 2%; residual failures are expected.",
              "- Extra PV is computed with minus without protection on EACH common realization. No damages, penalties or avoided-mission-loss benefit is priced.",
              "- The price factor changes PV, not physical feasibility of fixed plans. Extra Flex purchases precede the 2038-2039 price shock.",
              "- Early ZBO retains saved fuel; its advantage depends on zero commissioning lag and the throughput-only loss convention.",
              "- Frequencies are conditional on MANDATORY_STRESS and TEAM_ASSUMPTION ranges; they are not real-world risk probabilities or evidence of BASE feasibility.",
              "- samples.csv retains latent uniforms and both dependence transforms; runs.csv contains every realization, all first causes and paired cost deltas.",
              "- report.json contains reference controls, reason/date counts and mean/min/max/P5/P50/P95 for all severity and cost metrics.",
              "- run_manifest.json records parameters, versions, input/code/output SHA-256, plan/scenario/assumption snapshots. No timestamps or output paths enter its hashes."]
    return "\n".join(lines) + "\n"


def write_report(data, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    files = []
    def write_json(name, obj):
        (out / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        files.append(name)
    def write_csv(name, rows):
        with (out / name).open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
        files.append(name)
    write_csv("samples.csv", data["samples"])
    write_csv("runs.csv", data["runs"])
    report = data["report"]
    comparison = []
    for s in report["comparison"]:
        comparison.append(dict(mode=s["mode"], variant=s["variant"], n=s["n"], failures=s["failures"],
                               failure_frequency=s["failure_frequency"], ci95_low=s["failure_wilson95"][0], ci95_high=s["failure_wilson95"][1],
                               failure_reduction_pp=s["failure_reduction_pp"], eliminated_failures=s["eliminated_failures"],
                               introduced_failures=s["introduced_failures"],
                               **{f"{key}_{stat}": value for key, stats in s["metrics"].items() for stat, value in stats.items()}))
    write_csv("comparison.csv", comparison)
    write_json("report.json", report)
    for name, plan in data["manifest"]["plans"].items():
        write_json(f"{name}.plan.json", plan)
    text = summary_text(report)
    (out / "summary.md").write_text(text, encoding="utf-8")
    files.append("summary.md")
    manifest = dict(data["manifest"], output_sha256={name: sha256(out / name) for name in sorted(files)})
    write_json("run_manifest.json", manifest)
    return text


def compare_outputs(out, original):
    out, original = Path(out), Path(original)
    manifest = json.loads((out / "run_manifest.json").read_text(encoding="utf-8"))
    for name, digest in manifest["output_sha256"].items():
        if sha256(out / name) != digest or sha256(original / name) != digest:
            raise ValueError(f"reproducibility mismatch: {name}")
    if (out / "run_manifest.json").read_bytes() != (original / "run_manifest.json").read_bytes():
        raise ValueError("reproducibility mismatch: run_manifest.json")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=DEFAULT_N)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=RESULTS / "monte_carlo")
    parser.add_argument("--replay-samples", type=Path, help="replay saved CSV, verifying it against declared n/seed/assumptions")
    parser.add_argument("--compare", type=Path, help="verify all output bytes against an earlier run")
    args = parser.parse_args(argv)
    if args.compare and args.compare.resolve() == args.out.resolve():
        parser.error("--compare must differ from --out")
    try:
        data = analyze(args.n, args.seed, args.replay_samples)
        text = write_report(data, args.out)
        if args.compare:
            compare_outputs(args.out, args.compare)
    except ValueError as exc:
        parser.error(str(exc))
    print(text)
    if args.compare:
        print("Reproducibility verified: every artifact and manifest is byte-identical.")


if __name__ == "__main__":
    main()

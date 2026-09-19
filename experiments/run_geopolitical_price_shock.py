"""EXP-11: isolated TEAM Core/Flex price shock, fixed BASE P2z/P3/P4, copied data.

The existing annual scenario overlay applies the surcharge exactly once. Case CSVs
are copied unchanged: their single price column cannot express a two-year window.
No CASE_INPUT, global assumptions, plans or engine files are rewritten.
"""
from __future__ import annotations

import argparse
import csv
import json
import platform
import shutil
from dataclasses import asdict
from pathlib import Path

from common import ASSUMPTIONS, CASE_DIR, PLANS, RESULTS, ROOT, SCENARIOS
from provenance import HASH_FORMAT, SCHEMA_VERSION, input_hashes, sha256, verify_saved, write_json, write_text
from terraplan.assumptions import load_assumptions
from terraplan.case import load_case
from terraplan.engine import simulate
from terraplan.export import kpi_hash, write_results
from terraplan.plan import load_plan
from terraplan.scenario import load_scenario

PLAN_IDS = ("P2z_earth_new_zbo", "P3_isru_zbo", "P4_full")
SHOCK_PATH = SCENARIOS / "team_geopolitical_price_shock.yaml"
DEFAULT_OUT = RESULTS / "geopolitical_price_shock"


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def prepare_copy(out):
    """Only use an empty directory or an existing EXP-11 output; never overwrite inputs."""
    out = Path(out).resolve()
    protected = [ROOT / name for name in ("data", "configs", "src", "docs", "experiments", "tests")]
    if out == ROOT or out in ROOT.parents or any(out == p or p in out.parents for p in protected):
        raise ValueError("EXP-11 output must be separate from protected inputs")
    if out.exists() and any(out.iterdir()):
        report_path = out / "report.json"
        if not report_path.exists() or json.loads(report_path.read_text(encoding="utf-8")).get("experiment_id") != "EXP-11":
            raise ValueError("output must be empty or belong to EXP-11")
    case_dir = out / "case"
    case_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(CASE_DIR.glob("*.csv")):
        shutil.copyfile(path, case_dir / path.name)
    shutil.copyfile(SCENARIOS / "base.yaml", out / "baseline.yaml")
    shutil.copyfile(SHOCK_PATH, out / "shock.yaml")
    return out, case_dir


def metrics(result):
    return dict(
        pv_cost_mln=result.kpi["pv_cost_mln"], total_cost_mln=result.kpi["total_cost_mln"],
        shortage_t=result.kpi["shortage_total_t"], critical_shortage_t=result.kpi["shortage_critical_t"],
        min_service_total=result.kpi["min_service_level_total"],
        min_service_critical=result.kpi["min_service_level_critical"],
        min_reserve_slack_t=min(y.opening_t - y.reserve_required_t for y in result.years),
        max_reserve_gap_t=max(max(0.0, y.reserve_required_t - y.opening_t) for y in result.years),
        reserve_failed_years=";".join(str(y.year) for y in result.years if not y.reserve_ok),
        hard_violations=result.kpi["hard_violations"], guideline_violations=result.kpi["guideline_violations"],
        passes=not (result.kpi["hard_violations"] or result.kpi["guideline_violations"]),
    )


def run_experiment(out):
    paths = [ASSUMPTIONS, SCENARIOS / "base.yaml", SHOCK_PATH, Path(__file__), ROOT / "experiments/common.py"]
    paths += [PLANS / f"{pid}.json" for pid in PLAN_IDS]
    paths += sorted(CASE_DIR.glob("*.csv")) + sorted((ROOT / "src/terraplan").glob("*.py"))
    original_hashes = input_hashes(paths)
    out, case_dir = prepare_copy(out)
    case = load_case(case_dir)
    assumptions = load_assumptions(ASSUMPTIONS)
    base, shock = load_scenario(out / "baseline.yaml"), load_scenario(out / "shock.yaml")

    # Explicit audit of the annual effective price overlay on the copied dataset.
    prices = []
    for year in case.years:
        for source in case.sources.values():
            before = source.variable_cost_mln_per_t * base.price_mult(source, year)
            after = source.variable_cost_mln_per_t * shock.price_mult(source, year)
            prices.append(dict(year=year, source_id=source.source_id, source_name=source.name,
                               base_price_mln_per_t=before, shock_price_mln_per_t=after,
                               surcharge_mln_per_t=after - before,
                               multiplier=shock.price_mult(source, year), status="TEAM_ASSUMPTION"))
    write_csv(out / "price_overlay.csv", prices)
    comparison, yearly, exposure, runs = [], [], [], []
    for pid in PLAN_IDS:
        plan = load_plan(PLANS / f"{pid}.json", case)
        before = simulate(case, plan, base, assumptions)
        after = simulate(case, plan, shock, assumptions)
        if not before.feasible or before.kpi["guideline_violations"]:
            raise ValueError(f"reference {pid} must pass BASE")
        if before.months != after.months or before.years != after.years:
            raise ValueError("price-only experiment unexpectedly changed the physical balance")
        row = dict(plan_id=pid)
        for name, value in metrics(before).items():
            row[f"{name}_before"] = value
            row[f"{name}_after"] = metrics(after)[name]
        row.update(delta_pv_mln=after.kpi["pv_cost_mln"] - before.kpi["pv_cost_mln"],
                   delta_total_mln=after.kpi["total_cost_mln"] - before.kpi["total_cost_mln"])
        comparison.append(row)

        for variant, result in (("before", before), ("after", after)):
            relative = f"{pid}/{variant}"
            run_dir = out / relative
            write_results(result, run_dir, xlsx=False)
            for y in result.years:
                yearly.append(dict(plan_id=pid, variant=variant, scenario_id=result.scenario_id, year=y.year,
                                   opening_t=y.opening_t, reserve_required_t=y.reserve_required_t,
                                   reserve_slack_t=y.opening_t - y.reserve_required_t, reserve_ok=y.reserve_ok,
                                   shortage_t=y.shortage_total_t, critical_shortage_t=y.shortage_critical_t,
                                   service_total=y.service_level_total, service_critical=y.service_level_critical))
            runs.append(dict(plan_id=pid, variant=variant, result_dir=relative, scenario=result.scenario,
                             plan=result.plan, kpi=result.kpi, kpi_sha256=kpi_hash(result.kpi),
                             violations=[asdict(v) for v in result.violations]))
        # All source-years, including unchanged sources and years, retained for audit.
        finance = {f.year: f for f in before.finance}
        for old, new in zip(before.source_years, after.source_years):
            booked_year = old.year if old.period == "year" else case.first_year
            delta = new.procurement_mln - old.procurement_mln
            exposure.append(dict(plan_id=pid, year=old.year, period=old.period, source_id=old.source_id,
                                 payable_volume_t=old.payable_volume_t, price_before=old.price_mln_per_t,
                                 price_after=new.price_mln_per_t, delta_procurement_mln=delta,
                                 booked_year=booked_year, delta_pv_mln=delta * finance[booked_year].discount_factor))

    report = dict(experiment_id="EXP-11", schema_version=SCHEMA_VERSION, hash_format=HASH_FORMAT,
                  python=platform.python_version(), random_seed=None, input_sha256=original_hashes,
                  method=dict(status="TEAM_ASSUMPTION", reference="BASE", shock=shock.to_dict(),
                              case_copy="case/*.csv unchanged; shock.yaml applies the annual price overlay once",
                              fixed="orders, reservations, investments, opening stock and demand allocation",
                              costs="variable procurement surcharge only; reservation, TOP rules, CAPEX and OPEX unchanged",
                              reserve="annual opening stock minus 45-day requirement; all years reported",
                              service="minimum annual total/critical service; failure includes both hard and guideline violations (97%/99%)",
                              decision="strategy selection by advance-adapted mandatory-stress cost is unchanged",
                              limits="illustrative price-only shock; no outages, empirical probabilities, replanning or 2041+ claim"),
                  assumptions=assumptions.entries, comparison=comparison, yearly=yearly, runs=runs)
    write_json(out / "report.json", report)
    write_csv(out / "comparison.csv", comparison)
    write_csv(out / "yearly.csv", yearly)
    write_csv(out / "price_exposure.csv", exposure)
    lines = ["# EXP-11: geopolitical price shock, fixed BASE P2z/P3/P4", "",
             "TEAM_ASSUMPTION: Earth-Core and Earth-Flex variable prices +25% in 2038-2039 only.",
             "Run on a case copy with an annual scenario overlay; no mandatory-stress demand or ISRU shock.",
             "Costs: mln constant-2035 units, real discount rate 8%. Before/after use the same fixed plan.", "",
             "| Plan | PV before | PV after | Delta PV | Shortage t before / after | Min reserve slack t before / after | Min total SL before / after | Min critical SL before / after | Reserve failed years before / after |",
             "|---|---:|---:|---:|---|---|---|---|---|"]
    for row in comparison:
        pair = lambda key: f"{row[key + '_before']:.6f} / {row[key + '_after']:.6f}"
        lines.append(f"| {row['plan_id']} | {row['pv_cost_mln_before']:.6f} | {row['pv_cost_mln_after']:.6f} | "
                     f"{row['delta_pv_mln']:.6f} | {pair('shortage_t')} | {pair('min_reserve_slack_t')} | "
                     f"{pair('min_service_total')} | {pair('min_service_critical')} | "
                     f"{row['reserve_failed_years_before'] or 'none'} / {row['reserve_failed_years_after'] or 'none'} |")
    lines += ["", "## Interpretation and limits", "",
              "- The price shock changes procurement cost, not delivered fuel, stock or service under these fixed plans.",
              "- price_overlay.csv shows every source/year; price_exposure.csv attributes the cost change to payable volumes (including TOP).",
              "- yearly.csv exposes opening stock, reserve requirement/slack and total/critical service, not just aggregate feasibility.",
              "- Failure includes hard and guideline violations: TEAM service checks may be labeled guideline by the existing scenario-scoped rules; the 97%/99% criteria are not relaxed.",
              "- This is an illustrative surcharge on the organizer's aggregate variable price, not an inferred fuel/launch/insurance decomposition.",
              "- No outage, delay, capacity restriction, contract renegotiation, cash-budget constraint or adaptive response is modeled.",
              "- The background is BASE, not MANDATORY_STRESS. This is not a probability model or a universal resilience ranking.",
              "- The P2z selection by lowest advance-adapted mandatory-stress cost remains unchanged.", "",
              "## Reproduction", "", "```bash",
              "python experiments/run_geopolitical_price_shock.py",
              "python experiments/run_geopolitical_price_shock.py --out results/geopolitical_price_shock_replay --compare results/geopolitical_price_shock",
              "python experiments/provenance.py results/geopolitical_price_shock",
              "python -m terraplan verify results/geopolitical_price_shock/P2z_earth_new_zbo/after --case results/geopolitical_price_shock/case",
              "python tests/independent_recalc.py results/geopolitical_price_shock/P2z_earth_new_zbo/after results/geopolitical_price_shock/case",
              "```", "",
              "All six runs include standard CSV/JSON exports. The portable manifest hashes copied inputs, compact reports and stable per-run exports.",
              "Standard result.json/run_manifest.json contain output paths and export_envelope.json contains a timestamp; those three files per run are excluded from byte replay comparison.",
              "Their numerical results can be replayed with verify --case; same runtime versions are required for exact normalized-text replay."]
    text = "\n".join(lines) + "\n"
    write_text(out / "summary.md", text)
    if input_hashes(paths) != original_hashes:
        raise ValueError("input files changed during EXP-11")
    excluded = {"result.json", "run_manifest.json", "export_envelope.json"}
    outputs = {p.relative_to(out).as_posix(): sha256(p) for p in sorted(out.rglob("*"))
               if p.is_file() and p.name not in excluded}
    write_json(out / "run_manifest.json", dict(experiment_id="EXP-11", schema_version=SCHEMA_VERSION,
               hash_format=HASH_FORMAT, python=platform.python_version(), random_seed=None,
               input_sha256=original_hashes, output_sha256=outputs))
    return report, text


def compare_saved(out, reference):
    current, previous = verify_saved(out), verify_saved(reference)
    if current != previous:
        raise ValueError("EXP-11 replay differs from saved inputs, outputs or runtime")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--compare", type=Path)
    args = parser.parse_args(argv)
    if args.compare and args.compare.resolve() == args.out.resolve():
        parser.error("--compare must be different from --out")
    _, text = run_experiment(args.out)
    if args.compare:
        compare_saved(args.out, args.compare)
    print(text)


if __name__ == "__main__":
    main()

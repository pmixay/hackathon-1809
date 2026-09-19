"""EXP-07: reverse stress of the saved, fixed stress-adapted P3 (no re-planning).

From 2038 through 2040: demand *= 1+d, ISRU actual delivery share *= 1-s,
relative to MANDATORY_STRESS. Minimize the equal-weight L-infinity radius
max(d, s). Bisect rays; the diagonal certifies the minimum by monotonicity.
See experiments/README.md for the domain, failure definition and limitations.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import platform
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from common import ASSUMPTIONS, PLANS, RESULTS, ROOT, load_all, scenario
from provenance import HASH_FORMAT, SCHEMA_VERSION, input_hashes, write_json, write_text
from terraplan import __version__
from terraplan.engine import EPS, TOL_T, simulate
from terraplan.plan import load_plan
from terraplan.scenario import scenario_from_dict

YEARS = (2038, 2039, 2040)
RAYS = ((1.0, 0.0), (1.0, 0.25), (1.0, 0.5), (1.0, 0.75), (1.0, 1.0),
        (0.75, 1.0), (0.5, 1.0), (0.25, 1.0), (0.0, 1.0))
SERVICE_RULES = {"BASE_TOTAL_SERVICE", "BASE_CRITICAL_SERVICE"}
DEFAULT_TOLERANCE = 1e-12  # absolute radius, a fraction (not percentage points)
DEFAULT_MAX_SHOCK = 0.5


def shocked_scenario(stress, case, demand_increase: float, isru_reduction: float):
    """Copy the mandatory environment; reductions are relative, not percentage points."""
    if not math.isfinite(demand_increase) or demand_increase < 0:
        raise ValueError("demand_increase must be finite and >= 0")
    if not math.isfinite(isru_reduction) or not 0 <= isru_reduction <= 1:
        raise ValueError("isru_reduction must be finite and in [0, 1]")
    data = deepcopy(stress.to_dict())
    data.update(scenario_id=f"TEAM_REVERSE_d{demand_increase:.17g}_s{isru_reduction:.17g}",
                label="EXP-07: additional adverse shocks to MANDATORY_STRESS", status="TEAM_ASSUMPTION")
    data["demand_multiplier"] = {y: stress.demand_mult(y) * (1 + demand_increase if y in YEARS else 1)
                                 for y in case.years}
    data["critical_demand_multiplier"] = {y: stress.critical_mult(y) * (1 + demand_increase if y in YEARS else 1)
                                          for y in case.years}
    data["actual_delivery_share"] = {
        sid: {y: stress.delivery_share(source, y) * (1 - isru_reduction if sid == "D" and y in YEARS else 1)
              for y in case.years} for sid, source in case.sources.items()}
    data["changes"] += [dict(status="TEAM_ASSUMPTION", years=list(YEARS),
                             demand_increase=demand_increase, isru_relative_reduction=isru_reduction,
                             reference="MANDATORY_STRESS; all plan decisions frozen")]
    return scenario_from_dict(data)


def failure_violations(result):
    """Engine tolerances apply. Service guidelines count as failure in this experiment.

    First = earliest year/month; annual checks use December, undated checks first.
    Ties are resolved by rule_id and source_id, independently of engine append order.
    """
    return sorted((v for v in result.violations
                   if v.severity == "hard" or (v.severity == "guideline" and v.rule_id in SERVICE_RULES)),
                  key=lambda v: (v.year or 0, v.month or 12, v.rule_id, v.source_id or ""))


def bisect_boundary(fails, max_shock=DEFAULT_MAX_SHOCK, tolerance=DEFAULT_TOLERANCE):
    """Return (last passing radius, first failing radius), or (max_shock, None).

    Requires a nondecreasing failure predicate on [0, max_shock]. The endpoints
    bracket the infimum of failure; strict inequalities need not attain a minimum.
    """
    if not math.isfinite(max_shock) or not 0 < max_shock <= 1:
        raise ValueError("max_shock must be finite and in (0, 1]")
    if not math.isfinite(tolerance) or not 0 < tolerance < max_shock:
        raise ValueError("tolerance must be finite and in (0, max_shock)")
    if fails(0.0):
        raise ValueError("reference plan already fails: reverse stress needs a passing origin")
    if not fails(max_shock):
        return max_shock, None
    lo, hi = 0.0, max_shock
    while hi - lo > tolerance:
        mid = (lo + hi) / 2
        if mid == lo or mid == hi:
            raise ValueError("tolerance is below floating-point resolution")
        if fails(mid):
            hi = mid
        else:
            lo = mid
    return lo, hi


def analyze(max_shock=DEFAULT_MAX_SHOCK, tolerance=DEFAULT_TOLERANCE):
    case, assumptions = load_all()
    stress = scenario("MANDATORY_STRESS")
    plan_path = PLANS / "P3_isru_zbo_adapted.json"
    plan = load_plan(plan_path, case)
    baseline = simulate(case, plan, stress, assumptions)

    def evaluate(d, s):
        return simulate(case, plan, shocked_scenario(stress, case, d, s), assumptions)

    boundary = []
    minimum = None
    for u, v in RAYS:
        lo, hi = bisect_boundary(lambda t: bool(failure_violations(evaluate(u * t, v * t))), max_shock, tolerance)
        failed = evaluate(u * hi, v * hi) if hi is not None else None
        violations = failure_violations(failed) if failed is not None else []
        first = violations[0] if violations else None
        boundary.append(dict(
            demand_direction=u, isru_direction=v, status="bracketed" if hi is not None else "no_failure_in_domain",
            pass_radius=lo, fail_radius=hi, demand_pass=u * lo, isru_reduction_pass=v * lo,
            demand_fail=u * hi if hi is not None else None, isru_reduction_fail=v * hi if hi is not None else None,
            first_rule=first.rule_id if first else None, first_year=first.year if first else None,
            first_month=first.month if first else None, severity=first.severity if first else None,
            actual=first.actual if first else None, limit=first.limit if first else None,
            excess=first.excess if first else None))
        if (u, v) == (1.0, 1.0):
            passed = evaluate(lo, lo)
            minimum = dict(status=boundary[-1]["status"], pass_radius=lo, fail_radius=hi,
                           passing_scenario=passed.scenario, passing_kpi=passed.kpi,
                           failing_scenario=failed.scenario if failed else None,
                           failing_kpi=failed.kpi if failed else None,
                           violations=[asdict(x) for x in violations])

    paths = [plan_path, Path(stress.source_file), ASSUMPTIONS, Path(__file__), ROOT / "experiments/common.py"]
    paths += sorted((ROOT / "data/case").glob("*.csv")) + sorted((ROOT / "src/terraplan").glob("*.py"))
    return dict(
        experiment_id="EXP-07", python=platform.python_version(), terraplan_version=__version__, random_seed=None,
        schema_version=SCHEMA_VERSION, hash_format=HASH_FORMAT, input_sha256=input_hashes(paths),
        method=dict(status="TEAM_ASSUMPTION", metric="L_inf = max(demand_increase, isru_relative_reduction)",
                    reference="MANDATORY_STRESS", years=list(YEARS), domain=[0, max_shock], tolerance=tolerance,
                    rays=RAYS, failure="any hard violation OR annual total/critical service guideline violation",
                    engine_physical_tolerance_t=TOL_T, engine_service_tolerance=EPS,
                    algorithm="monotone radial bisection; diagonal brackets global failure infimum in L_inf",
                    justification="equal weights on relative changes; exploratory range, not a probability model"),
        plan=plan.to_dict(), reference_scenario=stress.to_dict(), assumptions=assumptions.entries,
        baseline_kpi=baseline.kpi,
        baseline_reserves=[dict(year=y.year, opening_t=y.opening_t, required_t=y.reserve_required_t,
                                slack_t=y.opening_t - y.reserve_required_t) for y in baseline.years],
        boundary=boundary, minimum=minimum)


def write_report(report, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    # Do not use common.write_table: its four-decimal rounding hides this tiny boundary.
    with (out / "boundary.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(report["boundary"][0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(report["boundary"])
    write_json(out / "report.json", report)
    lines = ["# EXP-07 Reverse stress: fixed P3_isru_zbo_adapted", "",
             "Reference: MANDATORY_STRESS. Additional shocks in 2038-2040: demand *= 1+d; ISRU share *= 1-s.",
             "Failure: any hard violation or annual service below the 97%/99% guidelines (engine tolerances apply).",
             f"Metric: max(d,s); domain [0, {report['method']['domain'][1]}]^2; absolute radius tolerance {report['method']['tolerance']:.1e}.",
             "All table shocks are fractions, NOT percent. Each row brackets one point on the boundary.", "",
             "| Direction d:s | Passing radius | Failing radius | d at failure | s at failure | First violation |",
             "|---|---:|---:|---:|---:|---|"]
    for row in report["boundary"]:
        fmt = lambda x: "--" if x is None else f"{x:.12g}"
        first = f"{row['first_rule']} @ {row['first_year']}-{row['first_month'] or 12:02d}" if row["first_rule"] else "none in domain"
        lines.append(f"| {row['demand_direction']:g}:{row['isru_direction']:g} | {fmt(row['pass_radius'])} | "
                     f"{fmt(row['fail_radius'])} | {fmt(row['demand_fail'])} | {fmt(row['isru_reduction_fail'])} | {first} |")
    minimum = report["minimum"]
    lines += ["", "## Minimum shock (diagonal certificate)", ""]
    if minimum["fail_radius"] is None:
        lines.append("No failure in the search domain; no finite failure threshold is claimed.")
    else:
        first = minimum["violations"][0]
        lines += [f"Failure infimum bracket: [{minimum['pass_radius']:.12g}, {minimum['fail_radius']:.12g}].",
                  f"First: {first['rule_id']} @ {first['year']}-{first['month'] or 12:02d}; severity={first['severity']}; "
                  f"actual={first['actual']:.12g}, limit={first['limit']:.12g}, excess={first['excess']:.12g}.",
                  "A sub-rounding-sized threshold is numerical slack, not evidence of operational resilience."]
    lines += ["", "The passing diagonal dominates every point in its L-inf square; the failing diagonal is a witness.",
              "Monotonicity is specific to this fixed P3: demand rises, net inflow falls, ZBO loss rate is constant",
              "in the shock years; contracts, capacities and investments stay fixed. Storage overflow cannot be introduced.",
              "The strict failure boundary is reported as an interval, not an exact attained minimum.",
              "report.json contains input/code hashes, snapshots, tolerances, endpoint scenarios/KPIs and all minimum-witness violations."]
    summary = "\n".join(lines) + "\n"
    write_text(out / "summary.md", summary)
    return summary


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=RESULTS / "reverse_stress")
    parser.add_argument("--max-shock", type=float, default=DEFAULT_MAX_SHOCK, help="upper bound for both relative shocks (0,1]")
    parser.add_argument("--tolerance", type=float, default=DEFAULT_TOLERANCE, help="absolute bisection radius tolerance")
    args = parser.parse_args(argv)
    try:
        report = analyze(args.max_shock, args.tolerance)
    except ValueError as exc:
        parser.error(str(exc))
    print(write_report(report, args.out))


if __name__ == "__main__":
    main()

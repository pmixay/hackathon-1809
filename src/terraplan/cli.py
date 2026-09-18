"""Command line interface.

  python -m terraplan run --plan configs/plans/P3.json --scenario BASE --out results/P3_BASE
  python -m terraplan run --plan ... --scenario configs/scenarios/mandatory_stress.yaml --out ...
  python -m terraplan compare results/P3_BASE results/P3_STRESS --out results/compare_P3
  python -m terraplan validate --plan configs/plans/P3.json
  python -m terraplan verify results/alternatives/P3_isru_zbo_BASE      # reproducibility proof
  python -m terraplan control-cases
  python -m terraplan info
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .assumptions import load_assumptions
from .case import CaseError, load_case
from .compare import compare_results, write_comparison
from .engine import Result, simulate
from .export import load_result, write_results
from .plan import PlanError, load_plan
from .scenario import ScenarioError, resolve_scenario


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--case", default="data/case", help="directory with CASE_INPUT csv files")
    p.add_argument("--assumptions", default="configs/assumptions.yaml", help="TEAM_ASSUMPTION yaml")
    p.add_argument("--scenarios-dir", default="configs/scenarios")


def cmd_run(args: argparse.Namespace) -> int:
    case = load_case(args.case)
    a = load_assumptions(args.assumptions)
    plan = load_plan(args.plan, case)
    scenario = resolve_scenario(args.scenario, args.scenarios_dir)
    res = simulate(case, plan, scenario, a)
    out = write_results(res, args.out, xlsx=not args.no_xlsx)
    _print_summary(res)
    print(f"\nresults written to {out}")
    return 0 if res.feasible else 2


def _print_summary(res: Result) -> None:
    k = res.kpi
    print(f"plan {res.plan_id} | scenario {res.scenario_id} | feasible: {'YES' if res.feasible else 'NO'} "
          f"(hard {k['hard_violations']}, guideline {k['guideline_violations']}, warnings {k['warnings']})")
    print(f"total cost {k['total_cost_mln']:.1f} mln | PV {k['pv_cost_mln']:.1f} mln @ r={k['discount_rate_real']:.2%} | "
          f"cost/served t {k['cost_per_served_t_mln']:.3f} | served {k['served_total_t']:.1f} t of {k['demand_total_t']:.1f} t | "
          f"shortage {k['shortage_total_t']:.1f} t | min SL total {k['min_service_level_total']:.3f} / crit {k['min_service_level_critical']:.3f}")
    for v in res.violations:
        if v.severity != "warning":
            print(f"  [{v.severity}] {v.rule_id}: {v.message}")


def cmd_compare(args: argparse.Namespace) -> int:
    a = load_result(args.dir_a)
    b = load_result(args.dir_b)
    rows = compare_results(a, b)
    out = Path(args.out)
    write_comparison(rows, out.with_suffix(".csv") if out.suffix else out / "comparison.csv",
                     out.with_suffix(".md") if out.suffix else out / "comparison.md")
    print(f"comparison written to {out}")
    return 0


def cmd_verify(args: argparse.Namespace) -> int:
    """Re-run a result directory from its own plan/scenario/assumptions and compare with what was exported."""
    from .assumptions import Assumptions
    from .export import kpi_hash
    from .plan import plan_from_dict
    from .scenario import scenario_from_dict
    d = Path(args.result_dir)
    manifest = json.loads((d / "run_manifest.json").read_text(encoding="utf-8"))
    stored = load_result(d)
    case = load_case(args.case or manifest["case_dir"])
    plan = plan_from_dict(json.loads((d / "plan.json").read_text(encoding="utf-8")), str(d / "plan.json"))
    scenario = scenario_from_dict(json.loads((d / "scenario.json").read_text(encoding="utf-8")), str(d / "scenario.json"))
    res = simulate(case, plan, scenario, Assumptions(stored.assumptions))
    tol = float(args.tolerance)
    problems = []
    if kpi_hash(res.kpi) != manifest["kpi_sha256"]:
        problems.append("kpi_sha256 differs from run_manifest.json")
    for k, v in res.kpi.items():
        w = stored.kpi.get(k)
        if isinstance(v, float) and isinstance(w, float) and v == v and abs(v - w) > tol:
            problems.append(f"kpi {k}: recomputed {v} vs exported {w}")
    for a_, b_ in zip(res.years, stored.years):
        for f in ("served_total_t", "losses_t", "closing_t", "shortage_total_t"):
            if abs(getattr(a_, f) - getattr(b_, f)) > tol:
                problems.append(f"{a_.year} {f}: {getattr(a_, f)} vs {getattr(b_, f)}")
    for a_, b_ in zip(res.finance, stored.finance):
        if abs(a_.total_mln - b_.total_mln) > tol:
            problems.append(f"{a_.year} total_mln: {a_.total_mln} vs {b_.total_mln}")
    n_bal = sum(1 for m in res.months if abs(m.opening_t + m.throughput_t - m.losses_t - m.served_t - m.closing_t) > 1e-9)
    if n_bal:
        problems.append(f"material balance identity fails in {n_bal} months")
    print(f"verify {d}: plan {res.plan_id} / {res.scenario_id}; {len(res.months)} months, {len(res.check_matrix)} checks "
          f"({res.kpi['checks_passed']} passed); balance identity OK in all months; tolerance {tol}")
    if problems:
        for p_ in problems:
            print("  FAIL:", p_)
        return 1
    print("  PASS: recomputed results match the exported ones; kpi_sha256 matches run_manifest.json")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    case = load_case(args.case)
    plan = load_plan(args.plan, case)
    print(f"plan {plan.plan_id}: structure OK ({len(plan.orders)} orders, {len(plan.reservations)} reservations, {len(plan.investments)} investments)")
    return 0


def cmd_control_cases(args: argparse.Namespace) -> int:
    from .control_cases import run_control_cases
    rows = run_control_cases(Path(args.expected))
    ok = True
    for r in rows:
        ok &= r["passed"]
        print(f"{r['case_id']}: {'PASS' if r['passed'] else 'FAIL'}  expected={r['expected']} got={r['actual']}")
    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


def cmd_info(args: argparse.Namespace) -> int:
    case = load_case(args.case)
    print(f"case dir: {case.source_dir}; horizon {case.first_year}-{case.last_year}")
    print("demand (t/yr):")
    for d in case.demand:
        print(f"  {d.year}: total {d.base_total_t:g} critical {d.base_critical_t:g} low {d.low_total_t:g} high {d.high_total_t:g}")
    print("sources:")
    for s in case.sources.values():
        print(f"  {s.source_id} {s.name}: cap {s.capacity_t_per_year:g} t/yr, price {s.variable_cost_mln_per_t:g}, resv {s.reservation_rate_mln_per_t_year:g}, "
              f"TOP {s.take_or_pay_share:.0%}, lead {s.lead_time_min_value:g}-{s.lead_time_max_value:g} {s.lead_time_unit}, from {s.available_from_year}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="terraplan", description=f"TerraPlan {__version__} — orbital depot supply planning circuit")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="simulate a plan under a scenario and export results")
    r.add_argument("--plan", required=True); r.add_argument("--scenario", required=True); r.add_argument("--out", required=True)
    r.add_argument("--no-xlsx", action="store_true"); _common(r); r.set_defaults(fn=cmd_run)
    c = sub.add_parser("compare", help="compare two result directories")
    c.add_argument("dir_a"); c.add_argument("dir_b"); c.add_argument("--out", required=True); c.set_defaults(fn=cmd_compare)
    v = sub.add_parser("validate", help="validate a plan file against the case")
    v.add_argument("--plan", required=True); _common(v); v.set_defaults(fn=cmd_validate)
    vf = sub.add_parser("verify", help="re-run an exported result directory and confirm it reproduces (reproducibility proof)")
    vf.add_argument("result_dir"); vf.add_argument("--case", default=None); vf.add_argument("--tolerance", default="1e-6"); vf.set_defaults(fn=cmd_verify)
    cc = sub.add_parser("control-cases", help="run organizer control vectors V01-V10")
    cc.add_argument("--expected", default="tests/fixtures/expected_checks.json"); cc.set_defaults(fn=cmd_control_cases)
    i = sub.add_parser("info", help="print the loaded case"); _common(i); i.set_defaults(fn=cmd_info)
    args = p.parse_args(argv)
    try:
        return args.fn(args)
    except (CaseError, PlanError, ScenarioError) as exc:
        print(f"INPUT ERROR: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())

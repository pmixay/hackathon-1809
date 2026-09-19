"""EXP-01: compare alternative strategies P1–P4 under BASE and MANDATORY_STRESS (same plan, no adaptation).

Outputs: results/alternatives/<plan>_<scenario>/ (full exports) and results/alternatives/summary.{csv,md}.
Plans are written to configs/plans/<plan>.json (TEAM_DECISION drafts).
"""
from common import PLANS, RESULTS, STRATEGIES, kpi_row, load_all, run_and_save, scenario, write_table
from terraplan.planner import build_plan
from terraplan.plan import save_plan


def main() -> None:
    case, a = load_all()
    base, stress = scenario("BASE"), scenario("MANDATORY_STRESS")
    rows = []
    for name, strat in STRATEGIES.items():
        plan = build_plan(case, base, strat, a)
        save_plan(plan, PLANS / f"{name}.json")
        for sc in (base, stress):
            res = run_and_save(case, plan, sc, a, RESULTS / "alternatives" / f"{name}_{sc.scenario_id}")
            rows.append(kpi_row(res, experiment="EXP-01"))
            print(f"{name:20s} {sc.scenario_id:16s} feasible={res.feasible!s:5s} PV={res.kpi['pv_cost_mln']:9.1f} cost/t={res.kpi['cost_per_served_t_mln']:.3f} "
                  f"shortage={res.kpi['shortage_total_t']:7.1f} minSL={res.kpi['min_service_level_total']:.3f} hard={res.kpi['hard_violations']}")
    write_table(rows, RESULTS / "alternatives" / "summary.csv", RESULTS / "alternatives" / "summary.md",
                "EXP-01 Альтернативы в BASE и MANDATORY_STRESS (план построен для BASE, в стрессе не меняется)")


if __name__ == "__main__":
    main()

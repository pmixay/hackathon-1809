"""EXP-03: low / high demand checks (organizer columns) for the candidate strategies.

Two views per strategy: the BASE plan unchanged (what happens if demand deviates and nothing is done)
and a re-planned version (same investments, orders re-sized). Outputs: results/demand/.
"""
from common import RESULTS, STRATEGIES, kpi_row, load_all, run_and_save, scenario, write_table
from terraplan.planner import build_plan

CANDIDATES = ["P2z_earth_new_zbo", "P3_isru_zbo", "P4_full"]


def main() -> None:
    case, a = load_all()
    base = scenario("BASE")
    rows = []
    for sid in ("TEAM_LOW_DEMAND", "TEAM_HIGH_DEMAND"):
        sc = scenario(sid)
        for name in CANDIDATES:
            strat = STRATEGIES[name]
            fixed = build_plan(case, base, strat, a)
            replanned = build_plan(case, sc, dict(strat, plan_id=f"{name}_{sid.lower()}", stress_aware=True), a)
            r1 = run_and_save(case, fixed, sc, a, RESULTS / "demand" / f"{name}_fixed_{sid}", xlsx=False)
            r2 = run_and_save(case, replanned, sc, a, RESULTS / "demand" / f"{name}_replanned_{sid}", xlsx=False)
            rows += [kpi_row(r1, experiment="EXP-03", variant="BASE plan unchanged"), kpi_row(r2, experiment="EXP-03", variant="re-planned")]
            print(f"{sid:16s} {name:20s} fixed: PV={r1.kpi['pv_cost_mln']:.0f} minSL={r1.kpi['min_service_level_total']:.3f} hard={r1.kpi['hard_violations']} | "
                  f"re-planned: PV={r2.kpi['pv_cost_mln']:.0f} minSL={r2.kpi['min_service_level_total']:.3f} hard={r2.kpi['hard_violations']}")
    write_table(rows, RESULTS / "demand" / "summary.csv", RESULTS / "demand" / "summary.md", "EXP-03 Low / high demand checks")


if __name__ == "__main__":
    main()

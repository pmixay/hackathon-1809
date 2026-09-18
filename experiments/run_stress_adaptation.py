"""EXP-02: mandatory stress — fixed plan vs stress-adapted plan for the candidate strategies.

Adapted plan = the same strategy re-planned against the stress environment (demand x1.15 from 2038,
ISRU 55 %/75 %, price x1.25): larger 2037 closing stock (pre-committed), extra Earth-Flex / Emergency
orders sized with advance knowledge, respecting source lead times (not post-observation reaction).
P3 uses extra Core/Flex and no Emergency. Investments are NOT changed. All adapted plans are
also evaluated in BASE, where the saved fixed orders cause storage overflow (17/25/25 hard checks).
Outputs: results/stress/<plan>_adapted_MANDATORY_STRESS/, results/stress/compare_<plan>.{csv,md}, summary.
"""
from common import PLANS, RESULTS, STRATEGIES, kpi_row, load_all, run_and_save, scenario, write_table
from terraplan.compare import compare_results, write_comparison
from terraplan.plan import save_plan
from terraplan.planner import build_plan

CANDIDATES = ["P2z_earth_new_zbo", "P3_isru_zbo", "P4_full"]


def main() -> None:
    case, a = load_all()
    base, stress = scenario("BASE"), scenario("MANDATORY_STRESS")
    rows = []
    for name in CANDIDATES:
        strat = dict(STRATEGIES[name])
        fixed = build_plan(case, base, strat, a)
        adapted = build_plan(case, stress, dict(strat, plan_id=f"{name}_adapted", stress_aware=True,
                                                description=strat["description"] + " — re-planned for MANDATORY_STRESS"), a)
        save_plan(adapted, PLANS / f"{name}_adapted.json")
        r_fixed = run_and_save(case, fixed, stress, a, RESULTS / "stress" / f"{name}_fixed_MANDATORY_STRESS")
        r_adapt = run_and_save(case, adapted, stress, a, RESULTS / "stress" / f"{name}_adapted_MANDATORY_STRESS")
        r_adapt_base = run_and_save(case, adapted, base, a, RESULTS / "stress" / f"{name}_adapted_BASE")
        rows += [kpi_row(r_fixed, experiment="EXP-02", variant="fixed plan"), kpi_row(r_adapt, experiment="EXP-02", variant="adapted plan"),
                 kpi_row(r_adapt_base, experiment="EXP-02", variant="adapted plan run in BASE (cost of hedging)")]
        write_comparison(compare_results(r_fixed, r_adapt, f"{name} fixed/STRESS", f"{name} adapted/STRESS"),
                         RESULTS / "stress" / f"compare_{name}.csv", RESULTS / "stress" / f"compare_{name}.md")
        print(f"{name}: fixed PV={r_fixed.kpi['pv_cost_mln']:.1f} shortage={r_fixed.kpi['shortage_total_t']:.1f} hard={r_fixed.kpi['hard_violations']} | "
              f"adapted PV={r_adapt.kpi['pv_cost_mln']:.1f} shortage={r_adapt.kpi['shortage_total_t']:.1f} hard={r_adapt.kpi['hard_violations']} "
              f"minSL={r_adapt.kpi['min_service_level_total']:.3f}")
    write_table(rows, RESULTS / "stress" / "summary.csv", RESULTS / "stress" / "summary.md", "EXP-02 Mandatory stress: fixed vs adapted plans")


if __name__ == "__main__":
    main()

"""EXP-06: observe-then-react under MANDATORY_STRESS (no foresight of the stress).

Decisions taken before the shock are frozen as in the BASE plan (P3): Earth-Core reservations/orders for
2038 and 2039 (12-month lead, TOP), ISRU orders, investments, 2037 closing stock (30.8 t = BASE reserve).
The ISRU shortfall is observed at the first ISRU delivery, 2038-03. From then on only two levers react,
each after its own lead time: Earth-Flex (4 months -> extra deliveries from 2038-07) and Emergency
(6 weeks = 2 months -> from 2038-05). Earth-Core for 2040 may be re-ordered (12-month lead) up to capacity.
Reaction rule: each month from the reaction date, add the cheapest available extra delivery so that the
end-of-month stock follows the stress reserve trajectory (linear path to next year's 45-day reserve).
Outputs: results/reaction/ (fixed, reactive, pre-committed adapted runs + comparison + summary).
"""
from __future__ import annotations

from common import PLANS, RESULTS, STRATEGIES, kpi_row, load_all, run_and_save, scenario, write_table
from terraplan import rules
from terraplan.compare import compare_results, write_comparison
from terraplan.engine import midx, simulate
from terraplan.plan import Order, Plan, Reservation, save_plan
from terraplan.planner import build_plan

PLAN = "P3_isru_zbo"
OBSERVE = midx(2038, 3)          # first ISRU delivery reveals the 55 % share
LEVERS = [("B", 4), ("E", 2)]    # source, reaction lead time in months (Flex 4 mo, Emergency 6 weeks -> 2 mo)


def main() -> None:
    case, a = load_all()
    base, stress = scenario("BASE"), scenario("MANDATORY_STRESS")
    fixed = build_plan(case, base, STRATEGIES[PLAN], a)
    r_fixed = simulate(case, fixed, stress, a)

    # reactive plan: copy of the fixed plan with monthly profiles for the levers from 2038
    orders = {(o.source_id, o.year): o for o in fixed.orders}
    resv = {(r.source_id, r.year): r.reserved_capacity_t for r in fixed.reservations}
    extra: dict[tuple[str, int], list[float]] = {}
    for sid, _ in LEVERS:
        for y in (2038, 2039, 2040):
            base_o = orders.get((sid, y))
            monthly = [base_o.ordered_t / 12.0] * 12 if base_o else [0.0] * 12
            extra[(sid, y)] = monthly
    cap = {sid: case.sources[sid].capacity_t_per_year / 12.0 for sid, _ in LEVERS}
    first = {sid: OBSERVE + lt for sid, lt in LEVERS}
    # Earth-Core 2040 can still be raised (ordered by 2039-01 at the latest for 2040-01 delivery): allow up to capacity
    # walk the stress simulation month by month, adding deliveries where the stock trajectory falls short
    inv = None
    trace = {(m.year, m.month): m for m in r_fixed.months}
    D = {y: r.demand_total_t for y, r in ((yr.year, yr) for yr in r_fixed.years)}
    R = {y: rules.reserve_45d(D[y]) for y in D}
    for y in (2038, 2039, 2040):
        target_end = R.get(y + 1, R[y])
        target_start = R[y]
        for mth in range(1, 13):
            idx = midx(y, mth)
            m = trace[(y, mth)]
            if inv is None:
                inv = m.opening_t
            loss = m.loss_rate
            planned_actual = m.throughput_t                      # from the fixed plan (already includes ISRU share)
            for sid, _ in LEVERS:                                # replace fixed monthly B/E with the (possibly raised) monthly profile
                pass
            desired = target_start + (target_end - target_start) * mth / 12.0
            projected = inv + planned_actual * (1 - loss) - m.demand_t
            need = max(0.0, desired - projected)                  # net tonnes missing this month
            added = 0.0
            for sid, _ in sorted(LEVERS, key=lambda t: case.sources[t[0]].variable_cost_mln_per_t):
                if idx < first[sid] or need <= 1e-9:
                    continue
                room = cap[sid] - extra[(sid, y)][mth - 1]
                take_gross = min(room, need / (1 - loss))
                if take_gross <= 1e-9:
                    continue
                extra[(sid, y)][mth - 1] += take_gross
                added += take_gross * (1 - loss)
                need -= take_gross * (1 - loss)
            inv = max(0.0, projected + added)
    new_orders = [o for o in fixed.orders if not ((o.source_id, o.year) in extra)]
    new_resv = [r for r in fixed.reservations if not ((r.source_id, r.year) in extra)]
    for (sid, y), monthly in extra.items():
        total = sum(monthly)
        if total <= 1e-9:
            continue
        new_orders.append(Order(sid, y, round(total, 4), "monthly", [round(v, 4) for v in monthly]))
        new_resv.append(Reservation(sid, y, min(case.sources[sid].capacity_t_per_year, max(resv.get((sid, y), 0.0), round(max(monthly) * 12 + 1e-3, 3)))))
    reactive = Plan(plan_id=f"{PLAN}_reactive", scenario_id="MANDATORY_STRESS", description="P3 with observe-then-react: Flex from 2038-07, Emergency from 2038-05",
                    reservations=new_resv, orders=new_orders, investments=fixed.investments, opening_stock=fixed.opening_stock,
                    meta={"experiment": "EXP-06", "observation_month": "2038-03", "levers": {"B": "4 months", "E": "2 months"}, "status": "TEAM_DECISION"})
    save_plan(reactive, PLANS / f"{PLAN}_reactive.json")
    r_react = run_and_save(case, reactive, stress, a, RESULTS / "reaction" / f"{PLAN}_reactive_MANDATORY_STRESS")
    run_and_save(case, fixed, stress, a, RESULTS / "reaction" / f"{PLAN}_fixed_MANDATORY_STRESS", xlsx=False)
    adapted = build_plan(case, stress, dict(STRATEGIES[PLAN], plan_id=f"{PLAN}_adapted", stress_aware=True), a)
    r_adapt = simulate(case, adapted, stress, a)
    write_comparison(compare_results(r_fixed, r_react, "fixed/STRESS", "reactive/STRESS"), RESULTS / "reaction" / "compare_fixed_vs_reactive.csv", RESULTS / "reaction" / "compare_fixed_vs_reactive.md")
    write_comparison(compare_results(r_react, r_adapt, "reactive/STRESS", "pre-committed adapted/STRESS"), RESULTS / "reaction" / "compare_reactive_vs_adapted.csv", RESULTS / "reaction" / "compare_reactive_vs_adapted.md")
    rows = [kpi_row(r_fixed, experiment="EXP-06", variant="fixed (no reaction)"), kpi_row(r_react, experiment="EXP-06", variant="reactive after 2038-03"),
            kpi_row(r_adapt, experiment="EXP-06", variant="pre-committed adaptation (EXP-02)")]
    write_table(rows, RESULTS / "reaction" / "summary.csv", RESULTS / "reaction" / "summary.md", "EXP-06 Observe-then-react vs fixed vs pre-committed adaptation (P3, MANDATORY_STRESS)")
    for r in (r_fixed, r_react, r_adapt):
        k = r.kpi
        print(f"{r.plan_id:24s} feasible={r.feasible!s:5s} PV={k['pv_cost_mln']:9.1f} shortage={k['shortage_total_t']:6.1f} minSL={k['min_service_level_total']:.3f} hard={k['hard_violations']} guideline={k['guideline_violations']}")
    months_short = [(m.year, m.month, round(m.shortage_t, 2)) for m in r_react.months if m.shortage_t > 1e-6]
    print("reactive plan shortage months:", months_short)
    e_use = {y: sum(o.ordered_t for o in reactive.orders if o.source_id == "E" and o.year == y) for y in (2038, 2039, 2040)}
    b_use = {y: sum(o.ordered_t for o in reactive.orders if o.source_id == "B" and o.year == y) for y in (2038, 2039, 2040)}
    print("Earth-Flex ordered:", b_use, "Emergency ordered:", e_use)
    for v in r_react.violations:
        if v.severity != "warning":
            print("  ", v.severity, v.rule_id, v.message)


if __name__ == "__main__":
    main()

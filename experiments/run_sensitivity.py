"""EXP-04: one-at-a-time sensitivity sweeps with threshold detection, on the candidate plan P3_isru_zbo.

Parameters and ranges (TEAM_ASSUMPTION ranges, see experiments/README.md):
  demand multiplier (all years)          0.80 .. 1.30   fixed plan and re-planned
  ISRU actual delivery share in 2038     0.30 .. 1.00   fixed plan
  Earth-Core/Flex variable price mult.   0.80 .. 1.50   fixed plan
  real discount rate                     0.00 .. 0.12   fixed plan
  ZBO commissioning lag (months)         0 .. 12        fixed plan, under MANDATORY_STRESS (loss ceiling)
Reported thresholds are adverse GRID observations, not exact continuous boundaries. Re-planned
P3 at demand x1.25 passes constraints but already has shortage; x1.30 fails. ZBO's threshold
is specific to the annual loss check; this BASE plan already fails other stress checks at lag 0.
Outputs: results/sensitivity/sweep_<param>.csv, tornado.csv, summary.md
"""
from __future__ import annotations

from common import RESULTS, STRATEGIES, load_all, scenario, write_table
from terraplan.engine import simulate
from terraplan.planner import build_plan
from terraplan.scenario import scenario_from_dict

PLAN = "P3_isru_zbo"


def frange(a: float, b: float, step: float):
    x = a
    while x <= b + 1e-9:
        yield round(x, 4)
        x += step


def row(res, **kw):
    k = res.kpi
    return dict(**kw, pv_cost_mln=k["pv_cost_mln"], total_cost_mln=k["total_cost_mln"], cost_per_served_t=k["cost_per_served_t_mln"],
                shortage_t=k["shortage_total_t"], min_sl_total=k["min_service_level_total"], min_sl_critical=k["min_service_level_critical"],
                hard=k["hard_violations"], guideline=k["guideline_violations"], losses_t=k["losses_total_t"],
                violations="; ".join(sorted({f"{v.rule_id}@{v.year}" for v in res.violations if v.severity != "warning"})))


def breaks(res) -> bool:
    return res.kpi["hard_violations"] > 0 or res.kpi["min_service_level_total"] < 0.97 or res.kpi["min_service_level_critical"] < 0.99


def main() -> None:
    case, a = load_all()
    base, stress = scenario("BASE"), scenario("MANDATORY_STRESS")
    strat = STRATEGIES[PLAN]
    plan = build_plan(case, base, strat, a)
    ref = simulate(case, plan, base, a)
    summary, tornado = [], []

    # 1. demand multiplier
    rows, thr_fixed, thr_replan = [], None, None
    for x in frange(0.80, 1.30, 0.05):
        sc = scenario_from_dict({"scenario_id": f"TEAM_SENS_DEMAND_{x}", "status": "TEAM_ASSUMPTION", "demand_multiplier": {"default": x}})
        r1 = simulate(case, plan, sc, a)
        r2 = simulate(case, build_plan(case, sc, dict(strat, plan_id=f"{PLAN}_d{x}", stress_aware=True), a), sc, a)
        rows.append(dict(row(r1, param="demand_multiplier", value=x, variant="fixed plan"), replanned_pv=r2.kpi["pv_cost_mln"],
                         replanned_min_sl=r2.kpi["min_service_level_total"], replanned_hard=r2.kpi["hard_violations"], replanned_shortage=r2.kpi["shortage_total_t"]))
        if thr_fixed is None and x > 1.0 and breaks(r1):
            thr_fixed = x
        if thr_replan is None and x > 1.0 and breaks(r2):
            thr_replan = x
    write_table(rows, RESULTS / "sensitivity" / "sweep_demand_multiplier.csv")
    summary.append(dict(param="demand_multiplier", range="0.80..1.30", threshold_fixed_plan=thr_fixed, threshold_replanned=thr_replan,
                        note="first failed adverse grid points; not exact boundaries; re-planned x1.25 passes constraints with 12.437 t shortage and 97.45% minimum annual service; x1.30 fails"))
    tornado.append(dict(param="demand_multiplier", low=0.80, high=1.30, pv_low=rows[0]["pv_cost_mln"], pv_base=ref.kpi["pv_cost_mln"], pv_high=rows[-1]["pv_cost_mln"]))

    # 2. ISRU delivery share 2038
    rows, thr = [], None
    for x in frange(0.30, 1.00, 0.05):
        sc = scenario_from_dict({"scenario_id": f"TEAM_SENS_ISRU_{x}", "status": "TEAM_ASSUMPTION", "actual_delivery_share": {"Lunar-ISRU": {2038: x}}})
        r = simulate(case, plan, sc, a)
        rows.append(row(r, param="isru_delivery_share_2038", value=x, variant="fixed plan"))
    for rr in reversed(rows):
        if rr["hard"] > 0 or rr["min_sl_total"] < 0.97:
            thr = rr["value"]
            break
    write_table(rows, RESULTS / "sensitivity" / "sweep_isru_share_2038.csv")
    summary.append(dict(param="isru_delivery_share_2038", range="0.30..1.00", threshold_fixed_plan=thr, threshold_replanned=None,
                        note="largest sampled share failing reserve checks; 1.00 passes and 0.95 fails; exact boundary between them not searched"))
    tornado.append(dict(param="isru_delivery_share_2038", low=0.30, high=1.00, pv_low=rows[0]["pv_cost_mln"], pv_base=ref.kpi["pv_cost_mln"], pv_high=rows[-1]["pv_cost_mln"]))

    # 3. Core/Flex price multiplier
    rows = []
    for x in frange(0.80, 1.50, 0.10):
        sc = scenario_from_dict({"scenario_id": f"TEAM_SENS_PRICE_{x}", "status": "TEAM_ASSUMPTION",
                                 "variable_price_multiplier": {"Earth-Core": {"default": x}, "Earth-Flex": {"default": x}}})
        rows.append(row(simulate(case, plan, sc, a), param="earth_price_multiplier", value=x, variant="fixed plan"))
    write_table(rows, RESULTS / "sensitivity" / "sweep_earth_price_multiplier.csv")
    summary.append(dict(param="earth_price_multiplier", range="0.80..1.50", threshold_fixed_plan=None, threshold_replanned=None,
                        note="pure cost effect; no physical constraint depends on price"))
    tornado.append(dict(param="earth_price_multiplier", low=0.80, high=1.50, pv_low=rows[0]["pv_cost_mln"], pv_base=ref.kpi["pv_cost_mln"], pv_high=rows[-1]["pv_cost_mln"]))

    # 4. discount rate
    rows = []
    for x in frange(0.00, 0.12, 0.02):
        rows.append(row(simulate(case, plan, base, a.with_overrides(discount_rate_real=x)), param="discount_rate_real", value=x, variant="fixed plan"))
    write_table(rows, RESULTS / "sensitivity" / "sweep_discount_rate.csv")
    summary.append(dict(param="discount_rate_real", range="0.00..0.12", threshold_fixed_plan=None, threshold_replanned=None,
                        note="affects PV only; ranking of alternatives must be re-checked at each rate (see summary.md)"))
    tornado.append(dict(param="discount_rate_real", low=0.0, high=0.12, pv_low=rows[0]["pv_cost_mln"], pv_base=ref.kpi["pv_cost_mln"], pv_high=rows[-1]["pv_cost_mln"]))

    # 5. ZBO commissioning lag under mandatory stress (loss ceiling from 2038)
    rows, thr = [], None
    for lag in range(0, 13):
        r = simulate(case, plan, stress, a.with_overrides(zbo_commissioning_lag_months=lag))
        rows.append(row(r, param="zbo_commissioning_lag_months", value=lag, variant="fixed plan / MANDATORY_STRESS"))
        if thr is None and any(v.rule_id == "STRESS_LOSS_LIMIT" for v in r.violations):
            thr = lag
    write_table(rows, RESULTS / "sensitivity" / "sweep_zbo_lag_stress.csv")
    summary.append(dict(param="zbo_commissioning_lag_months", range="0..12", threshold_fixed_plan=thr, threshold_replanned=None,
                        note="first annual loss-check failure at lag 10; lags 7-9 still pass that check; reserve/service already fail at lag 0; ZBO decision 2037-07"))

    # ranking of alternatives across discount rates
    rank_rows = []
    for x in (0.0, 0.04, 0.08, 0.12):
        for name, st in STRATEGIES.items():
            p = build_plan(case, base, st, a)
            r = simulate(case, p, base, a.with_overrides(discount_rate_real=x))
            rank_rows.append(dict(discount_rate=x, plan_id=name, pv_cost_mln=r.kpi["pv_cost_mln"], feasible=r.feasible))
    write_table(rank_rows, RESULTS / "sensitivity" / "ranking_by_discount_rate.csv")

    write_table(summary, RESULTS / "sensitivity" / "thresholds.csv")
    write_table(tornado, RESULTS / "sensitivity" / "tornado.csv")
    lines = [f"# EXP-04 Sensitivity — plan {PLAN} (BASE plan, fixed unless stated)", "", f"Reference PV cost (BASE, r=8 %): {ref.kpi['pv_cost_mln']:,.1f} mln", "",
             "## Thresholds", "", "| Parameter | Range | Threshold (fixed plan) | Threshold (re-planned) | Note |", "|---|---|---:|---:|---|"]
    for s in summary:
        lines.append(f"| {s['param']} | {s['range']} | {s['threshold_fixed_plan'] if s['threshold_fixed_plan'] is not None else '—'} | "
                     f"{s['threshold_replanned'] if s['threshold_replanned'] is not None else '—'} | {s['note']} |")
    lines += ["", "## Tornado (PV cost, mln)", "", "| Parameter | Low | PV @ low | PV @ base | High | PV @ high | Swing |", "|---|---:|---:|---:|---:|---:|---:|"]
    for t in sorted(tornado, key=lambda t: -abs(t["pv_high"] - t["pv_low"])):
        lines.append(f"| {t['param']} | {t['low']} | {t['pv_low']:,.0f} | {t['pv_base']:,.0f} | {t['high']} | {t['pv_high']:,.0f} | {abs(t['pv_high'] - t['pv_low']):,.0f} |")
    lines += ["", "## Ranking of alternatives by PV cost at different discount rates (BASE)", "", "| r | " + " | ".join(STRATEGIES) + " |", "|---|" + "|".join("---:" for _ in STRATEGIES) + "|"]
    for x in (0.0, 0.04, 0.08, 0.12):
        vals = [next(rr for rr in rank_rows if rr["discount_rate"] == x and rr["plan_id"] == n) for n in STRATEGIES]
        lines.append(f"| {x:.2f} | " + " | ".join(f"{v['pv_cost_mln']:,.0f}{'' if v['feasible'] else ' (infeasible)'}" for v in vals) + " |")
    (RESULTS / "sensitivity" / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

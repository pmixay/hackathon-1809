"""EXP-04: one-at-a-time sensitivity sweeps with threshold detection, on the candidate plan P3_isru_zbo.

Parameters and ranges (TEAM_ASSUMPTION ranges, see experiments/README.md):
  demand multiplier (all years)          0.80 .. 1.30   fixed plan and re-planned
  ISRU actual delivery share in 2038     0.30 .. 1.00   fixed plan
  Earth-Core/Flex variable price mult.   0.80 .. 1.50   fixed plan
  real discount rate                     0.00 .. 0.12   fixed plan
  ZBO commissioning lag (months)         0 .. 12        fixed plan, under MANDATORY_STRESS (loss ceiling)
Additionally: the value of each parameter at which the RECOMMENDED plan stops being the cheaper one,
i.e. where P3 (Lunar-ISRU) overtakes P2z (Earth-New) on the decision metric. Found by bisection to a
declared tolerance, on both the BASE present value and the advance-adapted mandatory-stress present
value that actually drives the choice. Outputs: crossover_P2z_vs_P3.csv.
Reported sweep thresholds are adverse GRID observations, not exact continuous boundaries. Re-planned
P3 at demand x1.25 passes constraints but already has shortage; x1.30 fails. ZBO's threshold
is specific to the annual loss check; this BASE plan already fails other stress checks at lag 0.
Outputs: results/sensitivity/sweep_<param>.csv, tornado.csv, summary.md
"""
from __future__ import annotations

from dataclasses import replace

from common import RESULTS, STRATEGIES, load_all, scenario, write_table
from terraplan.engine import simulate
from terraplan.planner import build_plan
from terraplan.scenario import scenario_from_dict

PLAN = "P3_isru_zbo"
RECOMMENDED, CHALLENGER = "P2z_earth_new_zbo", "P3_isru_zbo"
EARTH_PRICE_SOURCES = ("A", "B")            # Earth-Core, Earth-Flex — the channels P2z leans on
CROSSOVER_TOL = {"earth_price_multiplier": 0.001, "discount_rate_real": 0.0005, "isru_capex_mln": 0.5}


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


def scaled_prices(scen, case, x: float, years, sources=EARTH_PRICE_SOURCES):
    """Scenario copy whose Earth-Core/Flex prices are x times the scenario's own prices.

    Multiplying the scenario's effective multiplier (rather than replacing it) keeps the mandatory
    stress price step intact, so the sweep asks "what if Earth procurement is x times dearer than the
    scenario already assumes", not "what if the stress never happened".
    """
    d = scen.to_dict()
    vpm = dict(d.get("variable_price_multiplier") or {})
    for sid in sources:
        src = case.sources[sid]
        vpm[sid] = {y: scen.price_mult(src, y) * x for y in years}
    d["variable_price_multiplier"] = vpm
    d["scenario_id"] = f"{scen.scenario_id}_PRICEX_{x:.4f}"
    d["status"] = "TEAM_ASSUMPTION"
    return scenario_from_dict(d)


def case_with_isru_capex(case, capex_mln: float):
    """Case copy in which the Lunar-ISRU pilot costs a hypothetical amount (TEAM_ASSUMPTION).

    The organizer's figure is 1250 mln; varying it answers "how much cheaper would the ISRU pilot
    have to be before it becomes the better architecture", which is the question the reader of the
    recommendation actually asks. Nothing else about the option changes.
    """
    opt = case.investments["LUNAR_ISRU"]
    scaled = replace(opt, exercise_cost_mln=capex_mln, total_capex_mln=capex_mln + opt.option_fee_mln,
                     status="TEAM_ASSUMPTION", notes=f"гипотетический CAPEX {capex_mln:.1f} млн вместо {opt.exercise_cost_mln:.0f} млн (анализ порога)")
    return replace(case, investments=dict(case.investments, LUNAR_ISRU=scaled))


def plan_pv(case, a, scen, name: str, stress_aware: bool) -> tuple[float, bool]:
    """Present value of costs and admissibility of one architecture under one environment."""
    strat = dict(STRATEGIES[name], plan_id=f"{name}_x", stress_aware=stress_aware)
    r = simulate(case, build_plan(case, scen, strat, a), scen, a)
    return r.kpi["pv_cost_mln"], r.feasible


def crossover(f, lo: float, hi: float, tol: float):
    """Bisect the value where f (= PV of the recommendation - PV of the challenger) changes sign.

    Returns (value, None) when a sign change exists in [lo, hi], otherwise (None, reason).
    """
    f_lo, f_hi = f(lo), f(hi)
    if f_lo == 0:
        return lo, None
    if (f_lo > 0) == (f_hi > 0):
        return None, ("рекомендация дороже на всём диапазоне" if f_lo > 0 else "рекомендация дешевле на всём диапазоне")
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if (f(mid) > 0) == (f_lo > 0):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi), None


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
        rows.append(dict(row(r1, param="demand_multiplier", value=x, variant="план без изменений"), replanned_pv=r2.kpi["pv_cost_mln"],
                         replanned_min_sl=r2.kpi["min_service_level_total"], replanned_hard=r2.kpi["hard_violations"], replanned_shortage=r2.kpi["shortage_total_t"]))
        if thr_fixed is None and x > 1.0 and breaks(r1):
            thr_fixed = x
        if thr_replan is None and x > 1.0 and breaks(r2):
            thr_replan = x
    write_table(rows, RESULTS / "sensitivity" / "sweep_demand_multiplier.csv")
    summary.append(dict(param="demand_multiplier", range="0.80..1.30", threshold_fixed_plan=thr_fixed, threshold_replanned=thr_replan,
                        note="первые неуспешные точки сетки, не точные границы; перепланированный план при ×1,25 проходит ограничения, но уже имеет дефицит 12,437 т и минимальный годовой сервис 97,45 %; при ×1,30 нарушает ограничения"))
    tornado.append(dict(param="demand_multiplier", low=0.80, high=1.30, pv_low=rows[0]["pv_cost_mln"], pv_base=ref.kpi["pv_cost_mln"], pv_high=rows[-1]["pv_cost_mln"]))

    # 2. ISRU delivery share 2038
    rows, thr = [], None
    for x in frange(0.30, 1.00, 0.05):
        sc = scenario_from_dict({"scenario_id": f"TEAM_SENS_ISRU_{x}", "status": "TEAM_ASSUMPTION", "actual_delivery_share": {"Lunar-ISRU": {2038: x}}})
        r = simulate(case, plan, sc, a)
        rows.append(row(r, param="isru_delivery_share_2038", value=x, variant="план без изменений"))
    for rr in reversed(rows):
        if rr["hard"] > 0 or rr["min_sl_total"] < 0.97:
            thr = rr["value"]
            break
    write_table(rows, RESULTS / "sensitivity" / "sweep_isru_share_2038.csv")
    summary.append(dict(param="isru_delivery_share_2038", range="0.30..1.00", threshold_fixed_plan=thr, threshold_replanned=None,
                        note="наибольшая проверенная доля, при которой нарушается проверка резерва; 1,00 проходит, 0,95 нарушает; точная граница между ними не искалась"))
    tornado.append(dict(param="isru_delivery_share_2038", low=0.30, high=1.00, pv_low=rows[0]["pv_cost_mln"], pv_base=ref.kpi["pv_cost_mln"], pv_high=rows[-1]["pv_cost_mln"]))

    # 3. Core/Flex price multiplier
    rows = []
    for x in frange(0.80, 1.50, 0.10):
        sc = scenario_from_dict({"scenario_id": f"TEAM_SENS_PRICE_{x}", "status": "TEAM_ASSUMPTION",
                                 "variable_price_multiplier": {"Earth-Core": {"default": x}, "Earth-Flex": {"default": x}}})
        rows.append(row(simulate(case, plan, sc, a), param="earth_price_multiplier", value=x, variant="план без изменений"))
    write_table(rows, RESULTS / "sensitivity" / "sweep_earth_price_multiplier.csv")
    summary.append(dict(param="earth_price_multiplier", range="0.80..1.50", threshold_fixed_plan=None, threshold_replanned=None,
                        note="чисто стоимостной эффект; физические ограничения от цены не зависят"))
    tornado.append(dict(param="earth_price_multiplier", low=0.80, high=1.50, pv_low=rows[0]["pv_cost_mln"], pv_base=ref.kpi["pv_cost_mln"], pv_high=rows[-1]["pv_cost_mln"]))

    # 4. discount rate
    rows = []
    for x in frange(0.00, 0.12, 0.02):
        rows.append(row(simulate(case, plan, base, a.with_overrides(discount_rate_real=x)), param="discount_rate_real", value=x, variant="план без изменений"))
    write_table(rows, RESULTS / "sensitivity" / "sweep_discount_rate.csv")
    summary.append(dict(param="discount_rate_real", range="0.00..0.12", threshold_fixed_plan=None, threshold_replanned=None,
                        note="влияет только на PV; ранжирование альтернатив проверяется при каждой ставке (см. summary.md)"))
    tornado.append(dict(param="discount_rate_real", low=0.0, high=0.12, pv_low=rows[0]["pv_cost_mln"], pv_base=ref.kpi["pv_cost_mln"], pv_high=rows[-1]["pv_cost_mln"]))

    # 5. ZBO commissioning lag under mandatory stress (loss ceiling from 2038)
    rows, thr = [], None
    for lag in range(0, 13):
        r = simulate(case, plan, stress, a.with_overrides(zbo_commissioning_lag_months=lag))
        rows.append(row(r, param="zbo_commissioning_lag_months", value=lag, variant="план без изменений / MANDATORY_STRESS"))
        if thr is None and any(v.rule_id == "STRESS_LOSS_LIMIT" for v in r.violations):
            thr = lag
    write_table(rows, RESULTS / "sensitivity" / "sweep_zbo_lag_stress.csv")
    summary.append(dict(param="zbo_commissioning_lag_months", range="0..12", threshold_fixed_plan=thr, threshold_replanned=None,
                        note="первое нарушение именно годовой проверки потерь при задержке 10 мес.; задержки 7–9 мес. эту проверку ещё проходят; резерв и сервис нарушены уже при задержке 0; решение о ZBO 2037-07"))

    # 6. crossover: where does the challenger (P3) become cheaper than the recommendation (P2z)?
    years = case.years
    cross_rows = []

    def price_diff(scen, stress_aware: bool):
        def f(x: float) -> float:
            sc = scaled_prices(scen, case, x, years)
            return plan_pv(case, a, sc, RECOMMENDED, stress_aware)[0] - plan_pv(case, a, sc, CHALLENGER, stress_aware)[0]
        return f

    def rate_diff(scen, stress_aware: bool):
        def f(x: float) -> float:
            aa = a.with_overrides(discount_rate_real=x)
            return plan_pv(case, aa, scen, RECOMMENDED, stress_aware)[0] - plan_pv(case, aa, scen, CHALLENGER, stress_aware)[0]
        return f

    def isru_capex_diff(scen, stress_aware: bool):
        def f(x: float) -> float:
            c = case_with_isru_capex(case, x)
            return plan_pv(c, a, scen, RECOMMENDED, stress_aware)[0] - plan_pv(c, a, scen, CHALLENGER, stress_aware)[0]
        return f

    for metric_label, scen, stress_aware in (("PV в BASE", base, False),
                                             ("PV заблаговременно адаптированного обязательного стресса", stress, True)):
        for param, lo, hi, f in (("earth_price_multiplier", 0.50, 3.00, price_diff(scen, stress_aware)),
                                 ("discount_rate_real", 0.00, 0.20, rate_diff(scen, stress_aware)),
                                 ("isru_capex_mln", 100.0, 1250.0, isru_capex_diff(scen, stress_aware))):
            value, reason = crossover(f, lo, hi, CROSSOVER_TOL[param])
            row_ = dict(metric=metric_label, param=param, search_range=f"{lo:g}..{hi:g}",
                        crossover_value=(round(value, 4) if value is not None else None),
                        tolerance=CROSSOVER_TOL[param],
                        diff_at_low=round(f(lo), 1), diff_at_high=round(f(hi), 1))
            if value is None:
                row_["note"] = f"смены победителя в диапазоне нет: {reason}"
                row_["recommended_feasible_at_crossover"] = ""
                row_["challenger_feasible_at_crossover"] = ""
            else:
                case_at, a_at, sc_at = case, a, scen
                if param == "earth_price_multiplier":
                    sc_at = scaled_prices(scen, case, value, years)
                elif param == "discount_rate_real":
                    a_at = a.with_overrides(discount_rate_real=value)
                else:
                    case_at = case_with_isru_capex(case, value)
                pv_rec, ok_rec = plan_pv(case_at, a_at, sc_at, RECOMMENDED, stress_aware)
                pv_cha, ok_cha = plan_pv(case_at, a_at, sc_at, CHALLENGER, stress_aware)
                row_["pv_recommended_mln"] = round(pv_rec, 1)
                row_["pv_challenger_mln"] = round(pv_cha, 1)
                row_["recommended_feasible_at_crossover"] = ok_rec
                row_["challenger_feasible_at_crossover"] = ok_cha
                row_["note"] = (f"при значении выше {value:.4g} дешевле становится {CHALLENGER}"
                                if f(hi) > 0 else f"при значении ниже {value:.4g} дешевле становится {CHALLENGER}")
            cross_rows.append(row_)
    write_table(cross_rows, RESULTS / "sensitivity" / "crossover_P2z_vs_P3.csv")

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
    lines = [f"# EXP-04 Чувствительность — план {PLAN} (план BASE без изменений, если не указано иное)", "", f"Опорное значение PV затрат (BASE, r = 8 %): {ref.kpi['pv_cost_mln']:,.1f} млн", "",
             "## Пороги", "", "| Параметр | Диапазон | Порог (план без изменений) | Порог (перепланирован) | Примечание |", "|---|---|---:|---:|---|"]
    for s in summary:
        lines.append(f"| {s['param']} | {s['range']} | {s['threshold_fixed_plan'] if s['threshold_fixed_plan'] is not None else '—'} | "
                     f"{s['threshold_replanned'] if s['threshold_replanned'] is not None else '—'} | {s['note']} |")
    lines += ["", "## Торнадо (PV затрат, млн)", "", "| Параметр | Мин. | PV при мин. | PV база | Макс. | PV при макс. | Размах |", "|---|---:|---:|---:|---:|---:|---:|"]
    for t in sorted(tornado, key=lambda t: -abs(t["pv_high"] - t["pv_low"])):
        lines.append(f"| {t['param']} | {t['low']} | {t['pv_low']:,.0f} | {t['pv_base']:,.0f} | {t['high']} | {t['pv_high']:,.0f} | {abs(t['pv_high'] - t['pv_low']):,.0f} |")
    lines += ["", "## Порог смены победителя (P2z — рекомендация, P3 — альтернатива)", "",
              "Бисекция по каждому параметру: значение, при котором PV альтернативы становится ниже PV рекомендации. "
              "Оба плана перестраиваются под каждое значение параметра, поэтому это порог выбора архитектуры, а не сравнение фиксированных графиков.", "",
              "| Метрика решения | Параметр | Диапазон поиска | Порог | Точность | PV рекомендации | PV альтернативы | Допустимость на пороге | Вывод |",
              "|---|---|---|---:|---:|---:|---:|---|---|"]
    for c in cross_rows:
        adm = ("рекомендация: " + ("да" if c["recommended_feasible_at_crossover"] is True else "нет" if c["recommended_feasible_at_crossover"] is False else "—")
               + "; альтернатива: " + ("да" if c["challenger_feasible_at_crossover"] is True else "нет" if c["challenger_feasible_at_crossover"] is False else "—"))
        lines.append(f"| {c['metric']} | {c['param']} | {c['search_range']} | "
                     f"{c['crossover_value'] if c['crossover_value'] is not None else '—'} | ±{c['tolerance']:g} | "
                     f"{c.get('pv_recommended_mln', '—')} | {c.get('pv_challenger_mln', '—')} | {adm} | {c['note']} |")
    lines += ["", "## Ранжирование альтернатив по PV затрат при разных ставках дисконтирования (BASE)", "", "| r | " + " | ".join(STRATEGIES) + " |", "|---|" + "|".join("---:" for _ in STRATEGIES) + "|"]
    for x in (0.0, 0.04, 0.08, 0.12):
        vals = [next(rr for rr in rank_rows if rr["discount_rate"] == x and rr["plan_id"] == n) for n in STRATEGIES]
        lines.append(f"| {x:.2f} | " + " | ".join(f"{v['pv_cost_mln']:,.0f}{'' if v['feasible'] else ' (неисполним)'}" for v in vals) + " |")
    (RESULTS / "sensitivity" / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()

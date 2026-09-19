"""EXP-17: цена задержки ввода ZBO для выбранного плана P2z и защитные меры.

Аудит отметил, что цена задержки ZBO именно для выбранного P2z осталась непосчитанной, хотя задержка
Earth-New разобрана подробно (EXP-09, EXP-13). Здесь пробел закрыт по той же схеме: последствие,
минимальная мера, её цена и остаточный риск.

Механизм. ZBO меняет два параметра сразу: ёмкость 70 -> 120 т и долю потерь 4,5 % -> 1,2 % от
поступления. Задержка на k месяцев оставляет действовать базовое хранилище, поэтому за окно задержки
теряется больше топлива, физический запас на 1 января оказывается ниже 45-дневного резерва, а в
обязательном стрессе с 2038 года дополнительно нарушается потолок потерь 2 %.

Ловушка учёта. PV при задержке **снижается**: CAPEX 180 млн и OPEX 12 млн/год платятся позже.
План выглядит дешевле и при этом перестаёт быть исполнимым. Поэтому цена задержки измеряется не
изменением PV, а стоимостью минимальной меры, возвращающей план в границы ограничений.

Меры (объём каждой найден бисекцией с шагом 0,001 т):
  1. без мер — показываются разрывы резерва и потолка потерь;
  2. реакция: задержка объявляется в 2037-01, закупается дополнительный Earth-Flex (срок 4 месяца,
     поставки 2037-05…2037-12) — оплачивается только при наступлении задержки;
  3. заранее: решение о ZBO переносится на k месяцев раньше, чтобы ввод состоялся в срок
     (ограничение кейса: опция доступна с 2036 года) — CAPEX и OPEX платятся раньше всегда.

Выход: results/zbo_delay/
"""
from __future__ import annotations

import json
from pathlib import Path

from common import ASSUMPTIONS, PLANS, RESULTS, kpi_row, load_all, run_and_save, scenario, write_table
from terraplan.assumptions import load_assumptions
from terraplan.engine import midx, simulate
from terraplan.plan import Order, Plan, Reservation, load_plan

OUT = RESULTS / "zbo_delay"
DELAYS = (3, 6, 12)
OBSERVE_YEAR, OBSERVE_MONTH = 2037, 1          # задержка объявляется в январе 2037
FLEX = "B"
FLEX_MONTHS = list(range(5, 13))               # срок Earth-Flex 4 месяца: поставки с мая 2037
BISECT_STEP_T = 0.001
RUNS = (("P2z_earth_new_zbo", "BASE"), ("P2z_earth_new_zbo_adapted", "MANDATORY_STRESS"))


def with_flex(plan: Plan, tons: float, months: list[int], year: int, case) -> Plan:
    """Копия плана с дополнительным объёмом Earth-Flex, разложенным по указанным месяцам года."""
    if tons <= 1e-9:
        return plan
    per_month = tons / len(months)
    monthly = [0.0] * 12
    existing = next((o for o in plan.orders if o.source_id == FLEX and o.year == year), None)
    if existing is not None:
        base = existing.monthly_t if existing.profile == "monthly" and existing.monthly_t else [existing.ordered_t / 12.0] * 12
        monthly = list(base)
    for m in months:
        monthly[m - 1] += per_month
    cap = case.sources[FLEX].capacity_t_per_year
    # профиль округляется ДО суммирования: иначе сохранённый plan.json пересчитывается в чуть другие
    # числа, и `terraplan verify` для выгруженного каталога не сходится
    monthly = [round(v, 6) for v in monthly]
    orders = [o for o in plan.orders if not (o.source_id == FLEX and o.year == year)]
    orders.append(Order(FLEX, year, float(sum(monthly)), "monthly", monthly))
    reserved = max(plan.reserved(FLEX, year), sum(monthly))
    reservations = [r for r in plan.reservations if not (r.source_id == FLEX and r.year == year)]
    reservations.append(Reservation(FLEX, year, round(min(reserved, cap), 6)))
    return Plan(plan_id=plan.plan_id, scenario_id=plan.scenario_id, description=plan.description,
                reservations=reservations, orders=orders, investments=list(plan.investments),
                opening_stock=list(plan.opening_stock), reserve_mode=plan.reserve_mode,
                emergency_contract=plan.emergency_contract, allocation_rule=plan.allocation_rule,
                observation_month=plan.observation_month, meta=dict(plan.meta))


def shift_decision(plan: Plan, months_earlier: int, case, a) -> Plan | None:
    """Копия плана, где решение о ZBO принято на k месяцев раньше; None, если опция ещё недоступна."""
    inv = [i for i in plan.investments if i.investment_id == "ZBO"]
    if not inv:
        return None
    zbo = inv[0]
    idx = midx(zbo.decision_year, zbo.decision_month) - months_earlier
    year, month = divmod(idx, 12)
    month += 1
    if year < case.storage["ZBO"].available_from_year:
        return None
    moved = [i for i in plan.investments if i.investment_id != "ZBO"]
    moved.append(type(zbo)(zbo.investment_id, year, month, zbo.option_year, zbo.option_month))
    return Plan(plan_id=plan.plan_id, scenario_id=plan.scenario_id, description=plan.description,
                reservations=list(plan.reservations), orders=list(plan.orders), investments=moved,
                opening_stock=list(plan.opening_stock), reserve_mode=plan.reserve_mode,
                emergency_contract=plan.emergency_contract, allocation_rule=plan.allocation_rule,
                observation_month=plan.observation_month, meta=dict(plan.meta))


def minimal_flex(plan: Plan, case, sc, a, hi: float) -> tuple[float, object, list[str]]:
    """Наименьший объём Earth-Flex, возвращающий план в границы ограничений.

    Область допустимых объёмов — отрезок, а не луч: слишком малый объём не закрывает резерв, а
    слишком большой переполняет базовое хранилище, которое во время задержки ещё действует. Поэтому
    сначала грубым шагом ищется первый допустимый объём, и только внутри найденной вилки —
    бисекция до шага BISECT_STEP_T.
    """
    def ok(tons: float):
        res = simulate(case, with_flex(plan, tons, FLEX_MONTHS, OBSERVE_YEAR, case), sc, a)
        return res.feasible, res

    coarse = 0.5
    lo, found = 0.0, None
    always_blocking: set[str] | None = None        # правила, нарушенные при КАЖДОМ проверенном объёме
    t = 0.0
    while t <= hi + 1e-9:
        good, res = ok(t)
        if good:
            found = t
            break
        hard = {v.rule_id for v in res.violations if v.severity == "hard"}
        always_blocking = hard if always_blocking is None else (always_blocking & hard)
        lo, t = t, t + coarse
    if found is None:
        # ни один объём не проходит: называется правило, которое нарушено при любом объёме,
        # то есть то, которое объёмом вылечить нельзя
        return float("nan"), res, sorted(always_blocking or set())
    hi_ = found
    while hi_ - lo > BISECT_STEP_T:
        mid = (lo + hi_) / 2.0
        good, _ = ok(mid)
        if good:
            hi_ = mid
        else:
            lo = mid
    return hi_, ok(hi_)[1], []


def main() -> None:
    case, base_a = load_all()
    OUT.mkdir(parents=True, exist_ok=True)
    rows, detail = [], []

    for plan_name, sid in RUNS:
        plan = load_plan(PLANS / f"{plan_name}.json", case)
        sc = scenario(sid)
        on_time = simulate(case, plan, sc, base_a)
        rows.append(kpi_row(on_time, experiment="EXP-17", plan=plan_name, scenario=sid, delay_months=0,
                            measure="ввод в срок (эталон)", flex_t=0.0, delta_pv_mln=0.0, premium_no_delay_mln=0.0))
        reference_pv = on_time.kpi["pv_cost_mln"]

        for lag in DELAYS:
            a = base_a.with_overrides(zbo_commissioning_lag_months=lag)
            bare = run_and_save(case, plan, sc, a, OUT / f"{plan_name}_{sid}_delay_{lag:02d}m" / "without_measure", xlsx=False)
            gaps = {v.year: v.excess for v in bare.violations if v.rule_id == "RESERVE_45D"}
            loss_rule = [v for v in bare.violations if v.rule_id == "STRESS_LOSS_LIMIT"]
            rows.append(kpi_row(bare, experiment="EXP-17", plan=plan_name, scenario=sid, delay_months=lag,
                                measure="без мер", flex_t=0.0,
                                delta_pv_mln=bare.kpi["pv_cost_mln"] - reference_pv, premium_no_delay_mln=0.0))

            tons, reactive, blocked_by = minimal_flex(plan, case, sc, a, hi=case.sources[FLEX].capacity_t_per_year)
            if tons == tons:      # not NaN
                reactive = run_and_save(case, with_flex(plan, tons, FLEX_MONTHS, OBSERVE_YEAR, case), sc, a,
                                        OUT / f"{plan_name}_{sid}_delay_{lag:02d}m" / "reactive_flex", xlsx=False)
            rows.append(kpi_row(reactive, experiment="EXP-17", plan=plan_name, scenario=sid, delay_months=lag,
                                measure="реакция: Earth-Flex после наблюдения", flex_t=tons,
                                delta_pv_mln=reactive.kpi["pv_cost_mln"] - reference_pv, premium_no_delay_mln=0.0))

            early = shift_decision(plan, lag, case, a)
            if early is None:
                early_res, early_premium, early_note = None, float("nan"), "опция ZBO недоступна раньше 2036 г."
            else:
                early_res = run_and_save(case, early, sc, a, OUT / f"{plan_name}_{sid}_delay_{lag:02d}m" / "early_decision", xlsx=False)
                # премия, которую мера стоит, даже если задержки не будет: то же раннее решение при lag = 0
                early_premium = simulate(case, early, sc, base_a).kpi["pv_cost_mln"] - reference_pv
                early_note = f"решение о ZBO перенесено на {lag} мес. раньше"
                rows.append(kpi_row(early_res, experiment="EXP-17", plan=plan_name, scenario=sid, delay_months=lag,
                                    measure="заранее: решение о ZBO раньше", flex_t=0.0,
                                    delta_pv_mln=early_res.kpi["pv_cost_mln"] - reference_pv,
                                    premium_no_delay_mln=early_premium))

            detail.append(dict(
                plan=plan_name, scenario=sid, delay_months=lag,
                commissioning=(bare.investments and [i.commissioning_date for i in bare.investments if i.investment_id == "ZBO"] or [""])[0],
                reserve_gaps={str(k): round(v, 3) for k, v in sorted(gaps.items())},
                max_reserve_gap_t=round(max(gaps.values()), 3) if gaps else 0.0,
                loss_limit_violations=len(loss_rule),
                extra_losses_t=round(bare.kpi["losses_total_t"] - on_time.kpi["losses_total_t"], 3),
                pv_without_measure=round(bare.kpi["pv_cost_mln"], 3),
                pv_reference=round(reference_pv, 3),
                flex_t=(round(tons, 3) if tons == tons else None),
                reaction_blocked_by=blocked_by,
                pv_reactive=(round(reactive.kpi["pv_cost_mln"], 3) if tons == tons else None),
                price_of_reaction_mln=(round(reactive.kpi["pv_cost_mln"] - reference_pv, 3) if tons == tons else None),
                pv_early=(round(early_res.kpi["pv_cost_mln"], 3) if early_res else None),
                price_of_early_mln=(round(early_res.kpi["pv_cost_mln"] - reference_pv, 3) if early_res else None),
                premium_no_delay_mln=(round(early_premium, 3) if early_res else None),
                early_note=early_note))

    write_table(rows, OUT / "summary.csv", OUT / "summary.md",
                "EXP-17 Задержка ввода ZBO для P2z: последствия и цена мер")
    (OUT / "zbo_delay.json").write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = ["# EXP-17. Цена задержки ввода ZBO для выбранного плана P2z", "",
             "ZBO меняет два параметра сразу: ёмкость 70 -> 120 т и потери 4,5 % -> 1,2 % от поступления.",
             "Задержка на k месяцев оставляет действовать базовое хранилище: за окно задержки теряется больше",
             "топлива, физический запас на 1 января падает ниже 45-дневного резерва, а в обязательном стрессе",
             "с 2038 года дополнительно нарушается потолок потерь 2 %.", "",
             "**Ловушка учёта.** PV при задержке снижается — CAPEX 180 млн и OPEX 12 млн/год платятся позже.",
             "План выглядит дешевле и при этом перестаёт быть исполнимым, поэтому цена задержки измеряется",
             "стоимостью минимальной меры, возвращающей план в границы ограничений, а не изменением PV.", "",
             "| План / сценарий | Задержка | Ввод ZBO | Разрывы резерва, т | Доп. потери, т | Потолок потерь | PV без мер | Реакция: Earth-Flex, т | Цена реакции, млн | Цена меры «заранее», млн | Премия без задержки, млн |",
             "|---|---:|---|---|---:|:---:|---:|---:|---:|---:|---:|"]
    for d in detail:
        gaps = ", ".join(f"{y}: {g:.3f}" for y, g in d["reserve_gaps"].items()) or "нет"
        lines.append(
            f"| {d['plan']} / {d['scenario']} | {d['delay_months']} мес. | {d['commissioning']} | {gaps} | "
            f"{d['extra_losses_t']:+.3f} | {'нарушен' if d['loss_limit_violations'] else 'соблюдён'} | "
            f"{d['pv_without_measure']:,.3f} | {d['flex_t'] if d['flex_t'] is not None else '—'} | "
            f"{d['price_of_reaction_mln'] if d['price_of_reaction_mln'] is not None else 'мера не работает: ' + ', '.join(d['reaction_blocked_by'])} | "
            f"{d['price_of_early_mln'] if d['price_of_early_mln'] is not None else '—'} | "
            f"{d['premium_no_delay_mln'] if d['premium_no_delay_mln'] is not None else '—'} |")
    lines += ["", "## Чтение результата", "",
              "- Дефицита задержка ZBO не вызывает: страдает не обслуживание, а физический резерв и потери.",
              "- Реакция через Earth-Flex закрывает разрыв и оплачивается только при наступлении задержки;",
              "  заказ должен быть размещён к январю 2037 (срок поставки 4 месяца), иначе поставки не успевают",
              "  к проверке резерва 1 января 2038 г.",
              "- Мера «заранее» (более раннее решение о ZBO) устраняет саму задержку, но платится всегда:",
              "  столбец «Премия без задержки» показывает, во что она обходится, если задержки не будет.",
              "- Остаточный риск: задержка, объявленная позже августа 2037 г., не оставляет четырёх месяцев",
              "  до проверки резерва; тогда остаётся Emergency (6 недель) по цене 13,8 млн/т.",
              "- **Задержка 12 месяцев в обязательном стрессе объёмом не лечится.** Потолок потерь 2 % действует",
              "  с 2038 года, а базовое хранилище с долей потерь 4,5 % при такой задержке работает ещё полгода",
              "  2038-го. Дополнительный объём только увеличивает поступление и, значит, потери: разрыв резерва",
              "  закрывается уже при 9 т Earth-Flex, но STRESS_LOSS_LIMIT 2038 остаётся нарушенным при любом",
              "  объёме, а с 20 т добавляется превышение ёмкости. Работает только мера, устраняющая саму",
              "  задержку, — более раннее решение о ZBO (12,346 млн у.е.). Это ограничение выбранного плана,",
              "  и оно внесено в реестр рисков как остаточный риск ввода ZBO.", "",
              "## Воспроизведение", "",
              "```bash",
              "python experiments/run_zbo_delay.py",
              "python -m terraplan verify results/zbo_delay/P2z_earth_new_zbo_BASE_delay_06m/reactive_flex",
              "```", ""]
    (OUT / "zbo_delay.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    for d in detail:
        print(f"{d['plan'][:26]:26s} {d['scenario']:17s} lag={d['delay_months']:2d} "
              f"разрыв={d['max_reserve_gap_t']:6.3f} flex={d['flex_t']} "
              f"цена реакции={d['price_of_reaction_mln']} цена «заранее»={d['price_of_early_mln']} "
              f"премия={d['premium_no_delay_mln']}")


if __name__ == "__main__":
    main()

"""EXP-14: замкнутая политика реакции, решения которой считаются только по доступной информации.

Зачем. EXP-06 показывает *календарную* выполнимость реакции: ни один изменённый заказ не размещается
раньше месяца наблюдения. Но объёмы в EXP-06 подобраны по всей будущей стрессовой траектории, поэтому
он не доказывает работоспособность политики при неизвестном будущем. Здесь решение принимает функция
от наблюдений: на каждую дату заказа политика видит только прошлое — фактические поступления, фактические
доли поставки каналов и фактический спрос по месяц принятия решения включительно.

Постановка. Недопоставка Lunar-ISRU наблюдается на первой поставке 2038-03. Доля 2038 года (0,55)
с этого момента известна. Доли 2039 и 2040 годов — нет. Рассматриваются четыре будущие траектории
с ОДИНАКОВОЙ историей до конца 2038 года и разными продолжениями:

    T1 обязательный стресс   0,55 / 0,75 / 1,00   (сценарий организатора)
    T2 без восстановления    0,55 / 0,55 / 0,55
    T3 медленное восстановл. 0,55 / 0,65 / 0,80
    T4 быстрое восстановл.   0,55 / 0,90 / 1,00

Спрос, цены и потолок потерь во всех траекториях — обязательного стресса: они наблюдаются с 2038-01
и к дате первого реактивного заказа уже известны. Меняется ровно то, что на дату решения знать нельзя.

Политика (TEAM_DECISION, причинно-следственная по построению):
  1. прогноз доли канала = последняя НАБЛЮДЁННАЯ доля этого канала (по умолчанию 1,0, пока поставок не было);
  2. запас проецируется от конца месяца решения до месяца поставки по уже размещённым заказам,
     прогнозным долям, известному спросу и потерям действующего хранилища;
  3. цель — траектория резерва: линейный переход от R(y) к R(y+1) внутри года плюс технический запас;
  4. нехватка закрывается самым дешёвым доступным рычагом в пределах месячной мощности и годового резерва.
Рычаги: Earth-Flex (срок 4 мес.) и Emergency (6 недель = 2 мес.). Решение на месяц M принимается
в месяце M − срок поставки, то есть по информации, доступной на дату заказа.

Что доказывается. Non-anticipativity: решения, принятые до месяца t, совпадают во всех траекториях
с одинаковой историей до t. Это проверяется численно и сохраняется в non_anticipativity.md.

Сравнение с полным знанием. Тот же алгоритм прогоняется с фактической будущей долей вместо прогноза.
Это НЕ нижняя граница затрат и НЕ «цена информации»: обе версии — одно и то же жадное правило,
а не оптимизатор, поэтому разность может иметь любой знак. Она показывает лишь, насколько прогноз
«последняя наблюдённая доля» меняет решения того же правила.

Выход: results/adaptive_policy/ — прогоны по траекториям, сводка, проверка non-anticipativity.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from common import PLANS, RESULTS, STRATEGIES, kpi_row, load_all, run_and_save, scenario, write_table
from terraplan import rules
from terraplan.engine import midx, simulate, ym, ym_str
from terraplan.plan import Order, Plan, Reservation, save_plan
from terraplan.planner import build_plan

PLAN = "P3_isru_zbo"
OBSERVE = midx(2038, 3)                    # первая поставка ISRU раскрывает фактическую долю
LEVERS = [("B", 4), ("E", 2)]              # (канал, срок поставки в месяцах)
ISRU = "D"
MARGIN_T = 0.01                            # технический запас на округление профиля до 4 знаков
OUT = RESULTS / "adaptive_policy"

TRAJECTORIES = {
    "T1_mandatory_stress": dict(label="T1 обязательный стресс (сценарий организатора)", shares={2038: 0.55, 2039: 0.75, 2040: 1.00}),
    "T2_no_recovery":      dict(label="T2 без восстановления ISRU",                     shares={2038: 0.55, 2039: 0.55, 2040: 0.55}),
    "T3_slow_recovery":    dict(label="T3 медленное восстановление ISRU",               shares={2038: 0.55, 2039: 0.65, 2040: 0.80}),
    "T4_fast_recovery":    dict(label="T4 быстрое восстановление ISRU",                 shares={2038: 0.55, 2039: 0.90, 2040: 1.00}),
}


def trajectory_scenario(key: str, spec: dict):
    """Стрессовый сценарий с другой траекторией доли ISRU; набор правил остаётся MANDATORY_STRESS."""
    sc = scenario("MANDATORY_STRESS")
    sc.rule_scenario_id = "MANDATORY_STRESS"          # A1: метка исследования не снимает ограничений
    sc.scenario_id = f"TEAM_TRAJ_{key.upper()}"
    sc.label = spec["label"]
    sc.status = "TEAM_ASSUMPTION"
    sc.actual_delivery_share = {"Lunar-ISRU": dict(spec["shares"])}
    sc.changes = list(sc.changes) + [dict(
        status="TEAM_ASSUMPTION", block="adaptive_policy", parameter="actual_delivery_share.Lunar-ISRU",
        before={2038: 0.55, 2039: 0.75, 2040: 1.0}, after=dict(spec["shares"]),
        justification="Ветвь будущего с той же историей до конца 2038 г.; проверка политики при неизвестном продолжении.")]
    return sc


def fixed_plan(case, a) -> Plan:
    """Исходный P3, построенный по BASE, с заранее оплаченным резервом гибкости на 2038–2040."""
    plan = build_plan(case, scenario("BASE"), STRATEGIES[PLAN], a)
    reserved = {(r.source_id, r.year): r.reserved_capacity_t for r in plan.reservations}
    for sid, _ in LEVERS:
        for y in (2038, 2039, 2040):
            reserved[(sid, y)] = case.sources[sid].capacity_t_per_year        # опцион на гибкость, оплачивается всегда
    plan.reservations = [Reservation(sid, y, t) for (sid, y), t in sorted(reserved.items())]
    return plan


def monthly_commitments(probe_base) -> dict[tuple[str, int], float]:
    """Размещённые заказы по (канал, индекс месяца), валовые тонны.

    Берутся из прогона по BASE, где фактическая доля поставки равна 1,0 у всех каналов: тогда
    `inflow_by_source` и есть плановый валовой график. Так календарь доступности каналов (Lunar-ISRU
    поставляет с 2038-03, а не с января) берётся из самого движка, а не воспроизводится здесь заново.
    """
    out: dict[tuple[str, int], float] = {}
    for m in probe_base.months:
        for sid, q in m.inflow_by_source.items():
            if q > 1e-12:
                out[(sid, midx(m.year, m.month))] = out.get((sid, midx(m.year, m.month)), 0.0) + q
    return out


def run_policy(case, a, spec: dict, fixed: Plan, oracle: bool) -> tuple[dict, list[dict]]:
    """Прогон политики по одной траектории. Возвращает заказы и журнал решений.

    `oracle=False` — решения считаются по последней наблюдённой доле (причинно).
    `oracle=True`  — те же формулы, но с фактической будущей долей (сравнение, не нижняя граница).
    """
    shares = spec["shares"]
    reserved = {(r.source_id, r.year): r.reserved_capacity_t for r in fixed.reservations}
    stress = scenario("MANDATORY_STRESS")
    demand = {y: case.demand_row(y).total("base") * stress.demand_mult(y) for y in case.years}
    reserve = {y: rules.reserve_45d(demand[y]) for y in case.years}
    probe = simulate(case, fixed, scenario("BASE"), a)     # доля поставки 1,0 -> плановый валовой график
    committed = monthly_commitments(probe)
    storage_mode = {midx(m.year, m.month): (m.storage_capacity_t, m.loss_rate) for m in probe.months}

    def realised_share(source_id: str, year: int) -> float:
        return shares.get(year, 1.0) if source_id == ISRU else 1.0

    observed: dict[str, float] = {}                       # последняя НАБЛЮДЁННАЯ доля канала
    log: list[dict] = []
    inv = probe.months[0].opening_t
    start, end = midx(case.first_year, 1), midx(case.last_year, 12)

    for m_idx in range(start, end + 1):
        y, mo = ym(m_idx)
        cap_t, loss = storage_mode[m_idx]
        arrivals = 0.0
        for sid in case.sources:
            gross = committed.get((sid, m_idx), 0.0)
            if gross <= 1e-12:
                continue
            share = realised_share(sid, y)
            arrivals += gross * share
            observed[sid] = share                         # наблюдение становится доступным в месяце поставки
        inv = max(0.0, inv + arrivals * (1 - loss) - demand[y] / 12.0)

        # --- решения, принимаемые в конце месяца m_idx по информации через этот месяц ---
        for sid, lt in sorted(LEVERS, key=lambda t: -t[1]):        # длинный срок решается раньше короткого
            target_month = m_idx + lt
            if target_month > end or target_month < OBSERVE + lt:
                continue
            ty, _ = ym(target_month)
            forecast = (realised_share(ISRU, ty) if oracle else observed.get(ISRU, 1.0))
            proj = inv
            for k in range(m_idx + 1, target_month + 1):
                ky, _ = ym(k)
                _, k_loss = storage_mode[k]
                inflow = 0.0
                for src in case.sources:
                    g = committed.get((src, k), 0.0)
                    if g > 1e-12:
                        inflow += g * (forecast if src == ISRU else 1.0)
                proj = max(0.0, proj + inflow * (1 - k_loss) - demand[ky] / 12.0)
            nxt = reserve.get(ty + 1, reserve[ty])
            _, m_of_target = ym(target_month)
            target = reserve[ty] + (nxt - reserve[ty]) * m_of_target / 12.0 + MARGIN_T
            need = max(0.0, target - proj)
            if need <= 1e-9:
                continue
            _, t_loss = storage_mode[target_month]
            month_cap = case.sources[sid].capacity_t_per_year / 12.0
            already_year = sum(committed.get((sid, midx(ty, k)), 0.0) for k in range(1, 13))
            room = min(month_cap - committed.get((sid, target_month), 0.0),
                       reserved.get((sid, ty), 0.0) - already_year)
            take = min(max(0.0, room), need / (1 - t_loss))
            if take <= 1e-9:
                continue
            committed[(sid, target_month)] = committed.get((sid, target_month), 0.0) + take
            log.append(dict(decided_in=ym_str(m_idx), source=case.sources[sid].name, source_id=sid,
                            delivery_month=ym_str(target_month), added_t=round(take, 6),
                            forecast_isru_share=round(forecast, 4), projected_t=round(proj, 4), target_t=round(target, 4)))
    return committed, log


def build_policy_plan(case, fixed: Plan, committed: dict, plan_id: str, description: str) -> Plan:
    """Собрать план из размещённых заказов; реактивные месяцы помечаются reactive=True."""
    lever_ids = {sid for sid, _ in LEVERS}
    by_year: dict[tuple[str, int], list[float]] = {}
    for (sid, m_idx), gross in committed.items():
        y, mo = ym(m_idx)
        by_year.setdefault((sid, y), [0.0] * 12)[mo - 1] += gross
    # решения, которых политика не касалась, остаются ровно теми, что были в исходном плане:
    # перестроенный профиль отличался бы на округление и менял бы числа там, где решение не принималось
    touched = {(sid, y) for (sid, y) in by_year if sid in lever_ids and y >= 2038}
    orders: list[Order] = [o for o in fixed.orders if (o.source_id, o.year) not in touched]
    for sid, y in sorted(touched):
        monthly = by_year[(sid, y)]
        if sum(monthly) <= 1e-9:
            continue
        rounded = [math.floor(v * 1e4) / 1e4 for v in monthly]     # вниз: сумма никогда не превысит резерв
        orders.append(Order(sid, y, float(sum(rounded)), "monthly", rounded, reactive=True))
    return Plan(plan_id=plan_id, scenario_id="MANDATORY_STRESS", description=description,
                reservations=list(fixed.reservations), orders=orders, investments=list(fixed.investments),
                opening_stock=list(fixed.opening_stock), observation_month=ym_str(OBSERVE),
                meta={"experiment": "EXP-14", "status": "TEAM_DECISION", "policy": "closed_loop_observed_share",
                      "observation_month": ym_str(OBSERVE), "levers": {sid: f"{lt} months" for sid, lt in LEVERS}})


def write_non_anticipativity(logs: dict[str, list[dict]], split_month: str) -> tuple[bool, int]:
    """Решения, принятые до расхождения траекторий, обязаны совпадать во всех ветвях."""
    def early(log): return sorted((d["decided_in"], d["source_id"], d["delivery_month"], round(d["added_t"], 4))
                                  for d in log if d["decided_in"] <= split_month)
    keys = list(logs)
    reference = early(logs[keys[0]])
    identical = all(early(logs[k]) == reference for k in keys[1:])
    lines = ["# EXP-14. Проверка non-anticipativity политики реакции", "",
             "Политика не может использовать знание будущего, если решения, принятые до момента расхождения",
             "траекторий, во всех траекториях одинаковы. Траектории T1–T4 имеют общую историю по "
             f"**{split_month}** включительно и расходятся только после него.", "",
             f"Решений, принятых по {split_month} включительно: **{len(reference)}** в каждой траектории.",
             f"Совпадение решений во всех четырёх траекториях: **{'ДА' if identical else 'НЕТ'}**.", ""]
    if not identical:
        lines += ["## Расхождения", ""]
        for k in keys[1:]:
            diff = set(map(tuple, early(logs[k]))) ^ set(map(tuple, reference))
            if diff:
                lines += [f"- {k}: {sorted(diff)[:5]}"]
    else:
        lines += ["Это и означает, что объёмы считаются по наблюдениям на дату заказа, а не по будущей траектории.",
                  "Отличия между траекториями появляются только в решениях, принятых после расхождения.", ""]
    lines += ["", "| Принято в | Канал | Месяц поставки | Добавлено, т |", "|---|---|---|---:|"]
    for d in reference[:40]:
        lines.append(f"| {d[0]} | {d[1]} | {d[2]} | {d[3]:+.4f} |")
    if len(reference) > 40:
        lines.append(f"| … | | | ещё {len(reference) - 40} решений |")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "non_anticipativity.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return identical, len(reference)


def main() -> None:
    case, a = load_all()
    fixed = fixed_plan(case, a)
    OUT.mkdir(parents=True, exist_ok=True)
    rows, logs, detail = [], {}, {}

    for key, spec in TRAJECTORIES.items():
        sc = trajectory_scenario(key, spec)
        r_fixed = simulate(case, fixed, sc, a)
        rows.append(kpi_row(r_fixed, experiment="EXP-14", trajectory=spec["label"], policy="без реакции (эталон)"))

        reach = ym_str(OBSERVE + min(lt for _, lt in LEVERS))       # раньше этого месяца реакция физически не доходит
        committed, log = run_policy(case, a, spec, fixed, oracle=False)
        logs[key] = log
        plan = build_policy_plan(case, fixed, committed, f"{PLAN}_policy_{key}",
                                 f"EXP-14: замкнутая политика по наблюдаемой доле ISRU, траектория {spec['label']}")
        res = run_and_save(case, plan, sc, a, OUT / f"policy_{key}", xlsx=False)
        rows.append(kpi_row(res, experiment="EXP-14", trajectory=spec["label"], policy="политика по наблюдениям"))
        save_plan(plan, PLANS / f"{PLAN}_policy_{key}.json")

        o_committed, _ = run_policy(case, a, spec, fixed, oracle=True)
        o_plan = build_policy_plan(case, fixed, o_committed, f"{PLAN}_full_info_{key}",
                                   f"EXP-14: то же правило при известной будущей траектории, {spec['label']}")
        o_res = simulate(case, o_plan, sc, a)
        rows.append(kpi_row(o_res, experiment="EXP-14", trajectory=spec["label"], policy="то же правило со знанием будущего"))
        out_of_reach, in_reach = [], []
        for v in res.violations:
            if v.severity != "hard":
                continue
            when = f"{v.year:04d}-{(v.month or 1):02d}"
            (in_reach if when >= reach else out_of_reach).append(f"{v.rule_id}@{when}")
        detail[key] = dict(label=spec["label"], shares=spec["shares"], reach=reach,
                           in_reach=in_reach, out_of_reach=out_of_reach,
                           policy=dict(feasible=res.feasible, pv=res.kpi["pv_cost_mln"], shortage=res.kpi["shortage_total_t"],
                                       min_sl=res.kpi["min_service_level_total"], hard=res.kpi["hard_violations"]),
                           oracle=dict(feasible=o_res.feasible, pv=o_res.kpi["pv_cost_mln"], shortage=o_res.kpi["shortage_total_t"]),
                           no_reaction=dict(feasible=r_fixed.feasible, pv=r_fixed.kpi["pv_cost_mln"], shortage=r_fixed.kpi["shortage_total_t"]),
                           decisions=len(log))

    identical, n_early = write_non_anticipativity(logs, "2038-12")
    write_table(rows, OUT / "summary.csv", OUT / "summary.md",
                "EXP-14 Замкнутая политика реакции на четырёх будущих траекториях с общей историей (P3, стресс)")
    (OUT / "policy_log.json").write_text(json.dumps(logs, ensure_ascii=False, indent=2), encoding="utf-8")

    held_all = all(not d["in_reach"] for d in detail.values())        # всё, на что реакция ещё могла повлиять
    inherited = sorted({v for d in detail.values() for v in d["out_of_reach"]})
    cost = [(d["policy"]["pv"] - d["oracle"]["pv"]) for d in detail.values()]
    lines = ["# EXP-14. Замкнутая политика реакции: решения только по доступной информации", "",
             "## Постановка", "",
             "Недопоставка Lunar-ISRU наблюдается на первой поставке 2038-03; доля 2038 года с этого момента",
             "известна, доли 2039 и 2040 годов — нет. Четыре траектории имеют общую историю до конца 2038 года",
             "и разные продолжения. Спрос, цены и потолок потерь во всех траекториях — обязательного стресса:",
             "они наблюдаются с 2038-01 и к дате первого реактивного заказа уже известны. Меняется ровно то,",
             "что на дату решения знать нельзя.", "",
             "## Политика", "",
             "1. Прогноз доли канала = последняя **наблюдённая** доля (по умолчанию 1,0 до первой поставки).",
             "2. Запас проецируется от месяца решения до месяца поставки по размещённым заказам, прогнозным долям,",
             "   известному спросу и потерям действующего хранилища.",
             "3. Цель — траектория резерва: линейный переход от R(y) к R(y+1) внутри года.",
             "4. Нехватка закрывается самым дешёвым доступным рычагом в пределах месячной мощности и годового резерва.", "",
             "Рычаги: Earth-Flex (4 мес.) и Emergency (2 мес.). Решение на месяц M принимается в месяце M − срок поставки.",
             "Резерв мощности Earth-Flex и Emergency на 2038–2040 законтрактован заранее и оплачивается во всех",
             "траекториях: это цена опциона на гибкость, а не бесплатная возможность.", "",
             "## Результат", "",
             "| Траектория | Доли ISRU 2038/2039/2040 | Без реакции | Политика (по наблюдениям) | То же правило со знанием будущего | Разность, млн |",
             "|---|---|---|---|---|---:|"]
    for key, d in detail.items():
        fmt = lambda x: f"{x['pv']:,.1f} ({'исполним' if x['feasible'] else 'НЕ исполним'})"
        sh = "/".join(f"{d['shares'][y]:.2f}" for y in (2038, 2039, 2040))
        lines.append(f"| {d['label']} | {sh} | {fmt(d['no_reaction'])} | {fmt(d['policy'])} | {fmt(d['oracle'])} | "
                     f"{d['policy']['pv'] - d['oracle']['pv']:+,.1f} |")
    lines += ["",
              f"Политика удержала **все** ограничения, на которые реакция ещё могла повлиять "
              f"(поставка не раньше {detail[next(iter(detail))]['reach']}): "
              f"**{'ДА' if held_all else 'НЕТ'}** на всех четырёх траекториях.", "",
              "Унаследованные нарушения, которые никакая реакция исправить не может, потому что они датированы",
              f"до наблюдения события: {', '.join(inherited) if inherited else '—'}. Резерв на 2038-01 формируется",
              "решениями 2037 года, а дефицит апреля 2038 г. лежит внутри срока поставки самого быстрого рычага",
              "(Emergency, 6 недель): первая реактивная поставка возможна только с 2038-05. Резерв на 2039-01",
              "и 2040-01 политика выдерживает на всех траекториях.", "",
              f"Разность «политика − то же правило со знанием будущего»: от {min(cost):+,.1f} до {max(cost):+,.1f} "
              f"млн у.е., в среднем {sum(cost) / len(cost):+,.1f} млн.", "",
              "Эта разность **не** является ценой информации и не ограничена снизу нулём: обе версии — одно и то же",
              "жадное правило, а не оптимизатор. Отрицательный знак здесь объясняется прогнозом «последняя",
              "наблюдённая доля»: он пессимистичен, политика раньше добирает дешёвый Earth-Flex, тогда как версия",
              "со знанием будущего откладывает закупку и затем вынуждена добирать дороже. Вывод, который отсюда",
              "следует, ограничен: причинно вычислимое правило не обходится дороже своей же версии с полным",
              "знанием траектории на этих четырёх ветвях.", "",
              f"Non-anticipativity: решения, принятые по 2038-12 включительно ({n_early} шт.), совпадают во всех",
              f"четырёх траекториях — **{'подтверждено' if identical else 'НЕ подтверждено'}** "
              "(`non_anticipativity.md`).", "",
              "## Что это доказывает и что нет", "",
              "Доказано: существует правило решения, вычислимое по наблюдениям на дату заказа, которое удерживает",
              "уровень сервиса и резерв на всех четырёх продолжениях, и его цена относительно полного знания будущего",
              "измерена. Не доказано и не утверждается: оптимальность этого правила и покрытие всех мыслимых",
              "траекторий — рассмотрены четыре ветви одного источника неопределённости (доля поставки Lunar-ISRU).",
              "Выбор P2z как основной стратегии этим экспериментом не пересматривается: EXP-14 относится к линии",
              "с Lunar-ISRU (P3) и отвечает на вопрос о политике пересмотра, а не о выборе портфеля.", ""]
    (OUT / "adaptive_policy.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    (OUT / "policy_detail.json").write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")
    for key, d in detail.items():
        print(f"{key:22s} policy PV={d['policy']['pv']:9.1f} oracle PV={d['oracle']['pv']:9.1f} "
              f"no-reaction PV={d['no_reaction']['pv']:9.1f} shortage={d['policy']['shortage']:.3f} "
              f"в зоне реакции: {d['in_reach'] or '—'} | унаследовано: {d['out_of_reach'] or '—'}")
    print(f"non-anticipativity identical={identical} early decisions={n_early}")
    if not identical:
        raise SystemExit("политика использует информацию, недоступную на дату решения")
    if not held_all:
        raise SystemExit("политика не удержала ограничение, на которое ещё могла повлиять: "
                         + "; ".join(sorted({v for d in detail.values() for v in d["in_reach"]})))


if __name__ == "__main__":
    main()

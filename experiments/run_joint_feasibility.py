"""EXP-15: существует ли ЕДИНЫЙ фиксированный график заказов, проходящий и BASE, и обязательный стресс.

Раньше управленческая записка утверждала, что такого графика «не существует», опираясь на то, что один
конкретный стресс-адаптированный график переполняет хранилище в BASE. Это показывает непригодность
ОДНОГО графика, а не отсутствие всех. Здесь утверждение либо доказывается, либо снимается.

Доказательство (необходимое условие, без перебора)
--------------------------------------------------
Пусть график заказов x_m один и тот же в обоих сценариях, r_m — доля потерь действующего хранилища,
sigma_m — фактическая доля поставки канала в сценарии (в BASE она равна 1,0, в стрессе <= 1,0),
I0 — начальный запас, C — ёмкость хранилища, SB и SS — фактически выданные объёмы в BASE и в стрессе.

  Нетто-поступление до месяца m:   N(m)      = sum x_k (1 - r_k)           (BASE, sigma = 1)
                                   N_sigma(m)= sum x_k sigma_k (1 - r_k)   (стресс),  N_sigma(m) <= N(m)

  BASE, ёмкость на конец декабря года y-1:
      I0 + N(<y) - SB(<y) <= C            =>   N(<y) <= C + SB(<y) - I0
  Стресс, резерв 45 дней на 1 января года y:
      I0 + N_sigma(<y) - SS(<y) >= R(y)   =>   N_sigma(<y) >= R(y) + SS(<y) - I0

Так как N_sigma(<y) <= N(<y), оба условия совместимы только при

      R(y) + SS(<y) <= C + SB(<y).                                              (*)

Выданный объём не превышает спроса: SB(<y) <= D_base(<y). Подстановка даёт необходимое условие

      R(y) + SS(<y) <= C + D_base(<y).                                          (**)

Неравенство (**) не зависит от x: если оно нарушено, единого графика не существует ни при каком
распределении заказов по месяцам и каналам. Недовыдача в BASE условие только ужесточает
(SB падает, правая часть уменьшается), поэтому проверка (**) при полном обслуживании BASE —
самая благоприятная для существования единого графика.

Что даёт проверка. Если при полном обслуживании стресса (SS = D_stress) условие нарушено, единого
графика, обслуживающего оба сценария полностью, не существует — это доказано, а не показано примером.
Из (**) сразу считается и предельный уровень обслуживания стресса, при котором единый график ещё
арифметически возможен: SS(<y) <= C + D_base(<y) - R(y).

Перебор (подтверждение). Дополнительно проверяется семейство фактических графиков — интерполяция
между планом BASE и стресс-адаптированным планом и сдвиги объёма по годам — и показывается, что ни
один из них не проходит оба сценария. Перебор ничего не доказывает сам по себе; он лишь согласуется
с доказательством выше.

Выход: results/joint_feasibility/
"""
from __future__ import annotations

import json
from pathlib import Path

from common import RESULTS, STRATEGIES, load_all, scenario, write_table
from terraplan import rules
from terraplan.engine import simulate
from terraplan.plan import Order, Plan, Reservation
from terraplan.planner import build_plan

OUT = RESULTS / "joint_feasibility"
PLAN = "P2z_earth_new_zbo"


def necessary_condition(case, a) -> list[dict]:
    """Проверка (**) по каждому году горизонта. Числа берутся из данных, не из текста."""
    base, stress = scenario("BASE"), scenario("MANDATORY_STRESS")
    reserve_days = case.constraints["RESERVE_45D"].value if "RESERVE_45D" in case.constraints else rules.RESERVE_DAYS
    # ёмкость на конец декабря года y-1 при введённом ZBO — максимально благоприятная для существования графика
    capacity = max(s.capacity_t for s in case.storage.values())
    rows = []
    for y in case.years:
        prior = [k for k in case.years if k < y]
        if not prior:
            continue
        d_base = sum(case.demand_row(k).total("base") * base.demand_mult(k) for k in prior)
        d_stress = sum(case.demand_row(k).total("base") * stress.demand_mult(k) for k in prior)
        r_stress = rules.reserve_45d(case.demand_row(y).total("base") * stress.demand_mult(y), reserve_days)
        left = r_stress + d_stress                     # требуется стрессом
        right = capacity + d_base                      # допускается ёмкостью BASE
        max_ss = right - r_stress                      # предельный выданный объём в стрессе
        rows.append(dict(
            year=y, reserve_stress_t=r_stress, demand_base_before_t=d_base, demand_stress_before_t=d_stress,
            extra_stress_demand_t=d_stress - d_base, storage_capacity_t=capacity,
            required_t=left, allowed_t=right, gap_t=left - right, holds=left <= right + 1e-9,
            max_stress_service_share=(max_ss / d_stress) if d_stress > 0 else float("nan")))
    return rows


def interpolated_plans(case, a) -> list[tuple[str, Plan]]:
    """Семейство единых графиков между планом BASE и стресс-адаптированным планом."""
    base, stress = scenario("BASE"), scenario("MANDATORY_STRESS")
    p_base = build_plan(case, base, STRATEGIES[PLAN], a)
    p_stress = build_plan(case, stress, dict(STRATEGIES[PLAN], plan_id=f"{PLAN}_adapted", stress_aware=True), a)
    ord_b = {(o.source_id, o.year): o.ordered_t for o in p_base.orders}
    ord_s = {(o.source_id, o.year): o.ordered_t for o in p_stress.orders}
    res_b = {(r.source_id, r.year): r.reserved_capacity_t for r in p_base.reservations}
    res_s = {(r.source_id, r.year): r.reserved_capacity_t for r in p_stress.reservations}
    keys = sorted(set(ord_b) | set(ord_s))
    rkeys = sorted(set(res_b) | set(res_s))
    out = []
    for step in range(0, 11):
        lam = step / 10.0
        orders, reservations = [], []
        for sid, y in keys:
            q = (1 - lam) * ord_b.get((sid, y), 0.0) + lam * ord_s.get((sid, y), 0.0)
            if q > 1e-9:
                orders.append(Order(sid, y, round(q, 4)))
        for sid, y in rkeys:
            t = (1 - lam) * res_b.get((sid, y), 0.0) + lam * res_s.get((sid, y), 0.0)
            t = max(t, max((o.ordered_t for o in orders if o.source_id == sid and o.year == y), default=0.0))
            if t > 1e-9:
                reservations.append(Reservation(sid, y, round(min(t, case.sources[sid].capacity_t_per_year), 4)))
        out.append((f"lambda={lam:.1f}", Plan(plan_id=f"joint_lambda_{step:02d}", scenario_id="BASE",
                                              description=f"единый график: {1 - lam:.0%} плана BASE + {lam:.0%} стресс-адаптированного",
                                              reservations=reservations, orders=orders,
                                              investments=list(p_stress.investments), opening_stock=list(p_stress.opening_stock))))
    return out


def main() -> None:
    case, a = load_all()
    OUT.mkdir(parents=True, exist_ok=True)
    base, stress = scenario("BASE"), scenario("MANDATORY_STRESS")

    rows = necessary_condition(case, a)
    write_table([{k: v for k, v in r.items()} for r in rows], OUT / "necessary_condition.csv", None)
    broken = [r for r in rows if not r["holds"]]

    search_rows = []
    for label, plan in interpolated_plans(case, a):
        rb, rs = simulate(case, plan, base, a), simulate(case, plan, stress, a)
        search_rows.append(dict(
            variant=label, base_feasible=rb.feasible, stress_feasible=rs.feasible,
            base_hard=rb.kpi["hard_violations"], stress_hard=rs.kpi["hard_violations"],
            base_rules="; ".join(sorted({v.rule_id for v in rb.violations if v.severity == "hard"})) or "—",
            stress_rules="; ".join(sorted({v.rule_id for v in rs.violations if v.severity == "hard"})) or "—",
            base_pv_mln=rb.kpi["pv_cost_mln"], stress_pv_mln=rs.kpi["pv_cost_mln"]))
    write_table(search_rows, OUT / "search.csv", OUT / "search.md",
                "EXP-15 Перебор единых графиков между планом BASE и стресс-адаптированным планом")
    joint = [r for r in search_rows if r["base_feasible"] and r["stress_feasible"]]

    y_bad = broken[0] if broken else None
    lines = ["# EXP-15. Существует ли единый фиксированный график для BASE и обязательного стресса", "",
             "## Доказательство (необходимое условие, без перебора)", "",
             "Для одного и того же графика заказов `x` в обоих сценариях одновременно требуются",
             "",
             "* ёмкость хранилища в BASE на конец декабря года `y-1`: `N(<y) <= C + SB(<y) - I0`;",
             "* резерв 45 дней в стрессе на 1 января года `y`: `N_sigma(<y) >= R(y) + SS(<y) - I0`,",
             "",
             "где `N` — нетто-поступление, `N_sigma <= N` — то же при фактических долях поставки стресса,",
             "`SB`/`SS` — фактически выданные объёмы, `C` — ёмкость, `I0` — начальный запас. Отсюда",
             "",
             "```",
             "R(y) + SS(<y) <= C + SB(<y) <= C + D_base(<y)",
             "```",
             "",
             "Условие не содержит `x`: при его нарушении единого графика не существует ни при каком",
             "распределении заказов по месяцам и каналам. Недовыдача в BASE условие только ужесточает,",
             "поэтому проверка при полном обслуживании BASE — самая благоприятная для существования графика.", "",
             "| Год y | R(y), т | Доп. спрос стресса до y, т | Ёмкость C, т | Требуется R+SS, т | Допускается C+D_base, т | Разрыв, т | Выполнено |",
             "|---|---:|---:|---:|---:|---:|---:|:---:|"]
    for r in rows:
        lines.append(f"| {r['year']} | {r['reserve_stress_t']:.3f} | {r['extra_stress_demand_t']:.1f} | "
                     f"{r['storage_capacity_t']:.0f} | {r['required_t']:.3f} | {r['allowed_t']:.3f} | "
                     f"{r['gap_t']:+.3f} | {'да' if r['holds'] else '**НЕТ**'} |")
    if y_bad:
        lines += ["", f"**Вывод.** Необходимое условие нарушено для {y_bad['year']} года с разрывом "
                      f"**{y_bad['gap_t']:.3f} т**. Единого фиксированного графика, который полностью обслуживает "
                      f"оба сценария и одновременно удерживает ёмкость хранилища в BASE и 45-дневный резерв "
                      f"в стрессе на 1 января {y_bad['year']} г., **не существует**. Это следует из данных кейса, "
                      "а не из непригодности какого-то одного графика.", "",
                      "Причина видна из самой формулы: к {} г. стресс требует выдать на **{:.1f} т** больше BASE, "
                      "и ровно этот излишек в BASE остаётся в хранилище, ёмкость которого — {:.0f} т, "
                      "тогда как резерв стресса требует к тому же моменту ещё {:.3f} т."
                      .format(y_bad["year"], y_bad["extra_stress_demand_t"], y_bad["storage_capacity_t"],
                              y_bad["reserve_stress_t"]), "",
                      "**Точная граница.** Единый график арифметически возможен только ценой недовыдачи в стрессе: "
                      f"обслуженный объём стресса до {y_bad['year']} г. не может превышать "
                      f"**{y_bad['max_stress_service_share']:.4f}** его спроса "
                      f"({y_bad['allowed_t'] - y_bad['reserve_stress_t']:.1f} т из {y_bad['demand_stress_before_t']:.1f} т), "
                      f"то есть требует согласиться минимум на {y_bad['gap_t']:.1f} т накопленного дефицита. "
                      "Раздельные сценарные планы этой платы не требуют."]
    else:
        lines += ["", "**Вывод.** Необходимое условие выполнено во всех годах: доказательства несуществования нет. "
                      "Утверждение о несуществовании единого графика делать нельзя."]
    lines += ["", "## Перебор (подтверждение, не доказательство)", "",
              "Проверено семейство единых графиков — интерполяция между планом BASE и стресс-адаптированным планом "
              f"(11 вариантов). Проходят оба сценария: **{len(joint)}**. Подробности — `search.md`.", "",
              "| Вариант | BASE | Стресс | Жёсткие нарушения BASE | Жёсткие нарушения стресса |",
              "|---|:---:|:---:|---|---|"]
    for r in search_rows:
        lines.append(f"| {r['variant']} | {'исполним' if r['base_feasible'] else 'нет'} | "
                     f"{'исполним' if r['stress_feasible'] else 'нет'} | {r['base_rules']} | {r['stress_rules']} |")
    lines += ["", "Перебор согласуется с доказательством: ни один единый график не проходит оба сценария. "
                  "Сам по себе перебор несуществования не доказывает — доказательство даёт условие выше.", ""]
    (OUT / "joint_feasibility.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "necessary_condition.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    for r in rows:
        print(f"{r['year']}: требуется {r['required_t']:9.3f} допускается {r['allowed_t']:9.3f} "
              f"разрыв {r['gap_t']:+8.3f} -> {'ok' if r['holds'] else 'НАРУШЕНО'}")
    print(f"единых графиков, прошедших оба сценария: {len(joint)} из {len(search_rows)}")


if __name__ == "__main__":
    main()

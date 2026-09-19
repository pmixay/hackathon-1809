"""Independent check that a stress response uses only information available at the time.

A план реакции is only honest if it changes nothing that had to be decided before the event was
visible. The engine already refuses a reactive delivery ordered before the observation month; this
checker is a second, independent gate that reads the two plan files and compares them decision by
decision, so a hand-edited or regenerated response plan cannot quietly acquire foresight.

Rules (each failure names the decision, the month and why it is not available):
  I1  investments identical — an irreversible commitment cannot be rewritten after the fact;
  I2  opening stock identical — it is delivered in the preparatory period, before the horizon;
  I3  every changed delivery must be orderable after the observation:
      order placement month = delivery month - lead time >= observation month;
  I4  only the declared reaction channels may change;
  I5  a reservation may only be raised for a period that can still be contracted after the
      observation, i.e. from the observation year onwards.

Usage:  python experiments/check_stress_response.py <base plan.json> <response plan.json>
                [--levers B,E] [--observation YYYY-MM]
Exit code 0 when every rule holds, 1 otherwise.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import load_all
from terraplan.engine import lead_months, midx, parse_ym, ym_str
from terraplan.plan import load_plan

TOL_T = 1e-6                     # tonnes below this are rounding of the saved 4-decimal profile


def monthly_orders(plan, case) -> dict[tuple[str, int, int], float]:
    """Deliveries by (source, year, month).

    An order without a monthly profile is spread over the whole year, so its earliest delivery is
    January: the checker then requires the ORDER for that January delivery to be placeable after the
    observation. This is deliberately strict — a response that reacts inside a year must say in which
    months it delivers, otherwise it is indistinguishable from a plan written with foresight.
    """
    out: dict[tuple[str, int, int], float] = {}
    for o in plan.orders:
        if o.monthly_t:
            months = [float(v) for v in o.monthly_t]
        else:
            months = [o.ordered_t / 12.0] * 12
        for i, tons in enumerate(months):
            if abs(tons) > TOL_T:
                out[(o.source_id, o.year, i + 1)] = out.get((o.source_id, o.year, i + 1), 0.0) + tons
    return out


def reservations(plan) -> dict[tuple[str, int], float]:
    out: dict[tuple[str, int], float] = {}
    for r in plan.reservations:
        out[(r.source_id, r.year)] = out.get((r.source_id, r.year), 0.0) + r.reserved_capacity_t
    return out


def investments(plan) -> dict[str, tuple]:
    return {i.investment_id: (i.option_year, i.option_month, i.decision_year, i.decision_month) for i in plan.investments}


def check(base_plan, response_plan, case, a, levers: list[str] | None, observation: str | None):
    """Return (list of violations, list of change rows). Both are plain dicts, ready to print."""
    obs = observation or response_plan.observation_month
    if not obs:
        return ([{"rule": "I0", "what": "месяц наблюдения",
                  "why": "план реакции не объявляет месяц наблюдения события (inventory_policy.observation_month)"}], [])
    obs_idx = parse_ym(obs)
    allowed = levers if levers is not None else sorted({o.source_id for o in response_plan.orders if o.reactive})
    viol: list[dict] = []
    rows: list[dict] = []

    b_inv, r_inv = investments(base_plan), investments(response_plan)
    for inv_id in sorted(set(b_inv) | set(r_inv)):
        if b_inv.get(inv_id) != r_inv.get(inv_id):
            viol.append({"rule": "I1", "what": f"инвестиция {inv_id}",
                         "why": f"инвестиционное решение изменено в ответе ({b_inv.get(inv_id)} → {r_inv.get(inv_id)}); "
                                "оно принимается до наблюдения события и необратимо"})

    b_stock = [(s.source_id, s.delivery_year, s.delivery_month, s.tons) for s in base_plan.opening_stock]
    r_stock = [(s.source_id, s.delivery_year, s.delivery_month, s.tons) for s in response_plan.opening_stock]
    if b_stock != r_stock:
        viol.append({"rule": "I2", "what": "начальный запас",
                     "why": "поставки подготовительного периода изменены; они происходят до начала горизонта и до наблюдения"})

    b_ord, r_ord = monthly_orders(base_plan, case), monthly_orders(response_plan, case)
    for key in sorted(set(b_ord) | set(r_ord)):
        sid, year, month = key
        before, after = b_ord.get(key, 0.0), r_ord.get(key, 0.0)
        delta = after - before
        if abs(delta) <= TOL_T:
            continue
        lt = lead_months(case.sources[sid], a)
        placement = midx(year, month) - lt
        rows.append({"source_id": sid, "source": case.sources[sid].name, "year": year, "month": month,
                     "delivery_month": f"{year:04d}-{month:02d}", "before_t": round(before, 4), "after_t": round(after, 4),
                     "delta_t": round(delta, 4), "lead_time_months": lt, "order_by": ym_str(placement),
                     "available": placement >= obs_idx})
        if sid not in allowed:
            viol.append({"rule": "I4", "what": f"{case.sources[sid].name} {year}-{month:02d}",
                         "why": f"канал {sid} не объявлен рычагом реакции (разрешены: {', '.join(allowed) or '—'})"})
        if placement < obs_idx:
            viol.append({"rule": "I3", "what": f"{case.sources[sid].name} поставка {year}-{month:02d} ({delta:+.3f} т)",
                         "why": f"заказ пришлось бы разместить {ym_str(placement)} (срок поставки {lt} мес.), "
                                f"то есть до наблюдения события {obs}"})

    b_res, r_res = reservations(base_plan), reservations(response_plan)
    obs_year = int(obs.split("-")[0])
    for key in sorted(set(b_res) | set(r_res)):
        sid, year = key
        before, after = b_res.get(key, 0.0), r_res.get(key, 0.0)
        if abs(after - before) <= TOL_T:
            continue
        rows.append({"source_id": sid, "source": case.sources[sid].name, "year": year, "month": 0,
                     "delivery_month": f"{year} (резерв мощности)", "before_t": round(before, 4), "after_t": round(after, 4),
                     "delta_t": round(after - before, 4), "lead_time_months": "", "order_by": f"{year}",
                     "available": year >= obs_year and sid in allowed})
        if sid not in allowed:
            viol.append({"rule": "I4", "what": f"резерв {case.sources[sid].name} {year}",
                         "why": f"канал {sid} не объявлен рычагом реакции (разрешены: {', '.join(allowed) or '—'})"})
        elif year < obs_year:
            viol.append({"rule": "I5", "what": f"резерв {case.sources[sid].name} {year}",
                         "why": f"период {year} закончился до наблюдения события {obs}; договорной объём этого года уже нельзя пересмотреть"})
    return viol, rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Проверка того, что план реакции не использует будущую информацию")
    ap.add_argument("base", type=Path, help="план до события")
    ap.add_argument("response", type=Path, help="план реакции")
    ap.add_argument("--levers", default=None, help="разрешённые каналы реакции через запятую, например B,E")
    ap.add_argument("--observation", default=None, help="месяц наблюдения ГГГГ-ММ (по умолчанию из плана реакции)")
    args = ap.parse_args(argv)

    case, a = load_all()
    base_plan, response_plan = load_plan(args.base), load_plan(args.response)
    levers = [s.strip() for s in args.levers.split(",") if s.strip()] if args.levers else None
    viol, rows = check(base_plan, response_plan, case, a, levers, args.observation)

    obs = args.observation or response_plan.observation_month or "—"
    print(f"План до события: {base_plan.plan_id}")
    print(f"План реакции:    {response_plan.plan_id}")
    print(f"Месяц наблюдения события: {obs}")
    if rows:
        print(f"\nИзменённые решения ({len(rows)}):")
        print(f"  {'канал':<14}{'период':<22}{'было, т':>12}{'стало, т':>12}{'изменение, т':>14}  заказать до  доступно")
        for r in sorted(rows, key=lambda r: (r["year"], r["month"], r["source_id"])):
            print(f"  {r['source']:<14}{r['delivery_month']:<22}{r['before_t']:>12.3f}{r['after_t']:>12.3f}"
                  f"{r['delta_t']:>+14.3f}  {r['order_by']:<12} {'да' if r['available'] else 'НЕТ'}")
    else:
        print("\nИзменённых решений нет.")
    if viol:
        print(f"\nНАРУШЕНИЯ ПРАВИЛА РЕАКЦИИ ({len(viol)}):")
        for v in viol:
            print(f"  [{v['rule']}] {v['what']}: {v['why']}")
        return 1
    print("\nПравило реакции выполнено: изменены только объявленные рычаги и только те решения, "
          "которые ещё можно принять после наблюдения события.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

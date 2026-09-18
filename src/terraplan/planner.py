"""Greedy merit-order plan builder (a TEAM_DECISION helper, not an optimizer).

Given a strategy (investments, reservation caps per source, merit order, closing-stock rule) it
produces a Plan whose orders cover demand plus the next year's 45-day reserve, using the cheapest
available sources first. The engine (simulate) remains the only source of truth: the builder uses a
dry run of the engine to learn availability and storage modes, then the resulting plan is simulated
again and all constraint checks come from the engine, never from the builder.
"""
from __future__ import annotations

import math
from typing import Any, Optional

from . import rules
from .assumptions import Assumptions, load_assumptions
from .case import Case
from .engine import simulate
from .plan import Investment, OpeningStock, Order, Plan, Reservation
from .scenario import Scenario


def default_merit_order(case: Case) -> list[str]:
    return [k for k, _ in sorted(case.sources.items(), key=lambda kv: (kv[1].variable_cost_mln_per_t, kv[0]))]


def build_plan(case: Case, scenario: Scenario, strategy: dict[str, Any], assumptions: Optional[Assumptions] = None) -> Plan:
    a = assumptions or load_assumptions(None)
    plan_id = strategy["plan_id"]
    investments = [Investment(**inv) for inv in strategy.get("investments", [])]
    caps: dict[str, float] = {k: float(v) for k, v in strategy.get("reservation_caps", {}).items()}
    mode = strategy.get("reservation_mode", "as_ordered")
    merit = strategy.get("merit_order") or default_merit_order(case)
    stress_aware = bool(strategy.get("stress_aware", False))
    emergency_max_share = float(strategy.get("emergency_max_share", 0.15))
    opening_source = strategy.get("opening_stock_source", "B")
    closing_rule = strategy.get("closing_target", "next_year_reserve")
    buffer_days = float(strategy.get("extra_buffer_days", 0.0))
    reserve_days = case.constraints["RESERVE_45D"].value if "RESERVE_45D" in case.constraints else rules.RESERVE_DAYS
    emergency_ids = [k for k, s in case.sources.items() if s.name.lower().startswith("emergency") or k == "E"]

    # demand basis for planning
    def D(y: int) -> float:
        row = case.demand_row(y)
        if stress_aware:
            return row.total(scenario.demand_variant) * scenario.demand_mult(y)
        return row.base_total_t

    def share(sid: str, y: int) -> float:
        return scenario.delivery_share(case.sources[sid], y) if stress_aware else 1.0

    # dry run: investments only -> availability and storage modes
    dry = simulate(case, Plan(plan_id=plan_id + "__dry", investments=investments), scenario, a)
    frac = {(sy.source_id, sy.year): sy.period_fraction for sy in dry.source_years if sy.period == "year"}
    loss_by_year = {y: sum(m.loss_rate for m in dry.months if m.year == y) / 12.0 for y in case.years}
    loss_first = dry.months[0].loss_rate

    years = case.years
    R = {y: rules.reserve_45d(D(y), reserve_days) for y in years}
    buffer = {y: D(y) * buffer_days / 365.0 for y in years}

    def target_close(y: int) -> float:
        if isinstance(closing_rule, (int, float)):
            return float(closing_rule)
        nxt = years[years.index(y) + 1] if y != years[-1] else y
        return R[nxt] + buffer[nxt]

    orders: list[Order] = []
    reservations: list[Reservation] = []
    # opening stock: gross tonnes so that net stock at start = R(y0) + buffer
    y0 = years[0]
    net0 = R[y0] + buffer[y0]
    gross0 = net0 / (1.0 - loss_first)
    s0 = case.sources[opening_source]
    opening = [OpeningStock(opening_source, math.ceil(gross0 * 1e4) / 1e4, y0 - 1, 12)]
    inv_open = net0
    notes = []
    for y in years:
        eff_loss = loss_by_year[y]
        need_net = D(y) + target_close(y) - inv_open
        remaining = max(0.0, need_net / (1.0 - eff_loss))      # gross tonnes to be actually delivered
        delivered_total = 0.0
        for sid in merit:
            s = case.sources[sid]
            f = frac.get((sid, y), 0.0)
            cap = min(caps.get(sid, 0.0), s.capacity_t_per_year) * f
            if sid in emergency_ids:
                cap = min(cap, emergency_max_share * D(y))
            if cap <= 1e-9 or remaining <= 1e-9:
                if mode == "cap" and caps.get(sid, 0.0) > 0 and f > 0:
                    reservations.append(Reservation(sid, y, min(caps[sid], s.capacity_t_per_year)))
                continue
            sh = share(sid, y)
            deliverable = cap * sh
            take = min(deliverable, remaining)
            order_q = take / sh if sh > 0 else 0.0
            order_q = math.ceil(order_q * 1e4) / 1e4
            orders.append(Order(sid, y, order_q))
            reserved = min(caps[sid], s.capacity_t_per_year) if mode == "cap" else math.ceil(order_q / f * 1000) / 1000
            reservations.append(Reservation(sid, y, reserved))
            delivered_total += take
            remaining -= take
        if remaining > 1e-6:
            notes.append(f"{y}: planned gross shortfall {remaining:.2f} t (available reserved capacity exhausted)")
        inv_open = max(0.0, inv_open + delivered_total * (1.0 - eff_loss) - D(y))
    plan = Plan(plan_id=plan_id, scenario_id=scenario.scenario_id, description=strategy.get("description", ""),
                reservations=reservations, orders=orders, investments=investments, opening_stock=opening,
                reserve_mode=strategy.get("reserve_mode", "physical"),
                meta={"builder": "greedy_merit_order", "strategy": {k: v for k, v in strategy.items() if k != "investments"},
                      "stress_aware": stress_aware, "builder_notes": notes, "status": "TEAM_DECISION"})
    return plan

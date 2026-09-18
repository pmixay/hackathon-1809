"""Participant plan (TEAM_DECISION): reservations, orders, investments, inventory policy.

JSON layout is compatible with the organizer's schemas/plan.schema.json envelope:
{
  "plan_id": "...", "scenario_id": "BASE", "description": "...",
  "decisions": {
    "capacity_reservations": [{"source_id": "A", "year": 2035, "reserved_capacity_t": 100}],
    "supply_orders":         [{"source_id": "A", "year": 2035, "ordered_t": 96, "profile": "uniform"}],
    "investments":           [{"investment_id": "ZBO", "decision_year": 2037, "decision_month": 1},
                              {"investment_id": "EARTH_NEW", "option_year": 2035, "option_month": 1,
                               "decision_year": 2035, "decision_month": 6}],
    "inventory_policy":      {"opening_stock": [{"source_id": "B", "tons": 13.0, "delivery_year": 2034, "delivery_month": 12}],
                              "reserve_mode": "physical", "allocation_rule": "critical_first"}
  }
}
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

from .case import Case


class PlanError(ValueError):
    """Raised for structurally invalid plans (missing fields, negative values, unknown ids)."""


@dataclass
class Reservation:
    source_id: str
    year: int
    reserved_capacity_t: float


@dataclass
class Order:
    source_id: str
    year: int
    ordered_t: float
    profile: str = "uniform"                  # uniform over available months, or "monthly"
    monthly_t: Optional[list[float]] = None   # 12 values when profile == "monthly"


@dataclass
class Investment:
    investment_id: str
    decision_year: int                        # exercise / CAPEX payment date
    decision_month: int = 1
    option_year: Optional[int] = None         # option fee date (Earth-New style two-step options)
    option_month: Optional[int] = None


@dataclass
class OpeningStock:
    source_id: str
    tons: float                               # gross delivered tonnes in the preparatory period
    delivery_year: int
    delivery_month: int


@dataclass
class Plan:
    plan_id: str
    scenario_id: str = "BASE"
    description: str = ""
    reservations: list[Reservation] = field(default_factory=list)
    orders: list[Order] = field(default_factory=list)
    investments: list[Investment] = field(default_factory=list)
    opening_stock: list[OpeningStock] = field(default_factory=list)
    reserve_mode: str = "physical"            # physical | emergency_contract
    allocation_rule: str = "critical_first"
    meta: dict = field(default_factory=dict)

    # ---- convenience ----------------------------------------------------
    def reserved(self, source_id: str, year: int) -> float:
        return sum(r.reserved_capacity_t for r in self.reservations if r.source_id == source_id and r.year == year)

    def order(self, source_id: str, year: int) -> Optional[Order]:
        for o in self.orders:
            if o.source_id == source_id and o.year == year:
                return o
        return None

    def to_dict(self) -> dict:
        return {
            "plan_id": self.plan_id, "scenario_id": self.scenario_id, "description": self.description,
            "decisions": {
                "capacity_reservations": [asdict(r) for r in self.reservations],
                "supply_orders": [{k: v for k, v in asdict(o).items() if v is not None} for o in self.orders],
                "investments": [{k: v for k, v in asdict(i).items() if v is not None} for i in self.investments],
                "inventory_policy": {
                    "opening_stock": [asdict(s) for s in self.opening_stock],
                    "reserve_mode": self.reserve_mode, "allocation_rule": self.allocation_rule,
                },
            },
            "meta": self.meta,
        }


def _req(d: dict, key: str, ctx: str):
    if key not in d:
        raise PlanError(f"{ctx}: missing required field '{key}'")
    return d[key]


def _nonneg(v, key: str, ctx: str) -> float:
    try:
        x = float(v)
    except (TypeError, ValueError):
        raise PlanError(f"{ctx}: '{key}' must be a number, got {v!r}")
    if x < 0:
        raise PlanError(f"{ctx}: '{key}' must be >= 0, got {x}")
    return x


def _year(v, key: str, ctx: str) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        raise PlanError(f"{ctx}: '{key}' must be an integer year, got {v!r}")


def _month(v, key: str, ctx: str) -> int:
    m = _year(v, key, ctx)
    if not 1 <= m <= 12:
        raise PlanError(f"{ctx}: '{key}' must be 1..12, got {m}")
    return m


def plan_from_dict(data: dict, source_file: str = "") -> Plan:
    ctx = f"plan {source_file or '<dict>'}"
    if not isinstance(data, dict):
        raise PlanError(f"{ctx}: top level must be a JSON object")
    plan_id = _req(data, "plan_id", ctx)
    if not isinstance(plan_id, str) or not plan_id:
        raise PlanError(f"{ctx}: plan_id must be a non-empty string")
    dec = _req(data, "decisions", ctx)
    if not isinstance(dec, dict):
        raise PlanError(f"{ctx}: 'decisions' must be an object")
    for key in ("supply_orders", "capacity_reservations", "investments", "inventory_policy"):
        if key not in dec:
            raise PlanError(f"{ctx}: decisions.{key} is required (may be empty)")

    reservations = []
    for i, r in enumerate(dec["capacity_reservations"]):
        c = f"{ctx}: capacity_reservations[{i}]"
        reservations.append(Reservation(str(_req(r, "source_id", c)), _year(_req(r, "year", c), "year", c),
                                        _nonneg(_req(r, "reserved_capacity_t", c), "reserved_capacity_t", c)))
    orders = []
    for i, o in enumerate(dec["supply_orders"]):
        c = f"{ctx}: supply_orders[{i}]"
        profile = str(o.get("profile", "uniform"))
        monthly = o.get("monthly_t")
        if profile == "monthly":
            if not isinstance(monthly, list) or len(monthly) != 12:
                raise PlanError(f"{c}: profile 'monthly' requires monthly_t with 12 values")
            monthly = [_nonneg(v, f"monthly_t[{k}]", c) for k, v in enumerate(monthly)]
            ordered = float(sum(monthly))
            if "ordered_t" in o and abs(_nonneg(o["ordered_t"], "ordered_t", c) - ordered) > 1e-6:
                raise PlanError(f"{c}: ordered_t {o['ordered_t']} != sum(monthly_t) {ordered}")
        elif profile == "uniform":
            ordered = _nonneg(_req(o, "ordered_t", c), "ordered_t", c)
            monthly = None
        else:
            raise PlanError(f"{c}: unknown profile {profile!r} (uniform|monthly)")
        orders.append(Order(str(_req(o, "source_id", c)), _year(_req(o, "year", c), "year", c), ordered, profile, monthly))
    investments = []
    for i, inv in enumerate(dec["investments"]):
        c = f"{ctx}: investments[{i}]"
        investments.append(Investment(
            str(_req(inv, "investment_id", c)), _year(_req(inv, "decision_year", c), "decision_year", c),
            _month(inv.get("decision_month", 1), "decision_month", c),
            _year(inv["option_year"], "option_year", c) if inv.get("option_year") is not None else None,
            _month(inv.get("option_month", 1), "option_month", c) if inv.get("option_year") is not None else None,
        ))
    pol = dec["inventory_policy"] or {}
    opening = []
    for i, s in enumerate(pol.get("opening_stock", []) or []):
        c = f"{ctx}: inventory_policy.opening_stock[{i}]"
        opening.append(OpeningStock(str(_req(s, "source_id", c)), _nonneg(_req(s, "tons", c), "tons", c),
                                    _year(_req(s, "delivery_year", c), "delivery_year", c),
                                    _month(_req(s, "delivery_month", c), "delivery_month", c)))
    reserve_mode = str(pol.get("reserve_mode", "physical"))
    if reserve_mode not in ("physical", "emergency_contract"):
        raise PlanError(f"{ctx}: inventory_policy.reserve_mode must be physical|emergency_contract")
    alloc = str(pol.get("allocation_rule", "critical_first"))
    if alloc not in ("critical_first", "proportional"):
        raise PlanError(f"{ctx}: inventory_policy.allocation_rule must be critical_first|proportional")
    return Plan(plan_id=plan_id, scenario_id=str(data.get("scenario_id", "BASE")), description=str(data.get("description", "")),
                reservations=reservations, orders=orders, investments=investments, opening_stock=opening,
                reserve_mode=reserve_mode, allocation_rule=alloc, meta=dict(data.get("meta") or {}))


def validate_plan(plan: Plan, case: Case) -> None:
    """Cross-check plan against the case: known ids, years inside horizon, no duplicate lines."""
    years = set(case.years)
    seen_r, seen_o = set(), set()
    for r in plan.reservations:
        if r.source_id not in case.sources:
            raise PlanError(f"plan {plan.plan_id}: reservation refers to unknown source_id {r.source_id!r} (known: {sorted(case.sources)})")
        if r.year not in years:
            raise PlanError(f"plan {plan.plan_id}: reservation year {r.year} outside horizon {case.first_year}-{case.last_year}")
        if (r.source_id, r.year) in seen_r:
            raise PlanError(f"plan {plan.plan_id}: duplicate reservation for {r.source_id} {r.year}")
        seen_r.add((r.source_id, r.year))
    for o in plan.orders:
        if o.source_id not in case.sources:
            raise PlanError(f"plan {plan.plan_id}: order refers to unknown source_id {o.source_id!r}")
        if o.year not in years:
            raise PlanError(f"plan {plan.plan_id}: order year {o.year} outside horizon {case.first_year}-{case.last_year}")
        if (o.source_id, o.year) in seen_o:
            raise PlanError(f"plan {plan.plan_id}: duplicate order for {o.source_id} {o.year}")
        seen_o.add((o.source_id, o.year))
    seen_i = set()
    for inv in plan.investments:
        if inv.investment_id not in case.investments:
            raise PlanError(f"plan {plan.plan_id}: unknown investment_id {inv.investment_id!r} (known: {sorted(case.investments)})")
        if inv.investment_id in seen_i:
            raise PlanError(f"plan {plan.plan_id}: investment {inv.investment_id} listed twice")
        seen_i.add(inv.investment_id)
        if inv.option_year is not None and (inv.option_year, inv.option_month) > (inv.decision_year, inv.decision_month):
            raise PlanError(f"plan {plan.plan_id}: {inv.investment_id} option fee date is after exercise date")
    for s in plan.opening_stock:
        if s.source_id not in case.sources:
            raise PlanError(f"plan {plan.plan_id}: opening stock refers to unknown source_id {s.source_id!r}")
        if (s.delivery_year, s.delivery_month) >= (case.first_year, 1):
            raise PlanError(f"plan {plan.plan_id}: opening stock must be delivered before {case.first_year}-01 (preparatory period)")


def load_plan(path: str | Path, case: Optional[Case] = None) -> Plan:
    p = Path(path)
    if not p.exists():
        raise PlanError(f"plan file not found: {p}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PlanError(f"plan file {p} is not valid JSON: {exc}") from exc
    plan = plan_from_dict(data, str(p))
    if case is not None:
        validate_plan(plan, case)
    return plan


def save_plan(plan: Plan, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return p

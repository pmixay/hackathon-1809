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
Error messages are in Russian (jury-facing) and always name the file, the field and the offending value.
"""
from __future__ import annotations

import json
import math
from contextlib import contextmanager
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

from .case import Case, InputError

ORDERED_TOL_T = 1e-3   # tonnes: ordered_t may differ from sum(monthly_t) by rounding of a hand-edited 4-decimal profile


class PlanError(InputError):
    """Raised for structurally invalid plans (missing fields, negative values, unknown ids)."""


class _Problems:
    """Collect independent problems so one pass reports every broken line, not just the first.

    Structural failures that make the rest unreadable (not an object, missing `decisions`) still stop
    immediately — there is nothing left to check after them.
    """

    def __init__(self) -> None:
        self.items: list[dict] = []

    @contextmanager
    def at(self, path: str):
        try:
            yield
        except PlanError as exc:
            for d in exc.details:
                self.items.append({"path": d.get("path") or path, "message": d["message"]})

    def add(self, path: str, message: str) -> None:
        self.items.append({"path": path, "message": message})

    def raise_if_any(self, summary: str = "") -> None:
        if self.items:
            raise PlanError.from_problems(self.items, summary)


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
    reactive: bool = False                    # order placed only after the event observed in inventory_policy.observation_month


@dataclass
class Investment:
    investment_id: str
    decision_year: int                        # exercise / CAPEX payment date
    decision_month: int = 1
    option_year: Optional[int] = None         # option fee date (Earth-New style two-step options)
    option_month: Optional[int] = None


@dataclass
class EmergencyContract:
    """Договорный аварийный резерв: объём партии, срок активации и срок исполнения.

    Организатор засчитывает контрактный резерв только при описанном контракте и графике
    (кейс, §«Начальный запас и резерв»). Лимит мощности канала сам по себе эквивалентности
    не доказывает: нужны гарантированный размер партии, срок активации, срок исполнения
    и покрытие спроса физическим запасом до прибытия партии.
    """
    source_id: str
    guaranteed_batch_t: float                 # гарантированная договором аварийная партия, валовые тонны
    activation_days: float                    # от решения об активации до размещения заказа
    delivery_days: float                      # договорный срок исполнения партии, от заказа до прибытия
    max_activations_per_year: int = 1
    notes: str = ""


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
    emergency_contract: Optional[EmergencyContract] = None   # required when reserve_mode == emergency_contract
    allocation_rule: str = "critical_first"
    observation_month: Optional[str] = None   # "YYYY-MM": reactive orders cannot be placed before this month (reaction-time check)
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
                "supply_orders": [{k: v for k, v in asdict(o).items() if v is not None and not (k == "reactive" and not v)} for o in self.orders],
                "investments": [{k: v for k, v in asdict(i).items() if v is not None} for i in self.investments],
                "inventory_policy": {
                    "opening_stock": [asdict(s) for s in self.opening_stock],
                    "reserve_mode": self.reserve_mode, "allocation_rule": self.allocation_rule,
                    **({"emergency_contract": asdict(self.emergency_contract)} if self.emergency_contract else {}),
                    **({"observation_month": self.observation_month} if self.observation_month else {}),
                },
            },
            "meta": self.meta,
        }


def _req(d: dict, key: str, ctx: str):
    if key not in d:
        raise PlanError(f"{ctx}: отсутствует обязательное поле '{key}'")
    return d[key]


def _nonneg(v, key: str, ctx: str) -> float:
    if isinstance(v, bool):
        raise PlanError(f"{ctx}: поле '{key}' должно быть числом, получено {v!r}")
    try:
        x = float(v)
    except (TypeError, ValueError):
        raise PlanError(f"{ctx}: поле '{key}' должно быть числом, получено {v!r}")
    if not math.isfinite(x):                       # NaN проходит проверку "x < 0", поэтому конечность проверяется явно
        raise PlanError(f"{ctx}: поле '{key}' должно быть конечным числом, получено {v!r}")
    if x < 0:
        raise PlanError(f"{ctx}: поле '{key}' должно быть >= 0, получено {x}")
    return x


def _year(v, key: str, ctx: str) -> int:
    try:
        return int(v)
    except (TypeError, ValueError):
        raise PlanError(f"{ctx}: поле '{key}' должно быть целым годом, получено {v!r}")


def _month(v, key: str, ctx: str) -> int:
    m = _year(v, key, ctx)
    if not 1 <= m <= 12:
        raise PlanError(f"{ctx}: поле '{key}' должно быть в диапазоне 1..12, получено {m}")
    return m


def plan_from_dict(data: dict, source_file: str = "") -> Plan:
    ctx = f"план {source_file or '<dict>'}"
    if not isinstance(data, dict):
        raise PlanError(f"{ctx}: верхний уровень должен быть JSON-объектом")
    plan_id = _req(data, "plan_id", ctx)
    if not isinstance(plan_id, str) or not plan_id:
        raise PlanError(f"{ctx}: plan_id должен быть непустой строкой")
    dec = _req(data, "decisions", ctx)
    if not isinstance(dec, dict):
        raise PlanError(f"{ctx}: поле 'decisions' должно быть объектом")
    for key in ("supply_orders", "capacity_reservations", "investments", "inventory_policy"):
        if key not in dec:
            raise PlanError(f"{ctx}: decisions.{key} обязателен (может быть пустым)")

    pr = _Problems()
    reservations = []
    for i, r in enumerate(dec["capacity_reservations"]):
        c = f"{ctx}: capacity_reservations[{i}]"
        with pr.at(c):
            reservations.append(Reservation(str(_req(r, "source_id", c)), _year(_req(r, "year", c), "year", c),
                                            _nonneg(_req(r, "reserved_capacity_t", c), "reserved_capacity_t", c)))
    orders = []
    for i, o in enumerate(dec["supply_orders"]):
        c = f"{ctx}: supply_orders[{i}]"
        with pr.at(c):
            profile = str(o.get("profile", "uniform"))
            monthly = o.get("monthly_t")
            if profile == "monthly":
                if not isinstance(monthly, list) or len(monthly) != 12:
                    raise PlanError(f"{c}: профиль 'monthly' требует monthly_t из 12 значений")
                monthly = [_nonneg(v, f"monthly_t[{k}]", c) for k, v in enumerate(monthly)]
                ordered = float(sum(monthly))      # the monthly profile is the source of truth; ordered_t is a cross-check
                if "ordered_t" in o and abs(_nonneg(o["ordered_t"], "ordered_t", c) - ordered) > ORDERED_TOL_T:
                    raise PlanError(f"{c}: ordered_t {o['ordered_t']} не равен сумме monthly_t {ordered:.6f} (допуск {ORDERED_TOL_T} т)")
            elif profile == "uniform":
                ordered = _nonneg(_req(o, "ordered_t", c), "ordered_t", c)
                monthly = None
            else:
                raise PlanError(f"{c}: неизвестный профиль {profile!r} (допустимо: uniform | monthly)")
            reactive = o.get("reactive", False)
            if not isinstance(reactive, bool):
                raise PlanError(f"{c}: поле 'reactive' должно быть true|false, получено {reactive!r}")
            orders.append(Order(str(_req(o, "source_id", c)), _year(_req(o, "year", c), "year", c), ordered, profile, monthly, reactive))
    investments = []
    for i, inv in enumerate(dec["investments"]):
        c = f"{ctx}: investments[{i}]"
        with pr.at(c):
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
        with pr.at(c):
            opening.append(OpeningStock(str(_req(s, "source_id", c)), _nonneg(_req(s, "tons", c), "tons", c),
                                        _year(_req(s, "delivery_year", c), "delivery_year", c),
                                        _month(_req(s, "delivery_month", c), "delivery_month", c)))
    reserve_mode = str(pol.get("reserve_mode", "physical"))
    if reserve_mode not in ("physical", "emergency_contract"):
        pr.add(f"{ctx}: inventory_policy.reserve_mode",
               f"{ctx}: inventory_policy.reserve_mode должен быть physical | emergency_contract, получено {reserve_mode!r}")
        reserve_mode = "physical"
    contract = None
    raw_contract = pol.get("emergency_contract")
    cc = f"{ctx}: inventory_policy.emergency_contract"
    if raw_contract is not None:
        with pr.at(cc):
            if not isinstance(raw_contract, dict):
                raise PlanError(f"{cc}: ожидается объект с описанием договора аварийной поставки")
            activations = _year(raw_contract.get("max_activations_per_year", 1), "max_activations_per_year", cc)
            if activations < 1:
                raise PlanError(f"{cc}: поле 'max_activations_per_year' должно быть >= 1, получено {activations}")
            contract = EmergencyContract(
                source_id=str(_req(raw_contract, "source_id", cc)),
                guaranteed_batch_t=_nonneg(_req(raw_contract, "guaranteed_batch_t", cc), "guaranteed_batch_t", cc),
                activation_days=_nonneg(_req(raw_contract, "activation_days", cc), "activation_days", cc),
                delivery_days=_nonneg(_req(raw_contract, "delivery_days", cc), "delivery_days", cc),
                max_activations_per_year=activations,
                notes=str(raw_contract.get("notes", "")),
            )
            if contract.guaranteed_batch_t <= 0:
                raise PlanError(f"{cc}: поле 'guaranteed_batch_t' должно быть > 0 — иначе договор не гарантирует объём")
            if contract.delivery_days <= 0:
                raise PlanError(f"{cc}: поле 'delivery_days' должно быть > 0 — иначе договор не задаёт срок исполнения партии")
    if reserve_mode == "emergency_contract" and contract is None:
        pr.add(cc, f"{cc}: режим 'emergency_contract' требует описания договора "
                   f"(source_id, guaranteed_batch_t, activation_days, delivery_days). "
                   f"Без размера партии, срока активации и срока исполнения эквивалентность резерва не доказана — "
                   f"используйте reserve_mode='physical'.")
    alloc = str(pol.get("allocation_rule", "critical_first"))
    if alloc not in ("critical_first", "proportional"):
        pr.add(f"{ctx}: inventory_policy.allocation_rule",
               f"{ctx}: inventory_policy.allocation_rule должен быть critical_first | proportional, получено {alloc!r}")
        alloc = "critical_first"
    obs = pol.get("observation_month")
    if obs is not None:
        obs = str(obs)
        parts = obs.split("-")
        if len(parts) != 2 or not (parts[0].isdigit() and parts[1].isdigit() and 1 <= int(parts[1]) <= 12):
            pr.add(f"{ctx}: inventory_policy.observation_month",
                   f"{ctx}: inventory_policy.observation_month должен иметь вид ГГГГ-ММ, получено {obs!r}")
            obs = None
    if any(o.reactive for o in orders) and obs is None:
        pr.add(f"{ctx}: inventory_policy.observation_month",
               f"{ctx}: заказы с reactive=true требуют inventory_policy.observation_month (месяц наблюдения события)")
    pr.raise_if_any()
    return Plan(plan_id=plan_id, scenario_id=str(data.get("scenario_id", "BASE")), description=str(data.get("description", "")),
                reservations=reservations, orders=orders, investments=investments, opening_stock=opening,
                reserve_mode=reserve_mode, emergency_contract=contract, allocation_rule=alloc, observation_month=obs,
                meta=dict(data.get("meta") or {}))


def validate_plan(plan: Plan, case: Case) -> None:
    """Cross-check plan against the case: known ids, years inside horizon, no duplicate lines.

    Every problem found is reported in one pass (PlanError.details), so an operator fixing a plan by
    hand does not have to rerun the check once per mistake.
    """
    years = set(case.years)
    horizon = f"{case.first_year}–{case.last_year}"
    pr = _Problems()
    ctx = f"план {plan.plan_id}"
    seen_r, seen_o = set(), set()
    for i, r in enumerate(plan.reservations):
        path = f"{ctx}: capacity_reservations[{i}]"
        if r.source_id not in case.sources:
            pr.add(path, f"{ctx}: резервирование ссылается на неизвестный source_id {r.source_id!r} (известные: {sorted(case.sources)})")
        if r.year not in years:
            pr.add(path, f"{ctx}: год резервирования {r.year} вне горизонта {horizon}")
        if (r.source_id, r.year) in seen_r:
            pr.add(path, f"{ctx}: повторное резервирование для {r.source_id} {r.year}")
        seen_r.add((r.source_id, r.year))
    for i, o in enumerate(plan.orders):
        path = f"{ctx}: supply_orders[{i}]"
        if o.source_id not in case.sources:
            pr.add(path, f"{ctx}: заказ ссылается на неизвестный source_id {o.source_id!r} (известные: {sorted(case.sources)})")
        if o.year not in years:
            pr.add(path, f"{ctx}: год заказа {o.year} вне горизонта {horizon}")
        if (o.source_id, o.year) in seen_o:
            pr.add(path, f"{ctx}: повторный заказ для {o.source_id} {o.year}")
        seen_o.add((o.source_id, o.year))
    seen_i = set()
    for i, inv in enumerate(plan.investments):
        path = f"{ctx}: investments[{i}]"
        if inv.investment_id not in case.investments:
            pr.add(path, f"{ctx}: неизвестный investment_id {inv.investment_id!r} (известные: {sorted(case.investments)})")
        if inv.investment_id in seen_i:
            pr.add(path, f"{ctx}: инвестиция {inv.investment_id} указана дважды")
        seen_i.add(inv.investment_id)
        if inv.option_year is not None and (inv.option_year, inv.option_month) > (inv.decision_year, inv.decision_month):
            pr.add(path, f"{ctx}: {inv.investment_id}: дата платы за опцион позже даты реализации")
    if plan.emergency_contract is not None:
        path = f"{ctx}: inventory_policy.emergency_contract"
        ec = plan.emergency_contract
        if ec.source_id not in case.sources:
            pr.add(path, f"{ctx}: договор аварийной поставки ссылается на неизвестный source_id {ec.source_id!r} "
                         f"(известные: {sorted(case.sources)})")
        elif ec.guaranteed_batch_t > case.sources[ec.source_id].capacity_t_per_year + 1e-9:
            pr.add(path, f"{ctx}: гарантированная партия {ec.guaranteed_batch_t:g} т превышает годовую мощность канала "
                         f"{case.sources[ec.source_id].name} ({case.sources[ec.source_id].capacity_t_per_year:g} т/год)")
    for i, s_ in enumerate(plan.opening_stock):
        path = f"{ctx}: inventory_policy.opening_stock[{i}]"
        if s_.source_id not in case.sources:
            pr.add(path, f"{ctx}: начальный запас ссылается на неизвестный source_id {s_.source_id!r}")
        if (s_.delivery_year, s_.delivery_month) >= (case.first_year, 1):
            pr.add(path, f"{ctx}: начальный запас должен быть поставлен до {case.first_year}-01 (подготовительный период)")
    pr.raise_if_any()


def load_plan(path: str | Path, case: Optional[Case] = None) -> Plan:
    p = Path(path)
    if not p.exists():
        raise PlanError(f"файл плана не найден: {p}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PlanError(f"файл плана {p} не является корректным JSON: {exc}") from exc
    plan = plan_from_dict(data, str(p))
    if case is not None:
        validate_plan(plan, case)
    return plan


def save_plan(plan: Plan, path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
    return p

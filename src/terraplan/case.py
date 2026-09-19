"""CASE_INPUT loader: demand, supply sources, storage options, investment options, constraints.

Data lives in CSV files with the organizer's column names (data/case/*.csv). Adding a source row,
a demand year or a constraint row extends the model without code changes (see tests/test_extensibility.py).
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


class CaseError(ValueError):
    """Raised when CASE_INPUT files are missing, malformed or internally inconsistent."""


def _num(row: dict, key: str, path: str, allow_blank: bool = False) -> Optional[float]:
    raw = (row.get(key) or "").strip()
    if raw == "":
        if allow_blank:
            return None
        raise CaseError(f"{path}: отсутствует числовое поле '{key}' в строке {row}")
    try:
        return float(raw.replace(",", "."))
    except ValueError as exc:
        raise CaseError(f"{path}: поле '{key}' не является числом: {raw!r}") from exc


@dataclass(frozen=True)
class DemandRow:
    year: int
    base_total_t: float
    base_critical_t: float
    low_total_t: float
    high_total_t: float
    status: str = "CASE_INPUT"

    @property
    def critical_share(self) -> float:
        return self.base_critical_t / self.base_total_t if self.base_total_t > 0 else 0.0

    def total(self, variant: str = "base") -> float:
        return {"base": self.base_total_t, "low": self.low_total_t, "high": self.high_total_t}[variant]

    def critical(self, variant: str = "base") -> float:
        """Critical demand keeps the base-year critical share in low/high variants (case rule)."""
        return self.total(variant) * self.critical_share


@dataclass(frozen=True)
class Source:
    source_id: str
    name: str
    capacity_t_per_year: float
    variable_cost_mln_per_t: float
    reservation_rate_mln_per_t_year: float
    take_or_pay_share: float
    lead_time_min_value: float
    lead_time_max_value: float
    lead_time_unit: str
    reliability_profile: str
    available_from_year: Optional[int]
    status: str = "CASE_INPUT"
    notes: str = ""


@dataclass(frozen=True)
class StorageOption:
    storage_id: str
    name: str
    capacity_t: float
    loss_rate_on_throughput: float
    holding_cost_mln_per_t_year: float
    capex_mln: float
    fixed_opex_mln_per_year: float
    available_from_year: int
    status: str = "CASE_INPUT"
    notes: str = ""


@dataclass(frozen=True)
class InvestmentOption:
    investment_id: str
    name: str
    option_fee_mln: float
    exercise_cost_mln: float
    total_capex_mln: float
    commissioning_rule: str
    fixed_opex_mln_per_year: float
    status: str = "CASE_INPUT"
    notes: str = ""


@dataclass(frozen=True)
class Constraint:
    constraint_id: str
    metric: str
    operator: str
    value: float
    unit: str
    period: str
    scenario: str
    severity: str
    status: str = "CASE_INPUT"
    description: str = ""


@dataclass
class Case:
    demand: list[DemandRow]
    sources: dict[str, Source]
    storage: dict[str, StorageOption]
    investments: dict[str, InvestmentOption]
    constraints: dict[str, Constraint]
    source_dir: str = ""
    files: dict[str, str] = field(default_factory=dict)

    @property
    def years(self) -> list[int]:
        return [d.year for d in self.demand]

    @property
    def first_year(self) -> int:
        return self.demand[0].year

    @property
    def last_year(self) -> int:
        return self.demand[-1].year

    def demand_row(self, year: int) -> DemandRow:
        for d in self.demand:
            if d.year == year:
                return d
        raise CaseError(f"нет строки спроса для {year} г.")

    def source_by_name_or_id(self, key: str) -> Optional[Source]:
        if key in self.sources:
            return self.sources[key]
        for s in self.sources.values():
            if s.name == key:
                return s
        return None


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise CaseError(f"отсутствует файл CASE_INPUT: {path}")
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise CaseError(f"{path}: пустой CSV")
    return rows


def load_case(case_dir: str | Path) -> Case:
    """Load the CASE_INPUT set from a directory with the organizer CSV layout."""
    d = Path(case_dir)
    p_dem, p_src, p_sto, p_inv, p_con = (d / n for n in
        ("demand.csv", "supply_sources.csv", "storage_options.csv", "investment_options.csv", "constraints.csv"))

    demand: list[DemandRow] = []
    for r in _read_csv(p_dem):
        row = DemandRow(
            year=int(_num(r, "year", str(p_dem))),
            base_total_t=_num(r, "base_total_t", str(p_dem)),
            base_critical_t=_num(r, "base_critical_t", str(p_dem)),
            low_total_t=_num(r, "low_total_t", str(p_dem)),
            high_total_t=_num(r, "high_total_t", str(p_dem)),
            status=r.get("status", "CASE_INPUT"),
        )
        if row.base_critical_t > row.base_total_t:
            raise CaseError(f"{p_dem}: критический спрос превышает общий спрос в {row.year} г.")
        if min(row.base_total_t, row.low_total_t, row.high_total_t) < 0:
            raise CaseError(f"{p_dem}: отрицательный спрос в {row.year} г.")
        demand.append(row)
    demand.sort(key=lambda x: x.year)
    years = [x.year for x in demand]
    if years != list(range(years[0], years[0] + len(years))):
        raise CaseError(f"{p_dem}: годы должны идти подряд, получено {years}")

    sources: dict[str, Source] = {}
    for r in _read_csv(p_src):
        sid = (r.get("source_id") or "").strip()
        if not sid:
            raise CaseError(f"{p_src}: пустой source_id в строке {r}")
        if sid in sources:
            raise CaseError(f"{p_src}: повторяющийся source_id {sid}")
        unit = (r.get("lead_time_unit") or "month").strip()
        if unit not in ("day", "week", "month", "year"):
            raise CaseError(f"{p_src}: неизвестная единица lead_time_unit {unit!r} для {sid} (допустимо day|week|month|year)")
        afy = _num(r, "available_from_year", str(p_src), allow_blank=True)
        s = Source(
            source_id=sid,
            name=(r.get("name") or sid).strip(),
            capacity_t_per_year=_num(r, "capacity_t_per_year", str(p_src)),
            variable_cost_mln_per_t=_num(r, "variable_cost_mln_per_t", str(p_src)),
            reservation_rate_mln_per_t_year=_num(r, "reservation_rate_mln_per_t_year_capacity", str(p_src)),
            take_or_pay_share=_num(r, "take_or_pay_share", str(p_src)),
            lead_time_min_value=_num(r, "lead_time_min_value", str(p_src)),
            lead_time_max_value=_num(r, "lead_time_max_value", str(p_src)),
            lead_time_unit=unit,
            reliability_profile=(r.get("reliability_profile") or "").strip(),
            available_from_year=int(afy) if afy is not None else None,
            status=r.get("status", "CASE_INPUT"),
            notes=r.get("notes", ""),
        )
        if s.capacity_t_per_year < 0 or s.variable_cost_mln_per_t < 0 or s.reservation_rate_mln_per_t_year < 0:
            raise CaseError(f"{p_src}: отрицательный параметр у источника {sid}")
        if not 0 <= s.take_or_pay_share <= 1:
            raise CaseError(f"{p_src}: take_or_pay_share вне диапазона [0,1] для {sid}")
        if s.lead_time_max_value < s.lead_time_min_value:
            raise CaseError(f"{p_src}: lead_time_max < lead_time_min для {sid}")
        sources[sid] = s

    storage: dict[str, StorageOption] = {}
    for r in _read_csv(p_sto):
        so = StorageOption(
            storage_id=r["storage_id"].strip(), name=r.get("name", "").strip(),
            capacity_t=_num(r, "capacity_t", str(p_sto)),
            loss_rate_on_throughput=_num(r, "loss_rate_on_throughput", str(p_sto)),
            holding_cost_mln_per_t_year=_num(r, "holding_cost_mln_per_t_year", str(p_sto)),
            capex_mln=_num(r, "capex_mln", str(p_sto)),
            fixed_opex_mln_per_year=_num(r, "fixed_opex_mln_per_year", str(p_sto)),
            available_from_year=int(_num(r, "available_from_year", str(p_sto))),
            status=r.get("status", "CASE_INPUT"), notes=r.get("notes", ""),
        )
        if not 0 <= so.loss_rate_on_throughput < 1:
            raise CaseError(f"{p_sto}: доля потерь вне диапазона [0,1) для {so.storage_id}")
        storage[so.storage_id] = so
    if "BASE" not in storage:
        raise CaseError(f"{p_sto}: требуется строка хранилища со storage_id=BASE (существующее хранилище)")

    investments: dict[str, InvestmentOption] = {}
    for r in _read_csv(p_inv):
        io = InvestmentOption(
            investment_id=r["investment_id"].strip(), name=r.get("name", "").strip(),
            option_fee_mln=_num(r, "option_fee_mln", str(p_inv)),
            exercise_cost_mln=_num(r, "exercise_cost_mln", str(p_inv)),
            total_capex_mln=_num(r, "total_capex_mln", str(p_inv)),
            commissioning_rule=r.get("commissioning_rule", ""),
            fixed_opex_mln_per_year=_num(r, "fixed_opex_mln_per_year", str(p_inv)),
            status=r.get("status", "CASE_INPUT"), notes=r.get("notes", ""),
        )
        if abs(io.option_fee_mln + io.exercise_cost_mln - io.total_capex_mln) > 1e-9:
            raise CaseError(f"{p_inv}: option_fee + exercise_cost != total_capex для {io.investment_id}")
        investments[io.investment_id] = io

    constraints: dict[str, Constraint] = {}
    for r in _read_csv(p_con):
        c = Constraint(
            constraint_id=r["constraint_id"].strip(), metric=r["metric"].strip(), operator=r["operator"].strip(),
            value=_num(r, "value", str(p_con)), unit=r.get("unit", ""), period=r.get("period", "").strip(),
            scenario=r.get("scenario", "ALL").strip(), severity=r.get("severity", "hard").strip(),
            status=r.get("status", "CASE_INPUT"), description=r.get("description", ""),
        )
        if c.operator not in (">=", "<="):
            raise CaseError(f"{p_con}: неподдерживаемый оператор {c.operator!r} в {c.constraint_id} (допустимо >= или <=)")
        constraints[c.constraint_id] = c

    return Case(demand=demand, sources=sources, storage=storage, investments=investments,
                constraints=constraints, source_dir=str(d),
                files={p.name: str(p) for p in (p_dem, p_src, p_sto, p_inv, p_con)})

"""CASE_INPUT loader: demand, supply sources, storage options, investment options, constraints.

Data lives in CSV files with the organizer's column names (data/case/*.csv). Adding a source row,
a demand year or a constraint row extends the model without code changes (see tests/test_extensibility.py).
"""
from __future__ import annotations

import csv
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


class InputError(ValueError):
    """Base class for input errors that can report every problem found, not only the first.

    `details` is a list of {"path", "message"}: the operator sees the whole list of things to fix in
    one pass instead of rerunning the check after each correction. `str(error)` stays the first
    message, so existing callers and log lines are unchanged.
    """

    def __init__(self, message: str, details: Optional[list[dict]] = None):
        super().__init__(message)
        self.details: list[dict] = list(details) if details else [{"path": "", "message": str(message)}]

    @classmethod
    def from_problems(cls, problems: list[dict], summary: str = ""):
        """Build one error from several collected problems; the message names how many there are."""
        head = problems[0]["message"]
        if len(problems) > 1:
            head = f"{head} (и ещё {len(problems) - 1}: " + "; ".join(p["message"] for p in problems[1:]) + ")"
        return cls(f"{summary}{head}" if summary else head, problems)


class CaseError(InputError):
    """Raised when CASE_INPUT files are missing, malformed or internally inconsistent."""


class _Checks:
    """Collect every input problem in one pass so the operator sees the whole list, not only the first.

    A problem is recorded against `<таблица>[<строка>].<поле>` and the value is replaced by a neutral
    substitute, so loading continues and the remaining fields are checked too. Nothing is returned to
    the caller while `items` is non-empty: `raise_if_any()` turns the collected list into one CaseError.
    """

    def __init__(self, path: str) -> None:
        self.path = path              # file name shown to the operator
        self.items: list[dict] = []

    def add(self, field: str, message: str, where: str = "") -> None:
        self.items.append({"path": f"{self.path}{where}.{field}" if field else f"{self.path}{where}",
                           "message": f"{self.path}{where}: {message}"})

    def num(self, row: dict, key: str, where: str = "", *, allow_blank: bool = False,
            minimum: Optional[float] = None, maximum: Optional[float] = None,
            unit: str = "", substitute: float = 0.0) -> Optional[float]:
        """Read one numeric field: present, a real number, finite, and inside the physical range."""
        raw = (row.get(key) or "").strip()
        bounds = f" ({unit})" if unit else ""
        if raw == "":
            if allow_blank:
                return None
            self.add(key, f"отсутствует обязательное числовое поле '{key}'{bounds}", where)
            return substitute
        try:
            value = float(raw.replace(",", "."))
        except ValueError:
            self.add(key, f"поле '{key}'{bounds} не является числом: {raw!r}", where)
            return substitute
        if not math.isfinite(value):
            self.add(key, f"поле '{key}'{bounds} должно быть конечным числом, получено {raw!r}", where)
            return substitute
        if minimum is not None and value < minimum:
            self.add(key, f"поле '{key}'{bounds} должно быть >= {minimum:g}, получено {value:g}", where)
            return substitute
        if maximum is not None and value > maximum:
            self.add(key, f"поле '{key}'{bounds} должно быть <= {maximum:g}, получено {value:g}", where)
            return substitute
        return value

    def integer(self, row: dict, key: str, where: str = "", *, allow_blank: bool = False,
                minimum: Optional[float] = None, maximum: Optional[float] = None, substitute: int = 0):
        value = self.num(row, key, where, allow_blank=allow_blank, minimum=minimum, maximum=maximum,
                         substitute=float(substitute))
        if value is None:
            return None
        if abs(value - round(value)) > 1e-9:
            self.add(key, f"поле '{key}' должно быть целым числом, получено {value:g}", where)
            return substitute
        return int(round(value))

    def text(self, row: dict, key: str, where: str = "", *, allowed: Optional[tuple] = None,
             default: str = "", required: bool = False) -> str:
        value = (row.get(key) or "").strip() or default
        if required and not value:
            self.add(key, f"поле '{key}' не может быть пустым", where)
        if allowed is not None and value and value not in allowed:
            self.add(key, f"поле '{key}' должно быть одним из {'|'.join(allowed)}, получено {value!r}", where)
        return value

    def failed(self, *fields: str, where: str = "") -> bool:
        """True when one of these fields of this row already has a problem (skip dependent cross-checks)."""
        keys = {f"{self.path}{where}.{f}" for f in fields}
        return any(item["path"] in keys for item in self.items)

    def raise_if_any(self) -> None:
        if self.items:
            raise CaseError.from_problems(self.items)


def _num(row: dict, key: str, path: str, allow_blank: bool = False) -> Optional[float]:
    """Single-field reader kept for callers outside load_case; raises on the first problem."""
    checks = _Checks(path)
    value = checks.num(row, key, allow_blank=allow_blank)
    checks.raise_if_any()
    return value


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


def validate_case(case: Case) -> None:
    """Re-check the loaded CASE_INPUT invariants at the engine boundary.

    `load_case` already rejects a bad CSV. This guard covers the other entry point — a `Case` built
    in code or deserialised — so no path into the engine can carry a negative or non-finite demand,
    lead time, capacity, cost or rate. The engine skips zero-cost events, so a negative CAPEX that
    slipped through would silently *reduce* the plan cost instead of failing loudly.
    """
    bad: list[dict] = []

    def need(ok: bool, path: str, message: str) -> None:
        if not ok:
            bad.append({"path": path, "message": message})

    def finite_nonneg(value, path: str, what: str) -> bool:
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
            need(False, path, f"{what} должен быть конечным числом, получено {value!r}")
            return False
        if float(value) < 0:
            need(False, path, f"{what} должен быть >= 0, получено {float(value):g}")
            return False
        return True

    for row in case.demand:
        at = f"demand.csv[{row.year}]"
        for key, what in (("base_total_t", "общий спрос"), ("base_critical_t", "критический спрос"),
                          ("low_total_t", "низкий вариант спроса"), ("high_total_t", "высокий вариант спроса")):
            finite_nonneg(getattr(row, key), f"{at}.{key}", what)
        need(row.base_critical_t <= row.base_total_t, f"{at}.base_critical_t",
             f"критический спрос {row.base_critical_t:g} т превышает общий {row.base_total_t:g} т")

    for sid, s_ in case.sources.items():
        at = f"supply_sources.csv[{sid}]"
        for key, what in (("capacity_t_per_year", "мощность"), ("variable_cost_mln_per_t", "переменная цена"),
                          ("reservation_rate_mln_per_t_year", "ставка резервирования"),
                          ("lead_time_min_value", "минимальный срок поставки"),
                          ("lead_time_max_value", "максимальный срок поставки")):
            finite_nonneg(getattr(s_, key), f"{at}.{key}", what)
        need(0.0 <= s_.take_or_pay_share <= 1.0, f"{at}.take_or_pay_share",
             f"доля take-or-pay должна быть в [0,1], получено {s_.take_or_pay_share!r}")
        need(s_.lead_time_unit in ("day", "week", "month", "year"), f"{at}.lead_time_unit",
             f"неизвестная единица срока поставки {s_.lead_time_unit!r}")
        need(s_.lead_time_max_value >= s_.lead_time_min_value, f"{at}.lead_time_max_value",
             "максимальный срок поставки меньше минимального")

    for stid, so in case.storage.items():
        at = f"storage_options.csv[{stid}]"
        for key, what in (("capacity_t", "ёмкость"), ("holding_cost_mln_per_t_year", "стоимость хранения"),
                          ("capex_mln", "CAPEX"), ("fixed_opex_mln_per_year", "постоянный OPEX")):
            finite_nonneg(getattr(so, key), f"{at}.{key}", what)
        need(0.0 <= so.loss_rate_on_throughput < 1.0, f"{at}.loss_rate_on_throughput",
             f"доля потерь должна быть в [0,1), получено {so.loss_rate_on_throughput!r}")

    for iid, io in case.investments.items():
        at = f"investment_options.csv[{iid}]"
        for key, what in (("option_fee_mln", "плата за опцион"), ("exercise_cost_mln", "стоимость реализации"),
                          ("total_capex_mln", "суммарный CAPEX"), ("fixed_opex_mln_per_year", "постоянный OPEX")):
            finite_nonneg(getattr(io, key), f"{at}.{key}", what)
        need(abs(io.option_fee_mln + io.exercise_cost_mln - io.total_capex_mln) <= 1e-9, f"{at}.total_capex_mln",
             "option_fee_mln + exercise_cost_mln != total_capex_mln")

    for cid, c in case.constraints.items():
        at = f"constraints.csv[{cid}]"
        finite_nonneg(c.value, f"{at}.value", "значение ограничения")
        need(c.operator in (">=", "<="), f"{at}.operator", f"неподдерживаемый оператор {c.operator!r}")
        if c.unit == "share":
            need(0.0 <= c.value <= 1.0, f"{at}.value", f"доля должна быть в [0,1], получено {c.value!r}")

    if bad:
        raise CaseError.from_problems(bad, "CASE_INPUT не прошёл проверку перед расчётом: ")


def _read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise CaseError(f"отсутствует файл CASE_INPUT: {path}")
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise CaseError(f"{path}: пустой CSV")
    return rows


def load_case(case_dir: str | Path) -> Case:
    """Load the CASE_INPUT set from a directory with the organizer CSV layout.

    Every numeric field is checked for presence, being a real finite number and lying inside its
    physical range (no negative demand, lead time, capacity, cost or rate), and duplicated parameters
    are checked for consistency. All problems of a table are reported together, each naming the file,
    the row and the field, so a wrong input can never be silently simulated as a feasible plan.
    """
    d = Path(case_dir)
    p_dem, p_src, p_sto, p_inv, p_con = (d / n for n in
        ("demand.csv", "supply_sources.csv", "storage_options.csv", "investment_options.csv", "constraints.csv"))

    # ---- demand ---------------------------------------------------------------
    ck = _Checks(str(p_dem))
    demand: list[DemandRow] = []
    for n, r in enumerate(_read_csv(p_dem), start=2):
        at = f" строка {n}"
        year = ck.integer(r, "year", at, minimum=1900, maximum=9999, substitute=1900)
        row = DemandRow(
            year=year,
            base_total_t=ck.num(r, "base_total_t", at, minimum=0.0, unit="т/год"),
            base_critical_t=ck.num(r, "base_critical_t", at, minimum=0.0, unit="т/год"),
            low_total_t=ck.num(r, "low_total_t", at, minimum=0.0, unit="т/год"),
            high_total_t=ck.num(r, "high_total_t", at, minimum=0.0, unit="т/год"),
            status=r.get("status", "CASE_INPUT"),
        )
        if not ck.failed("base_total_t", "base_critical_t", where=at) and row.base_critical_t > row.base_total_t:
            ck.add("base_critical_t", f"критический спрос {row.base_critical_t:g} т превышает общий спрос "
                                      f"{row.base_total_t:g} т в {row.year} г.", at)
        if not ck.failed("base_total_t", "low_total_t", "high_total_t", where=at) and not (
                row.low_total_t <= row.base_total_t <= row.high_total_t):
            ck.add("low_total_t", f"варианты спроса {row.year} г. несогласованны: требуется "
                                  f"low_total_t ({row.low_total_t:g}) <= base_total_t ({row.base_total_t:g}) "
                                  f"<= high_total_t ({row.high_total_t:g})", at)
        demand.append(row)
    ck.raise_if_any()
    demand.sort(key=lambda x: x.year)
    years = [x.year for x in demand]
    if len(set(years)) != len(years):
        dup = sorted({y for y in years if years.count(y) > 1})
        raise CaseError(f"{p_dem}: повторяющиеся годы спроса {dup}")
    if years != list(range(years[0], years[0] + len(years))):
        raise CaseError(f"{p_dem}: годы должны идти подряд, получено {years}")
    horizon = range(years[0], years[-1] + 1)

    # ---- supply sources -------------------------------------------------------
    ck = _Checks(str(p_src))
    sources: dict[str, Source] = {}
    for n, r in enumerate(_read_csv(p_src), start=2):
        at = f" строка {n}"
        sid = ck.text(r, "source_id", at, required=True)
        if sid and sid in sources:
            ck.add("source_id", f"повторяющийся source_id {sid!r}", at)
        unit = ck.text(r, "lead_time_unit", at, allowed=("day", "week", "month", "year"), default="month")
        afy = ck.integer(r, "available_from_year", at, allow_blank=True, minimum=1900, maximum=9999)
        s = Source(
            source_id=sid or f"<строка {n}>",
            name=ck.text(r, "name", at, default=sid),
            capacity_t_per_year=ck.num(r, "capacity_t_per_year", at, minimum=0.0, unit="т/год"),
            variable_cost_mln_per_t=ck.num(r, "variable_cost_mln_per_t", at, minimum=0.0, unit="млн у.е./т"),
            reservation_rate_mln_per_t_year=ck.num(r, "reservation_rate_mln_per_t_year_capacity", at, minimum=0.0,
                                                   unit="млн у.е. за т/год"),
            take_or_pay_share=ck.num(r, "take_or_pay_share", at, minimum=0.0, maximum=1.0, unit="доля 0..1"),
            lead_time_min_value=ck.num(r, "lead_time_min_value", at, minimum=0.0, unit=f"{unit or 'месяц'}, >= 0"),
            lead_time_max_value=ck.num(r, "lead_time_max_value", at, minimum=0.0, unit=f"{unit or 'месяц'}, >= 0"),
            lead_time_unit=unit or "month",
            reliability_profile=(r.get("reliability_profile") or "").strip(),
            available_from_year=afy,
            status=r.get("status", "CASE_INPUT"),
            notes=r.get("notes", ""),
        )
        if not ck.failed("lead_time_min_value", "lead_time_max_value", where=at) and s.lead_time_max_value < s.lead_time_min_value:
            ck.add("lead_time_max_value", f"lead_time_max_value ({s.lead_time_max_value:g}) < lead_time_min_value "
                                          f"({s.lead_time_min_value:g}) для {sid}", at)
        if afy is not None and afy not in horizon and afy < years[0]:
            ck.add("available_from_year", f"год начала доступности {afy} раньше горизонта {years[0]}–{years[-1]} для {sid}", at)
        if sid:
            sources[sid] = s
    ck.raise_if_any()
    if not sources:
        raise CaseError(f"{p_src}: нужен хотя бы один канал поставки")

    # ---- storage --------------------------------------------------------------
    ck = _Checks(str(p_sto))
    storage: dict[str, StorageOption] = {}
    for n, r in enumerate(_read_csv(p_sto), start=2):
        at = f" строка {n}"
        stid = ck.text(r, "storage_id", at, required=True)
        if stid and stid in storage:
            ck.add("storage_id", f"повторяющийся storage_id {stid!r}", at)
        so = StorageOption(
            storage_id=stid or f"<строка {n}>", name=ck.text(r, "name", at, default=stid),
            capacity_t=ck.num(r, "capacity_t", at, minimum=0.0, unit="т"),
            loss_rate_on_throughput=ck.num(r, "loss_rate_on_throughput", at, minimum=0.0, maximum=0.999999, unit="доля 0..1"),
            holding_cost_mln_per_t_year=ck.num(r, "holding_cost_mln_per_t_year", at, minimum=0.0, unit="млн у.е. за т-год"),
            capex_mln=ck.num(r, "capex_mln", at, minimum=0.0, unit="млн у.е."),
            fixed_opex_mln_per_year=ck.num(r, "fixed_opex_mln_per_year", at, minimum=0.0, unit="млн у.е./год"),
            available_from_year=ck.integer(r, "available_from_year", at, minimum=1900, maximum=9999, substitute=years[0]),
            status=r.get("status", "CASE_INPUT"), notes=r.get("notes", ""),
        )
        if stid:
            storage[stid] = so
    ck.raise_if_any()
    if "BASE" not in storage:
        raise CaseError(f"{p_sto}: требуется строка хранилища со storage_id=BASE (существующее хранилище)")
    if storage["BASE"].capacity_t <= 0:
        raise CaseError(f"{p_sto}: ёмкость базового хранилища (BASE.capacity_t) должна быть > 0")

    # ---- investments ----------------------------------------------------------
    ck = _Checks(str(p_inv))
    investments: dict[str, InvestmentOption] = {}
    for n, r in enumerate(_read_csv(p_inv), start=2):
        at = f" строка {n}"
        iid = ck.text(r, "investment_id", at, required=True)
        if iid and iid in investments:
            ck.add("investment_id", f"повторяющийся investment_id {iid!r}", at)
        io = InvestmentOption(
            investment_id=iid or f"<строка {n}>", name=ck.text(r, "name", at, default=iid),
            option_fee_mln=ck.num(r, "option_fee_mln", at, minimum=0.0, unit="млн у.е."),
            exercise_cost_mln=ck.num(r, "exercise_cost_mln", at, minimum=0.0, unit="млн у.е."),
            total_capex_mln=ck.num(r, "total_capex_mln", at, minimum=0.0, unit="млн у.е."),
            commissioning_rule=r.get("commissioning_rule", ""),
            fixed_opex_mln_per_year=ck.num(r, "fixed_opex_mln_per_year", at, minimum=0.0, unit="млн у.е./год"),
            status=r.get("status", "CASE_INPUT"), notes=r.get("notes", ""),
        )
        if not ck.failed("option_fee_mln", "exercise_cost_mln", "total_capex_mln", where=at) and \
                abs(io.option_fee_mln + io.exercise_cost_mln - io.total_capex_mln) > 1e-9:
            ck.add("total_capex_mln", f"option_fee_mln ({io.option_fee_mln:g}) + exercise_cost_mln "
                                      f"({io.exercise_cost_mln:g}) != total_capex_mln ({io.total_capex_mln:g}) "
                                      f"для {iid}", at)
        if iid:
            investments[iid] = io
    ck.raise_if_any()

    # ---- constraints ----------------------------------------------------------
    ck = _Checks(str(p_con))
    constraints: dict[str, Constraint] = {}
    for n, r in enumerate(_read_csv(p_con), start=2):
        at = f" строка {n}"
        cid = ck.text(r, "constraint_id", at, required=True)
        if cid and cid in constraints:
            ck.add("constraint_id", f"повторяющийся constraint_id {cid!r}", at)
        unit = ck.text(r, "unit", at)
        limits = {"share": (0.0, 1.0), "days": (0.0, None), "years": (0.0, None),
                  "mln_units": (0.0, None)}.get(unit, (None, None))
        c = Constraint(
            constraint_id=cid or f"<строка {n}>",
            metric=ck.text(r, "metric", at, required=True),
            operator=ck.text(r, "operator", at, allowed=(">=", "<="), required=True),
            value=ck.num(r, "value", at, minimum=limits[0], maximum=limits[1], unit=unit),
            unit=unit, period=ck.text(r, "period", at),
            scenario=ck.text(r, "scenario", at, default="ALL", required=True),
            severity=ck.text(r, "severity", at, allowed=("hard", "guideline", "warning"), default="hard"),
            status=r.get("status", "CASE_INPUT"), description=r.get("description", ""),
        )
        if c.period.startswith("through_") and not c.period.split("_")[-1].isdigit():
            ck.add("period", f"период {c.period!r} должен иметь вид through_ГГГГ", at)
        if cid:
            constraints[cid] = c
    ck.raise_if_any()

    return Case(demand=demand, sources=sources, storage=storage, investments=investments,
                constraints=constraints, source_dir=str(d),
                files={p.name: str(p) for p in (p_dem, p_src, p_sto, p_inv, p_con)})

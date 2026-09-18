"""TerraPlan calculation engine: monthly simulation of the depot supply plan.

Pipeline (organizer "core contract" §24):  load_case -> validate_plan -> apply_scenario ->
calculate_deliveries -> calculate_inventory -> calculate_service -> calculate_costs -> check_constraints.

Time step: calendar month. Absolute month index = year*12 + (month-1). Demand is uniform within a year
(organizer convention). All money in mln units, constant 2035 prices. Deterministic: no randomness.
"""
from __future__ import annotations

import math
from math import fsum
from dataclasses import dataclass, field, asdict
from typing import Optional

from . import rules
from .assumptions import Assumptions, load_assumptions
from .case import Case, Source
from .plan import Plan, validate_plan
from .scenario import Scenario

EPS = 1e-9
TOL_T = 1e-6   # tonnes tolerance for physical checks (rounding of plan files to 4 decimals)


# --------------------------------------------------------------------------- records
@dataclass
class Violation:
    rule_id: str
    severity: str                 # hard | guideline | warning
    scenario_id: str
    message: str
    year: Optional[int] = None
    month: Optional[int] = None
    source_id: Optional[str] = None
    actual: Optional[float] = None
    limit: Optional[float] = None
    excess: Optional[float] = None


@dataclass
class MonthRecord:
    year: int
    month: int
    storage_mode: str
    storage_capacity_t: float
    loss_rate: float
    opening_t: float
    planned_inflow_t: float
    throughput_t: float
    losses_t: float
    available_t: float
    demand_t: float
    critical_demand_t: float
    served_t: float
    served_critical_t: float
    shortage_t: float
    shortage_critical_t: float
    closing_t: float
    holding_cost_mln: float
    inflow_by_source: dict = field(default_factory=dict)


@dataclass
class YearRecord:
    year: int
    demand_total_t: float
    demand_critical_t: float
    served_total_t: float
    served_critical_t: float
    service_level_total: float
    service_level_critical: float
    shortage_total_t: float
    shortage_critical_t: float
    opening_t: float
    closing_t: float
    planned_inflow_t: float
    throughput_t: float
    losses_t: float
    loss_ratio: float
    reserve_required_t: float
    reserve_ok: bool
    average_stock_t: float
    storage_mode_end: str
    storage_capacity_end_t: float
    emergency_share_of_demand: float
    balance_residual_t: float


@dataclass
class SourceYearRecord:
    source_id: str
    name: str
    year: int
    period: str                    # "year" or "prep"
    available_months: int
    period_fraction: float
    capacity_t_per_year: float
    reserved_capacity_t: float
    reserved_period_t: float
    ordered_t: float
    planned_delivery_t: float
    actual_delivery_t: float
    delivery_share: float
    price_mln_per_t: float
    price_multiplier: float
    payable_volume_t: float
    take_or_pay_idle_t: float
    procurement_mln: float
    reservation_payment_mln: float


@dataclass
class FinanceYear:
    year: int
    procurement_mln: float
    reservation_mln: float
    holding_mln: float
    fixed_opex_mln: float
    capex_mln: float
    total_mln: float
    discount_factor: float
    pv_total_mln: float
    cumulative_capex_mln: float


@dataclass
class InvestmentRecord:
    investment_id: str
    name: str
    option_fee_mln: float
    option_date: str
    exercise_cost_mln: float
    exercise_date: str
    commissioning_date: str
    fixed_opex_mln_per_year: float
    note: str = ""


@dataclass
class Result:
    plan_id: str
    scenario_id: str
    scenario_label: str
    case_dir: str
    months: list[MonthRecord]
    years: list[YearRecord]
    source_years: list[SourceYearRecord]
    finance: list[FinanceYear]
    investments: list[InvestmentRecord]
    violations: list[Violation]
    kpi: dict
    assumptions: dict
    scenario: dict
    plan: dict
    check_matrix: list = field(default_factory=list)     # every rule x year with actual, limit, ok (passed checks included)
    deliveries: list = field(default_factory=list)       # order calendar: delivery month, order placement month, lead time
    units: dict = field(default_factory=lambda: {
        "fuel": "t", "money": "mln conventional units, constant 2035 prices", "capacity": "t/year",
        "reservation_rate": "mln per (t/year)", "service_level": "share 0..1", "time_step": "calendar month"})

    @property
    def feasible(self) -> bool:
        return not any(v.severity == "hard" for v in self.violations)

    def hard_violations(self) -> list[Violation]:
        return [v for v in self.violations if v.severity == "hard"]


# --------------------------------------------------------------------------- helpers
def midx(year: int, month: int) -> int:
    return year * 12 + (month - 1)


def ym(idx: int) -> tuple[int, int]:
    y, m = divmod(idx, 12)
    return y, m + 1


def ym_str(idx: Optional[int]) -> str:
    if idx is None:
        return ""
    y, m = ym(idx)
    return f"{y:04d}-{m:02d}"


def parse_ym(s: str) -> int:
    y, m = str(s).split("-")
    return midx(int(y), int(m))


def lead_months(source: Source, a: Assumptions) -> int:
    pol = a.lead_time_policy
    v = {"max": source.lead_time_max_value, "min": source.lead_time_min_value,
         "mean": 0.5 * (source.lead_time_min_value + source.lead_time_max_value)}[pol]
    unit = source.lead_time_unit
    if unit == "month":
        return int(math.ceil(v - EPS))
    if unit == "week":
        return int(math.ceil(v / float(a.weeks_per_month) - EPS))
    if unit == "day":
        return int(math.ceil(v / float(a.days_per_month) - EPS))
    if unit == "year":
        return int(math.ceil(v * 12 - EPS))
    raise ValueError(f"unknown lead time unit {unit}")


# --------------------------------------------------------------------------- engine
def simulate(case: Case, plan: Plan, scenario: Scenario, assumptions: Optional[Assumptions] = None) -> Result:
    a = assumptions or load_assumptions(None)
    validate_plan(plan, case)
    sid = scenario.scenario_id
    viol: list[Violation] = []

    def add(rule_id: str, severity: str, message: str, **kw) -> None:
        viol.append(Violation(rule_id=rule_id, severity=severity, scenario_id=sid, message=message, **kw))

    years = case.years
    y0, yN = case.first_year, case.last_year
    start_idx, end_idx = midx(y0, 1), midx(yN, 12)
    prep_start = parse_ym(a.prep_period_start)
    variant = scenario.demand_variant

    def dem_total(y: int) -> float:
        return case.demand_row(y).total(variant) * scenario.demand_mult(y)

    def dem_crit(y: int) -> float:
        return case.demand_row(y).critical(variant) * scenario.critical_mult(y)

    # ---- investments -------------------------------------------------------
    src_link: dict[str, str] = dict(a.source_investment_link or {})
    sto_link: dict[str, str] = dict(a.storage_investment_link or {})
    inv_to_source = {v: k for k, v in src_link.items()}
    capex_events: list[tuple[int, float, str, str]] = []        # (idx, amount, investment_id, label)
    commissioning: dict[str, Optional[int]] = {}
    opex_streams: list[tuple[int, float, str]] = []              # (from_idx, mln_per_year, id)
    inv_records: list[InvestmentRecord] = []
    for inv in plan.investments:
        opt = case.investments[inv.investment_id]
        dec_idx = midx(inv.decision_year, inv.decision_month)
        opt_idx = midx(inv.option_year, inv.option_month) if inv.option_year is not None else dec_idx
        note = ""
        if opt.option_fee_mln > 0:
            capex_events.append((opt_idx, opt.option_fee_mln, opt.investment_id, "option fee"))
        if opt.exercise_cost_mln > 0:
            capex_events.append((dec_idx, opt.exercise_cost_mln, opt.investment_id, "exercise / CAPEX"))
        comm: Optional[int]
        if opt.investment_id in sto_link:                      # storage modernization (ZBO)
            so = case.storage[sto_link[opt.investment_id]]
            if inv.decision_year < so.available_from_year:
                add("INVESTMENT_TIMING", "hard", f"{opt.name}: option is available from {so.available_from_year}, decision dated {ym_str(dec_idx)}",
                    year=inv.decision_year, month=inv.decision_month, actual=inv.decision_year, limit=so.available_from_year)
            comm = dec_idx + int(a.zbo_commissioning_lag_months)
        elif opt.investment_id in inv_to_source:               # capacity-creating investment
            s = case.sources[inv_to_source[opt.investment_id]]
            if s.available_from_year is not None:              # Lunar-ISRU style: fixed start year, financing deadline
                deadline = parse_ym(a.isru_financing_deadline)
                if dec_idx > deadline:
                    add("INVESTMENT_TIMING", "hard", f"{opt.name}: CAPEX must be financed by {ym_str(deadline)}, decision dated {ym_str(dec_idx)}; source {s.name} is not available",
                        year=inv.decision_year, month=inv.decision_month, source_id=s.source_id)
                    comm = None
                    note = "not commissioned: financed too late"
                else:
                    comm = max(dec_idx, midx(s.available_from_year, 1))
            else:                                              # Earth-New style: decision + lead time
                comm = dec_idx + lead_months(s, a)
        else:                                                  # generic investment: active from decision
            comm = dec_idx
        commissioning[opt.investment_id] = comm
        if comm is not None and opt.fixed_opex_mln_per_year > 0:
            opex_streams.append((comm, opt.fixed_opex_mln_per_year, opt.investment_id))
        inv_records.append(InvestmentRecord(opt.investment_id, opt.name, opt.option_fee_mln, ym_str(opt_idx) if opt.option_fee_mln > 0 else "",
                                            opt.exercise_cost_mln, ym_str(dec_idx), ym_str(comm), opt.fixed_opex_mln_per_year, note))

    # ---- storage timeline --------------------------------------------------
    base_storage = case.storage["BASE"]
    storage_switches: list[tuple[int, str]] = []
    for inv_id, sto_id in sto_link.items():
        c = commissioning.get(inv_id)
        if c is not None:
            storage_switches.append((c, sto_id))
    storage_switches.sort()

    def storage_at(idx: int):
        mode = base_storage
        for c, sto_id in storage_switches:
            if c <= idx:
                mode = case.storage[sto_id]
        return mode

    # ---- source availability -------------------------------------------------
    def first_delivery_idx(s: Source) -> Optional[int]:
        link = src_link.get(s.source_id)
        if link:
            c = commissioning.get(link)
            if c is None:
                return None
            if s.available_from_year is not None:
                return c + lead_months(s, a)
            return c + int(a.earth_new_post_commissioning_lead_months)
        if s.available_from_year is not None and s.available_from_year > y0:
            return midx(s.available_from_year, 1)
        return prep_start

    avail_idx: dict[str, Optional[int]] = {k: first_delivery_idx(s) for k, s in case.sources.items()}

    # ---- delivery schedule ---------------------------------------------------
    schedule: dict[int, dict[str, float]] = {}
    ordered_by_sy: dict[tuple[str, int], float] = {}
    for o in plan.orders:
        s = case.sources[o.source_id]
        ordered_by_sy[(o.source_id, o.year)] = o.ordered_t
        fa = avail_idx[o.source_id]
        months = [midx(o.year, m) for m in range(1, 13)]
        avail_months = [i for i in months if fa is not None and i >= fa]
        if o.ordered_t <= EPS:
            continue
        if not avail_months:
            add("SOURCE_NOT_AVAILABLE", "hard", f"{s.name}: {o.ordered_t:.3f} t ordered for {o.year} but the source cannot deliver in that year"
                + (f" (first delivery {ym_str(fa)})" if fa is not None else " (required investment missing or financed too late)"),
                year=o.year, source_id=s.source_id, actual=o.ordered_t, limit=0.0, excess=o.ordered_t)
            continue
        if o.profile == "monthly" and o.monthly_t:
            for k, q in enumerate(o.monthly_t):
                i = months[k]
                if q <= EPS:
                    continue
                if i not in avail_months:
                    add("SOURCE_NOT_AVAILABLE", "hard", f"{s.name}: {q:.3f} t scheduled for {ym_str(i)} before first possible delivery {ym_str(fa)}",
                        year=o.year, month=k + 1, source_id=s.source_id, actual=q, limit=0.0, excess=q)
                    continue
                schedule.setdefault(i, {})[s.source_id] = schedule.get(i, {}).get(s.source_id, 0.0) + q
        else:
            q = o.ordered_t / len(avail_months)
            for i in avail_months:
                schedule.setdefault(i, {})[s.source_id] = schedule.get(i, {}).get(s.source_id, 0.0) + q
        # lead-time check: order placement date must fall inside the preparatory period or later,
        # and, for sources unlocked by an investment, not before commissioning.
        lt = lead_months(s, a)
        link = src_link.get(s.source_id)
        earliest_order = prep_start if not link else (commissioning.get(link) or prep_start)
        first_month = min(i for i in avail_months if schedule.get(i, {}).get(s.source_id, 0) > EPS) if any(
            schedule.get(i, {}).get(s.source_id, 0) > EPS for i in avail_months) else None
        if first_month is not None and not link and first_month - lt < earliest_order:
            add("LEAD_TIME_VIOLATED", "hard", f"{s.name}: delivery in {ym_str(first_month)} needs an order by {ym_str(first_month - lt)} "
                f"(lead time {lt} months), before the preparatory period starts {ym_str(earliest_order)}",
                year=o.year, month=ym(first_month)[1], source_id=s.source_id, actual=first_month - lt, limit=earliest_order)

    # ---- order calendar (delivery month -> order placement month) -------------------
    deliveries: list[dict] = []
    for idx in sorted(schedule):
        for k, q in sorted(schedule[idx].items()):
            if q <= EPS:
                continue
            s_ = case.sources[k]
            lt = lead_months(s_, a)
            link = src_link.get(k)
            earliest = prep_start if not link else (commissioning.get(link) or prep_start)
            placement = idx - lt
            deliveries.append(dict(source_id=k, name=s_.name, year=ym(idx)[0], month=ym(idx)[1], delivery_month=ym_str(idx),
                                   planned_t=q, actual_t=q * scenario.delivery_share(s_, ym(idx)[0]), lead_time_months=lt,
                                   order_placement_month=ym_str(placement), earliest_allowed_order=ym_str(earliest), lead_time_ok=placement >= earliest))

    # ---- preparatory period: opening stock -------------------------------------
    prep_records: list[SourceYearRecord] = []
    opening_inventory = 0.0
    prep_procurement = prep_reservation = 0.0
    for st in plan.opening_stock:
        s = case.sources[st.source_id]
        d_idx = midx(st.delivery_year, st.delivery_month)
        fa = avail_idx[st.source_id]
        if fa is None or d_idx < fa or src_link.get(st.source_id):
            add("SOURCE_NOT_AVAILABLE", "hard", f"{s.name}: cannot deliver opening stock in {ym_str(d_idx)} (source not available in the preparatory period)",
                year=st.delivery_year, month=st.delivery_month, source_id=s.source_id, actual=st.tons)
            continue
        lt = lead_months(s, a)
        if d_idx - lt < prep_start:
            add("LEAD_TIME_VIOLATED", "hard", f"{s.name}: opening stock delivery {ym_str(d_idx)} needs an order by {ym_str(d_idx - lt)}, before preparatory period start {ym_str(prep_start)}",
                year=st.delivery_year, month=st.delivery_month, source_id=s.source_id, actual=d_idx - lt, limit=prep_start)
        mode = storage_at(d_idx)
        losses = rules.losses_on_throughput(st.tons, mode.loss_rate_on_throughput)
        opening_inventory += st.tons - losses
        price = s.variable_cost_mln_per_t * scenario.price_mult(s, y0)
        proc = price * st.tons
        resv = rules.reservation_payment(s.reservation_rate_mln_per_t_year, st.tons, float(a.opening_stock_reservation_years))
        prep_procurement += proc
        prep_reservation += resv
        prep_records.append(SourceYearRecord(s.source_id, s.name, st.delivery_year, "prep", 1, float(a.opening_stock_reservation_years),
                                             s.capacity_t_per_year, st.tons, st.tons, st.tons, st.tons, st.tons - losses, 1.0, price,
                                             scenario.price_mult(s, y0), st.tons, 0.0, proc, resv))
    cap0 = storage_at(start_idx).capacity_t
    if opening_inventory > cap0 + EPS:
        add("STORAGE_OVERFLOW", "hard", f"opening stock {opening_inventory:.3f} t exceeds storage capacity {cap0:.1f} t at {y0}-01",
            year=y0, month=1, actual=opening_inventory, limit=cap0, excess=opening_inventory - cap0)

    # ---- monthly simulation ----------------------------------------------------
    months: list[MonthRecord] = []
    inv = opening_inventory
    for idx in range(start_idx, end_idx + 1):
        y, mo = ym(idx)
        mode = storage_at(idx)
        planned = schedule.get(idx, {})
        actual = {k: q * scenario.delivery_share(case.sources[k], y) for k, q in planned.items()}
        thr = fsum(actual.values())
        losses = rules.losses_on_throughput(thr, mode.loss_rate_on_throughput)
        d = dem_total(y) / 12.0
        c = dem_crit(y) / 12.0
        available = inv + thr - losses
        served, shortage = rules.serve(available, d)
        if plan.allocation_rule == "critical_first":
            served_c = min(served, c)
        else:
            served_c = served * (c / d) if d > 0 else 0.0
        shortage_c = max(0.0, c - served_c)
        closing = rules.material_balance(inv, thr, losses, served)
        holding = mode.holding_cost_mln_per_t_year * 0.5 * (inv + closing) / 12.0
        months.append(MonthRecord(y, mo, mode.storage_id, mode.capacity_t, mode.loss_rate_on_throughput, inv, fsum(planned.values()),
                                  thr, losses, available, d, c, served, served_c, shortage, shortage_c, closing, holding, dict(actual)))
        if closing > mode.capacity_t + EPS:
            add("STORAGE_OVERFLOW", "hard", f"end-of-month stock {closing:.3f} t exceeds {mode.name} capacity {mode.capacity_t:.1f} t in {ym_str(idx)}",
                year=y, month=mo, actual=closing, limit=mode.capacity_t, excess=closing - mode.capacity_t)
        elif available > mode.capacity_t + EPS:
            add("INTRA_MONTH_PEAK", "warning", f"stock after inflow {available:.3f} t exceeds {mode.name} capacity {mode.capacity_t:.1f} t within {ym_str(idx)} (before withdrawals)",
                year=y, month=mo, actual=available, limit=mode.capacity_t, excess=available - mode.capacity_t)
        inv = closing

    # ---- yearly aggregation -----------------------------------------------------
    reserve_days = case.constraints["RESERVE_45D"].value if "RESERVE_45D" in case.constraints else rules.RESERVE_DAYS
    year_records: list[YearRecord] = []
    emergency_threshold = float(a.emergency_base_share_threshold)
    emergency_ids = [k for k, s in case.sources.items() if s.name.lower().startswith("emergency") or k == "E"]
    for y in years:
        ms = [m for m in months if m.year == y]
        D, C = dem_total(y), dem_crit(y)
        served = fsum(m.served_t for m in ms)
        served_c = fsum(m.served_critical_t for m in ms)
        thr = fsum(m.throughput_t for m in ms)
        losses = fsum(m.losses_t for m in ms)
        R = rules.reserve_45d(D, reserve_days)
        opening = ms[0].opening_t
        closing = ms[-1].closing_t
        residual = opening + thr - losses - served - closing
        e_ordered = fsum(ordered_by_sy.get((e, y), 0.0) for e in emergency_ids)
        year_records.append(YearRecord(
            y, D, C, served, served_c, rules.service_level(served, D), rules.service_level(served_c, C),
            max(0.0, D - served), max(0.0, C - served_c), opening, closing, fsum(m.planned_inflow_t for m in ms), thr, losses,
            (losses / thr) if thr > 0 else 0.0, R, opening + TOL_T >= R, fsum(0.5 * (m.opening_t + m.closing_t) for m in ms) / len(ms),
            ms[-1].storage_mode, ms[-1].storage_capacity_t, (e_ordered / D) if D > 0 else 0.0, residual))

    # ---- contracts, procurement, reservation per source-year ----------------------
    source_years: list[SourceYearRecord] = list(prep_records)
    for y in years:
        for k, s in case.sources.items():
            fa = avail_idx[k]
            n_avail = sum(1 for m in range(1, 13) if fa is not None and midx(y, m) >= fa)
            f = n_avail / 12.0
            reserved = plan.reserved(k, y)
            ordered = ordered_by_sy.get((k, y), 0.0)
            planned_del = fsum(schedule.get(midx(y, m), {}).get(k, 0.0) for m in range(1, 13))
            actual_del = fsum(mrec.inflow_by_source.get(k, 0.0) for mrec in months if mrec.year == y)
            share = scenario.delivery_share(s, y)
            if reserved > s.capacity_t_per_year + EPS:
                add("CAPACITY_EXCEEDED", "hard", f"{s.name} {y}: reserved {reserved:.3f} t/yr exceeds capacity {s.capacity_t_per_year:.1f} t/yr",
                    year=y, source_id=k, actual=reserved, limit=s.capacity_t_per_year, excess=reserved - s.capacity_t_per_year)
            if reserved > EPS and n_avail == 0:
                add("SOURCE_NOT_AVAILABLE", "hard", f"{s.name} {y}: capacity reserved but the source is not available in {y}"
                    + (f" (first delivery {ym_str(fa)})" if fa is not None else " (investment missing or financed too late)"),
                    year=y, source_id=k, actual=reserved, limit=0.0, excess=reserved)
            reserved_period = reserved * f
            if ordered > reserved_period + 1e-6:
                add("ORDER_EXCEEDS_RESERVATION", "hard", f"{s.name} {y}: ordered {ordered:.3f} t exceeds contractually available {reserved_period:.3f} t "
                    f"(reserved {reserved:.1f} t/yr x {f:.3f} of year)", year=y, source_id=k, actual=ordered, limit=reserved_period, excess=ordered - reserved_period)
            pm = scenario.price_mult(s, y)
            price = s.variable_cost_mln_per_t * pm
            q_pay = rules.take_or_pay_volume(ordered, reserved_period, s.take_or_pay_share)
            source_years.append(SourceYearRecord(k, s.name, y, "year", n_avail, f, s.capacity_t_per_year, reserved, reserved_period, ordered,
                                                 planned_del, actual_del, share, price, pm, q_pay, q_pay - ordered, price * q_pay,
                                                 rules.reservation_payment(s.reservation_rate_mln_per_t_year, reserved, f)))

    # ---- finance -----------------------------------------------------------------
    r = float(a.discount_rate_real)
    t0 = int(a.discount_t0_year)
    timing_offset = {"start": 0.0, "mid": 0.5, "end": 1.0}[str(a.get("discount_timing", "start"))]
    finance: list[FinanceYear] = []
    cum_capex = 0.0
    for y in years:
        proc = fsum(sy.procurement_mln for sy in source_years if sy.year == y and sy.period == "year")
        resv = fsum(sy.reservation_payment_mln for sy in source_years if sy.year == y and sy.period == "year")
        if y == y0:
            proc += prep_procurement
            resv += prep_reservation
        hold = fsum(m.holding_cost_mln for m in months if m.year == y)
        opex = 0.0
        for from_idx, per_year, _ in opex_streams:
            active = sum(1 for m in range(1, 13) if midx(y, m) >= from_idx)
            opex += per_year * active / 12.0
        capex = fsum(amt for i, amt, _, _ in capex_events if ym(i)[0] == y)
        cum_capex += capex
        total = proc + resv + hold + opex + capex
        df = 1.0 / (1.0 + r) ** (y - t0 + timing_offset)
        finance.append(FinanceYear(y, proc, resv, hold, opex, capex, total, df, total * df, cum_capex))
    for i, amt, inv_id, label in capex_events:
        if ym(i)[0] < y0 or ym(i)[0] > yN:
            add("INVESTMENT_TIMING", "hard", f"{inv_id} {label} {amt:.1f} mln dated {ym_str(i)} is outside the horizon {y0}-{yN}", year=ym(i)[0], actual=amt)

    # ---- constraint checks from constraints.csv ------------------------------------
    for c in case.constraints.values():
        applies = c.scenario in ("ALL", sid)
        if c.metric in ("total_service_level", "critical_service_level"):
            sev = "hard" if (applies and scenario.service_thresholds_hard) else "guideline"
            for yr in year_records:
                val = yr.service_level_total if c.metric == "total_service_level" else yr.service_level_critical
                if val + EPS < c.value:
                    kind = "total" if c.metric == "total_service_level" else "critical"
                    short = yr.shortage_total_t if kind == "total" else yr.shortage_critical_t
                    add(c.constraint_id, sev, f"{yr.year}: {kind} service level {val:.4f} < {c.value:.2f} (shortage {short:.3f} t)"
                        + ("" if sev == "hard" else " [guideline in this scenario]"), year=yr.year, actual=val, limit=c.value, excess=c.value - val)
        elif c.metric == "cumulative_capex":
            if not applies:
                continue
            through = int(c.period.split("_")[-1]) if c.period.startswith("through_") else yN
            cum = fsum(fy.capex_mln for fy in finance if fy.year <= through)
            if cum > c.value + EPS:
                add(c.constraint_id, "hard", f"cumulative CAPEX through {through} = {cum:.1f} mln exceeds limit {c.value:.0f} mln",
                    year=through, actual=cum, limit=c.value, excess=cum - c.value)
        elif c.metric == "reserve_equivalent_days":
            if not applies:
                continue
            for yr in year_records:
                ok = yr.reserve_ok
                detail = ""
                if not ok and plan.reserve_mode == "emergency_contract":
                    e_res = fsum(plan.reserved(e, yr.year) for e in emergency_ids)
                    lt_days = max((lead_months(case.sources[e], a) for e in emergency_ids), default=2) * 30.4167
                    cover = yr.demand_total_t * lt_days / 365.0
                    ok = yr.opening_t + TOL_T >= cover and e_res + TOL_T >= yr.reserve_required_t
                    detail = f"; contracted-equivalent test: stock {yr.opening_t:.2f} t vs lead-time cover {cover:.2f} t, reserved Emergency {e_res:.1f} t/yr vs R {yr.reserve_required_t:.2f} t"
                if not ok:
                    add(c.constraint_id, "hard", f"{yr.year}-01: physical stock {yr.opening_t:.3f} t < 45-day reserve {yr.reserve_required_t:.3f} t{detail}",
                        year=yr.year, month=1, actual=yr.opening_t, limit=yr.reserve_required_t, excess=yr.reserve_required_t - yr.opening_t)
        elif c.metric == "emergency_base_channel_consecutive_years":
            if not applies:
                continue
            streak, best, best_years = 0, 0, []
            cur: list[int] = []
            for yr in year_records:
                if yr.emergency_share_of_demand > emergency_threshold:
                    cur.append(yr.year)
                    if len(cur) > best:
                        best, best_years = len(cur), list(cur)
                else:
                    cur = []
            if best > c.value:
                add(c.constraint_id, "hard", f"Emergency is the base channel (> {emergency_threshold:.0%} of demand) for {best} consecutive years {best_years}, limit {int(c.value)}",
                    year=best_years[0], actual=best, limit=c.value, excess=best - c.value)
        elif c.metric == "losses_divided_by_throughput":
            pass  # driven by the scenario's loss_ceiling block below
        else:
            add("UNSUPPORTED_CONSTRAINT", "warning", f"constraint {c.constraint_id} with metric {c.metric!r} is not implemented by the engine", actual=c.value)
    if scenario.loss_ceiling_enabled:
        lim = float(scenario.loss_ceiling.get("max_losses_divided_by_throughput"))
        from_year = int(scenario.loss_ceiling.get("from_year", y0))
        for yr in year_records:
            if yr.year >= from_year and yr.throughput_t > 0 and yr.loss_ratio > lim + EPS:
                add("STRESS_LOSS_LIMIT", "hard", f"{yr.year}: losses/throughput {yr.loss_ratio:.4f} > {lim:.2f} ({yr.losses_t:.3f} t of {yr.throughput_t:.3f} t)",
                    year=yr.year, actual=yr.loss_ratio, limit=lim, excess=yr.loss_ratio - lim)

    # ---- check matrix: every rule x year, passed or not ------------------------------------
    matrix: list[dict] = []
    def mrow(rule, year, metric, actual, limit, op, ok, severity, scope=""):
        matrix.append(dict(rule_id=rule, year=year, metric=metric, actual=actual, limit=limit, operator=op, ok=bool(ok), severity=severity, scope=scope))
    for c in case.constraints.values():
        applies = c.scenario in ("ALL", sid)
        if c.metric in ("total_service_level", "critical_service_level"):
            sev = "hard" if (applies and scenario.service_thresholds_hard) else "guideline"
            for yr in year_records:
                val = yr.service_level_total if c.metric == "total_service_level" else yr.service_level_critical
                mrow(c.constraint_id, yr.year, c.metric, val, c.value, ">=", val + EPS >= c.value, sev)
        elif c.metric == "cumulative_capex" and applies:
            through = int(c.period.split("_")[-1]) if c.period.startswith("through_") else yN
            for fy in finance:
                if fy.year <= through:
                    mrow(c.constraint_id, fy.year, "cumulative_capex", fy.cumulative_capex_mln, c.value, "<=", fy.cumulative_capex_mln <= c.value + EPS, "hard", f"through_{through}")
        elif c.metric == "reserve_equivalent_days" and applies:
            for yr in year_records:
                ok = yr.reserve_ok or not any(v.rule_id == c.constraint_id and v.year == yr.year for v in viol)
                mrow(c.constraint_id, yr.year, "opening_stock_vs_45d_reserve_t", yr.opening_t, yr.reserve_required_t, ">=", ok, "hard", plan.reserve_mode)
        elif c.metric == "emergency_base_channel_consecutive_years" and applies:
            for yr in year_records:
                mrow(c.constraint_id, yr.year, "emergency_share_of_demand", yr.emergency_share_of_demand, emergency_threshold, "<= (else counts as base year)",
                     not any(v.rule_id == c.constraint_id and v.year == yr.year for v in viol), "hard", f"max {int(c.value)} consecutive base years")
    if scenario.loss_ceiling_enabled:
        lim = float(scenario.loss_ceiling.get("max_losses_divided_by_throughput")); from_year = int(scenario.loss_ceiling.get("from_year", y0))
        for yr in year_records:
            if yr.year >= from_year:
                mrow("STRESS_LOSS_LIMIT", yr.year, "losses_divided_by_throughput", yr.loss_ratio, lim, "<=", yr.loss_ratio <= lim + EPS, "hard")
    for y in years:
        ms = [m for m in months if m.year == y]
        peak = max(m.closing_t for m in ms); cap = min(m.storage_capacity_t for m in ms)
        mrow("STORAGE_OVERFLOW", y, "max_end_of_month_stock_t", peak, cap, "<=", peak <= cap + EPS, "hard", "monthly")
        for k, s_ in case.sources.items():
            res_ = plan.reserved(k, y)
            if res_ > EPS or ordered_by_sy.get((k, y), 0.0) > EPS:
                mrow("CAPACITY_EXCEEDED", y, f"reserved_{k}_t_per_year", res_, s_.capacity_t_per_year, "<=", res_ <= s_.capacity_t_per_year + EPS, "hard", s_.name)
                sy = next(x for x in source_years if x.period == "year" and x.source_id == k and x.year == y)
                mrow("ORDER_EXCEEDS_RESERVATION", y, f"ordered_{k}_t", sy.ordered_t, sy.reserved_period_t, "<=", sy.ordered_t <= sy.reserved_period_t + 1e-6, "hard", s_.name)
        lt_ok = all(d["lead_time_ok"] for d in deliveries if d["year"] == y) and not any(v.rule_id == "LEAD_TIME_VIOLATED" and v.year == y for v in viol)
        av_ok = not any(v.rule_id == "SOURCE_NOT_AVAILABLE" and v.year == y for v in viol)
        mrow("LEAD_TIME_VIOLATED", y, "all_deliveries_ordered_within_lead_time", 1.0 if lt_ok else 0.0, 1.0, "==", lt_ok, "hard")
        mrow("SOURCE_NOT_AVAILABLE", y, "all_orders_from_available_sources", 1.0 if av_ok else 0.0, 1.0, "==", av_ok, "hard")

    # ---- KPIs -------------------------------------------------------------------------
    total_cost = fsum(f_.total_mln for f_ in finance)
    pv_cost = fsum(f_.pv_total_mln for f_ in finance)
    served_all = fsum(yr.served_total_t for yr in year_records)
    kpi = {
        "total_cost_mln": total_cost, "pv_cost_mln": pv_cost, "discount_rate_real": r,
        "demand_total_t": fsum(yr.demand_total_t for yr in year_records), "served_total_t": served_all,
        "served_critical_t": fsum(yr.served_critical_t for yr in year_records),
        "shortage_total_t": fsum(yr.shortage_total_t for yr in year_records),
        "shortage_critical_t": fsum(yr.shortage_critical_t for yr in year_records),
        "cost_per_served_t_mln": (total_cost / served_all) if served_all > 0 else float("nan"),
        "pv_cost_per_served_t_mln": (pv_cost / served_all) if served_all > 0 else float("nan"),
        "min_service_level_total": min(yr.service_level_total for yr in year_records),
        "min_service_level_critical": min(yr.service_level_critical for yr in year_records),
        "losses_total_t": fsum(yr.losses_t for yr in year_records), "throughput_total_t": fsum(yr.throughput_t for yr in year_records),
        "capex_total_mln": fsum(f_.capex_mln for f_ in finance), "procurement_total_mln": fsum(f_.procurement_mln for f_ in finance),
        "reservation_total_mln": fsum(f_.reservation_mln for f_ in finance), "holding_total_mln": fsum(f_.holding_mln for f_ in finance),
        "fixed_opex_total_mln": fsum(f_.fixed_opex_mln for f_ in finance),
        "take_or_pay_idle_t": fsum(sy.take_or_pay_idle_t for sy in source_years if sy.period == "year"),
        "opening_inventory_t": opening_inventory, "closing_inventory_t": months[-1].closing_t,
        "hard_violations": sum(1 for v in viol if v.severity == "hard"),
        "guideline_violations": sum(1 for v in viol if v.severity == "guideline"),
        "warnings": sum(1 for v in viol if v.severity == "warning"),
    }
    kpi["feasible"] = kpi["hard_violations"] == 0
    kpi["checks_total"] = len(matrix)
    kpi["checks_passed"] = sum(1 for m in matrix if m["ok"])
    return Result(plan.plan_id, sid, scenario.label, case.source_dir, months, year_records, source_years, finance, inv_records, viol, kpi,
                  a.to_dict(), scenario.to_dict(), plan.to_dict(), matrix, deliveries)


def result_to_dict(res: Result) -> dict:
    return {
        "plan_id": res.plan_id, "scenario_id": res.scenario_id, "scenario_label": res.scenario_label, "case_dir": res.case_dir,
        "units": res.units, "kpi": res.kpi, "feasible": res.feasible,
        "years": [asdict(y) for y in res.years], "months": [asdict(m) for m in res.months],
        "source_years": [asdict(s) for s in res.source_years], "finance": [asdict(f) for f in res.finance],
        "investments": [asdict(i) for i in res.investments], "violations": [asdict(v) for v in res.violations],
        "assumptions": res.assumptions, "scenario": res.scenario, "plan": res.plan,
        "check_matrix": res.check_matrix, "deliveries": res.deliveries,
    }

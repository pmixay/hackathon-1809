"""TEAM_ASSUMPTION registry: every parameter not given by the organizer, with meaning, unit, range, status.

Values are loaded from configs/assumptions.yaml; each entry may be a bare value or a mapping with
value/unit/status/range/justification. Defaults below are used when the file does not mention a key.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

DEFAULTS: dict[str, dict[str, Any]] = {
    "discount_rate_real": dict(value=0.08, unit="share per year", status="TEAM_ASSUMPTION", range=[0.0, 0.15],
        justification="Real rate for infrastructure with technology risk; same rate for all alternatives. Sensitivity 0-12%."),
    "discount_t0_year": dict(value=2035, unit="year", status="TEAM_ASSUMPTION", range=[2035, 2035],
        justification="Cash flows are annual sums dated at the start of each year; PV exponent = year - 2035."),
    "discount_timing": dict(value="start", unit="enum start|mid|end", status="TEAM_ASSUMPTION", range=["start", "mid", "end"],
        justification="Moment within the year to which annual cash flows are dated: start (exponent y-2035), mid (+0.5) or end (+1). Same for all alternatives."),
    "prep_period_start": dict(value="2034-01", unit="YYYY-MM", status="TEAM_ASSUMPTION", range=["2033-01", "2034-12"],
        justification="Earliest month an order can be placed in the preparatory period; Earth-Core needs 12 months before 2035-01."),
    "lead_time_policy": dict(value="max", unit="enum min|max|mean", status="TEAM_ASSUMPTION", range=["min", "max", "mean"],
        justification="Conservative end of the organizer lead-time range is used for scheduling checks."),
    "weeks_per_month": dict(value=4.345, unit="weeks", status="TEAM_ASSUMPTION", range=[4.0, 4.5],
        justification="365/12/7; week-denominated lead times are converted with ceil(weeks/4.345): 6 weeks -> 2 months."),
    "days_per_month": dict(value=30.4167, unit="days", status="TEAM_ASSUMPTION", range=[28, 31],
        justification="365/12; day-denominated lead times converted with ceil."),
    "zbo_commissioning_lag_months": dict(value=0, unit="months", status="TEAM_ASSUMPTION", range=[0, 12],
        justification="Case gives no ZBO build time; modernization is assumed active from the CAPEX payment month. Vary in sensitivity."),
    "earth_new_post_commissioning_lead_months": dict(value=0, unit="months", status="TEAM_ASSUMPTION", range=[0, 12],
        justification="The 18-24 month Earth-New lead time is treated as decision-to-first-delivery; orders are placed during preparation."),
    "isru_commissioning_month": dict(value="2038-01", unit="YYYY-MM", status="CASE_INPUT", range=["2038-01", "2038-01"],
        justification="Case: Lunar-ISRU available from 2038 if CAPEX financed before 2038."),
    "isru_financing_deadline": dict(value="2037-12", unit="YYYY-MM", status="CASE_INPUT", range=["2037-12", "2037-12"],
        justification="Case: CAPEX 1250 must be financed before 2038."),
    "source_investment_link": dict(value={"C": "EARTH_NEW", "D": "LUNAR_ISRU"}, unit="map source_id -> investment_id", status="CASE_INPUT",
        range=None, justification="Earth-New capacity needs the option exercised; Lunar-ISRU needs the pilot CAPEX."),
    "storage_investment_link": dict(value={"ZBO": "ZBO"}, unit="map investment_id -> storage_id", status="CASE_INPUT", range=None,
        justification="ZBO modernization switches the active storage mode."),
    "emergency_base_share_threshold": dict(value=0.20, unit="share of annual total demand", status="TEAM_ASSUMPTION", range=[0.1, 0.5],
        justification="Emergency counts as a 'base channel' in a year when its ordered volume exceeds this share of the year's demand."),
    "holding_cost_averaging": dict(value="trapezoid_monthly", unit="enum", status="TEAM_ASSUMPTION", range=["trapezoid_monthly"],
        justification="Average physical stock per month = (I_start + I_end)/2; holding = 0.72 * avg * 1/12."),
    "storage_capacity_check": dict(value="end_of_month_hard_peak_warning", unit="enum", status="TEAM_ASSUMPTION", range=None,
        justification="Hard violation if end-of-month stock > capacity; warning if stock after inflow and before withdrawals exceeds capacity."),
    "emergency_reserve_equivalence": dict(value="stock_covers_lead_time_and_reserved_capacity_covers_45d", unit="rule", status="TEAM_ASSUMPTION", range=None,
        justification="Contracted reserve counts only if physical stock covers demand during the 6-week Emergency lead time and reserved Emergency capacity >= R_y."),
    "opening_stock_reservation_years": dict(value=1.0, unit="years", status="TEAM_ASSUMPTION", range=[0.0, 1.0],
        justification="Preparatory-period purchase pays the source's reservation rate on the purchased tonnage for one year; booked in 2035."),
    "prep_period_holding_charged": dict(value=False, unit="bool", status="TEAM_ASSUMPTION", range=[True, False],
        justification="Holding cost is charged from 2035-01; the preparatory period's storage time is not charged (immaterial, < 1 month)."),
    "intra_year_demand_profile": dict(value="uniform", unit="enum", status="CASE_INPUT", range=["uniform"],
        justification="Organizer control convention: uniform demand within a year, 365 days."),
}


@dataclass
class Assumptions:
    entries: dict[str, dict[str, Any]] = field(default_factory=dict)
    source_file: str = ""

    def __getattr__(self, key: str) -> Any:
        entries = self.__dict__.get("entries", {})
        if key in entries:
            return entries[key]["value"]
        raise AttributeError(key)

    def get(self, key: str, default: Any = None) -> Any:
        return self.entries[key]["value"] if key in self.entries else default

    def with_overrides(self, **overrides: Any) -> "Assumptions":
        new = {k: dict(v) for k, v in self.entries.items()}
        for k, v in overrides.items():
            if k not in new:
                new[k] = dict(value=v, unit="", status="TEAM_ASSUMPTION", range=None, justification="override")
            else:
                new[k] = dict(new[k], value=v)
        return Assumptions(new, self.source_file)

    def table(self) -> list[dict[str, Any]]:
        return [dict(key=k, **v) for k, v in self.entries.items()]

    def to_dict(self) -> dict[str, Any]:
        return {k: dict(v) for k, v in self.entries.items()}


def load_assumptions(path: str | Path | None = None) -> Assumptions:
    entries = {k: dict(v) for k, v in DEFAULTS.items()}
    src = ""
    if path is not None and Path(path).exists():
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        src = str(path)
        for k, v in data.items():
            if isinstance(v, dict) and "value" in v:
                base = dict(entries.get(k, dict(unit="", status="TEAM_ASSUMPTION", range=None, justification="")))
                base.update(v)
                entries[k] = base
            else:
                base = dict(entries.get(k, dict(unit="", status="TEAM_ASSUMPTION", range=None, justification="")))
                base["value"] = v
                entries[k] = base
    return Assumptions(entries, src)

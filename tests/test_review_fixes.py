"""Defects found by the independent review of criteria 1–6 (18.09, evening) — each fixed and pinned here."""
import json

import pytest

from terraplan.engine import simulate
from terraplan.plan import PlanError, plan_from_dict


def _p3(root):
    return json.loads((root / "configs/plans/P3_isru_zbo.json").read_text(encoding="utf-8"))


def _plan(**decisions):
    d = {"plan_id": "probe", "decisions": {"capacity_reservations": [], "supply_orders": [], "investments": [], "inventory_policy": {}}}
    d["decisions"].update(decisions)
    return plan_from_dict(d)


def test_storage_matrix_row_uses_the_capacity_of_each_month(root, case, base, assumptions):
    """ZBO switches capacity 70 -> 120 in 2037-07: stock of 80 t in December is legal and the matrix must say so."""
    d = _p3(root)
    for r in d["decisions"]["capacity_reservations"]:
        if r["source_id"] == "B" and r["year"] == 2037:
            r["reserved_capacity_t"] = 110
    for o in d["decisions"]["supply_orders"]:
        if o["source_id"] == "B" and o["year"] == 2037:
            base_m = o["ordered_t"] / 12
            o.update(profile="monthly", monthly_t=[base_m] * 11 + [base_m + 50.0], ordered_t=o["ordered_t"] + 50.0)
    res = simulate(case, plan_from_dict(d), base, assumptions)
    dec = next(m for m in res.months if m.year == 2037 and m.month == 12)
    assert 70 < dec.closing_t <= 120 and dec.storage_mode == "ZBO"
    row = next(m for m in res.check_matrix if m["rule_id"] == "STORAGE_OVERFLOW" and m["year"] == 2037)
    assert row["ok"] and row["limit"] == pytest.approx(120) and "2037-12" in row["scope"]
    assert res.feasible and all(m["ok"] for m in res.check_matrix if m["severity"] == "hard")


def test_emergency_streak_matrix_marks_every_year_of_the_streak(case, base, assumptions):
    plan = _plan(capacity_reservations=[{"source_id": "E", "year": y, "reserved_capacity_t": 80} for y in (2035, 2036, 2037)],
                 supply_orders=[{"source_id": "E", "year": y, "ordered_t": 40} for y in (2035, 2036, 2037)])
    res = simulate(case, plan, base, assumptions)
    rows = {m["year"]: m for m in res.check_matrix if m["rule_id"] == "EMERGENCY_BASE_STREAK"}
    assert all(rows[y]["actual"] == 3 and not rows[y]["ok"] for y in (2035, 2036, 2037))
    assert rows[2038]["actual"] == 0 and rows[2038]["ok"]
    v = [x for x in res.violations if x.rule_id == "EMERGENCY_BASE_STREAK"]
    assert len(v) == 1 and v[0].year == 2035 and v[0].actual == 3


def test_contracted_reserve_equivalence_uses_the_six_week_lead_time(case, base, assumptions):
    """Physical stock 11.65 t < R 12.33 t but >= 42-day cover 11.51 t, and Emergency reserved >= R -> 2035 reserve proven by contract."""
    common = dict(capacity_reservations=[{"source_id": "A", "year": 2035, "reserved_capacity_t": 100}, {"source_id": "E", "year": 2035, "reserved_capacity_t": 80}],
                  supply_orders=[{"source_id": "A", "year": 2035, "ordered_t": 100}])
    stock = [{"source_id": "B", "tons": 12.2, "delivery_year": 2034, "delivery_month": 12}]
    ok = simulate(case, _plan(**common, inventory_policy={"opening_stock": stock, "reserve_mode": "emergency_contract"}), base, assumptions)
    assert not any(v.rule_id == "RESERVE_45D" and v.year == 2035 for v in ok.violations)
    physical = simulate(case, _plan(**common, inventory_policy={"opening_stock": stock, "reserve_mode": "physical"}), base, assumptions)
    assert any(v.rule_id == "RESERVE_45D" and v.year == 2035 for v in physical.violations)
    no_contract = dict(common, capacity_reservations=[{"source_id": "A", "year": 2035, "reserved_capacity_t": 100}])
    failed = simulate(case, _plan(**no_contract, inventory_policy={"opening_stock": stock, "reserve_mode": "emergency_contract"}), base, assumptions)
    v = next(x for x in failed.violations if x.rule_id == "RESERVE_45D" and x.year == 2035)
    assert "11.51" in v.message and "0.0 т/год" in v.message     # cover = 100 t x 42/365; no Emergency reserved


def test_reactive_orders_cannot_be_placed_before_the_observation_month(case, stress, assumptions):
    def plan_with_flex_in(month_index):
        monthly = [0.0] * 12
        monthly[month_index] = 10.0
        return _plan(capacity_reservations=[{"source_id": "B", "year": 2038, "reserved_capacity_t": 110}],
                     supply_orders=[{"source_id": "B", "year": 2038, "profile": "monthly", "monthly_t": monthly, "reactive": True}],
                     inventory_policy={"observation_month": "2038-03"})
    early = simulate(case, plan_with_flex_in(4), stress, assumptions)       # delivery 2038-05, 4-month lead -> ordered 2038-01 < 2038-03
    v = [x for x in early.violations if x.rule_id == "LEAD_TIME_VIOLATED"]
    assert v and v[0].source_id == "B" and "2038-03" in v[0].message
    late = simulate(case, plan_with_flex_in(6), stress, assumptions)        # delivery 2038-07 -> ordered 2038-03: allowed
    assert not any(x.rule_id == "LEAD_TIME_VIOLATED" for x in late.violations)
    d = next(x for x in late.deliveries if x["source_id"] == "B" and x["delivery_month"] == "2038-07")
    assert d["earliest_allowed_order"] == "2038-03" and d["lead_time_ok"]
    with pytest.raises(PlanError, match="observation_month"):
        _plan(supply_orders=[{"source_id": "B", "year": 2038, "ordered_t": 1, "reactive": True}])


def test_saved_reactive_plan_is_checked_against_its_observation_month(root, case, stress, assumptions):
    from terraplan.plan import load_plan
    plan = load_plan(root / "configs/plans/P3_isru_zbo_reactive.json", case)
    assert plan.observation_month == "2038-03" and any(o.reactive for o in plan.orders)
    res = simulate(case, plan, stress, assumptions)
    assert not any(v.rule_id == "LEAD_TIME_VIOLATED" for v in res.violations)
    assert all(d["earliest_allowed_order"] == "2038-03" for d in res.deliveries if d["source_id"] in ("B", "E") and d["year"] >= 2038)


def test_undelivered_volume_payment_is_a_registered_switch(root, case, stress, assumptions):
    plan = plan_from_dict(_p3(root))
    default = simulate(case, plan, stress, assumptions)
    isru = next(s for s in default.source_years if s.source_id == "D" and s.year == 2038)
    assert isru.actual_delivery_t == pytest.approx(55) and isru.procurement_mln == pytest.approx(300)   # organizer: ordered 100 t paid
    research = simulate(case, plan, stress, assumptions.with_overrides(undelivered_volume_paid=False))
    isru2 = next(s for s in research.source_years if s.source_id == "D" and s.year == 2038)
    assert isru2.procurement_mln == pytest.approx(165) and isru2.take_or_pay_idle_t == pytest.approx(0)
    assert research.kpi["pv_cost_mln"] < default.kpi["pv_cost_mln"]
    assert default.assumptions["undelivered_volume_paid"]["status"] == "CASE_INPUT"


def test_opening_stock_above_source_capacity_is_reported(case, base, assumptions):
    res = simulate(case, _plan(inventory_policy={"opening_stock": [{"source_id": "B", "tons": 200, "delivery_year": 2034, "delivery_month": 12}]}), base, assumptions)
    v = [x for x in res.violations if x.rule_id == "CAPACITY_EXCEEDED"]
    assert v and v[0].source_id == "B" and v[0].actual == pytest.approx(200) and v[0].limit == pytest.approx(110)

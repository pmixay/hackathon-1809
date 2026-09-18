"""Integration checks of the monthly engine on the real case data."""
import json

import pytest

from terraplan.engine import simulate
from terraplan.plan import plan_from_dict
from terraplan.planner import build_plan

P3 = dict(plan_id="T_isru_zbo", reservation_caps={"A": 190, "B": 110, "D": 120},
          investments=[dict(investment_id="LUNAR_ISRU", decision_year=2036, decision_month=1),
                       dict(investment_id="ZBO", decision_year=2037, decision_month=7)])


@pytest.fixture(scope="module")
def plan(case, base, assumptions):
    return build_plan(case, base, P3, assumptions)


def test_material_balance_holds_every_month(case, plan, base, assumptions):
    res = simulate(case, plan, base, assumptions)
    for m in res.months:
        assert abs(m.opening_t + m.throughput_t - m.losses_t - m.served_t - m.closing_t) < 1e-9
        assert m.closing_t >= -1e-9, "physical stock must never be negative"
        assert m.served_t <= m.demand_t + 1e-9
        assert m.served_critical_t <= m.served_t + 1e-9
        assert abs(m.losses_t - m.throughput_t * m.loss_rate) < 1e-9
    for y in res.years:
        assert abs(y.balance_residual_t) < 1e-9
        assert y.demand_critical_t <= y.demand_total_t + 1e-9


def test_base_plan_is_feasible_and_costs_decompose(case, plan, base, assumptions):
    res = simulate(case, plan, base, assumptions)
    assert res.feasible, [v.message for v in res.hard_violations()]
    for f in res.finance:
        assert abs(f.procurement_mln + f.reservation_mln + f.holding_mln + f.fixed_opex_mln + f.capex_mln - f.total_mln) < 1e-9
    k = res.kpi
    assert abs(sum(f.total_mln for f in res.finance) - k["total_cost_mln"]) < 1e-9
    assert abs(k["capex_total_mln"] - 1430.0) < 1e-9  # ISRU 1250 + ZBO 180
    assert k["min_service_level_total"] >= 0.97 and k["min_service_level_critical"] >= 0.99
    assert all(y.reserve_ok for y in res.years)


def test_reliability_is_not_a_base_multiplier(case, plan, base, assumptions):
    res = simulate(case, plan, base, assumptions)
    for s in res.source_years:
        if s.period == "year":
            assert abs(s.actual_delivery_t - s.planned_delivery_t) < 1e-9
            assert abs(s.planned_delivery_t - s.ordered_t) < 1e-9


def test_stress_applies_exact_multipliers(case, plan, base, stress, assumptions):
    rb = simulate(case, plan, base, assumptions)
    rs = simulate(case, plan, stress, assumptions)
    yb = {y.year: y for y in rb.years}
    ys = {y.year: y for y in rs.years}
    for y in (2035, 2036, 2037):
        assert abs(ys[y].demand_total_t - yb[y].demand_total_t) < 1e-9
    for y in (2038, 2039, 2040):
        assert abs(ys[y].demand_total_t - 1.15 * yb[y].demand_total_t) < 1e-9
        assert abs(ys[y].demand_critical_t - 1.15 * yb[y].demand_critical_t) < 1e-9
    sb = {(s.source_id, s.year): s for s in rb.source_years if s.period == "year"}
    ss = {(s.source_id, s.year): s for s in rs.source_years if s.period == "year"}
    # ISRU actual delivery = 55 % / 75 % / 100 % of plan, never multiplied by reliability 0.78/0.90/0.93
    assert abs(ss[("D", 2038)].actual_delivery_t - 0.55 * ss[("D", 2038)].planned_delivery_t) < 1e-9
    assert abs(ss[("D", 2039)].actual_delivery_t - 0.75 * ss[("D", 2039)].planned_delivery_t) < 1e-9
    assert abs(ss[("D", 2040)].actual_delivery_t - 1.00 * ss[("D", 2040)].planned_delivery_t) < 1e-9
    # ISRU under-delivery does not refund payment
    assert abs(ss[("D", 2038)].procurement_mln - sb[("D", 2038)].procurement_mln) < 1e-9
    # Core/Flex price x1.25 in 2038-2039 only; reservation rate unchanged
    for sid in ("A", "B"):
        for y in (2038, 2039):
            assert abs(ss[(sid, y)].price_mln_per_t - 1.25 * sb[(sid, y)].price_mln_per_t) < 1e-9
            assert abs(ss[(sid, y)].reservation_payment_mln - sb[(sid, y)].reservation_payment_mln) < 1e-9
        for y in (2035, 2036, 2037, 2040):
            assert abs(ss[(sid, y)].price_mln_per_t - sb[(sid, y)].price_mln_per_t) < 1e-9
    # loss ceiling is checked only in stress and only from 2038
    assert not any(v.rule_id == "STRESS_LOSS_LIMIT" for v in rb.violations)
    # service thresholds are guidelines (not hard) in stress
    assert all(v.severity == "guideline" for v in rs.violations if v.rule_id.endswith("_SERVICE"))


def test_runs_are_deterministic(case, plan, base, assumptions):
    a = simulate(case, plan, base, assumptions)
    b = simulate(case, plan, base, assumptions)
    assert json.dumps(a.kpi, sort_keys=True) == json.dumps(b.kpi, sort_keys=True)
    assert [m.closing_t for m in a.months] == [m.closing_t for m in b.months]


def test_take_or_pay_and_reservation_payments(case, base, assumptions):
    # reserve 100 t/yr of Earth-Core in 2035 but order only 50 t -> pay for 70 t (TOP 70 %) and 45 mln reservation
    d = {"plan_id": "top", "decisions": {
        "capacity_reservations": [{"source_id": "A", "year": 2035, "reserved_capacity_t": 100}],
        "supply_orders": [{"source_id": "A", "year": 2035, "ordered_t": 50}],
        "investments": [], "inventory_policy": {}}}
    res = simulate(case, plan_from_dict(d), base, assumptions)
    s = next(x for x in res.source_years if x.source_id == "A" and x.year == 2035)
    assert abs(s.payable_volume_t - 70) < 1e-9
    assert abs(s.procurement_mln - 6.2 * 70) < 1e-9
    assert abs(s.take_or_pay_idle_t - 20) < 1e-9
    assert abs(s.reservation_payment_mln - 0.45 * 100) < 1e-9
    assert res.finance[0].procurement_mln == pytest.approx(6.2 * 70)


def test_partial_year_reservation_is_prorated(case, base, assumptions):
    # Earth-New exercised 2035-01 -> commissioned 2037-01 (24 months, conservative) -> 2037 fraction 1.0
    # ISRU commissioned 2038-01, first delivery 2038-03 (2 months lead) -> 10/12 of 2038
    d = {"plan_id": "prorate", "decisions": {
        "capacity_reservations": [{"source_id": "D", "year": 2038, "reserved_capacity_t": 120}],
        "supply_orders": [{"source_id": "D", "year": 2038, "ordered_t": 100}],
        "investments": [{"investment_id": "LUNAR_ISRU", "decision_year": 2036, "decision_month": 1}],
        "inventory_policy": {}}}
    res = simulate(case, plan_from_dict(d), base, assumptions)
    s = next(x for x in res.source_years if x.source_id == "D" and x.year == 2038)
    assert s.available_months == 10 and abs(s.period_fraction - 10 / 12) < 1e-9
    assert abs(s.reserved_period_t - 100) < 1e-9
    months = [m for m in res.months if m.year == 2038]
    assert months[0].inflow_by_source.get("D", 0) == 0 and months[2].inflow_by_source["D"] == pytest.approx(10.0)
    # ISRU fixed OPEX 70/yr from 2038-01: full year in 2038
    f = {x.year: x for x in res.finance}
    assert f[2038].fixed_opex_mln == pytest.approx(70.0)
    assert f[2036].capex_mln == pytest.approx(1250.0)

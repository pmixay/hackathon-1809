"""Boundary values and deliberately infeasible plans: violations must name rule, period and value."""
import pytest

from conftest import copy_case
from terraplan.case import load_case
from terraplan.engine import simulate
from terraplan.plan import plan_from_dict
from terraplan.planner import build_plan


def _plan(**decisions):
    d = {"plan_id": "boundary", "decisions": {"capacity_reservations": [], "supply_orders": [], "investments": [], "inventory_policy": {}}}
    d["decisions"].update(decisions)
    return plan_from_dict(d)


def test_empty_plan_reports_shortage_not_negative_inventory(case, base, assumptions):
    res = simulate(case, _plan(), base, assumptions)
    assert all(m.closing_t == 0 for m in res.months)
    assert res.kpi["shortage_total_t"] == pytest.approx(sum(d.base_total_t for d in case.demand))
    assert {v.rule_id for v in res.hard_violations()} >= {"BASE_TOTAL_SERVICE", "BASE_CRITICAL_SERVICE", "RESERVE_45D"}
    assert res.kpi["cost_per_served_t_mln"] != res.kpi["cost_per_served_t_mln"]  # NaN when nothing served (no division by zero crash)


def test_storage_overflow_is_detected(case, base, assumptions):
    # 200 t ordered from Earth-Flex in January 2035 into a 70 t depot
    res = simulate(case, _plan(capacity_reservations=[{"source_id": "B", "year": 2035, "reserved_capacity_t": 110}],
                               supply_orders=[{"source_id": "B", "year": 2035, "profile": "monthly", "monthly_t": [100] + [0] * 11}]), base, assumptions)
    v = [x for x in res.violations if x.rule_id == "STORAGE_OVERFLOW"]
    assert v and v[0].year == 2035 and v[0].month == 1 and v[0].limit == pytest.approx(70) and v[0].excess > 0


def test_emergency_streak_limit(case, base, assumptions):
    # Emergency > 20 % of demand for three consecutive years
    res = simulate(case, _plan(capacity_reservations=[{"source_id": "E", "year": y, "reserved_capacity_t": 80} for y in (2035, 2036, 2037)],
                               supply_orders=[{"source_id": "E", "year": y, "ordered_t": 40} for y in (2035, 2036, 2037)]), base, assumptions)
    v = [x for x in res.violations if x.rule_id == "EMERGENCY_BASE_STREAK"]
    assert v and v[0].actual == 3 and v[0].limit == 2


def test_capex_limit_through_2037(tmp_path, base, assumptions):
    case_dir = copy_case(tmp_path, extra_investment=dict(investment_id="BIG", name="Synthetic big CAPEX", option_fee_mln=0, exercise_cost_mln=600,
                                                          total_capex_mln=600, commissioning_rule="synthetic", fixed_opex_mln_per_year=0, status="TEAM_ASSUMPTION", notes=""))
    case = load_case(case_dir)
    res = simulate(case, _plan(investments=[{"investment_id": "LUNAR_ISRU", "decision_year": 2036}, {"investment_id": "BIG", "decision_year": 2037}]), base, assumptions)
    v = [x for x in res.violations if x.rule_id == "CAPEX_2037"]
    assert v and v[0].actual == pytest.approx(1850) and v[0].limit == 1800 and v[0].excess == pytest.approx(50)


def test_isru_financed_too_late_is_unavailable(case, base, assumptions):
    res = simulate(case, _plan(capacity_reservations=[{"source_id": "D", "year": 2039, "reserved_capacity_t": 100}],
                               supply_orders=[{"source_id": "D", "year": 2039, "ordered_t": 50}],
                               investments=[{"investment_id": "LUNAR_ISRU", "decision_year": 2038, "decision_month": 3}]), base, assumptions)
    ids = {v.rule_id for v in res.hard_violations()}
    assert "INVESTMENT_TIMING" in ids and "SOURCE_NOT_AVAILABLE" in ids


def test_zbo_before_2036_is_a_timing_violation(case, base, assumptions):
    res = simulate(case, _plan(investments=[{"investment_id": "ZBO", "decision_year": 2035}]), base, assumptions)
    assert any(v.rule_id == "INVESTMENT_TIMING" and v.year == 2035 for v in res.violations)


def test_lead_time_violation_when_prep_period_too_short(case, base, assumptions):
    a = assumptions.with_overrides(prep_period_start="2034-06")   # Earth-Core needs 12 months -> Jan 2035 delivery impossible
    res = simulate(case, _plan(capacity_reservations=[{"source_id": "A", "year": 2035, "reserved_capacity_t": 100}],
                               supply_orders=[{"source_id": "A", "year": 2035, "ordered_t": 96}]), base, a)
    v = [x for x in res.violations if x.rule_id == "LEAD_TIME_VIOLATED"]
    assert v and v[0].source_id == "A" and "2034-01" in v[0].message


def test_zero_demand_year_has_defined_service_level(tmp_path, base, assumptions):
    case_dir = copy_case(tmp_path, extra_demand=dict(year=2041, base_total_t=0, base_critical_t=0, low_total_t=0, high_total_t=0, status="TEAM_ASSUMPTION"))
    case = load_case(case_dir)
    res = simulate(case, _plan(), base, assumptions)
    y = next(x for x in res.years if x.year == 2041)
    assert y.service_level_total == 1.0 and y.service_level_critical == 1.0 and y.reserve_required_t == 0


def test_greedy_plan_hits_reserve_each_year(case, base, assumptions):
    plan = build_plan(case, base, dict(plan_id="g", reservation_caps={"A": 190, "B": 110, "C": 130},
                                       investments=[dict(investment_id="EARTH_NEW", option_year=2035, option_month=1, decision_year=2035, decision_month=1)]), assumptions)
    res = simulate(case, plan, base, assumptions)
    assert all(y.reserve_ok for y in res.years)
    assert res.feasible, [v.message for v in res.hard_violations()]

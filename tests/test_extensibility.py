"""Organizer check: add a source and a future year on a COPY of the dataset without touching the engine."""
import pytest

from conftest import SOURCE_X, copy_case
from terraplan.case import load_case
from terraplan.engine import simulate
from terraplan.plan import plan_from_dict
from terraplan.scenario import scenario_from_dict


def test_source_x_and_year_2041_on_a_copy(tmp_path, assumptions):
    case_dir = copy_case(tmp_path, extra_source=SOURCE_X,
                         extra_demand=dict(year=2041, base_total_t=450, base_critical_t=290, low_total_t=360, high_total_t=562.5, status="TEAM_ASSUMPTION"))
    case = load_case(case_dir)
    assert "X" in case.sources and case.last_year == 2041
    scen = scenario_from_dict({"scenario_id": "TEAM_2041_EXT", "status": "TEAM_ASSUMPTION", "changes": ["+Source-X 10 t/yr", "+2041 demand 450 t"]})
    plan = plan_from_dict({"plan_id": "ext", "decisions": {
        "capacity_reservations": [{"source_id": "X", "year": 2041, "reserved_capacity_t": 10}, {"source_id": "A", "year": 2041, "reserved_capacity_t": 190}],
        "supply_orders": [{"source_id": "X", "year": 2041, "ordered_t": 10}, {"source_id": "A", "year": 2041, "ordered_t": 190}],
        "investments": [], "inventory_policy": {}}})
    res = simulate(case, plan, scen, assumptions)
    sx = next(s for s in res.source_years if s.source_id == "X" and s.year == 2041)
    assert sx.actual_delivery_t == pytest.approx(10) and sx.procurement_mln == pytest.approx(50) and sx.reservation_payment_mln == pytest.approx(1.0)
    assert len(res.years) == 7 and res.years[-1].year == 2041
    # original constraints still apply (CAPEX limits, reserve) — nothing silently dropped
    assert any(v.rule_id == "RESERVE_45D" and v.year == 2041 for v in res.violations)

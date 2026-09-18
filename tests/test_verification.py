"""Criterion 5: golden values, manual hand-check, independent CSV recalculation, verify command, check matrix."""
import subprocess
import sys

import pytest

from independent_recalc import recalc
from terraplan.cli import main
from terraplan.engine import simulate
from terraplan.export import write_results
from terraplan.plan import load_plan


@pytest.fixture(scope="module")
def p3_base(root, case, base, assumptions):
    return simulate(case, load_plan(root / "configs/plans/P3_isru_zbo.json", case), base, assumptions)


def test_golden_kpis_p3_base(p3_base):
    """Regression guard: values from results/alternatives/P3_isru_zbo_BASE (2026-09-18)."""
    k = p3_base.kpi
    assert k["total_cost_mln"] == pytest.approx(10654.259, abs=1e-3)
    assert k["pv_cost_mln"] == pytest.approx(8638.857, abs=1e-3)
    assert k["cost_per_served_t_mln"] == pytest.approx(7.665, abs=1e-3)
    assert k["capex_total_mln"] == pytest.approx(1430.0)
    assert k["losses_total_t"] == pytest.approx(29.492, abs=1e-3)
    assert k["shortage_total_t"] == pytest.approx(0, abs=1e-9) and k["hard_violations"] == 0


def test_manual_hand_check_2035(p3_base):
    """docs/manual_check.md: hand-calculated 2035 values."""
    y = p3_base.years[0]; f = p3_base.finance[0]
    assert y.reserve_required_t == pytest.approx(12.329, abs=1e-3)
    assert y.opening_t == pytest.approx(12.329, abs=1e-3)
    assert y.closing_t == pytest.approx(17.260, abs=1e-3)
    assert y.losses_t == pytest.approx(4.944, abs=1e-3)
    core = next(s for s in p3_base.source_years if s.source_id == "A" and s.year == 2035)
    assert core.ordered_t == pytest.approx(109.876, abs=1e-3)
    assert core.procurement_mln == pytest.approx(681.23, abs=0.01)
    assert core.reservation_payment_mln == pytest.approx(49.44, abs=0.01)
    assert f.holding_mln == pytest.approx(10.65, abs=0.01)
    assert f.total_mln == pytest.approx(858.16, abs=0.01)


def test_check_matrix_covers_every_year_and_rule(p3_base, case):
    years = {m["year"] for m in p3_base.check_matrix}
    rules = {m["rule_id"] for m in p3_base.check_matrix}
    assert years == set(case.years)
    assert {"BASE_TOTAL_SERVICE", "BASE_CRITICAL_SERVICE", "CAPEX_2037", "CAPEX_2040", "RESERVE_45D", "EMERGENCY_BASE_STREAK",
            "STORAGE_OVERFLOW", "CAPACITY_EXCEEDED", "ORDER_EXCEEDS_RESERVATION", "LEAD_TIME_VIOLATED", "SOURCE_NOT_AVAILABLE"} <= rules
    assert all(m["ok"] for m in p3_base.check_matrix)
    assert p3_base.kpi["checks_passed"] == p3_base.kpi["checks_total"] == len(p3_base.check_matrix)


def test_delivery_calendar_respects_lead_times(p3_base):
    assert p3_base.deliveries and all(d["lead_time_ok"] for d in p3_base.deliveries)
    core_jan = next(d for d in p3_base.deliveries if d["source_id"] == "A" and d["delivery_month"] == "2035-01")
    assert core_jan["order_placement_month"] == "2034-01" and core_jan["lead_time_months"] == 12
    isru = [d for d in p3_base.deliveries if d["source_id"] == "D"]
    assert min(d["delivery_month"] for d in isru) == "2038-03"


def test_independent_recalc_and_verify_command(tmp_path, root, p3_base):
    out = write_results(p3_base, tmp_path / "res", xlsx=False)
    assert recalc(out, root / "data/case") == []
    assert main(["verify", str(out), "--case", str(root / "data/case")]) == 0
    # tamper with the export -> verify must fail
    import json
    d = json.loads((out / "result.json").read_text(encoding="utf-8"))
    d["kpi"]["pv_cost_mln"] += 1.0
    (out / "result.json").write_text(json.dumps(d), encoding="utf-8")
    assert main(["verify", str(out), "--case", str(root / "data/case")]) == 1


def test_discount_timing_conventions(case, base, assumptions, root):
    plan = load_plan(root / "configs/plans/P3_isru_zbo.json", case)
    start = simulate(case, plan, base, assumptions.with_overrides(discount_timing="start"))
    end = simulate(case, plan, base, assumptions.with_overrides(discount_timing="end"))
    assert end.kpi["pv_cost_mln"] == pytest.approx(start.kpi["pv_cost_mln"] / 1.08)
    assert end.kpi["total_cost_mln"] == start.kpi["total_cost_mln"]


def test_committed_results_reproduce(root):
    """The committed result directory re-runs to the same numbers (organizer: same data -> same result)."""
    rc = subprocess.run([sys.executable, "-m", "terraplan", "verify", str(root / "results/alternatives/P3_isru_zbo_BASE"), "--case", str(root / "data/case")],
                        capture_output=True, text=True, cwd=str(root), env={"PYTHONPATH": str(root / "src"), "PATH": "/usr/bin:/bin:/usr/local/bin"})
    assert rc.returncode == 0, rc.stdout + rc.stderr

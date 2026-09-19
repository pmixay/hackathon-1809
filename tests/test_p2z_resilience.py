"""EXP-12: independent arithmetic, residual risk, boundary witnesses and replay."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from independent_recalc import recalc
from provenance import verify_saved
from run_p2z_resilience import DELAYS, TOLERANCE, p2z_shock, run_experiment
from run_reverse_stress import failure_violations
from terraplan.cli import main as cli_main
from terraplan.engine import TOL_T, simulate
from terraplan.export import load_result
from terraplan.plan import plan_from_dict
from terraplan.scenario import scenario_from_dict


@pytest.fixture(scope="module")
def experiment(tmp_path_factory, root):
    immutable = list((root / "data/case").glob("*.csv")) + list((root / "configs").rglob("*.*"))
    before = {p: p.read_bytes() for p in immutable if p.is_file()}
    out = tmp_path_factory.mktemp("p2z_resilience")
    report, _ = run_experiment(out)
    assert {p: p.read_bytes() for p in before} == before
    return out, report


def test_stock_minimum_and_residual_contract_failures(experiment):
    out, report = experiment
    assert report["method"]["selected_stock_net_t"] == 3.2
    assert len(report["sizing"]) == 33
    assert all(not row["target_physical_pass"] for row in report["sizing"][:-1])
    before = load_result(out / "without_measure_delay_03m")
    after = load_result(out / "physical_stock_delay_03m")
    added_gross = 6 * 0.5399  # ceil(3.2/(6*0.988)*10000)/10000 per delivery
    added_net = added_gross * 0.988
    assert after.years[3].opening_t - before.years[3].opening_t == pytest.approx(added_net)
    assert all(y.reserve_ok for y in after.years)
    assert not after.feasible  # a physical buffer cannot cure unavailable C slots
    assert {v.rule_id for v in failure_violations(after)} == {"SOURCE_NOT_AVAILABLE", "ORDER_EXCEEDS_RESERVATION"}
    assert after.kpi["shortage_total_t"] == 0
    deliveries = [d for d in after.deliveries if d["source_id"] == "B" and d["year"] == 2037]
    assert [d["month"] for d in deliveries] == list(range(7, 13))
    assert all(d["lead_time_months"] == 4 and d["lead_time_ok"] for d in deliveries)


def test_stock_price_independently_from_monthly_balance(experiment):
    out, _ = experiment
    old = load_result(out / "without_measure_delay_03m")
    new = load_result(out / "physical_stock_delay_03m")
    annual_holding = {}
    extra_stock = 0.0
    for month in old.months:
        inflow = 0.5399 * 0.988 if month.year == 2037 and month.month >= 7 else 0.0
        annual_holding[month.year] = annual_holding.get(month.year, 0) + (extra_stock + inflow / 2) * 0.72 / 12
        extra_stock += inflow
    expected = sum((holding + (6 * 0.5399 * 8.9 + 6.479 * 0.15 if year == 2037 else 0)) / 1.08 ** (year - 2035)
                   for year, holding in annual_holding.items())
    assert new.kpi["pv_cost_mln"] - old.kpi["pv_cost_mln"] == pytest.approx(expected)
    assert new.plan["decisions"]["investments"] == old.plan["decisions"]["investments"]


@pytest.mark.parametrize("delay", DELAYS)
def test_guarded_calendar_preserves_annual_commitment_and_exposes_larger_delay(experiment, delay):
    out, report = experiment
    original = report["plans"]["without_measure"]["decisions"]
    guarded = report["plans"]["guarded_calendar"]["decisions"]
    old_orders = {(o["source_id"], o["year"]): o["ordered_t"] for o in original["supply_orders"]}
    assert {(o["source_id"], o["year"]): o["ordered_t"] for o in guarded["supply_orders"]} == pytest.approx(old_orders)
    assert guarded["investments"] == original["investments"]
    assert guarded["inventory_policy"] == original["inventory_policy"]
    res = load_result(out / f"guarded_calendar_delay_{delay:02d}m")
    assert res.feasible == (delay in (0, 3))
    assert res.kpi["shortage_total_t"] == 0
    if delay in (0, 3):
        assert all(y.reserve_ok for y in res.years)
        assert not failure_violations(res)
        c = [m.inflow_by_source.get("C", 0) for m in res.months if m.year == 2037]
        assert c[:3] == [0, 0, 0]
        assert sum(c) == pytest.approx(13.1882)
        assert max(c) * 12 <= 17.585
    else:
        assert not res.years[3].reserve_ok


def test_shocks_only_touch_named_source_years_and_respect_background(case, stress):
    sc = p2z_shock(stress, case, 0.01, 0.02, 1.25)
    for year in case.years:
        physical = year >= 2038
        assert sc.demand_mult(year) == pytest.approx(stress.demand_mult(year) * (1.01 if physical else 1))
        assert sc.critical_mult(year) == pytest.approx(stress.critical_mult(year) * (1.01 if physical else 1))
        for sid, source in case.sources.items():
            assert sc.delivery_share(source, year) == pytest.approx(stress.delivery_share(source, year) * (0.98 if physical and sid == "C" else 1))
            assert sc.price_mult(source, year) == pytest.approx(stress.price_mult(source, year) * (1.25 if sid in ("A", "B") and year in (2038, 2039) else 1))
    assert sc.loss_ceiling == stress.loss_ceiling


@pytest.mark.parametrize("variant", ["without_measure", "physical_stock", "guarded_calendar", "adapted_stress"])
def test_boundary_matches_independent_reserve_arithmetic(experiment, case, assumptions, variant):
    _, report = experiment
    plan = plan_from_dict(report["plans"][variant])
    ref = scenario_from_dict(report["references"][variant])
    reference = simulate(case, plan, ref, assumptions)
    # At each January: reserve slack / (prior cumulative demand + prior net C + current R_y).
    candidates = []
    for y in reference.years:
        if y.year < 2038:
            continue
        prior = [m for m in reference.months if 2038 <= m.year < y.year]
        denominator = y.reserve_required_t + sum(m.demand_t + m.inflow_by_source.get("C", 0) * (1 - m.loss_rate) for m in prior)
        candidates.append((y.opening_t - y.reserve_required_t + TOL_T) / denominator)
    exact = min(candidates)
    diagonal = next(r for r in report["boundary"][variant] if r["demand_direction"] == r["earth_new_direction"])
    assert diagonal["pass_radius"] <= exact + 1e-12
    assert exact <= diagonal["fail_radius"] + 1e-12
    assert diagonal["fail_radius"] - diagonal["pass_radius"] <= TOLERANCE
    for row in report["boundary"][variant]:
        for key, expected_failure in (("pass_radius", False), ("fail_radius", True)):
            radius = row[key]
            res = simulate(case, plan, p2z_shock(ref, case, row["demand_direction"] * radius, row["earth_new_direction"] * radius), assumptions)
            assert bool(failure_violations(res)) == expected_failure


def test_price_only_sensitivity_preserves_physics_and_pv_is_linear(experiment):
    _, report = experiment
    for variant in report["boundary"]:
        rows = [r for r in report["sensitivity"] if r["variant"] == variant and r["factor"] == "price"]
        baseline = next(r for r in rows if r["value"] == 1)
        slopes = []
        for row in rows:
            assert row["full_pass"] == baseline["full_pass"]
            assert row["max_reserve_gap_t"] == baseline["max_reserve_gap_t"]
            assert row["shortage_t"] == baseline["shortage_t"]
            if row["value"] != 1:
                slopes.append(row["delta_pv_mln"] / (row["value"] - 1))
        assert slopes == pytest.approx([slopes[0]] * len(slopes))


def test_export_replay_and_independent_csv_arithmetic(experiment):
    out, report = experiment
    verify_saved(out)
    for run in report["runs"]:
        folder, case_dir = out / run["result_dir"], out / run["case_dir"]
        assert cli_main(["verify", str(folder), "--case", str(case_dir)]) == 0
        assert recalc(folder, case_dir) == []
        assert sum(run["delta_components_mln"].values()) == pytest.approx(run["delta_total_same_delay_mln"], abs=1e-8)


def test_repeatability_and_tamper_detection(experiment, tmp_path):
    out, report = experiment
    again = tmp_path / "repeat"
    report2, _ = run_experiment(again)
    assert report2 == report
    first = verify_saved(out)
    second = verify_saved(again)
    assert first == second
    target = again / "cases/delay_03m/supply_sources.csv"
    target.write_bytes(target.read_bytes() + b" ")
    with pytest.raises(ValueError, match="output_sha256 mismatch"):
        verify_saved(again)


def test_published_p2z_artifacts_are_current(root):
    manifest = verify_saved(root / "results/p2z_resilience")
    assert manifest["experiment_id"] == "EXP-12"


@pytest.mark.parametrize("args", [(float("nan"), 0, 1), (0, 1.1, 1), (-0.1, 0, 1), (0, 0, 0)])
def test_invalid_shock_parameters(case, base, args):
    with pytest.raises(ValueError):
        p2z_shock(base, case, *args)

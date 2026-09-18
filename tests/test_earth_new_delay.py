"""EXP-09: isolated commissioning delay, frozen slots, finance and export replay."""
import hashlib
import json
import sys
from dataclasses import asdict
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from run_earth_new_delay import DELAYS, copy_delayed_case, run_experiment
from independent_recalc import recalc
from terraplan.case import load_case
from terraplan.cli import main as cli_main
from terraplan.engine import simulate
from terraplan.export import load_result
from terraplan.plan import load_plan


@pytest.fixture(scope="module")
def experiment(tmp_path_factory):
    out = tmp_path_factory.mktemp("earth_new_delay")
    report, _ = run_experiment(out)
    return out, report


@pytest.fixture(scope="module")
def reference(root, case, base, assumptions):
    plan = load_plan(root / "configs/plans/P2z_earth_new_zbo.json", case)
    return simulate(case, plan, base, assumptions)


def test_zero_delay_reproduces_original_plan(experiment, reference):
    out, report = experiment
    zero = load_result(out / "delay_00m")
    assert zero.kpi == pytest.approx(reference.kpi)
    assert zero.months == reference.months
    assert not report["runs"][0]["violations"]
    assert report["runs"][0]["first_violation"] is None
    assert report["runs"][0]["commissioning"] == "2037-01"


@pytest.mark.parametrize("delay,date", [(0, "2037-01"), (3, "2037-04"), (6, "2037-07"), (12, "2038-01")])
def test_case_overlay_and_investment_dates_are_isolated(experiment, case, reference, delay, date):
    out, report = experiment
    modified = load_case(out / f"delay_{delay:02d}m/case")
    res = load_result(out / f"delay_{delay:02d}m")
    assert modified.sources["C"].lead_time_min_value == case.sources["C"].lead_time_min_value + delay
    assert modified.sources["C"].lead_time_max_value == case.sources["C"].lead_time_max_value + delay
    for sid in ("A", "B", "D", "E"):
        assert modified.sources[sid] == case.sources[sid]
    for key in ("demand", "storage", "investments", "constraints"):
        assert getattr(modified, key) == getattr(case, key)
    allowed = {"lead_time_min_value", "lead_time_max_value", "status", "notes"}
    assert {k: v for k, v in asdict(modified.sources["C"]).items() if k not in allowed} == {
        k: v for k, v in asdict(case.sources["C"]).items() if k not in allowed}
    c = next(i for i in res.investments if i.investment_id == "EARTH_NEW")
    assert c.commissioning_date == date
    assert c.exercise_date == c.option_date == "2035-01"
    assert res.plan["decisions"]["investments"] == report["original_plan"]["decisions"]["investments"]
    assert res.plan["decisions"]["capacity_reservations"] == report["original_plan"]["decisions"]["capacity_reservations"]
    assert [f.capex_mln for f in res.finance] == [f.capex_mln for f in reference.finance]


@pytest.mark.parametrize("delay", [3, 6, 12])
def test_missed_slots_are_not_compressed_or_caught_up(experiment, reference, delay):
    out, report = experiment
    res = load_result(out / f"delay_{delay:02d}m")
    missed_gross = missed_net = 0.0
    for old, new in zip(reference.months, res.months):
        missed = old.year == 2037 and old.month <= delay
        original_c = old.inflow_by_source.get("C", 0.0)
        assert new.inflow_by_source.get("C", 0.0) == pytest.approx(0 if missed else original_c)
        for sid in ("A", "B", "D", "E"):
            assert new.inflow_by_source.get(sid, 0.0) == old.inflow_by_source.get(sid, 0.0)
        if missed:
            missed_gross += original_c
            missed_net += original_c * (1 - old.loss_rate)
    assert missed_gross == pytest.approx(13.1882 * delay / 12)
    for old, new in zip(reference.years, res.years):
        if old.year >= 2038:
            assert old.opening_t - new.opening_t == pytest.approx(missed_net)
            assert not new.reserve_ok
        assert new.shortage_total_t < 1e-9
        assert new.service_level_total == pytest.approx(1)
        assert new.service_level_critical == pytest.approx(1)
    row = next(r for r in report["runs"] if r["delay_months"] == delay)
    assert row["missed_earth_new_t"] == pytest.approx(missed_gross)
    assert row["reserve_failed_years"] == "2038;2039;2040"
    assert (row["first_rule"], row["first_year"], row["first_month"]) == ("SOURCE_NOT_AVAILABLE", 2037, 1)
    assert row["first_reserve_violation"]["year"] == 2038
    if delay == 12:
        assert "first missed frozen delivery slot" in row["first_violation"]["message"]
        assert all(v.month is None for v in res.violations if v.rule_id == "SOURCE_NOT_AVAILABLE")


@pytest.mark.parametrize("delay", [3, 6, 12])
def test_delay_cost_from_independent_lost_stock_arithmetic(experiment, reference, assumptions, delay):
    out, report = experiment
    res = load_result(out / f"delay_{delay:02d}m")
    lost_stock, expected_holding = 0.0, {y.year: 0.0 for y in reference.years}
    for m in reference.months:
        loss_this_month = m.inflow_by_source.get("C", 0.0) * (1 - m.loss_rate) if m.year == 2037 and m.month <= delay else 0
        expected_holding[m.year] -= 0.72 / 12 * (lost_stock + loss_this_month / 2)
        lost_stock += loss_this_month
    expected_reservation = -13.189 * 0.30 * delay / 12
    for old, new in zip(reference.finance, res.finance):
        assert new.procurement_mln == old.procurement_mln  # paid original orders, no refund
        assert new.holding_mln - old.holding_mln == pytest.approx(expected_holding[old.year])
        assert new.reservation_mln - old.reservation_mln == pytest.approx(expected_reservation if old.year == 2037 else 0)
    expected_pv = sum((value + (expected_reservation if year == 2037 else 0)) /
                      (1 + assumptions.discount_rate_real) ** (year - 2035) for year, value in expected_holding.items())
    row = next(r for r in report["runs"] if r["delay_months"] == delay)
    assert row["delta_pv_mln"] == pytest.approx(expected_pv)
    assert sum(row["delta_components_mln"].values()) == pytest.approx(row["delta_total_mln"])
    assert row["delta_components_mln"]["capex_total_mln"] == 0


def test_export_verify_independent_csv_and_repeatability(experiment, tmp_path, root):
    out, report = experiment
    for delay in DELAYS:
        folder = out / f"delay_{delay:02d}m"
        assert cli_main(["verify", str(folder), "--case", str(folder / "case")]) == 0
        assert recalc(folder, folder / "case") == []
    for path, digest in report["input_sha256"].items():
        assert hashlib.sha256((root / path).read_bytes()).hexdigest() == digest
    second = tmp_path / "repeat"
    report2, _ = run_experiment(second)
    assert report == report2
    for name in ("comparison.csv", "yearly.csv", "report.json", "summary.md"):
        assert (out / name).read_bytes() == (second / name).read_bytes()
    for delay in DELAYS:
        name = f"delay_{delay:02d}m"
        first_kpi = json.loads((out / name / "run_manifest.json").read_text())["kpi_sha256"]
        second_kpi = json.loads((second / name / "run_manifest.json").read_text())["kpi_sha256"]
        assert first_kpi == second_kpi


def test_reject_unplanned_delay(tmp_path):
    with pytest.raises(ValueError, match="delay"):
        copy_delayed_case(tmp_path / "invalid", -1)

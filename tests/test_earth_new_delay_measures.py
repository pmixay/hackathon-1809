"""EXP-12: меры P2z против задержки Earth-New — сроки реакции, минимальные объёмы, стоимость, воспроизводимость."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from run_earth_new_delay_measures import MEASURE_DELAYS, OBSERVATION_MONTH, REACTION_MONTHS, TOLERANCE_T, run_experiment
from independent_recalc import recalc
from terraplan.cli import main as cli_main
from terraplan.export import load_result
from terraplan.plan import load_plan
from terraplan.engine import simulate


@pytest.fixture(scope="module")
def experiment(tmp_path_factory):
    out = tmp_path_factory.mktemp("earth_new_delay_measures")
    report, _ = run_experiment(out)
    return out, report


def rows(report, delay):
    return {r["measure"]: r for r in report["comparison"] if r["delay_months"] == delay}


@pytest.mark.parametrize("delay", MEASURE_DELAYS)
def test_measures_remove_consequences_but_not_the_event(experiment, delay):
    out, report = experiment
    r = rows(report, delay)
    assert r["none"]["reserve_failed_years"] == "2038;2039;2040" and not r["none"]["passes"]
    for measure in ("reactive_flex", "advance_buffer"):
        assert r[measure]["passes"] and r[measure]["reserve_failed_years"] == ""
        assert r[measure]["shortage_t"] == 0 and r[measure]["min_service_total"] == pytest.approx(1)
        assert r[measure]["event_violations"] >= 1          # недоступность Earth-New остаётся фактом события
        assert r[measure]["consequence_violations"] == 0
        assert r[measure]["flex_volume_t"] > 0
        assert r[measure]["delta_pv_vs_no_measure_mln"] > 0  # защита стоит денег
    # объём минимален: на шаг ниже мера уже не защищает резерв
    assert r["reactive_flex"]["min_reserve_slack_t"] >= 0
    assert r["reactive_flex"]["min_reserve_slack_t"] < 0.05


@pytest.mark.parametrize("delay", MEASURE_DELAYS)
def test_reactive_orders_respect_observation_and_lead_time(experiment, delay):
    out, report = experiment
    folder = out / f"delay_{delay:02d}m" / "reactive_flex"
    res = load_result(folder)
    assert res.plan["decisions"]["inventory_policy"]["observation_month"] == OBSERVATION_MONTH
    order = next(o for o in res.plan["decisions"]["supply_orders"] if o["source_id"] == "B" and o["year"] == 2037)
    assert order["reactive"] is True
    assert [m for m in range(1, 13) if order["monthly_t"][m - 1] > 0] == REACTION_MONTHS
    b_rows = [d for d in res.deliveries if d["source_id"] == "B" and d["year"] == 2037 and d["planned_t"] > 0]
    assert b_rows and all(d["order_placement_month"] >= OBSERVATION_MONTH for d in b_rows)
    assert not any(v.rule_id == "LEAD_TIME_VIOLATED" for v in res.violations)


@pytest.mark.parametrize("delay", MEASURE_DELAYS)
def test_advance_buffer_is_paid_without_delay_and_reaction_is_not(experiment, delay):
    out, report = experiment
    r = rows(report, delay)
    assert r["advance_buffer"]["premium_if_no_delay_pv_mln"] > 0
    assert r["advance_buffer"]["premium_run_passes"]
    assert r["reactive_flex"]["premium_if_no_delay_pv_mln"] == 0
    premium = load_result(out / f"delay_{delay:02d}m" / "advance_buffer_no_delay")
    assert premium.feasible and premium.kpi["shortage_total_t"] == 0
    buffer_order = next(o for o in premium.plan["decisions"]["supply_orders"] if o["source_id"] == "B" and o["year"] == 2036)
    assert buffer_order["monthly_t"][11] == pytest.approx(r["advance_buffer"]["flex_volume_t"])


def test_exports_verify_recalculate_and_repeat(experiment, tmp_path, root):
    out, report = experiment
    dirs = sorted(p.parent for p in out.rglob("run_manifest.json") if (p.parent / "plan.json").exists())
    assert len(dirs) == 4 * len(MEASURE_DELAYS)
    for folder in dirs:
        assert cli_main(["verify", str(folder), "--case", str(folder / "case")]) == 0
        assert recalc(folder, folder / "case") == []
        assert cli_main(["validate", "--plan", str(folder / "plan.json"), "--case", str(folder / "case")]) == 0
    second = tmp_path / "repeat"
    report2, _ = run_experiment(second)
    assert report == report2
    for name in ("comparison.csv", "yearly.csv", "report.json", "summary.md"):
        assert (out / name).read_bytes() == (second / name).read_bytes()


def test_volume_is_minimal_within_tolerance(experiment, root, case, base, assumptions):
    out, report = experiment
    from run_earth_new_delay import copy_delayed_case, delay_scenario, freeze_earth_new_schedule
    from run_earth_new_delay_measures import consequence_violations, with_reactive_flex
    plan = load_plan(root / "configs/plans/P2z_earth_new_zbo.json", case)
    frozen = freeze_earth_new_schedule(plan, simulate(case, plan, base, assumptions))
    delay = MEASURE_DELAYS[0]
    volume = rows(report, delay)["reactive_flex"]["flex_volume_t"]
    modified = copy_delayed_case(out / "tol_case", delay)
    sc = delay_scenario(base, delay)
    a = assumptions.with_overrides(earth_new_preparation_delay_months=delay)
    assert not consequence_violations(simulate(modified, with_reactive_flex(frozen, volume, delay), sc, a))
    assert consequence_violations(simulate(modified, with_reactive_flex(frozen, volume - 2 * TOLERANCE_T, delay), sc, a))

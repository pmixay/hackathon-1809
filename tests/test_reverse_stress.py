"""EXP-07: shock isolation, analytical reserve boundary and reproducible CLI report."""
import csv
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from run_reverse_stress import RAYS, bisect_boundary, failure_violations, shocked_scenario
from provenance import sha256
from terraplan.engine import TOL_T, Violation, simulate
from terraplan.plan import load_plan, plan_from_dict
from terraplan.scenario import scenario_from_dict


@pytest.fixture(scope="module")
def adapted(root, case):
    return load_plan(root / "configs/plans/P3_isru_zbo_adapted.json", case)


def test_shocks_are_relative_isolated_and_do_not_change_plan(case, stress, assumptions, adapted):
    before_scenario, before_plan = deepcopy(stress.to_dict()), deepcopy(adapted.to_dict())
    baseline = simulate(case, adapted, stress, assumptions)
    zero = simulate(case, adapted, shocked_scenario(stress, case, 0, 0), assumptions)
    assert zero.kpi == baseline.kpi
    assert not failure_violations(zero)
    shock = shocked_scenario(stress, case, 0.1, 0.2)
    result = simulate(case, adapted, shock, assumptions)
    for old, new in zip(baseline.years, result.years):
        factor = 1.1 if old.year >= 2038 else 1.0
        assert new.demand_total_t == pytest.approx(old.demand_total_t * factor)
        assert new.demand_critical_t == pytest.approx(old.demand_critical_t * factor)
    for old, new in zip(baseline.source_years, result.source_years):
        factor = 0.8 if old.source_id == "D" and old.year >= 2038 else 1.0
        assert new.actual_delivery_t == pytest.approx(old.actual_delivery_t * factor)
        assert new.planned_delivery_t == old.planned_delivery_t
        assert new.procurement_mln == old.procurement_mln
        assert new.reservation_payment_mln == old.reservation_payment_mln
    assert [shock.delivery_share(case.sources["D"], y) for y in (2038, 2039, 2040)] == pytest.approx([0.44, 0.6, 0.8])
    assert shock.loss_ceiling == stress.loss_ceiling
    assert shock.variable_price_multiplier == stress.variable_price_multiplier
    assert stress.to_dict() == before_scenario
    assert adapted.to_dict() == before_plan
    # Nested scenario data must be independent as well.
    shock.loss_ceiling["enabled"] = False
    assert stress.to_dict() == before_scenario


@pytest.mark.parametrize("direction", RAYS)
def test_boundary_matches_independent_reserve_equation(case, stress, assumptions, adapted, direction):
    """Near the boundary no shortage occurs, so stocks are affine in both shocks.

    Reserve slack in y = original slack - d*(prior demand + current reserve)
    - s*(prior net ISRU). Solve each year's inequality directly, without bisection.
    """
    baseline = simulate(case, adapted, stress, assumptions)
    u, v = direction
    prior_demand, prior_isru = 0.0, 0.0
    thresholds = []
    for yr in baseline.years:
        if yr.year < 2038:
            continue
        slope = u * (prior_demand + yr.reserve_required_t) + v * prior_isru
        if slope > 0:
            thresholds.append(((yr.opening_t - yr.reserve_required_t + TOL_T) / slope, yr.year))
        prior_demand += yr.demand_total_t
        # CASE_INPUT: ZBO loss rate 1.2%, stress ISRU shares 55%, 75%, 100%.
        share = {2038: 0.55, 2039: 0.75, 2040: 1.0}[yr.year]
        prior_isru += adapted.order("D", yr.year).ordered_t * share * (1 - 0.012)
    expected, year = min(thresholds)

    def evaluate(t):
        return simulate(case, adapted, shocked_scenario(stress, case, u * t, v * t), assumptions)

    lo, hi = bisect_boundary(lambda t: bool(failure_violations(evaluate(t))))
    assert hi is not None and hi - lo <= 1e-12
    assert lo - 1e-14 <= expected <= hi + 1e-14
    assert not failure_violations(evaluate(lo))
    failed = evaluate(hi)
    first = failure_violations(failed)[0]
    assert (first.rule_id, first.year, first.month) == ("RESERVE_45D", year, 1)
    assert year == 2040
    assert first.limit - first.actual > TOL_T
    assert failed.kpi["shortage_total_t"] < 1e-9  # reserve fails before service
    # Failure remains present under larger adverse shocks on the same ray.
    assert all(failure_violations(evaluate(t)) for t in (1e-4, 0.01, 0.5))


def test_bisection_endpoints_and_missing_boundary():
    lo, hi = bisect_boundary(lambda t: t > 0.125)
    assert lo <= 0.125 < hi and hi - lo <= 1e-12
    assert bisect_boundary(lambda t: False) == (0.5, None)
    with pytest.raises(ValueError, match="already fails"):
        bisect_boundary(lambda t: True)


@pytest.mark.parametrize("maximum,tolerance", [(0, 1e-12), (1.1, 1e-12), (float("nan"), 1e-12),
                                              (0.5, 0), (0.5, 0.5), (0.5, float("nan"))])
def test_invalid_search_parameters(maximum, tolerance):
    with pytest.raises(ValueError):
        bisect_boundary(lambda t: False, maximum, tolerance)


def test_service_guidelines_count_warnings_do_not_and_first_is_chronological():
    warning = Violation("STORAGE_PEAK", "warning", "TEAM_TEST", "", year=2035, month=1)
    service = Violation("BASE_TOTAL_SERVICE", "guideline", "TEAM_TEST", "", year=2039, actual=0.96, limit=0.97)
    reserve = Violation("RESERVE_45D", "hard", "TEAM_TEST", "", year=2039, month=1)
    result = SimpleNamespace(violations=[warning])
    assert not failure_violations(result)
    result.violations.append(service)
    assert failure_violations(result) == [service]
    result.violations.append(reserve)
    assert failure_violations(result) == [reserve, service]


def test_cli_reproducibility_and_replay_of_exported_endpoints(tmp_path, root, case, assumptions):
    dirs = [tmp_path / "first", tmp_path / "second"]
    for out in dirs:
        command = [sys.executable, str(root / "experiments/run_reverse_stress.py"),
                   "--max-shock", "0.5", "--tolerance", "1e-12", "--out", str(out)]
        completed = subprocess.run(command, cwd=tmp_path, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stdout + completed.stderr
    for name in ("report.json", "boundary.csv", "summary.md"):
        assert (dirs[0] / name).read_bytes() == (dirs[1] / name).read_bytes()
    report = json.loads((dirs[0] / "report.json").read_text(encoding="utf-8"))
    for path, digest in report["input_sha256"].items():
        assert sha256(root / path) == digest
    assert report["random_seed"] is None
    plan = plan_from_dict(report["plan"])
    minimum = report["minimum"]
    for state, fails in (("passing", False), ("failing", True)):
        replay = simulate(case, plan, scenario_from_dict(minimum[f"{state}_scenario"]), assumptions)
        assert replay.kpi == minimum[f"{state}_kpi"]
        assert bool(failure_violations(replay)) is fails
    with (dirs[0] / "boundary.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(RAYS)
    for row in rows:
        lo, hi = float(row["pass_radius"]), float(row["fail_radius"])
        assert 0 < lo < hi and hi - lo <= 1e-12  # precision survives CSV export
        assert minimum["pass_radius"] <= hi
    diagonal = next(row for row in rows if row["demand_direction"] == row["isru_direction"])
    assert float(diagonal["fail_radius"]) == minimum["fail_radius"]

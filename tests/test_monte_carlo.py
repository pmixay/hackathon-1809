"""EXP-10: shock semantics, independent balance/cost checks, pairing and replay."""
import csv
import json
import copy
import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from run_monte_carlo import (MODES, analyze, compare_outputs, metric_summary, protection_plans,
                             result_row, sample_factors, sample_scenario, sha256,
                             wilson_interval, write_report)
from run_reverse_stress import failure_violations
from provenance import normalized_bytes
from terraplan.engine import Violation, simulate


def sample(d=0.017, s=0.013, p=0.07):
    return dict(sample_id=1, demand_increase=d, isru_reduction=s,
                coupled_isru_reduction=d, price_deviation=p)


@pytest.fixture(scope="module")
def experiment():
    return analyze(n=24, seed=203510)


def test_rng_local_reproducible_and_common_latents(assumptions):
    import random

    state = random.getstate()
    rows = sample_factors(100, 203510, assumptions)
    assert random.getstate() == state
    assert sample_factors(100, 203510, assumptions) == rows
    assert sample_factors(100, 203511, assumptions) != rows
    assert [r["sample_id"] for r in rows] == list(range(1, 101))
    for r in rows:
        assert 0 <= r["demand_increase"] < 0.02
        assert 0 <= r["isru_reduction"] < 0.02
        assert -0.1 <= r["price_deviation"] < 0.1
        assert r["coupled_isru_reduction"] == r["demand_increase"]
        assert r["demand_increase"] != r["isru_reduction"]


@pytest.mark.parametrize("n,seed", [(0, 1), (-1, 1), (1.5, 1), (True, 1), (1, -1), (1, 1.5)])
def test_invalid_sampling_arguments(n, seed, assumptions):
    with pytest.raises(ValueError):
        sample_factors(n, seed, assumptions)


def test_exact_stress_multipliers_periods_and_no_mutation(case, stress):
    before = stress.to_dict()
    for mode in MODES:
        sc = sample_scenario(stress, case, sample(), mode)
        reduction = 0.013 if mode == "independent" else 0.017
        assert sc.status == "TEAM_ASSUMPTION"
        assert sc.loss_ceiling == stress.loss_ceiling
        for year in case.years:
            dm = 1.15 * 1.017 if year >= 2038 else stress.demand_mult(year)
            assert sc.demand_mult(year) == pytest.approx(dm)
            assert sc.critical_mult(year) == pytest.approx(dm)
            for sid, source in case.sources.items():
                share = stress.delivery_share(source, year)
                if sid == "D" and year >= 2038:
                    share *= 1 - reduction
                assert sc.delivery_share(source, year) == pytest.approx(share)
                price = 1.25 * 1.07 if sid in ("A", "B") and year in (2038, 2039) else stress.price_mult(source, year)
                assert sc.price_mult(source, year) == pytest.approx(price)
    assert stress.to_dict() == before


def test_saved_exp08_plans_and_reference_controls(experiment, root):
    plans = experiment["manifest"]["plans"]
    for name, plan in plans.items():
        saved = json.loads((root / f"results/protection_measures/{name}.plan.json").read_text(encoding="utf-8"))
        # Python versions can differ in the last bit of monthly float sums.
        # Compare the declared annual volume tightly, retaining exact equality
        # for monthly profiles and every other decision and metadata field.
        normalized = copy.deepcopy(plan)
        orders = normalized["decisions"]["supply_orders"]
        saved_orders = saved["decisions"]["supply_orders"]
        assert len(orders) == len(saved_orders)
        for order, saved_order in zip(orders, saved_orders):
            assert order["ordered_t"] == pytest.approx(saved_order["ordered_t"], rel=0, abs=1e-12)
            order["ordered_t"] = saved_order["ordered_t"]
        assert normalized == saved
    reference = {r["variant"]: r for r in experiment["report"]["reference"]}
    assert all(not r["failed"] for r in reference.values())
    assert reference["without_measure"]["pv_cost_mln"] == pytest.approx(10637.025, abs=0.001)
    assert reference["physical_stock"]["delta_pv_mln"] == pytest.approx(83.667825, abs=1e-6)
    assert reference["early_zbo_plus_stock"]["delta_pv_mln"] == pytest.approx(49.458033, abs=1e-6)


def test_independent_reserve_balance_oracle(case, stress, assumptions):
    # Stock erosion equals extra demand + missing NET ISRU inflows - unserved
    # demand (which never left storage). Reserve requirements also rise.
    for name, plan in protection_plans(case).items():
        before = plan.to_dict()
        ref = simulate(case, plan, stress, assumptions)
        sc = sample_scenario(stress, case, sample(), "independent")
        res = simulate(case, plan, sc, assumptions)
        gaps = []
        for old, new in zip(ref.years, res.years):
            prior = [y for y in ref.years if 2038 <= y.year < old.year]
            missing = sum(m.inflow_by_source.get("D", 0) * (1 - m.loss_rate)
                          for m in ref.months if 2038 <= m.year < old.year) * 0.013
            unserved = sum(y.shortage_total_t for y in res.years if 2038 <= y.year < old.year)
            erosion = sum(y.demand_total_t for y in prior) * 0.017 + missing - unserved
            required = old.reserve_required_t * (1.017 if old.year >= 2038 else 1)
            assert new.opening_t == pytest.approx(old.opening_t - erosion)
            assert new.reserve_required_t == pytest.approx(required)
            gaps.append(max(0, required - old.opening_t + erosion))
        assert result_row(res, "independent", 1, name)["max_reserve_gap_t"] == pytest.approx(max(gaps))
        assert plan.to_dict() == before


def test_price_changes_only_cash_and_has_analytic_pv_delta(case, stress, assumptions):
    for plan in protection_plans(case).values():
        low = simulate(case, plan, sample_scenario(stress, case, sample(p=-0.1), "independent"), assumptions)
        high = simulate(case, plan, sample_scenario(stress, case, sample(p=0.1), "independent"), assumptions)
        ref = simulate(case, plan, stress, assumptions)
        discount = {f.year: f.discount_factor for f in ref.finance}
        expected = sum(s.procurement_mln * 0.2 * discount[s.year] for s in ref.source_years
                       if s.source_id in ("A", "B") and s.year in (2038, 2039) and s.period == "year")
        assert high.kpi["pv_cost_mln"] - low.kpi["pv_cost_mln"] == pytest.approx(expected)
        assert high.months == low.months and high.years == low.years
        assert bool(failure_violations(high)) == bool(failure_violations(low))


def test_guideline_service_is_failure_even_when_engine_feasible(case, stress, assumptions):
    plan = protection_plans(case)["without_measure"]
    result = simulate(case, plan, sample_scenario(stress, case, sample(d=0.4), "independent"), assumptions)
    guidelines = [v for v in result.violations if v.severity == "guideline"]
    assert any(v.rule_id == "BASE_TOTAL_SERVICE" for v in guidelines)
    guideline_only = replace(result, violations=guidelines)
    assert guideline_only.feasible
    row = result_row(guideline_only, "independent", 1, "without_measure")
    assert row["failed"] and row["service_failed"]


def test_first_failure_retains_simultaneous_causes_and_ignores_warning(case, stress, assumptions):
    ref = simulate(case, protection_plans(case)["without_measure"], stress, assumptions)
    violations = [
        Violation("WARNING", "warning", "TEAM_MC", "ignored", year=2035, month=1),
        Violation("BASE_TOTAL_SERVICE", "guideline", "TEAM_MC", "annual", year=2040),
        Violation("STORAGE_OVERFLOW", "hard", "TEAM_MC", "same time", year=2039, month=1),
        Violation("RESERVE_45D", "hard", "TEAM_MC", "first", year=2039, month=1),
    ]
    row = result_row(replace(ref, violations=violations), "independent", 1, "test")
    assert row["first_year"] == 2039 and row["first_month"] == 1
    assert row["first_rules"] == "RESERVE_45D;STORAGE_OVERFLOW"
    assert len(json.loads(row["first_violations"])) == 2
    assert row["reserve_failed"] and row["service_failed"]
    assert "WARNING" not in row["failure_rules"]
    annual = result_row(replace(ref, violations=[violations[1]]), "independent", 1, "test")
    assert annual["first_month"] == 12


def test_wilson_including_all_and_zero_failures():
    assert wilson_interval(5, 10) == pytest.approx([0.2365930905, 0.7634069095])
    assert wilson_interval(0, 10000)[1] == pytest.approx(0.0003839984)
    assert wilson_interval(10000, 10000)[0] == pytest.approx(0.9996160016)
    with pytest.raises(ValueError):
        wilson_interval(1, 0)


def test_quantiles_use_declared_interpolation():
    stats = metric_summary([0, 10, 20, 30, 40])
    assert stats == dict(mean=20, min=0, max=40, p05=2, p50=20, p95=38)
    assert metric_summary([7])["p95"] == 7


def test_common_samples_and_paired_aggregation(experiment):
    rows = experiment["runs"]
    assert len(rows) == 24 * 3 * 2
    for mode in MODES:
        for sid in range(1, 25):
            group = [r for r in rows if r["mode"] == mode and r["sample_id"] == sid]
            assert len(group) == 3
            for r in group:
                assert r["delta_pv_mln"] == pytest.approx(r["pv_cost_mln"] - group[0]["pv_cost_mln"])
    for summary in experiment["report"]["comparison"]:
        group = [r for r in rows if r["mode"] == summary["mode"] and r["variant"] == summary["variant"]]
        baseline = [r for r in rows if r["mode"] == summary["mode"] and r["variant"] == "without_measure"]
        assert summary["failures"] == sum(r["failed"] for r in group)
        assert sum(f["count"] for f in summary["first_failure_counts"]) == summary["failures"]
        assert summary["failure_reduction_pp"] == pytest.approx(100 * (sum(r["failed"] for r in baseline) - summary["failures"]) / 24)
        assert summary["introduced_failures"] == 0


def test_full_small_replay_hashes_and_tamper_detection(experiment, tmp_path, root):
    first, second = tmp_path / "first", tmp_path / "second"
    write_report(experiment, first)
    replay = analyze(24, 203510, first / "samples.csv")
    assert replay == experiment
    write_report(replay, second)
    compare_outputs(second, first)
    # A Windows checkout may rewrite all artifacts, including CSV and manifest.
    for path in second.iterdir():
        path.write_bytes(normalized_bytes(path.read_bytes()).replace(b"\n", b"\r\n"))
    compare_outputs(second, first)
    manifest = json.loads((first / "run_manifest.json").read_text(encoding="utf-8"))
    for name, digest in manifest["input_sha256"].items():
        assert sha256(root / name) == digest
    for name, digest in manifest["output_sha256"].items():
        assert sha256(first / name) == digest
    with (first / "runs.csv").open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 144
    assert float(rows[0]["pv_cost_mln"]) == experiment["runs"][0]["pv_cost_mln"]
    with pytest.raises(ValueError, match="replay samples"):
        analyze(24, 1, first / "samples.csv")
    (second / "runs.csv").write_text("tampered", encoding="utf-8")
    with pytest.raises(ValueError, match="runs.csv"):
        compare_outputs(second, first)

"""EXP-11: price/period isolation, independent cost attribution, physical invariance and replay."""
import csv
import json
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from independent_recalc import recalc
from provenance import verify_saved
from run_geopolitical_price_shock import PLAN_IDS, compare_saved, main, prepare_copy, run_experiment
from terraplan.cli import main as cli_main
from terraplan.engine import simulate
from terraplan.export import load_result
from terraplan.plan import load_plan
from terraplan.scenario import load_scenario


@pytest.fixture(scope="module")
def experiment(tmp_path_factory):
    root = Path(__file__).resolve().parents[1]
    protected = [*sorted((root / "data/case").glob("*.csv")),
                 *sorted((root / "src/terraplan").glob("*.py")),
                 *sorted((root / "configs").rglob("*.*"))]
    original = {p: p.read_bytes() for p in protected}
    out = tmp_path_factory.mktemp("geopolitical_price_shock")
    report, _ = run_experiment(out)
    assert original == {p: p.read_bytes() for p in protected}
    return out, report


def test_copied_data_and_team_scenario_are_isolated(experiment, root, case):
    out, _ = experiment
    for path in (root / "data/case").glob("*.csv"):
        assert (out / "case" / path.name).read_bytes() == path.read_bytes()
    shock = load_scenario(out / "shock.yaml")
    assert shock.scenario_id == "TEAM_GEOPOLITICAL_PRICE_SHOCK"
    assert shock.status == "TEAM_ASSUMPTION"
    assert shock.service_thresholds_hard
    assert not shock.loss_ceiling_enabled
    for year in range(2034, 2042):
        assert shock.demand_mult(year) == shock.critical_mult(year) == 1
        for sid, source in case.sources.items():
            assert shock.delivery_share(source, year) == 1
            assert shock.price_mult(source, year) == (1.25 if sid in ("A", "B") and year in (2038, 2039) else 1)
    with (out / "price_overlay.csv").open(encoding="utf-8", newline="") as f:
        changed = [r for r in csv.DictReader(f) if float(r["surcharge_mln_per_t"]) != 0]
    assert {(r["source_id"], int(r["year"])) for r in changed} == {
        ("A", 2038), ("A", 2039), ("B", 2038), ("B", 2039)}
    for row in changed:
        assert float(row["shock_price_mln_per_t"]) == pytest.approx(7.75 if row["source_id"] == "A" else 11.125)


@pytest.mark.parametrize("pid", PLAN_IDS)
def test_base_reproduction_and_physical_invariance(experiment, root, case, base, assumptions, pid):
    out, report = experiment
    before, after = (load_result(out / pid / variant) for variant in ("before", "after"))
    reference = simulate(case, load_plan(root / "configs/plans" / f"{pid}.json", case), base, assumptions)
    published = load_result(root / "results/alternatives" / f"{pid}_BASE")
    assert before.kpi == pytest.approx(reference.kpi)
    assert before.kpi == pytest.approx(published.kpi)
    assert before.plan == after.plan == reference.plan
    assert before.months == after.months == reference.months
    assert before.years == after.years == reference.years
    assert before.investments == after.investments
    # Existing CASE_INPUT service rules are scoped to BASE, hence TEAM labels
    # them guideline. EXP-11 counts these as failures too; do not modify the core.
    for old, new in zip(before.check_matrix, after.check_matrix):
        assert {k: v for k, v in old.items() if k != "severity"} == {
            k: v for k, v in new.items() if k != "severity"}
        if old["severity"] != new["severity"]:
            assert old["rule_id"] in ("BASE_CRITICAL_SERVICE", "BASE_TOTAL_SERVICE")
            assert (old["severity"], new["severity"]) == ("hard", "guideline")
    assert after.kpi["hard_violations"] == after.kpi["guideline_violations"] == 0
    assert after.kpi["shortage_total_t"] == after.kpi["shortage_critical_t"] == 0
    assert after.kpi["min_service_level_total"] == after.kpi["min_service_level_critical"] == 1
    assert all(y.reserve_ok for y in after.years)
    row = next(r for r in report["comparison"] if r["plan_id"] == pid)
    assert row["max_reserve_gap_t_before"] == row["max_reserve_gap_t_after"] == 0
    assert row["min_reserve_slack_t_before"] == row["min_reserve_slack_t_after"]


@pytest.mark.parametrize("pid", PLAN_IDS)
def test_cost_delta_from_independent_contract_arithmetic(experiment, case, assumptions, pid):
    out, report = experiment
    before, after = (load_result(out / pid / variant) for variant in ("before", "after"))
    expected = {year: 0.0 for year in case.years}
    for old, new in zip(before.source_years, after.source_years):
        source = case.sources[old.source_id]
        affected = old.source_id in ("A", "B") and old.year in (2038, 2039) and old.period == "year"
        payable = max(old.ordered_t, source.take_or_pay_share * old.reserved_capacity_t * old.period_fraction) if old.period == "year" else old.ordered_t
        delta = payable * source.variable_cost_mln_per_t * (0.25 if affected else 0)
        assert new.procurement_mln - old.procurement_mln == pytest.approx(delta)
        assert new.price_mln_per_t == pytest.approx(source.variable_cost_mln_per_t * (1.25 if affected else 1))
        assert new.payable_volume_t == old.payable_volume_t
        assert new.actual_delivery_t == old.actual_delivery_t
        assert new.reservation_payment_mln == old.reservation_payment_mln
        if affected:
            expected[old.year] += delta
    for old, new in zip(before.finance, after.finance):
        assert new.procurement_mln - old.procurement_mln == pytest.approx(expected[old.year])
        for key in ("reservation_mln", "holding_mln", "fixed_opex_mln", "capex_mln"):
            assert getattr(old, key) == getattr(new, key)
    assert assumptions.discount_timing == "start"
    expected_pv = math.fsum(delta / (1 + assumptions.discount_rate_real) ** (year - assumptions.discount_t0_year)
                            for year, delta in expected.items())
    row = next(r for r in report["comparison"] if r["plan_id"] == pid)
    assert row["delta_pv_mln"] == pytest.approx(expected_pv)
    assert row["delta_total_mln"] == pytest.approx(math.fsum(expected.values()))


def test_exports_independent_recalculation_and_replay(experiment, tmp_path):
    out, report = experiment
    for pid in PLAN_IDS:
        for variant in ("before", "after"):
            folder = out / pid / variant
            assert cli_main(["verify", str(folder), "--case", str(out / "case")]) == 0
            assert recalc(folder, out / "case") == []
    repeat = tmp_path / "repeat"
    repeated, _ = run_experiment(repeat)
    assert repeated == report
    compare_saved(repeat, out)
    # The copied scenario and case are covered, not only newly computed KPIs.
    path = repeat / "case/supply_sources.csv"
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="output_sha256 mismatch"):
        verify_saved(repeat)


def test_published_artifacts_and_numbers(experiment, root):
    folder = root / "results/geopolitical_price_shock"
    verify_saved(folder)
    saved = json.loads((folder / "report.json").read_text(encoding="utf-8"))
    for old, new in zip(saved["runs"], experiment[1]["runs"]):
        assert old["plan_id"] == new["plan_id"]
        assert old["variant"] == new["variant"]
        assert old["kpi"] == pytest.approx(new["kpi"])


def test_reject_protected_output_and_self_comparison(root, tmp_path):
    for path in (root, root / "data/case", root / "configs/scenarios", root / "src", root / "results/alternatives"):
        with pytest.raises(ValueError):
            prepare_copy(path)
    with pytest.raises(SystemExit):
        main(["--out", str(tmp_path), "--compare", str(tmp_path)])

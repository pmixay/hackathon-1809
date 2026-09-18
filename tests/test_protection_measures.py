"""EXP-08: practical minima, real stock, contract-only controls and cost parity."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from run_protection_measures import analyze, early_zbo_plan, inventory_plan, reservation_plan, write_report
from provenance import sha256
from run_reverse_stress import failure_violations, shocked_scenario
from terraplan.engine import simulate
from terraplan.plan import load_plan, plan_from_dict


@pytest.fixture(scope="module")
def report():
    return analyze()


def test_practical_minimum_and_predecessors(report):
    assert report["selections"]["physical_stock"]["minimum"] == 8.6
    assert report["selections"]["early_zbo_plus_stock"]["minimum"] == 0.1
    for family in ("physical_stock", "early_zbo_plus_stock"):
        minimum = report["selections"][family]["minimum"]
        trials = [r for r in report["trials"] if r["family"] == family]
        assert len(trials) == round(minimum * 10) + 1
        assert trials[-1]["reference_pass"] and trials[-1]["target_pass"]
        assert all(not (r["reference_pass"] and r["target_pass"]) for r in trials[:-1])
        assert trials[-2]["target_first_rule"] == "RESERVE_45D"
    # ZBO option starts in 2036: moving it further back is not an admissible hedge.
    zbo = report["selections"]["early_zbo"]
    assert zbo["minimum"] is None and zbo["selected_value"] == 18
    trials = [r for r in report["trials"] if r["family"] == "early_zbo"]
    assert [r["value"] for r in trials] == list(range(19))
    assert all(r["reference_pass"] and not r["target_pass"] for r in trials)


def test_actual_extra_stock_and_order_dates(report, case, stress, assumptions):
    base = plan_from_dict(report["variants"]["without_measure"]["plan"])
    plan = plan_from_dict(report["variants"]["physical_stock"]["plan"])
    before = simulate(case, base, stress, assumptions)
    after = simulate(case, plan, stress, assumptions)
    extra_gross = plan.order("B", 2037).ordered_t - base.order("B", 2037).ordered_t
    assert extra_gross == pytest.approx(8.7048)
    for old, new in zip(before.years, after.years):
        if old.year >= 2038:
            assert new.opening_t - old.opening_t == pytest.approx(extra_gross * 0.988)
    assert not failure_violations(after)
    assert plan.investments == base.investments
    assert plan.opening_stock == base.opening_stock
    deliveries = [d for d in after.deliveries if d["source_id"] == "B" and d["year"] == 2037]
    for d in deliveries:
        assert d["lead_time_ok"]
        assert d["planned_t"] <= plan.reserved("B", 2037) / 12 + 1e-9
        if d["month"] >= 7:
            assert d["order_placement_month"] == f"2037-{d['month'] - 4:02d}"
        else:
            assert d["planned_t"] == pytest.approx(base.order("B", 2037).ordered_t / 12)


def test_reservation_never_becomes_physical_fuel(report, case, stress, assumptions):
    base = plan_from_dict(report["variants"]["without_measure"]["plan"])
    for d, s in ((0, 0), (0.01, 0.01), (0.03, 0.1)):
        sc = shocked_scenario(stress, case, d, s)
        before = simulate(case, base, sc, assumptions)
        # Include intermediate levels as well as the full capacity control.
        for extra in (1, 17, 80, None):
            plan = reservation_plan(base, case, extra)
            after = simulate(case, plan, sc, assumptions)
            assert plan.orders == base.orders
            assert after.months == before.months and after.years == before.years
            assert after.kpi["reservation_total_mln"] > before.kpi["reservation_total_mln"]
            assert after.kpi["procurement_total_mln"] == before.kpi["procurement_total_mln"]
    baseline_boundary = report["variants"]["without_measure"]["boundary"]
    for key in ("reservation_1t_per_year", "reservation_full"):
        assert report["variants"][key]["boundary"] == baseline_boundary
    assert report["selections"]["reservation_only"]["minimum"] is None


def test_zbo_saves_losses_without_double_counting_or_earlier_illegal_capex(report, case, stress, assumptions):
    original = plan_from_dict(report["variants"]["without_measure"]["plan"])
    plan = plan_from_dict(report["variants"]["early_zbo"]["plan"])
    assert plan.orders == original.orders and plan.reservations == original.reservations
    investment = next(i for i in plan.investments if i.investment_id == "ZBO")
    assert (investment.decision_year, investment.decision_month) == (2036, 1)
    before = simulate(case, original, stress, assumptions)
    after = simulate(case, plan, stress, assumptions)
    # Independent net benefit: 18 months of original inflow lose 3.3 pp less.
    saved = sum(m.throughput_t * (0.045 - 0.012) for m in before.months
                if m.year == 2036 or (m.year == 2037 and m.month <= 6))
    assert saved == pytest.approx(8.48183655)
    assert after.years[3].opening_t - before.years[3].opening_t == pytest.approx(saved)
    costs = report["variants"]["early_zbo"]["delta_components_mln"]
    assert costs["procurement_total_mln"] == 0
    assert costs["capex_total_mln"] == 0
    assert costs["fixed_opex_total_mln"] == pytest.approx(18)
    illegal = simulate(case, early_zbo_plan(original, 19), stress, assumptions)
    assert any(v.rule_id == "INVESTMENT_TIMING" for v in failure_violations(illegal))


def test_costs_and_new_frontiers_replay(report, case, stress, assumptions):
    base = report["variants"]["without_measure"]["reference"]["kpi"]
    for name, variant in report["variants"].items():
        plan = plan_from_dict(variant["plan"])
        k = variant["reference"]["kpi"]
        assert sum(variant["delta_components_mln"].values()) == pytest.approx(variant["delta_total_mln"])
        assert k["pv_cost_mln"] - base["pv_cost_mln"] == pytest.approx(variant["delta_pv_mln"])
        assert sum(f["pv_total_mln"] for f in variant["reference"]["finance"]) == pytest.approx(k["pv_cost_mln"])
        for b in variant["boundary"]:
            lo, hi = b["pass_radius"], b["fail_radius"]
            assert hi - lo <= 1e-12
            u, v = b["demand_direction"], b["isru_direction"]
            for radius, fails in ((lo, False), (hi, True)):
                res = simulate(case, plan, shocked_scenario(stress, case, u * radius, v * radius), assumptions)
                assert bool(failure_violations(res)) is fails
            assert (b["first_violation"]["rule_id"], b["first_violation"]["year"]) == ("RESERVE_45D", 2040)
        diagonal = next(b for b in variant["boundary"] if b["demand_direction"] == b["isru_direction"])
        if name in ("physical_stock", "early_zbo_plus_stock"):
            assert diagonal["pass_radius"] >= 0.01
            assert not variant["target"]["failures"]
        else:
            assert diagonal["fail_radius"] < 0.01
            assert variant["target"]["failures"]
    assert report["variants"]["early_zbo_plus_stock"]["delta_pv_mln"] < report["variants"]["physical_stock"]["delta_pv_mln"]


def test_inputs_unchanged_and_report_reproducible(report, root, case, tmp_path):
    original = load_plan(root / "configs/plans/P3_isru_zbo_adapted.json", case)
    assert original.to_dict() == report["variants"]["without_measure"]["plan"]
    for path, digest in report["input_sha256"].items():
        assert sha256(root / path) == digest
    # Replay the entire computation, not just the serialization of one result.
    assert analyze() == report
    for directory in (tmp_path / "a", tmp_path / "b"):
        write_report(report, directory)
    for path in (tmp_path / "a").iterdir():
        assert path.read_bytes() == (tmp_path / "b" / path.name).read_bytes()
    assert json.loads((tmp_path / "a/report.json").read_text(encoding="utf-8")) == json.loads(
        (tmp_path / "b/report.json").read_text(encoding="utf-8"))
    # Measure builders must not mutate the shared original plan.
    before = original.to_dict()
    inventory_plan(original, case, 8.6)
    reservation_plan(original, case)
    early_zbo_plan(original, 18)
    assert original.to_dict() == before


@pytest.mark.parametrize("target", [0, -0.01, 0.6, float("nan"), float("inf")])
def test_invalid_target(target):
    with pytest.raises(ValueError, match="target"):
        analyze(target)

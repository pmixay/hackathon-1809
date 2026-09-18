"""Exports must reproduce the displayed numbers and reopen as the same result."""
import csv
import json

from terraplan.compare import compare_results, write_comparison
from terraplan.engine import simulate
from terraplan.export import load_result, write_results
from terraplan.plan import load_plan, save_plan
from terraplan.planner import build_plan


def test_write_and_reload_results(tmp_path, case, base, stress, assumptions):
    plan = build_plan(case, base, dict(plan_id="exp", reservation_caps={"A": 190, "B": 110, "C": 130},
                                       investments=[dict(investment_id="EARTH_NEW", option_year=2035, option_month=1, decision_year=2035, decision_month=1)]), assumptions)
    res = simulate(case, plan, base, assumptions)
    out = write_results(res, tmp_path / "out")
    for name in ("yearly_balance.csv", "inventory_trace.csv", "source_schedule.csv", "financial_breakdown.csv", "constraint_checks.csv",
                 "kpi.csv", "assumptions.csv", "plan.json", "scenario.json", "result.json", "export_envelope.json", "run_manifest.json", "summary.md", "results.xlsx"):
        assert (out / name).exists(), name
    rows = list(csv.DictReader((out / "yearly_balance.csv").open(encoding="utf-8")))
    assert len(rows) == 6 and {r["scenario_id"] for r in rows} == {"BASE"}
    assert abs(float(rows[-1]["served_total_t"]) - res.years[-1].served_total_t) < 1e-6
    env = json.loads((out / "export_envelope.json").read_text(encoding="utf-8"))
    for key in ("scenario_id", "plan_id", "units", "assumptions_reference", "yearly_balance", "source_schedule", "inventory_trace",
                "financial_breakdown", "constraint_checks", "risk_register"):
        assert key in env
    reloaded = load_result(out)
    assert reloaded.kpi == res.kpi and len(reloaded.months) == 72
    # plan save / reopen round trip
    p = save_plan(plan, tmp_path / "plan.json")
    plan2 = load_plan(p, case)
    res2 = simulate(case, plan2, base, assumptions)
    assert res2.kpi == res.kpi
    # comparison on the common basis
    rs = simulate(case, plan, stress, assumptions)
    rows = compare_results(res, rs)
    write_comparison(rows, tmp_path / "cmp.csv", tmp_path / "cmp.md")
    assert (tmp_path / "cmp.csv").exists() and any(r["section"] == "violation" for r in rows)

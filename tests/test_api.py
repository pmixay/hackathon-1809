"""Программный интерфейс «словарь → словарь» (terraplan.api) — тот же расчётный путь, что у CLI и выгрузок."""
import json

import pytest

from terraplan import api


def test_run_plan_from_file_and_dict_agree(root):
    r1 = api.run_plan(root / "configs/plans/P3_isru_zbo.json", "BASE", case=root / "data/case",
                      assumptions=root / "configs/assumptions.yaml", scenarios_dir=root / "configs/scenarios")
    assert r1["ok"] and r1["feasible"] and r1["kpi"]["hard_violations"] == 0
    plan_dict = json.loads((root / "configs/plans/P3_isru_zbo.json").read_text(encoding="utf-8"))
    r2 = api.run_plan(plan_dict, "BASE", case=root / "data/case", assumptions=root / "configs/assumptions.yaml", scenarios_dir=root / "configs/scenarios")
    assert r2["kpi"] == r1["kpi"]
    assert r1["kpi"]["pv_cost_mln"] == pytest.approx(8639.227, abs=1e-3)


def test_run_plan_stress_reports_violations_with_year_value_reason(root):
    r = api.run_plan(root / "configs/plans/P3_isru_zbo.json", "MANDATORY_STRESS", case=root / "data/case",
                     assumptions=root / "configs/assumptions.yaml", scenarios_dir=root / "configs/scenarios")
    assert r["ok"] and not r["feasible"]
    v = [x for x in r["violations"] if x["rule_id"] == "RESERVE_45D"]
    assert {x["year"] for x in v} == {2038, 2039, 2040}
    assert all(x["actual"] is not None and x["limit"] is not None and x["message"] for x in v)


def test_run_plan_returns_structured_input_error(root):
    bad = {"plan_id": "p", "decisions": {"capacity_reservations": [{"source_id": "A", "year": 2035, "reserved_capacity_t": -1}],
                                         "supply_orders": [], "investments": [], "inventory_policy": {}}}
    r = api.run_plan(bad, "BASE", case=root / "data/case", assumptions=root / "configs/assumptions.yaml", scenarios_dir=root / "configs/scenarios")
    assert r["ok"] is False and r["error"]["code"] == "PLAN_INVALID" and "reserved_capacity_t" in r["error"]["message"]
    r = api.run_plan(root / "configs/plans/P3_isru_zbo.json", "NO_SUCH_SCENARIO", case=root / "data/case",
                     assumptions=root / "configs/assumptions.yaml", scenarios_dir=root / "configs/scenarios")
    assert r["ok"] is False and r["error"]["code"] == "SCENARIO_INVALID"


def test_overrides_and_export(root, tmp_path):
    r = api.run_plan(root / "configs/plans/P3_isru_zbo.json", "BASE", case=root / "data/case", assumptions=root / "configs/assumptions.yaml",
                     scenarios_dir=root / "configs/scenarios", overrides={"discount_rate_real": 0.0}, out_dir=tmp_path / "out", xlsx=False)
    assert r["ok"] and r["kpi"]["pv_cost_mln"] == pytest.approx(r["kpi"]["total_cost_mln"])
    assert (tmp_path / "out" / "summary.md").exists() and (tmp_path / "out" / "run_manifest.json").exists()
    cmp = api.compare_runs(r, tmp_path / "out")
    assert cmp["ok"] and all(row["delta"] in ("", 0, 0.0) for row in cmp["rows"] if row["section"] == "kpi")


def test_listings(root):
    scen = {s["scenario_id"]: s for s in api.list_scenarios(root / "configs/scenarios")}
    assert {"BASE", "MANDATORY_STRESS"} <= set(scen) and scen["MANDATORY_STRESS"]["status"] == "CASE_INPUT"
    plans = {p["plan_id"] for p in api.list_plans(root / "configs/plans")}
    assert "P3_isru_zbo" in plans
    cs = api.case_summary(root / "data/case")
    assert cs["ok"] and len(cs["sources"]) == 5 and cs["horizon"] == [2035, 2040]
    assert any(a["key"] == "discount_rate_real" for a in api.assumptions_table(root / "configs/assumptions.yaml"))

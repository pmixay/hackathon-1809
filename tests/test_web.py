"""UI acceptance: UI/engine parity, editable copies, export and HTTP boundary."""
import copy
import io
import json
import threading
import urllib.error
import urllib.request
import zipfile

import pytest

from terraplan.cli import main
from terraplan.engine import simulate
from terraplan.plan import plan_from_dict
from terraplan.web import Workspace, make_server


@pytest.fixture
def workspace(root):
    return Workspace(root)


@pytest.fixture
def payload(workspace):
    boot = workspace.bootstrap()
    return {"plan": boot["plans"]["P2z_earth_new_zbo"], "scenario": "base", "case_tables": boot["case_tables"], "case_notes": ""}


def test_engine_ui_export_and_reopen_parity(workspace, payload, case, assumptions, base, tmp_path):
    response = workspace.run(payload)
    expected = simulate(case, plan_from_dict(payload["plan"]), base, assumptions)
    assert response["result"]["kpi"] == expected.kpi
    _, archive, xlsx = workspace.runs[response["run_id"]]
    assert xlsx
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        saved = json.loads(z.read("workspace.json"))
        assert json.loads(z.read("export_envelope.json"))["kpi"] == expected.kpi
        assert "constraint_matrix.csv" in z.namelist()
        z.extractall(tmp_path)
    assert main(["verify", str(tmp_path), "--case", str(tmp_path / "case")]) == 0
    assert workspace.run(saved)["result"]["kpi"] == expected.kpi


def test_stress_compare_and_adapted_plan(workspace, payload):
    base = workspace.run(payload)
    payload["scenario"] = "mandatory_stress"
    stress = workspace.run(payload)
    assert not stress["result"]["feasible"]
    assert any(v["rule_id"] == "RESERVE_45D" and v["year"] == 2038 for v in stress["result"]["violations"])
    rows = workspace.comparison(base["run_id"], stress["run_id"])
    row = next(r for r in rows if r["metric"] == "shortage_total_t")
    assert row["delta"] == pytest.approx(stress["result"]["kpi"]["shortage_total_t"])
    payload["plan"] = workspace.bootstrap()["plans"]["P2z_earth_new_zbo_adapted"]
    assert workspace.run(payload)["result"]["feasible"]


def test_modified_contracts_preserve_inputs_and_stress(workspace, payload):
    before = copy.deepcopy(workspace.original)
    payload["case_tables"] = copy.deepcopy(before)
    payload["case_tables"]["supply_sources.csv"] = before["supply_sources.csv"].replace("6.2", "7.2")
    with pytest.raises(ValueError, match="case_notes"):
        workspace.run(payload)
    payload["case_notes"] = "TEAM_ASSUMPTION: A price 7.2 mln/t, sensitivity to +1 mln/t vs 6.2."
    response = workspace.run(payload)["result"]
    assert response["scenario_id"] == "TEAM_COPY_BASE"
    assert response["scenario"]["enforce_service_thresholds"] is True
    payload["scenario"] = "mandatory_stress"
    stress = workspace.run(payload)["result"]
    assert stress["scenario"]["loss_ceiling"]["enabled"]
    assert stress["years"][-1]["demand_total_t"] == pytest.approx(390 * 1.15)
    assert workspace.original == before
    assert Workspace(workspace.root).original == before
    payload["case_tables"]["constraints.csv"] += "\n"
    with pytest.raises(ValueError, match="constraints.csv"):
        workspace.run(payload)


def test_extensibility_and_workspace_roundtrip(workspace, payload):
    demo = workspace.bootstrap()["extension"]
    assert demo
    payload.update(demo)
    response = workspace.run(payload)
    result = response["result"]
    assert result["years"][-1]["year"] == 2041
    assert any(s["source_id"] == "X" and s["ordered_t"] > 0 for s in result["source_years"])
    assert result["feasible"]
    with zipfile.ZipFile(io.BytesIO(workspace.runs[response["run_id"]][1])) as z:
        saved = json.loads(z.read("workspace.json"))
    assert workspace.run(saved)["result"]["kpi"] == result["kpi"]


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -1])
def test_invalid_numeric_decisions(workspace, payload, value):
    payload["plan"]["decisions"]["supply_orders"][0]["ordered_t"] = value
    with pytest.raises(ValueError):
        workspace.run(payload)


def test_http_routes_errors_and_origin(root, payload):
    server = make_server(root, 0)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    url = f"http://127.0.0.1:{server.server_port}"
    try:
        assert b"TerraPlan" in urllib.request.urlopen(url).read()
        req = urllib.request.Request(url + "/api/run", json.dumps(payload).encode(), {"Content-Type": "application/json"})
        response = json.load(urllib.request.urlopen(req))
        assert response["result"]["feasible"]
        assert urllib.request.urlopen(url + f"/download/{response['run_id']}/results.zip").read().startswith(b"PK")
        for body in [b"{", b"[]", b'{"plan":{}}']:
            req = urllib.request.Request(url + "/api/run", body, {"Content-Type": "application/json"})
            with pytest.raises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(req)
            assert error.value.code == 400
            assert "error" in json.load(error.value)
        req = urllib.request.Request(url + "/api/run", b"{}", {"Content-Type": "application/json", "Origin": "https://example.invalid"})
        with pytest.raises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(req)
        assert error.value.code == 403
        with pytest.raises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(url + "/../../README.md")
        assert error.value.code == 404
    finally:
        server.shutdown()
        server.server_close()
        worker.join()


# ---- Бонусный блок: геополитический ценовой шок из интерфейса ----

def _shock(**over):
    base = {"enabled": True, "label": "Ограничение экспорта: надбавка к цене Earth-Core/Earth-Flex", "sources": ["A", "B"],
            "years": [2038, 2039], "change_pct": 25, "combine": "replace", "justification": "условный сценарий, величина совпадает с ценовой частью обязательного стресса"}
    base.update(over)
    return base


def test_price_shock_reproduces_exp11_and_restores_prices(workspace, payload, root, tmp_path):
    before = workspace.run(payload)
    payload["price_shock"] = _shock()
    after = workspace.run(payload)
    assert before["price_shock"] is None and before["result"]["scenario_id"] == "BASE"
    assert after["result"]["scenario_id"] == "TEAM_GEO_BASE"
    assert after["price_shock"]["multiplier"] == pytest.approx(1.25)
    # Те же числа, что в опубликованном EXP-11 (fixed BASE P2z, A/B +25 % в 2038–2039).
    published = json.loads((root / "results/geopolitical_price_shock/report.json").read_text(encoding="utf-8"))
    row = next(r for r in published["comparison"] if r["plan_id"] == "P2z_earth_new_zbo")
    assert before["result"]["kpi"]["pv_cost_mln"] == pytest.approx(row["pv_cost_mln_before"])
    assert after["result"]["kpi"]["pv_cost_mln"] == pytest.approx(row["pv_cost_mln_after"])
    assert after["result"]["kpi"]["shortage_total_t"] == before["result"]["kpi"]["shortage_total_t"] == 0
    overlay = {(r["source_id"], r["year"]): r for r in after["price_overlay"]}
    assert overlay[("A", 2038)]["effective_price_mln_per_t"] == pytest.approx(6.2 * 1.25)
    assert overlay[("A", 2040)]["effective_multiplier"] == 1.0 and overlay[("C", 2038)]["effective_multiplier"] == 1.0
    assert overlay[("A", 2038)]["origin"] == "геополитический шок"
    changes = after["result"]["scenario"]["changes"]
    assert any(c.get("block") == "geopolitical_price_shock" and c["years"] == [2038, 2039] for c in changes if isinstance(c, dict))
    _, archive, _ = workspace.runs[after["run_id"]]
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        assert "price_overlay.csv" in z.namelist()
        saved = json.loads(z.read("workspace.json"))
        z.extractall(tmp_path)
    assert saved["price_shock"]["change_pct"] == 25
    assert main(["verify", str(tmp_path), "--case", str(tmp_path / "case")]) == 0
    assert workspace.run(saved)["result"]["kpi"] == after["result"]["kpi"]
    # Восстановление исходных цен: выключенный шок = контрольный расчёт.
    saved["price_shock"]["enabled"] = False
    restored = workspace.run(saved)
    assert restored["result"]["scenario_id"] == "BASE"
    assert restored["result"]["kpi"] == before["result"]["kpi"]
    assert workspace.original == Workspace(workspace.root).original


def test_price_shock_combination_rule_with_mandatory_stress(workspace, payload):
    payload["scenario"] = "mandatory_stress"
    plain = workspace.run(payload)
    payload["price_shock"] = _shock(years=[2038])
    replaced = workspace.run(payload)
    overlay = {(r["source_id"], r["year"]): r for r in replaced["price_overlay"]}
    # Тот же эффект +25 % не начисляется повторно поверх ценовой части обязательного стресса.
    assert overlay[("A", 2038)]["scenario_multiplier"] == pytest.approx(1.25)
    assert overlay[("A", 2038)]["effective_multiplier"] == pytest.approx(1.25)
    assert overlay[("A", 2038)]["origin"] == "шок заменяет множитель сценария"
    assert replaced["result"]["kpi"]["pv_cost_mln"] == pytest.approx(plain["result"]["kpi"]["pv_cost_mln"])
    assert replaced["result"]["scenario_id"] == "TEAM_GEO_MANDATORY_STRESS"
    assert replaced["result"]["scenario"]["loss_ceiling"]["enabled"]
    payload["price_shock"] = _shock(years=[2038], combine="multiply")
    stacked = workspace.run(payload)
    overlay = {(r["source_id"], r["year"]): r for r in stacked["price_overlay"]}
    assert overlay[("A", 2038)]["effective_multiplier"] == pytest.approx(1.25 * 1.25)
    assert stacked["result"]["kpi"]["pv_cost_mln"] > plain["result"]["kpi"]["pv_cost_mln"]
    # Физический баланс от цен не зависит: дефицит стресса тот же.
    assert stacked["result"]["kpi"]["shortage_total_t"] == pytest.approx(plain["result"]["kpi"]["shortage_total_t"])


@pytest.mark.parametrize("bad,field", [
    ({"sources": ["Z"]}, "price_shock.sources"), ({"sources": []}, "price_shock.sources"),
    ({"years": [2041]}, "price_shock.years"), ({"change_pct": None}, "price_shock.change_pct"),
    ({"change_pct": -100}, "price_shock.change_pct"), ({"combine": "add"}, "price_shock.combine"), ({"label": " "}, "price_shock.label"),
])
def test_price_shock_invalid_input_names_the_field(workspace, payload, bad, field):
    payload["price_shock"] = _shock(**bad)
    with pytest.raises(ValueError, match=field):
        workspace.run(payload)

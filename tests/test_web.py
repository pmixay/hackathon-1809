"""R4 acceptance: UI/engine parity, editable copies, export and HTTP boundary."""
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
    return {"plan": boot["plans"]["P3_isru_zbo"], "scenario": "base", "case_tables": boot["case_tables"], "case_notes": ""}


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
    payload["plan"] = workspace.bootstrap()["plans"]["P3_isru_zbo_adapted"]
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

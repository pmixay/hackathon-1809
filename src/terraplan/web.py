"""Offline, loopback-only operator UI. All calculations use the existing engine."""
from __future__ import annotations

import csv
import io
import json
import math
import tempfile
import uuid
import zipfile
from collections import OrderedDict
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from .assumptions import load_assumptions
from .case import load_case
from .compare import compare_results
from .engine import result_to_dict, simulate
from .export import write_results
from .plan import plan_from_dict
from .scenario import resolve_scenario

CASE_FILES = ("demand.csv", "supply_sources.csv", "storage_options.csv", "investment_options.csv", "constraints.csv")


def finite_tree(value, path="input"):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{path}: number must be finite")
    if isinstance(value, dict):
        for key, item in value.items():
            finite_tree(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            finite_tree(item, f"{path}[{index}]")


def json_safe(value):
    """The engine can report infinite cost/tonne for a zero-service plan."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    return value


class Workspace:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.runs = OrderedDict()
        self.original = {name: (self.root / "data/case" / name).read_text(encoding="utf-8") for name in CASE_FILES}

    def bootstrap(self):
        plans = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted((self.root / "configs/plans").glob("*.json"))}
        scenarios = {}
        for path in sorted((self.root / "configs/scenarios").glob("*.yaml")):
            sc = resolve_scenario(str(path))
            scenarios[path.stem] = {"id": sc.scenario_id, "label": sc.label}
        extended = self.root / "results/extensibility"
        demo = None
        if (extended / "run/plan.json").exists():
            demo = {"plan": json.loads((extended / "run/plan.json").read_text(encoding="utf-8")),
                    "case_tables": {name: (extended / "case_copy" / name).read_text(encoding="utf-8") for name in CASE_FILES},
                    "case_notes": "TEAM_ASSUMPTION: Source-X 60 t/year, price 5.5 mln/t, reservation 0.2, TOP 30%, lead 3 months, available 2039. Demand 2041: 450/290 t total/critical, low 360, high 562.5. Constraints unchanged. See experiments/run_extensibility.py."}
        return {"plans": plans, "scenarios": scenarios, "case_tables": self.original, "extension": demo}

    def run(self, payload):
        finite_tree(payload)
        if not isinstance(payload, dict):
            raise ValueError("request must be a JSON object")
        scenario_key = payload.get("scenario", "base")
        if scenario_key not in self.bootstrap()["scenarios"]:
            raise ValueError("scenario: select one of the configured scenarios")
        tables = payload.get("case_tables", self.original)
        if not isinstance(tables, dict) or set(tables) != set(CASE_FILES):
            raise ValueError("case_tables: all five CASE_INPUT CSV tables are required")
        modified = tables != self.original
        notes = payload.get("case_notes", "")
        if modified and (not isinstance(notes, str) or not notes.strip()):
            raise ValueError("case_notes: describe and justify changes as TEAM_ASSUMPTION")
        if tables["constraints.csv"] != self.original["constraints.csv"]:
            raise ValueError("constraints.csv: organizer constraints must remain unchanged")
        plan = plan_from_dict(payload["plan"])
        with tempfile.TemporaryDirectory(prefix="terraplan-ui-") as temp:
            directory = Path(temp)
            case_dir = directory / "case"
            case_dir.mkdir()
            for name, content in tables.items():
                if not isinstance(content, str):
                    raise ValueError(f"{name}: expected CSV text")
                for row in csv.DictReader(io.StringIO(content)):
                    for field, raw in row.items():
                        try:
                            number = float(raw)
                        except (ValueError, TypeError):
                            continue
                        if not math.isfinite(number):
                            raise ValueError(f"{name}.{field}: number must be finite")
                (case_dir / name).write_text(content, encoding="utf-8")
            case = load_case(case_dir)
            scenario = resolve_scenario(str(self.root / "configs/scenarios" / f"{scenario_key}.yaml"))
            if modified:
                scenario.scenario_id = f"TEAM_COPY_{scenario.scenario_id}"
                scenario.status = "TEAM_ASSUMPTION"
                # Preserve BASE hard service checks even under a research label.
                scenario.enforce_service_thresholds = scenario_key == "base" or scenario.service_thresholds_hard
                scenario.changes.append(notes)
            result = simulate(case, plan, scenario, load_assumptions(self.root / "configs/assumptions.yaml"))
            out = directory / "export"
            write_results(result, out)
            (out / "case").mkdir()
            for name, content in tables.items():
                (out / "case" / name).write_text(content, encoding="utf-8")
            bundle = {"format": "terraplan-workspace-v1", "plan": result.plan, "scenario": scenario_key,
                      "case_tables": tables, "case_notes": notes}
            (out / "workspace.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
            manifest_path = out / "run_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest.update(case_dir="case", case_dir_absolute_at_run="", ui_case_notes=notes)
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
            (out / "REOPEN.txt").write_text("Open workspace.json in the TerraPlan UI to restore the plan and data.\nAfter extracting this archive, verify with:\npython -m terraplan verify <export-directory> --case <export-directory>/case\n", encoding="utf-8")
            archive = io.BytesIO()
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
                for path in sorted(out.rglob("*")):
                    if path.is_file():
                        z.write(path, path.relative_to(out).as_posix())
            xlsx = (out / "results.xlsx").read_bytes() if (out / "results.xlsx").exists() else None
        run_id = uuid.uuid4().hex
        self.runs[run_id] = (result, archive.getvalue(), xlsx)
        while len(self.runs) > 12:
            self.runs.popitem(last=False)
        return {"run_id": run_id, "result": json_safe(result_to_dict(result)), "xlsx_available": xlsx is not None}

    def comparison(self, a, b):
        if a not in self.runs or b not in self.runs:
            raise ValueError("Run expired. Recalculate both comparison plans (last 12 runs retained).")
        return compare_results(self.runs[a][0], self.runs[b][0])


def make_server(root, port=8765):
    workspace = Workspace(root)
    assets = Path(__file__).with_name("static")

    class Handler(BaseHTTPRequestHandler):
        def reply(self, status, body, kind="application/json; charset=utf-8", filename=None):
            if not isinstance(body, bytes):
                body = json.dumps(json_safe(body), ensure_ascii=False, allow_nan=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", kind)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; object-src 'none'; frame-ancestors 'none'")
            if filename:
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
            self.end_headers()
            self.wfile.write(body)

        def local_request(self):
            expected = {f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"}
            if self.headers.get("Host") not in expected:
                self.reply(403, {"error": "Use the local TerraPlan URL."})
                return False
            origin = self.headers.get("Origin")
            if origin and origin not in {f"http://{host}" for host in expected}:
                self.reply(403, {"error": "Cross-origin requests are not allowed."})
                return False
            return True

        def do_GET(self):
            if not self.local_request():
                return
            path = urlsplit(self.path).path
            if path == "/api/bootstrap":
                self.reply(200, workspace.bootstrap())
            elif path in ("/", "/app.js", "/style.css"):
                name, kind = {"/": ("index.html", "text/html"), "/app.js": ("app.js", "text/javascript"), "/style.css": ("style.css", "text/css")}[path]
                self.reply(200, (assets / name).read_bytes(), kind + "; charset=utf-8")
            elif path.startswith("/download/"):
                parts = path.split("/")
                if len(parts) != 4 or parts[2] not in workspace.runs or parts[3] not in ("results.zip", "results.xlsx"):
                    self.reply(404, {"error": "Download expired or missing. Recalculate the plan."})
                    return
                _, archive, xlsx = workspace.runs[parts[2]]
                data = archive if parts[3].endswith("zip") else xlsx
                if data is None:
                    self.reply(404, {"error": "Install openpyxl for XLSX export. CSV is in the ZIP."})
                else:
                    self.reply(200, data, "application/zip" if parts[3].endswith("zip") else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", parts[3])
            else:
                self.reply(404, {"error": "Not found"})

        def do_POST(self):
            if not self.local_request():
                return
            try:
                if self.headers.get_content_type() != "application/json":
                    raise ValueError("Content-Type must be application/json")
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 2_000_000:
                    raise ValueError("Request must contain JSON and be at most 2 MB")
                body = json.loads(self.rfile.read(length))
                if self.path == "/api/run":
                    self.reply(200, workspace.run(body))
                elif self.path == "/api/compare":
                    rows = workspace.comparison(body["a"], body["b"])
                    buffer = io.StringIO(newline="")
                    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]))
                    writer.writeheader()
                    writer.writerows(rows)
                    self.reply(200, {"rows": rows, "csv": buffer.getvalue()})
                else:
                    self.reply(404, {"error": "Not found"})
            except (ValueError, TypeError, KeyError, AttributeError, OverflowError) as exc:
                self.reply(400, {"error": f"Invalid input: {exc}"})

    return HTTPServer(("127.0.0.1", port), Handler)


def serve(root=".", port=8765):
    server = make_server(root, port)
    print(f"TerraPlan operator UI: http://127.0.0.1:{server.server_port} (Ctrl+C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

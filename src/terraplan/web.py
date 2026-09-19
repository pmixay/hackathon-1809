"""Локальный интерфейс оператора (только loopback). Все расчёты выполняет существующий движок."""
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
SHOCK_COMBINE_RULES = ("replace", "multiply")
EXTENSION_NOTE = ("TEAM_ASSUMPTION: Source-X — 60 т/год, цена 5,5 млн/т, резерв 0,2 млн за т/год, take-or-pay 30 %, "
                  "срок поставки 3 месяца, доступен с 2039 года. Спрос 2041: 450/290 т (общий/критический), низкий 360, "
                  "высокий 562,5. Ограничения задания не изменены; это исследовательский сценарий на копии данных.")


def finite_tree(value, path="ввод"):
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{path}: число должно быть конечным")
    if isinstance(value, dict):
        for key, item in value.items():
            finite_tree(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            finite_tree(item, f"{path}[{index}]")


def json_safe(value):
    """Движок может вернуть бесконечную стоимость тонны для плана с нулевым обслуживанием."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [json_safe(v) for v in value]
    return value


def normalize_price_shock(raw, case):
    """Проверка описания геополитического ценового шока (бонусный блок).

    Возвращает None, если блок не задан или выключен. Иначе — словарь с проверенными полями:
    событие, каналы, годы, изменение цены в процентах, правило сочетания со сценарием, обоснование.
    Шок применяется как явно обозначенный сценарный коэффициент к агрегированной цене канала
    (доставка в узел включена): разбивка цены на составляющие организатором не задана.
    """
    if raw in (None, False):
        return None
    if not isinstance(raw, dict):
        raise ValueError("price_shock: ожидается объект с описанием ценового шока")
    if not raw.get("enabled", True):
        return None
    label = raw.get("label")
    if not isinstance(label, str) or not label.strip():
        raise ValueError("price_shock.label: назовите сценарное событие (например, «ограничение экспорта, страховая надбавка»)")
    sources = raw.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("price_shock.sources: выберите хотя бы один затронутый канал")
    unknown = [s for s in sources if s not in case.sources]
    if unknown:
        raise ValueError(f"price_shock.sources: неизвестные каналы {unknown}; доступны {list(case.sources)}")
    years = raw.get("years")
    if not isinstance(years, list) or not years:
        raise ValueError("price_shock.years: укажите период действия (годы горизонта)")
    try:
        years = sorted({int(y) for y in years})
    except (TypeError, ValueError):
        raise ValueError("price_shock.years: годы должны быть целыми числами") from None
    outside = [y for y in years if y not in case.years]
    if outside:
        raise ValueError(f"price_shock.years: годы {outside} вне горизонта {case.years[0]}–{case.years[-1]}")
    pct = raw.get("change_pct")
    if not isinstance(pct, (int, float)) or isinstance(pct, bool) or not math.isfinite(pct):
        raise ValueError("price_shock.change_pct: укажите величину изменения цены в процентах (например, 25 или −10)")
    if pct <= -100:
        raise ValueError("price_shock.change_pct: снижение цены не может быть 100 % и более")
    combine = raw.get("combine", "replace")
    if combine not in SHOCK_COMBINE_RULES:
        raise ValueError("price_shock.combine: правило сочетания должно быть replace (заменяет множитель сценария) или multiply (начисляется поверх)")
    justification = raw.get("justification", "")
    if not isinstance(justification, str):
        raise ValueError("price_shock.justification: ожидается текст")
    return dict(label=label.strip(), sources=[str(s) for s in dict.fromkeys(sources)], years=years, change_pct=float(pct),
                multiplier=1.0 + float(pct) / 100.0, combine=combine, justification=justification.strip())


def apply_price_shock(scenario, shock, case):
    """Наложить шок на копию сценария и вернуть таблицу эффективных цен (год × канал)."""
    factor = shock["multiplier"]
    table, overlay = {}, []
    for sid, src in case.sources.items():
        table[sid] = {y: scenario.price_mult(src, y) for y in case.years}
    for sid in shock["sources"]:
        for y in shock["years"]:
            table[sid][y] = factor if shock["combine"] == "replace" else table[sid][y] * factor
    for y in case.years:
        for sid, src in case.sources.items():
            scenario_m = scenario.price_mult(src, y)
            effective_m = table[sid][y]
            hit = sid in shock["sources"] and y in shock["years"]
            if hit and shock["combine"] == "replace" and abs(scenario_m - 1.0) > 1e-12:
                origin = "шок заменяет множитель сценария"
            elif hit and shock["combine"] == "multiply" and abs(scenario_m - 1.0) > 1e-12:
                origin = "шок поверх множителя сценария"
            elif hit:
                origin = "геополитический шок"
            elif abs(scenario_m - 1.0) > 1e-12:
                origin = "множитель сценария"
            else:
                origin = "исходная цена"
            overlay.append(dict(year=y, source_id=sid, source_name=src.name, base_price_mln_per_t=src.variable_cost_mln_per_t,
                                scenario_multiplier=scenario_m, shock_multiplier=factor if hit else 1.0,
                                effective_multiplier=effective_m, effective_price_mln_per_t=src.variable_cost_mln_per_t * effective_m,
                                origin=origin))
    scenario.variable_price_multiplier = {sid: dict(row) for sid, row in table.items()}
    scenario.changes.append(dict(
        status="TEAM_ASSUMPTION", block="geopolitical_price_shock", parameter="variable_price_multiplier",
        event=shock["label"], sources=shock["sources"], years=shock["years"], change_pct=shock["change_pct"],
        multiplier=factor, combine=shock["combine"],
        combination_rule=("на затронутых канал-годах множитель шока заменяет множитель сценария: один и тот же ценовой эффект не начисляется повторно"
                          if shock["combine"] == "replace" else
                          "множитель шока перемножается с множителем сценария: оператор явно заявил, что это иной ценовой эффект"),
        price_component="агрегированная переменная цена канала с доставкой в узел; разбивка на составляющие не задана организатором",
        restore="выключите шок и пересчитайте — исходные цены восстанавливаются", justification=shock["justification"]))
    return overlay


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
                    "case_notes": EXTENSION_NOTE}
        return {"plans": plans, "scenarios": scenarios, "case_tables": self.original, "extension": demo}

    def run(self, payload):
        finite_tree(payload)
        if not isinstance(payload, dict):
            raise ValueError("запрос должен быть JSON-объектом")
        scenario_key = payload.get("scenario", "base")
        if scenario_key not in self.bootstrap()["scenarios"]:
            raise ValueError("scenario: выберите один из настроенных сценариев")
        tables = payload.get("case_tables", self.original)
        if not isinstance(tables, dict) or set(tables) != set(CASE_FILES):
            raise ValueError("case_tables: нужны все пять таблиц исходных данных (CASE_INPUT)")
        modified = tables != self.original
        notes = payload.get("case_notes", "")
        if modified and (not isinstance(notes, str) or not notes.strip()):
            raise ValueError("case_notes: опишите и обоснуйте изменения данных как TEAM_ASSUMPTION (смысл, единицы, диапазон)")
        if tables["constraints.csv"] != self.original["constraints.csv"]:
            raise ValueError("constraints.csv: ограничения организатора должны оставаться неизменными")
        if "plan" not in payload:
            raise ValueError("plan: в запросе нет плана")
        plan = plan_from_dict(payload["plan"])
        with tempfile.TemporaryDirectory(prefix="terraplan-ui-") as temp:
            directory = Path(temp)
            case_dir = directory / "case"
            case_dir.mkdir()
            for name, content in tables.items():
                if not isinstance(content, str):
                    raise ValueError(f"{name}: ожидается текст CSV")
                for row in csv.DictReader(io.StringIO(content)):
                    for field, raw in row.items():
                        try:
                            number = float(raw)
                        except (ValueError, TypeError):
                            continue
                        if not math.isfinite(number):
                            raise ValueError(f"{name}.{field}: число должно быть конечным")
                (case_dir / name).write_text(content, encoding="utf-8")
            case = load_case(case_dir)
            scenario = resolve_scenario(str(self.root / "configs/scenarios" / f"{scenario_key}.yaml"))
            shock = normalize_price_shock(payload.get("price_shock"), case)
            tags = (["GEO"] if shock else []) + (["COPY"] if modified else [])
            if tags:
                scenario.scenario_id = "TEAM_" + "_".join(tags) + "_" + scenario.scenario_id
                scenario.status = "TEAM_ASSUMPTION"
                # Жёсткие проверки сервиса BASE сохраняются и под исследовательской меткой.
                scenario.enforce_service_thresholds = scenario_key == "base" or scenario.service_thresholds_hard
            if modified:
                scenario.changes.append(notes)
            overlay = apply_price_shock(scenario, shock, case) if shock else None
            result = simulate(case, plan, scenario, load_assumptions(self.root / "configs/assumptions.yaml"))
            out = directory / "export"
            write_results(result, out)
            (out / "case").mkdir()
            for name, content in tables.items():
                (out / "case" / name).write_text(content, encoding="utf-8")
            if overlay:
                with (out / "price_overlay.csv").open("w", encoding="utf-8", newline="") as f:
                    writer = csv.DictWriter(f, fieldnames=list(overlay[0]))
                    writer.writeheader()
                    writer.writerows(overlay)
            bundle = {"format": "terraplan-workspace-v1", "plan": result.plan, "scenario": scenario_key,
                      "case_tables": tables, "case_notes": notes, "price_shock": payload.get("price_shock")}
            (out / "workspace.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
            manifest_path = out / "run_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest.update(case_dir="case", case_dir_absolute_at_run="", ui_case_notes=notes, ui_price_shock=shock)
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
            (out / "REOPEN.txt").write_text(
                "Файл workspace.json открывается в интерфейсе TerraPlan (кнопка «Открыть JSON») и восстанавливает план, "
                "сценарий, копию данных и настройки ценового шока.\nПроверка выгрузки после распаковки архива:\n"
                "python -m terraplan verify <каталог-архива> --case <каталог-архива>/case\n", encoding="utf-8")
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
        return {"run_id": run_id, "result": json_safe(result_to_dict(result)), "xlsx_available": xlsx is not None,
                "price_shock": shock, "price_overlay": overlay}

    def comparison(self, a, b):
        if a not in self.runs or b not in self.runs:
            raise ValueError("Расчёт устарел: пересчитайте оба сравниваемых плана (хранятся последние 12 расчётов).")
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
                self.reply(403, {"error": "Откройте интерфейс по локальному адресу TerraPlan."})
                return False
            origin = self.headers.get("Origin")
            if origin and origin not in {f"http://{host}" for host in expected}:
                self.reply(403, {"error": "Запросы с других сайтов не допускаются."})
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
                    self.reply(404, {"error": "Выгрузка устарела или отсутствует. Пересчитайте план."})
                    return
                _, archive, xlsx = workspace.runs[parts[2]]
                data = archive if parts[3].endswith("zip") else xlsx
                if data is None:
                    self.reply(404, {"error": "Для выгрузки XLSX установите пакет openpyxl. CSV есть в ZIP-архиве."})
                else:
                    self.reply(200, data, "application/zip" if parts[3].endswith("zip") else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", parts[3])
            else:
                self.reply(404, {"error": "Страница не найдена"})

        def do_POST(self):
            if not self.local_request():
                return
            try:
                if self.headers.get_content_type() != "application/json":
                    raise ValueError("ожидается Content-Type application/json")
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 2_000_000:
                    raise ValueError("запрос должен содержать JSON размером не более 2 МБ")
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
                    self.reply(404, {"error": "Страница не найдена"})
            except (ValueError, TypeError, KeyError, AttributeError, OverflowError) as exc:
                self.reply(400, {"error": f"Ошибочный ввод: {exc}"})

    return HTTPServer(("127.0.0.1", port), Handler)


def serve(root=".", port=8765):
    server = make_server(root, port)
    print(f"Интерфейс оператора TerraPlan: http://127.0.0.1:{server.server_port} (остановка — Ctrl+C)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

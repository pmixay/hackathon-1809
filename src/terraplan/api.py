"""Программный интерфейс «словарь → словарь» для интерфейса оператора, ноутбуков и внешних вызовов.

Тот же расчётный путь, что у CLI и выгрузок: `simulate()`. Ошибки ввода не выбрасываются наружу, а возвращаются
структурой в духе формата организатора (§26 справочного репозитория): код, тип, сообщение с файлом/полем/значением.

    from terraplan.api import run_plan
    r = run_plan("configs/plans/P3_isru_zbo.json", "MANDATORY_STRESS")
    r["ok"], r["feasible"], r["kpi"]["pv_cost_mln"], r["violations"][0]["message"]
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

import yaml

from .assumptions import Assumptions, load_assumptions
from .case import Case, CaseError, load_case
from .compare import compare_results
from .engine import Result, result_to_dict, simulate
from .export import load_result, result_from_dict, write_results
from .plan import Plan, PlanError, load_plan, plan_from_dict, validate_plan
from .scenario import Scenario, ScenarioError, resolve_scenario, scenario_from_dict

ERROR_CODES = {PlanError: "PLAN_INVALID", CaseError: "CASE_INPUT_INVALID", ScenarioError: "SCENARIO_INVALID"}
INPUT_ERRORS = (PlanError, CaseError, ScenarioError)


def error_to_dict(exc: Exception) -> dict:
    """Структурированная ошибка ввода: код правила, тип исключения, сообщение (называет файл, поле и значение)."""
    code = next((c for t, c in ERROR_CODES.items() if isinstance(exc, t)), "INPUT_ERROR")
    return {"ok": False, "error": {"code": code, "type": type(exc).__name__, "message": str(exc)}}


def _case(case: Case | str | Path) -> Case:
    return case if isinstance(case, Case) else load_case(case)


def _plan(plan: Plan | dict | str | Path, case: Case) -> Plan:
    if isinstance(plan, Plan):
        validate_plan(plan, case)
        return plan
    if isinstance(plan, dict):
        p = plan_from_dict(plan)
        validate_plan(p, case)
        return p
    return load_plan(plan, case)


def _scenario(scenario: Scenario | dict | str | Path, scenarios_dir: str | Path) -> Scenario:
    if isinstance(scenario, Scenario):
        return scenario
    if isinstance(scenario, dict):
        return scenario_from_dict(scenario)
    return resolve_scenario(str(scenario), scenarios_dir)


def _assumptions(assumptions: Assumptions | dict | str | Path | None, overrides: Optional[dict]) -> Assumptions:
    if isinstance(assumptions, Assumptions):
        a = assumptions
    elif isinstance(assumptions, dict):
        a = Assumptions({k: (dict(v) if isinstance(v, dict) and "value" in v else dict(value=v, unit="", status="TEAM_ASSUMPTION", range=None, justification=""))
                         for k, v in assumptions.items()})
        base = load_assumptions(None)
        merged = base.to_dict(); merged.update(a.to_dict()); a = Assumptions(merged)
    else:
        a = load_assumptions(assumptions)
    return a.with_overrides(**overrides) if overrides else a


def run_plan(plan: Plan | dict | str | Path, scenario: Scenario | dict | str | Path = "BASE", case: Case | str | Path = "data/case",
             assumptions: Assumptions | dict | str | Path | None = "configs/assumptions.yaml", overrides: Optional[dict] = None,
             scenarios_dir: str | Path = "configs/scenarios", out_dir: str | Path | None = None, xlsx: bool = True) -> dict:
    """Рассчитать план в сценарии. Возвращает словарь результата (как result.json) с полем ok=True, либо {ok: False, error: {...}}.

    plan       — Plan, словарь в формате plan.schema.json или путь к JSON;
    scenario   — идентификатор (BASE / MANDATORY_STRESS / TEAM_*), путь к YAML, словарь или Scenario;
    overrides  — переопределения допущений, например {"discount_rate_real": 0.05};
    out_dir    — если задан, результаты выгружаются туда (CSV, XLSX, JSON, summary.md, run_manifest.json).
    """
    try:
        c = _case(case)
        p = _plan(plan, c)
        s = _scenario(scenario, scenarios_dir)
        a = _assumptions(assumptions, overrides)
        res = simulate(c, p, s, a)
    except INPUT_ERRORS as exc:
        return error_to_dict(exc)
    d = result_to_dict(res)
    d["ok"] = True
    if out_dir is not None:
        d["out_dir"] = str(write_results(res, out_dir, xlsx=xlsx))
    return d


def to_result(r: Result | dict | str | Path) -> Result:
    """Result из словаря run_plan(), из каталога результатов или как есть."""
    if isinstance(r, Result):
        return r
    if isinstance(r, dict):
        return result_from_dict({k: v for k, v in r.items() if k not in ("ok", "out_dir")})
    return load_result(r)


def compare_runs(a: Result | dict | str | Path, b: Result | dict | str | Path, label_a: str | None = None, label_b: str | None = None) -> dict:
    """Сравнение двух результатов на единой базе: {ok, rows: [{section, metric, year, a, b, delta, ...}]}."""
    try:
        rows = compare_results(to_result(a), to_result(b), label_a, label_b)
    except (KeyError, FileNotFoundError, ValueError) as exc:
        return {"ok": False, "error": {"code": "COMPARE_INPUT_INVALID", "type": type(exc).__name__, "message": str(exc)}}
    return {"ok": True, "rows": rows}


def list_scenarios(scenarios_dir: str | Path = "configs/scenarios") -> list[dict]:
    """Доступные сценарии: id, подпись, статус (CASE_INPUT / TEAM_ASSUMPTION), список изменений, файл."""
    out = []
    for p in sorted(Path(scenarios_dir).glob("*.yaml")):
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        out.append(dict(scenario_id=data.get("scenario_id", p.stem.upper()), label=data.get("label_ru") or data.get("label") or "",
                        status=data.get("status", "TEAM_ASSUMPTION"), changes=list(data.get("changes") or []), file=str(p)))
    return out


def list_plans(plans_dir: str | Path = "configs/plans") -> list[dict]:
    """Сохранённые планы: id, сценарий, описание, число решений, файл."""
    out = []
    for p in sorted(Path(plans_dir).glob("*.json")):
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        dec = data.get("decisions", {}) if isinstance(data, dict) else {}
        out.append(dict(plan_id=data.get("plan_id", p.stem), scenario_id=data.get("scenario_id", ""), description=data.get("description", ""),
                        orders=len(dec.get("supply_orders", []) or []), reservations=len(dec.get("capacity_reservations", []) or []),
                        investments=len(dec.get("investments", []) or []), file=str(p)))
    return out


def case_summary(case: Case | str | Path = "data/case") -> dict:
    """Данные кейса для отображения в интерфейсе: спрос, каналы (контрактные условия), хранилище, инвестиции, ограничения."""
    try:
        c = _case(case)
    except CaseError as exc:
        return error_to_dict(exc)
    from dataclasses import asdict
    return {"ok": True, "horizon": [c.first_year, c.last_year], "demand": [asdict(d) for d in c.demand],
            "sources": [asdict(s) for s in c.sources.values()], "storage": [asdict(s) for s in c.storage.values()],
            "investments": [asdict(i) for i in c.investments.values()], "constraints": [asdict(k) for k in c.constraints.values()],
            "files": dict(c.files)}


def assumptions_table(assumptions: str | Path | None = "configs/assumptions.yaml") -> list[dict]:
    """Реестр допущений TEAM_ASSUMPTION (ключ, значение, единица, статус, диапазон, обоснование)."""
    return load_assumptions(assumptions).table()


__all__ = ["run_plan", "compare_runs", "list_scenarios", "list_plans", "case_summary", "assumptions_table", "error_to_dict", "to_result"]

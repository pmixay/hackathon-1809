"""Exports: CSV set, JSON envelope (schemas/export.schema.json), XLSX workbook, run manifest.

Every number exported comes from the same Result object the UI shows; nothing is recomputed here.
"""
from __future__ import annotations

import csv
import hashlib
import json
import platform
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from . import __version__
from .engine import Result, result_to_dict


def _write_csv(path: Path, rows: Iterable[dict], fieldnames: list[str] | None = None) -> None:
    rows = list(rows)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = fieldnames or list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})


KPI_PRECISION = 6   # decimals: stated reproducibility precision of exported KPIs


def kpi_hash(kpi: dict) -> str:
    """SHA-256 of the KPI dict with floats rounded to KPI_PRECISION (stable across Python versions)."""
    rounded = {k: (round(v, KPI_PRECISION) if isinstance(v, float) and v == v else v) for k, v in kpi.items()}
    return hashlib.sha256(json.dumps(rounded, sort_keys=True).encode()).hexdigest()


def repo_relative(path: str | Path) -> str:
    """Path relative to the enclosing repo root (directory holding pyproject.toml), else as given. Portable manifests."""
    p = Path(path).resolve()
    for anc in [p] + list(p.parents):
        if (anc / "pyproject.toml").exists():
            return p.relative_to(anc).as_posix()
    return str(path)


def _sha256(path: str | Path) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return hashlib.sha256(p.read_bytes()).hexdigest()


def result_tables(res: Result) -> dict[str, list[dict]]:
    tag = {"scenario_id": res.scenario_id, "plan_id": res.plan_id}
    years = [dict(tag, **asdict(y)) for y in res.years]
    months = []
    for m in res.months:
        d = dict(tag, **{k: v for k, v in asdict(m).items() if k != "inflow_by_source"})
        for k, v in m.inflow_by_source.items():
            d[f"inflow_{k}_t"] = v
        months.append(d)
    src = [dict(tag, **asdict(s)) for s in res.source_years]
    fin = [dict(tag, **asdict(f)) for f in res.finance]
    checks = [dict(tag, **asdict(v)) for v in res.violations]
    kpi = [dict(tag, metric=k, value=v) for k, v in res.kpi.items()]
    inv = [dict(tag, **asdict(i)) for i in res.investments]
    assumptions = [dict(key=k, value=json.dumps(v.get("value"), ensure_ascii=False), unit=v.get("unit", ""), status=v.get("status", ""),
                        range=json.dumps(v.get("range"), ensure_ascii=False), justification=v.get("justification", "")) for k, v in res.assumptions.items()]
    matrix = [dict(tag, **m) for m in res.check_matrix]
    deliveries = [dict(tag, **d) for d in res.deliveries]
    return {"yearly_balance": years, "inventory_trace": months, "source_schedule": src, "financial_breakdown": fin,
            "constraint_checks": checks, "constraint_matrix": matrix, "delivery_schedule": deliveries, "kpi": kpi, "investments": inv, "assumptions": assumptions}


def export_envelope(res: Result, risk_register: list[dict] | None = None) -> dict:
    t = result_tables(res)
    return {
        "scenario_id": res.scenario_id, "plan_id": res.plan_id, "units": res.units,
        "assumptions_reference": {"file": "assumptions.csv", "entries": res.assumptions},
        "yearly_balance": t["yearly_balance"], "source_schedule": t["source_schedule"], "inventory_trace": t["inventory_trace"],
        "financial_breakdown": t["financial_breakdown"], "constraint_checks": t["constraint_checks"],
        "risk_register": risk_register or [], "kpi": res.kpi, "investments": t["investments"],
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "terraplan_version": __version__,
    }


def write_results(res: Result, out_dir: str | Path, xlsx: bool = True, risk_register: list[dict] | None = None) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    tables = result_tables(res)
    for name, rows in tables.items():
        _write_csv(out / f"{name}.csv", rows)
    (out / "plan.json").write_text(json.dumps(res.plan, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "scenario.json").write_text(json.dumps(res.scenario, ensure_ascii=False, indent=2), encoding="utf-8")
    (out / "result.json").write_text(json.dumps(result_to_dict(res), ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "export_envelope.json").write_text(json.dumps(export_envelope(res, risk_register), ensure_ascii=False, indent=1), encoding="utf-8")
    manifest = {
        "terraplan_version": __version__, "python": platform.python_version(), "plan_id": res.plan_id, "scenario_id": res.scenario_id,
        "case_dir": repo_relative(res.case_dir), "case_dir_absolute_at_run": str(Path(res.case_dir).resolve()), "case_file_sha256": {name: _sha256(Path(res.case_dir) / name) for name in
            ("demand.csv", "supply_sources.csv", "storage_options.csv", "investment_options.csv", "constraints.csv")},
        "plan_sha256": hashlib.sha256(json.dumps(res.plan, sort_keys=True).encode()).hexdigest(),
        "scenario_sha256": hashlib.sha256(json.dumps(res.scenario, sort_keys=True, default=str).encode()).hexdigest(),
        "assumptions_sha256": hashlib.sha256(json.dumps(res.assumptions, sort_keys=True, default=str).encode()).hexdigest(),
        "kpi_sha256": kpi_hash(res.kpi),
        "kpi_precision": KPI_PRECISION,
        "random_seed": None, "note": f"deterministic run; re-running with the same inputs reproduces kpi_sha256 (KPIs rounded to {KPI_PRECISION} decimals before hashing, "
                                     "which absorbs last-bit differences of float summation between Python versions)",
    }
    (out / "run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    _write_summary_md(res, out / "summary.md")
    if xlsx:
        try:
            _write_xlsx(tables, res, out / "results.xlsx")
        except ImportError:
            (out / "results.xlsx.SKIPPED.txt").write_text("openpyxl not installed; CSV files are the export", encoding="utf-8")
    return out


def _write_xlsx(tables: dict[str, list[dict]], res: Result, path: Path) -> None:
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "README"
    ws.append(["TerraPlan export", __version__])
    ws.append(["plan_id", res.plan_id])
    ws.append(["scenario_id", res.scenario_id])
    ws.append(["feasible", str(res.feasible)])
    for k, v in res.units.items():
        ws.append([f"unit:{k}", v])
    ws.append(["sheets", ", ".join(tables)])
    for name, rows in tables.items():
        w = wb.create_sheet(name[:31])
        if not rows:
            w.append(["(empty)"])
            continue
        fields = list(rows[0].keys())
        w.append(fields)
        for r in rows:
            w.append([r.get(k) for k in fields])
    wb.save(path)


def _write_summary_md(res: Result, path: Path) -> None:
    k = res.kpi
    lines = [f"# {res.plan_id} — {res.scenario_id} ({res.scenario_label})", "",
             f"Feasible: **{'YES' if res.feasible else 'NO'}** — hard violations: {k['hard_violations']}, guideline: {k['guideline_violations']}, warnings: {k['warnings']}", "",
             "| KPI | Value |", "|---|---:|"]
    for key in ("total_cost_mln", "pv_cost_mln", "cost_per_served_t_mln", "pv_cost_per_served_t_mln", "served_total_t", "demand_total_t",
                "shortage_total_t", "shortage_critical_t", "min_service_level_total", "min_service_level_critical", "losses_total_t",
                "capex_total_mln", "procurement_total_mln", "reservation_total_mln", "holding_total_mln", "fixed_opex_total_mln", "take_or_pay_idle_t"):
        lines.append(f"| {key} | {k[key]:,.3f} |")
    lines += ["", "## Yearly balance", "", "| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |",
              "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|"]
    for y in res.years:
        lines.append(f"| {y.year} | {y.demand_total_t:.1f} | {y.demand_critical_t:.1f} | {y.served_total_t:.1f} | {y.service_level_total:.3f} | {y.service_level_critical:.3f} | "
                     f"{y.shortage_total_t:.1f} | {y.throughput_t:.1f} | {y.losses_t:.2f} | {y.opening_t:.1f} | {y.closing_t:.1f} | {y.reserve_required_t:.1f} | {'yes' if y.reserve_ok else 'NO'} | {y.storage_mode_end} |")
    lines += ["", "## Finance (mln, constant 2035 prices)", "", "| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |", "|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for f in res.finance:
        lines.append(f"| {f.year} | {f.procurement_mln:.1f} | {f.reservation_mln:.1f} | {f.holding_mln:.1f} | {f.fixed_opex_mln:.1f} | {f.capex_mln:.1f} | {f.total_mln:.1f} | {f.pv_total_mln:.1f} |")
    lines += ["", "## Source schedule (t)", "", "| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |", "|---:|---|---:|---:|---:|---:|---:|---:|---:|"]
    for s in res.source_years:
        if s.period != "year" or (s.reserved_capacity_t <= 0 and s.ordered_t <= 0):
            continue
        lines.append(f"| {s.year} | {s.name} | {s.reserved_capacity_t:.1f} | {s.ordered_t:.1f} | {s.actual_delivery_t:.1f} | {s.price_mln_per_t:.2f} | {s.payable_volume_t:.1f} | {s.procurement_mln:.1f} | {s.reservation_payment_mln:.1f} |")
    lines += ["", "## Check matrix (every rule x year)", "", "| Rule | Year | Metric | Actual | Limit | Op | Result | Severity |", "|---|---:|---|---:|---:|---|:---:|---|"]
    for m in res.check_matrix:
        fa = lambda x: f"{x:.4f}" if isinstance(x, float) else str(x)
        lines.append(f"| {m['rule_id']} | {m['year']} | {m['metric']} | {fa(m['actual'])} | {fa(m['limit'])} | {m['operator']} | {'OK' if m['ok'] else 'VIOLATED'} | {m['severity']} |")
    lines += ["", "## Constraint checks", ""]
    if not res.violations:
        lines.append("No violations.")
    else:
        lines += ["| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |", "|---|---|---:|---:|---|---:|---:|---:|---|"]
        for v in res.violations:
            fmt = lambda x: "" if x is None else (f"{x:.3f}" if isinstance(x, float) else str(x))
            lines.append(f"| {v.rule_id} | {v.severity} | {fmt(v.year)} | {fmt(v.month)} | {v.source_id or ''} | {fmt(v.actual)} | {fmt(v.limit)} | {fmt(v.excess)} | {v.message} |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def result_from_dict(d: dict) -> Result:
    from .engine import FinanceYear, InvestmentRecord, MonthRecord, SourceYearRecord, Violation, YearRecord
    return Result(
        plan_id=d["plan_id"], scenario_id=d["scenario_id"], scenario_label=d.get("scenario_label", ""), case_dir=d.get("case_dir", ""),
        months=[MonthRecord(**m) for m in d["months"]], years=[YearRecord(**y) for y in d["years"]],
        source_years=[SourceYearRecord(**s) for s in d["source_years"]], finance=[FinanceYear(**f) for f in d["finance"]],
        investments=[InvestmentRecord(**i) for i in d["investments"]], violations=[Violation(**v) for v in d["violations"]],
        kpi=d["kpi"], assumptions=d["assumptions"], scenario=d["scenario"], plan=d["plan"], units=d.get("units", {}),
        check_matrix=d.get("check_matrix", []), deliveries=d.get("deliveries", []),
    )


def load_result(result_dir: str | Path) -> Result:
    p = Path(result_dir)
    f = p / "result.json" if p.is_dir() else p
    if not f.exists():
        raise FileNotFoundError(f"no result.json in {p}")
    return result_from_dict(json.loads(f.read_text(encoding="utf-8")))

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
        "random_seed": None, "note": f"детерминированный расчёт; повторный запуск с теми же входами воспроизводит kpi_sha256 (показатели округляются до {KPI_PRECISION} знаков "
                                     "перед хешированием, что поглощает различия последнего бита при суммировании float между версиями Python)",
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
    ws.append(["Выгрузка TerraPlan, версия", __version__])
    ws.append(["план (plan_id)", res.plan_id])
    ws.append(["сценарий (scenario_id)", res.scenario_id])
    ws.append(["план исполним", "да" if res.feasible else "нет"])
    ws.append(["жёстких нарушений / отклонений от ориентиров / предупреждений",
               f"{res.kpi['hard_violations']} / {res.kpi['guideline_violations']} / {res.kpi['warnings']}"])
    for k, v in res.units.items():
        ws.append([f"единица: {k}", v])
    ws.append(["периоды", f"{res.years[0].year}-01 … {res.years[-1].year}-12, шаг — календарный месяц; подготовительный период до {res.years[0].year}-01"])
    ws.append(["листы", ", ".join(tables)])
    ws.append(["yearly_balance", "годовой баланс: спрос, выдача, дефицит, уровни сервиса, поступление, потери, запасы, 45-дневный резерв"])
    ws.append(["inventory_trace", "помесячный материальный баланс и стоимость хранения"])
    ws.append(["source_schedule", "по источникам и годам: резерв, заказ, план/факт поставки, цена, оплачиваемый объём (take-or-pay), платежи"])
    ws.append(["financial_breakdown", "по годам: закупка, резервирование, хранение, постоянный OPEX, CAPEX, итого, PV, накопленный CAPEX"])
    ws.append(["constraint_checks", "нарушения: правило, строгость, год, месяц, источник, факт, лимит, превышение, сообщение"])
    ws.append(["constraint_matrix", "матрица проверок: каждое правило × год, включая выполненные"])
    ws.append(["delivery_schedule", "календарь поставок: месяц поставки, месяц размещения заказа, срок поставки, допустимость"])
    ws.append(["kpi", "итоговые показатели"])
    ws.append(["investments", "инвестиционные решения: даты опциона, реализации, ввода"])
    ws.append(["assumptions", "реестр допущений TEAM_ASSUMPTION: значение, единица, статус, диапазон, обоснование"])
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


KPI_LABELS = {
    "total_cost_mln": "Полные затраты, млн", "pv_cost_mln": "Приведённые затраты (PV), млн",
    "cost_per_served_t_mln": "Затраты на обслуженную тонну, млн/т", "pv_cost_per_served_t_mln": "PV затрат на обслуженную тонну, млн/т",
    "served_total_t": "Обслужено, т", "demand_total_t": "Спрос, т", "shortage_total_t": "Дефицит, т",
    "shortage_critical_t": "Дефицит критического спроса, т", "min_service_level_total": "Мин. уровень сервиса (общий)",
    "min_service_level_critical": "Мин. уровень сервиса (критический)", "losses_total_t": "Потери при хранении, т",
    "capex_total_mln": "CAPEX, млн", "procurement_total_mln": "Закупка, млн", "reservation_total_mln": "Резервирование мощности, млн",
    "holding_total_mln": "Хранение, млн", "fixed_opex_total_mln": "Постоянный OPEX, млн",
    "take_or_pay_idle_t": "Оплачено по take-or-pay сверх заказа, т",
    "take_or_pay_topup_mln": "Премия take-or-pay (оплата незаказанного объёма), млн",
}
SEVERITY_RU = {"hard": "жёсткое", "guideline": "ориентир", "warning": "предупреждение"}


def _write_summary_md(res: Result, path: Path) -> None:
    k = res.kpi
    lines = [f"# {res.plan_id} — {res.scenario_id} ({res.scenario_label})", "",
             f"План исполним: **{'ДА' if res.feasible else 'НЕТ'}** — жёстких нарушений: {k['hard_violations']}, "
             f"отклонений от ориентиров: {k['guideline_violations']}, предупреждений: {k['warnings']}", "",
             f"Единицы: топливо — т; деньги — млн у.е. в постоянных ценах 2035 г.; шаг расчёта — календарный месяц; "
             f"ставка дисконтирования r = {k['discount_rate_real']:.0%} (TEAM_ASSUMPTION, одинакова для всех альтернатив). "
             "Те же числа — в CSV/XLSX/JSON этого каталога; календарь заказов и поставок — `delivery_schedule.csv`; "
             "реестр допущений — `assumptions.csv`.", "",
             "## Итоговые показатели", "", "| Показатель | Ключ | Значение |", "|---|---|---:|"]
    for key in ("total_cost_mln", "pv_cost_mln", "cost_per_served_t_mln", "pv_cost_per_served_t_mln", "served_total_t", "demand_total_t",
                "shortage_total_t", "shortage_critical_t", "min_service_level_total", "min_service_level_critical", "losses_total_t",
                "capex_total_mln", "procurement_total_mln", "reservation_total_mln", "holding_total_mln", "fixed_opex_total_mln", "take_or_pay_idle_t", "take_or_pay_topup_mln"):
        lines.append(f"| {KPI_LABELS.get(key, key)} | `{key}` | {k[key]:,.3f} |")
    lines += ["", "## Годовой баланс (т)", "",
              "| Год | Спрос | в т.ч. критич. | Обслужено | УС общий | УС критич. | Дефицит | Поступление (факт) | Потери | Запас на начало | Запас на конец | R45 | Резерв на начало года | Хранилище |",
              "|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|"]
    for y in res.years:
        lines.append(f"| {y.year} | {y.demand_total_t:.1f} | {y.demand_critical_t:.1f} | {y.served_total_t:.1f} | {y.service_level_total:.3f} | {y.service_level_critical:.3f} | "
                     f"{y.shortage_total_t:.1f} | {y.throughput_t:.1f} | {y.losses_t:.2f} | {y.opening_t:.1f} | {y.closing_t:.1f} | {y.reserve_required_t:.1f} | "
                     f"{'выполнен' if y.reserve_ok else 'НЕ ВЫПОЛНЕН'} | {y.storage_mode_end} |")
    lines += ["", "УС — уровень сервиса (обслужено / спрос); R45 — 45-дневный резерв `D_y × 45 / 365`, проверяется по физическому запасу на начало года.", "",
              "## Финансы (млн у.е., постоянные цены 2035 г.)", "",
              "| Год | Закупка | в т.ч. премия TOP | Резервирование | Хранение | Пост. OPEX | CAPEX | Итого | PV |", "|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for f in res.finance:
        lines.append(f"| {f.year} | {f.procurement_mln:.1f} | {f.take_or_pay_topup_mln:.1f} | {f.reservation_mln:.1f} | {f.holding_mln:.1f} | {f.fixed_opex_mln:.1f} | {f.capex_mln:.1f} | {f.total_mln:.1f} | {f.pv_total_mln:.1f} |")
    lines += ["", "«Премия TOP» — часть строки «Закупка», оплаченная за объём сверх заказанного по условию take-or-pay; "
              "это разложение платежа, а не дополнительный платёж."]
    if res.investments:
        lines += ["", "## Инвестиции", "", "| Инвестиция | Плата за опцион, млн | Дата опциона | Реализация / CAPEX, млн | Дата решения | Ввод в строй | Пост. OPEX, млн/год | Примечание |",
                  "|---|---:|---|---:|---|---|---:|---|"]
        for i in res.investments:
            lines.append(f"| {i.name} ({i.investment_id}) | {i.option_fee_mln:.0f} | {i.option_date or '—'} | {i.exercise_cost_mln:.0f} | {i.exercise_date} | "
                         f"{i.commissioning_date or '—'} | {i.fixed_opex_mln_per_year:.0f} | {i.note} |")
    lines += ["", "## График по источникам (т)", "",
              "| Год | Источник | Резерв, т/год | Заказано | Поставлено (факт) | Цена, млн/т | Оплачиваемый объём | Закупка, млн | в т.ч. премия TOP, млн | Резервирование, млн |",
              "|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for s in res.source_years:
        if s.period != "year" or (s.reserved_capacity_t <= 0 and s.ordered_t <= 0):
            continue
        lines.append(f"| {s.year} | {s.name} | {s.reserved_capacity_t:.1f} | {s.ordered_t:.1f} | {s.actual_delivery_t:.1f} | {s.price_mln_per_t:.2f} | {s.payable_volume_t:.1f} | {s.procurement_mln:.1f} | {s.take_or_pay_topup_mln:.1f} | {s.reservation_payment_mln:.1f} |")
    lines += ["", "Оплачиваемый объём = max(заказ, take-or-pay × резерв × доля года); начальный запас подготовительного периода учтён в закупке первого года.", "",
              "## Матрица проверок (каждое правило × год, включая выполненные)", "",
              "| Правило | Год | Метрика | Факт | Лимит | Оп. | Результат | Строгость |", "|---|---:|---|---:|---:|---|:---:|---|"]
    for m in res.check_matrix:
        fa = lambda x: f"{x:.4f}" if isinstance(x, float) else str(x)
        lines.append(f"| {m['rule_id']} | {m['year']} | {m['metric']} | {fa(m['actual'])} | {fa(m['limit'])} | {m['operator']} | "
                     f"{'выполнено' if m['ok'] else 'НАРУШЕНО'} | {SEVERITY_RU.get(m['severity'], m['severity'])} |")
    lines += ["", "## Нарушения", ""]
    if not res.violations:
        lines.append("Нарушений нет.")
    else:
        lines += ["| Правило | Строгость | Год | Месяц | Источник | Факт | Лимит | Превышение | Сообщение |", "|---|---|---:|---:|---|---:|---:|---:|---|"]
        for v in res.violations:
            fmt = lambda x: "" if x is None else (f"{x:.3f}" if isinstance(x, float) else str(x))
            lines.append(f"| {v.rule_id} | {SEVERITY_RU.get(v.severity, v.severity)} | {fmt(v.year)} | {fmt(v.month)} | {v.source_id or ''} | {fmt(v.actual)} | {fmt(v.limit)} | {fmt(v.excess)} | {v.message} |")
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

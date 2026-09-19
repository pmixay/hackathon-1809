"""Единая количественная сводка по реестру рисков: каждое последствие ПЕРЕСЧИТЫВАЕТСЯ, а не копируется.

Реестр рисков хранится в машиночитаемом виде (configs/risks.json). Для каждого риска он задаёт не
только описание, период, владельца и меры, но и рецепт пересчёта последствия. Этот скрипт выполняет
рецепты расчётным контуром на данных кейса и сравнивает результат с опубликованным значением. Любое
расхождение выше объявленного допуска останавливает скрипт: устаревшее число в реестре невозможно
не заметить при следующем прогоне.

Выход: results/risk_assessment.csv и results/risk_assessment.md
"""
from __future__ import annotations

import csv
import json
import math
import shutil
import sys
import tempfile
from pathlib import Path

from common import CASE_DIR, PLANS, RESULTS, ROOT, load_all, scenario
from run_earth_new_delay import copy_delayed_case, delay_scenario, freeze_earth_new_schedule
from run_p2z_resilience import p2z_shock
from terraplan.engine import simulate
from terraplan.plan import load_plan
from terraplan.scenario import scenario_from_dict

RISKS_FILE = ROOT / "configs" / "risks.json"
OUT_CSV = RESULTS / "risk_assessment.csv"
OUT_MD = RESULTS / "risk_assessment.md"


def metric_of(res, name: str) -> float:
    """One number from a finished run. Named metrics only — no free-form expressions in the register."""
    if name == "max_reserve_gap_t":
        return max(max(0.0, y.reserve_required_t - y.opening_t) for y in res.years)
    if name == "storage_overflow_violations":
        return float(sum(1 for v in res.violations if v.rule_id == "STORAGE_OVERFLOW"))
    if name in ("shortage_total_t", "pv_cost_mln", "hard_violations", "min_service_level_total", "served_total_t"):
        return float(res.kpi[name])
    raise KeyError(f"неизвестная метрика риска: {name}")


def recompute(spec: dict, case, a, base, stress) -> tuple[float, str]:
    """Run the recipe and return (value, one-line description of what was simulated)."""
    kind = spec["kind"]
    plan = load_plan(PLANS / f"{spec['plan']}.json") if "plan" in spec else None

    if kind == "plan_scenario":
        sc = {"BASE": base, "MANDATORY_STRESS": stress}[spec["scenario"]]
        return metric_of(simulate(case, plan, sc, a), spec["metric"]), f"{spec['plan']} в сценарии {spec['scenario']}"

    if kind == "cumulative_capex":
        sc = {"BASE": base, "MANDATORY_STRESS": stress}[spec["scenario"]]
        res = simulate(case, plan, sc, a)
        y = int(spec["through_year"])
        return next(f.cumulative_capex_mln for f in res.finance if f.year == y), f"{spec['plan']}: накопленный CAPEX к {y} году"

    if kind == "demand_variant":
        sc = scenario_from_dict({"scenario_id": f"TEAM_RISK_{spec['variant'].upper()}_DEMAND", "status": "TEAM_ASSUMPTION",
                                 "demand_variant": spec["variant"]})
        return metric_of(simulate(case, plan, sc, a), spec["metric"]), f"{spec['plan']} при {spec['variant']}-варианте спроса"

    if kind == "price_shock":
        mult = 1.0 + float(spec["change_pct"]) / 100.0
        table = {sid: {int(y): mult for y in spec["years"]} for sid in spec["sources"]}
        sc = scenario_from_dict({"scenario_id": "TEAM_RISK_PRICE_SHOCK", "status": "TEAM_ASSUMPTION", "variable_price_multiplier": table})
        shocked = simulate(case, plan, sc, a).kpi["pv_cost_mln"]
        reference = simulate(case, plan, base, a).kpi["pv_cost_mln"]
        return shocked - reference, (f"{spec['plan']}: цены каналов {'/'.join(spec['sources'])} +{spec['change_pct']:g} % "
                                     f"в {'–'.join(str(y) for y in spec['years'])} против BASE")

    if kind == "joint_shock":
        sc = p2z_shock(base, case, demand=float(spec.get("demand", 0.0)),
                       delivery_reduction=float(spec.get("delivery_reduction", 0.0)), price=float(spec.get("price", 1.0)))
        return metric_of(simulate(case, plan, sc, a), "max_reserve_gap_t"), \
            f"{spec['plan']}: спрос +{float(spec.get('demand', 0.0)) * 100:g} % в 2038–2040"

    if kind == "zbo_lag_threshold":
        for lag in range(0, int(spec["max_lag"]) + 1):
            res = simulate(case, plan, stress, a.with_overrides(zbo_commissioning_lag_months=lag))
            if any(v.rule_id == "STRESS_LOSS_LIMIT" for v in res.violations):
                return float(lag), f"{spec['plan']} в обязательном стрессе: первый лаг ZBO с нарушением годовой проверки потерь"
        return float("nan"), f"{spec['plan']}: до {spec['max_lag']} мес. годовая проверка потерь не нарушается"

    if kind == "earth_new_delay":
        delay = int(spec["delay_months"])
        reference_plan = load_plan(PLANS / "P2z_earth_new_zbo.json")
        reference = simulate(case, reference_plan, base, a)
        frozen = freeze_earth_new_schedule(reference_plan, reference)
        tmp = Path(tempfile.mkdtemp(prefix="risk_delay_"))
        try:
            delayed_case = copy_delayed_case(tmp / f"case_{delay:02d}m", delay)
            res = simulate(delayed_case, frozen, delay_scenario(base, delay), a)
            return metric_of(res, "max_reserve_gap_t"), f"Earth-New: подготовка +{delay} мес., слоты поставок заморожены"
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    raise KeyError(f"неизвестный рецепт пересчёта: {kind}")


def main(argv: list[str] | None = None) -> int:
    register = json.loads(RISKS_FILE.read_text(encoding="utf-8"))
    case, a = load_all()
    base, stress = scenario("BASE"), scenario("MANDATORY_STRESS")
    rows, mismatches = [], []
    for risk in register["risks"]:
        q = risk["quantification"]
        value, how = recompute(q["recompute"], case, a, base, stress)
        expected, tol = float(q["expected"]), float(q.get("tolerance", 0.0))
        ok = math.isfinite(value) and abs(value - expected) <= tol + 1e-9
        costs = [m["cost_mln_pv"] for m in risk["measures"] if m["cost_mln_pv"] is not None]
        cheapest = min((c if isinstance(c, (int, float)) else min(x for x in c if x is not None)) for c in costs) if costs else None
        rows.append(dict(risk_id=risk["risk_id"], event=risk["event"], period=risk["period"], owner=risk["owner"],
                         basis=risk["basis"], protocol=";".join(risk["protocol"]), dependencies=";".join(risk["dependencies"]),
                         consequence_label=q["label"], metric=q["metric"], unit=q["unit"],
                         recomputed=round(value, 6), published=expected, tolerance=tol, matches=ok, recomputed_from=how,
                         measures_count=len(risk["measures"]),
                         cheapest_measure_cost_mln_pv=(round(cheapest, 3) if cheapest is not None else ""),
                         residual_risk=risk["residual"]))
        if not ok:
            mismatches.append(f"{risk['risk_id']}: пересчитано {value:.6f}, в реестре {expected} (допуск {tol})")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    lines = ["# Количественная сводка по реестру рисков", "",
             f"Стратегия: {register['plan_id']}. Деньги — {register['currency']}, ставка дисконтирования "
             f"{register['discount_rate_real'] * 100:.0f} %.", "",
             "Каждое последствие пересчитано расчётным контуром при построении этой таблицы и сверено с "
             "опубликованным значением реестра; расхождение выше допуска останавливает сборку.", "",
             "| ID | Событие | Период | Последствие без мер | Пересчитано | Опубликовано | Сверка | Мер | Дешевейшая мера, млн PV | Владелец |",
             "|---|---|---|---|---:|---:|:---:|---:|---:|---|"]
    for r in rows:
        lines.append(f"| {r['risk_id']} | {r['event']} | {r['period']} | {r['consequence_label']} ({r['unit']}) | "
                     f"{r['recomputed']:,.3f} | {r['published']:,.3f} | {'✓' if r['matches'] else '✗'} | "
                     f"{r['measures_count']} | {r['cheapest_measure_cost_mln_pv'] or '—'} | {r['owner']} |")
    lines += ["", "## Что именно пересчитано", ""]
    for r in rows:
        lines.append(f"- **{r['risk_id']}** — {r['recomputed_from']}; метрика `{r['metric']}`; основание оценки: {r['basis']}.")
    lines += ["", "## Остаточный риск после мер", ""]
    for r in rows:
        lines.append(f"- **{r['risk_id']}** — {r['residual_risk']}")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for r in rows:
        print(f"{r['risk_id']:4s} {r['metric']:28s} пересчитано {r['recomputed']:12.3f}  реестр {r['published']:12.3f}  {'ok' if r['matches'] else 'РАСХОЖДЕНИЕ'}")
    if mismatches:
        print("\nРеестр рисков разошёлся с расчётом:")
        for m in mismatches:
            print("  ", m)
        return 1
    print(f"\n{len(rows)} рисков пересчитано, расхождений нет -> {OUT_CSV.name}, {OUT_MD.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

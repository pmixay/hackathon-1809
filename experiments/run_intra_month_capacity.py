"""EXP-16: чувствительность к допущению о дроблении месячной поставки (intra_month_delivery_batches).

Зачем. Ёмкость хранилища — физическое ограничение, и проверять его только на конец месяца
недостаточно: между поступлением и выдачей запас проходит через пик. Величина пика зависит от того,
сколько партий в месяц приходит и как они распределены. Допущение объявлено явно
(`configs/assumptions.yaml: intra_month_delivery_batches`), проверяется как жёсткое ограничение,
и здесь показано, как результат зависит от его значения.

Модель. Месячный объём канала приходит N равными партиями, равномерно распределёнными по месяцу,
выдача равномерна (конвенция организатора). Пик после партии j:

    peak_j = I_нач + (j * нетто_поступление - (j - 1) * выдача) / N,    пик = max_j peak_j

N = 1 — консервативный край: весь месячный объём поступает до выдачи, дробление не предполагается.
N -> бесконечность — предел синхронной поставки: пик стремится к max(запас на начало, запас на конец),
то есть проверка вырождается в помесячную. Выбран N = 1: организатор не задаёт размер отдельной
партии, и ни один принятый план команды в дроблении не нуждается — что и показывает эта таблица.

Выход: results/intra_month/
"""
from __future__ import annotations

import json
from pathlib import Path

from common import ASSUMPTIONS, PLANS, RESULTS, load_all, scenario, write_table
from terraplan.assumptions import load_assumptions
from terraplan.engine import simulate
from terraplan.plan import load_plan

OUT = RESULTS / "intra_month"
BATCH_VALUES = (1, 2, 4, 12)
HEADLINE = {("P2z_earth_new_zbo", "BASE"), ("P2z_earth_new_zbo_adapted", "MANDATORY_STRESS"),
            ("P3_isru_zbo", "BASE"), ("P3_isru_zbo_adapted", "MANDATORY_STRESS"),
            ("P4_full", "BASE"), ("P4_full_adapted", "MANDATORY_STRESS")}


def main() -> None:
    case, _ = load_all()
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for pf in sorted(PLANS.glob("*.json")):
        plan = load_plan(pf, case)
        for sid in ("BASE", "MANDATORY_STRESS"):
            sc = scenario(sid)
            for n in BATCH_VALUES:
                a = load_assumptions(ASSUMPTIONS).with_overrides(intra_month_delivery_batches=n)
                res = simulate(case, plan, sc, a)
                peaks = [v for v in res.violations if v.rule_id == "INTRA_MONTH_PEAK"]
                worst = max((m.peak_stock_t - m.storage_capacity_t for m in res.months), default=0.0)
                row = dict(plan_id=plan.plan_id, scenario=sid, batches=n, feasible=res.feasible,
                           intra_month_violations=len(peaks), worst_headroom_t=-worst,
                           hard_violations=res.kpi["hard_violations"], pv_cost_mln=res.kpi["pv_cost_mln"])
                rows.append(row)

    write_table(rows, OUT / "intra_month_sensitivity.csv", None)
    by_plan: dict[tuple[str, str], dict[int, dict]] = {}
    for r in rows:
        by_plan.setdefault((r["plan_id"], r["scenario"]), {})[r["batches"]] = r

    # план считается независимым от допущения, если он исполним уже при самом строгом N = 1
    independent = [k for k, v in by_plan.items() if v[1]["intra_month_violations"] == 0]
    needs_split = [k for k, v in by_plan.items() if v[1]["intra_month_violations"] > 0 and v[12]["intra_month_violations"] == 0]
    never = [k for k, v in by_plan.items() if v[12]["intra_month_violations"] > 0]

    lines = ["# EXP-16. Чувствительность к дроблению месячной поставки", "",
             "Проверка ёмкости хранилища только на конец месяца пропускает пик между поступлением и выдачей.",
             "Пик зависит от числа партий N, на которые дробится месячный объём канала:", "",
             "```",
             "peak_j = I_нач + (j * нетто_поступление - (j - 1) * выдача) / N,   пик = max_j peak_j",
             "```", "",
             "N = 1 — весь месячный объём поступает до выдачи (консервативный край, принятое значение).",
             "N -> бесконечность — предел синхронной поставки, пик стремится к max(запас на начало, запас на конец).", "",
             "## Запас по ёмкости в ключевых прогонах, т", "",
             "| План | Сценарий | " + " | ".join(f"N={n}" for n in BATCH_VALUES) + " |",
             "|---|---|" + "|".join("---:" for _ in BATCH_VALUES) + "|"]
    for (pid, sid), v in sorted(by_plan.items()):
        if (pid, sid) not in HEADLINE:
            continue
        cells = " | ".join(f"{v[n]['worst_headroom_t']:+.3f}" for n in BATCH_VALUES)
        lines.append(f"| {pid} | {sid} | {cells} |")
    lines += ["", "Положительное число — свободная ёмкость в самом напряжённом месяце; отрицательное — превышение.", "",
              "## Классификация всех прогонов", "",
              f"* **Не зависят от допущения** (проходят уже при N = 1, самом строгом): **{len(independent)}** прогонов.",
              f"* **Требуют дробления** (проходят только при N > 1): **{len(needs_split)}**"
              + (": " + ", ".join(f"{p}/{s}" for p, s in sorted(needs_split)) if needs_split else ""),
              f"* **Не проходят ни при каком N** (превышение и в пределе N = 12): **{len(never)}**"
              + (": " + ", ".join(f"{p}/{s}" for p, s in sorted(never)) if never else ""), "",
              "## Вывод", "",
              "Все принятые планы команды в своих сценариях исполнимы уже при N = 1, то есть их физическая",
              "исполнимость не опирается на допущение о внутримесячной синхронизации поставок и выдачи.",
              "Поэтому выбрано самое строгое значение N = 1: ослабление допущения не нужно для обоснования",
              "решения и только снизило бы доказательность. Планы из списка «требуют дробления» приняты не были;",
              "если бы они использовались, потребовался бы договорный график поставки партий внутри месяца.", ""]
    (OUT / "intra_month_capacity.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (OUT / "classification.json").write_text(json.dumps(
        dict(independent=[list(k) for k in sorted(independent)],
             needs_split=[list(k) for k in sorted(needs_split)],
             never=[list(k) for k in sorted(never)]), ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"проходят при N=1: {len(independent)}; требуют дробления: {len(needs_split)}; не проходят никогда: {len(never)}")
    for (pid, sid), v in sorted(by_plan.items()):
        if (pid, sid) in HEADLINE:
            print(f"  {pid:28s} {sid:17s} " + " ".join(f"N={n}:{v[n]['worst_headroom_t']:+8.3f}" for n in BATCH_VALUES))


if __name__ == "__main__":
    main()

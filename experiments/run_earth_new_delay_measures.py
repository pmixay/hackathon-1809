"""EXP-13: защитные меры выбранного плана P2z от задержки ввода Earth-New (риск R6).

Продолжение EXP-09: та же копия данных, тот же замороженный календарь Earth-New и задержки
0/3/6/12 месяцев. Добавляются две меры на канале Earth-Flex (B), минимальный объём каждой
находится бисекцией с точностью 0,001 т:

* «реакция» — заказ размещается после наблюдения задержки в 2037-01 (первый пропущенный слот),
  срок Earth-Flex 4 месяца, поставки равномерно 2037-05 … 2037-12, чтобы успеть к проверке резерва
  1 января 2038 г.; резерв мощности B на 2037 год закладывается заранее (плата 0,15 млн за т/год);
* «заранее» — буфер заказывается до того, как задержка известна (заказ 2036-08, поставка 2036-12),
  поэтому оплачивается и тогда, когда задержки нет (страховая премия рассчитана отдельно).

Оплата замороженных заказов Earth-New не возвращается (правило EXP-09); экономия при договорном
исключении недоступного объёма показана как арифметическая справка, а не как результат движка.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import platform
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from common import ASSUMPTIONS, CASE_DIR, PLANS, RESULTS, ROOT, load_all, scenario
from provenance import HASH_FORMAT, SCHEMA_VERSION, input_hashes, sha256, write_json, write_text
from run_earth_new_delay import DELAYS, chronological_failures, copy_delayed_case, delay_scenario, freeze_earth_new_schedule
from run_reverse_stress import failure_violations
from terraplan.engine import simulate
from terraplan.export import write_results
from terraplan.plan import Order, Reservation, load_plan

PLAN_PATH = PLANS / "P2z_earth_new_zbo.json"
MEASURE_DELAYS = tuple(d for d in DELAYS if d > 0)
OBSERVATION_MONTH = "2037-01"          # первый пропущенный слот Earth-New: задержка становится известной
REACTION_MONTHS = list(range(5, 13))   # поставки реактивного заказа: 2037-05 … 2037-12 (срок B = 4 месяца)
BUFFER_YEAR, BUFFER_MONTH = 2036, 12   # заблаговременный буфер: заказ 2036-08, поставка 2036-12
TOLERANCE_T = 0.001
MEASURES = ("none", "reactive_flex", "advance_buffer")
MEASURE_LABEL = {"none": "без мер", "reactive_flex": "реакция: замена через Earth-Flex", "advance_buffer": "заранее: буфер Earth-Flex"}
EVENT_RULES = ("SOURCE_NOT_AVAILABLE", "ORDER_EXCEEDS_RESERVATION")   # нарушения по самому Earth-New в год задержки — это событие, а не его последствие


def is_event(v):
    return v.rule_id in EVENT_RULES and v.source_id == "C"


def consequence_violations(result):
    """Последствия события: все отказы, кроме недоступности самого Earth-New в год задержки."""
    return [v for v in failure_violations(result) if not is_event(v)]


def with_reactive_flex(frozen, volume, delay):
    plan = deepcopy(frozen)
    plan.plan_id = f"P2z_delay{delay:02d}m_reactive_flex"
    plan.description = (f"P2z с замороженным календарём Earth-New; задержка {delay} мес.; реактивный заказ Earth-Flex "
                        f"{volume:.3f} т после наблюдения {OBSERVATION_MONTH}, поставки 2037-05…2037-12")
    monthly = [volume / len(REACTION_MONTHS) if m in REACTION_MONTHS else 0.0 for m in range(1, 13)]
    plan.orders.append(Order("B", 2037, volume, "monthly", monthly, True))
    plan.reservations.append(Reservation("B", 2037, volume))
    plan.observation_month = OBSERVATION_MONTH
    plan.meta = dict(plan.meta, experiment="EXP-13", measure="reactive_flex", delay_months=delay,
                     decision_timing="резерв B заложен заранее; заказ размещён после наблюдения задержки, срок 4 месяца")
    return plan


def with_advance_buffer(frozen, volume, delay):
    plan = deepcopy(frozen)
    plan.plan_id = f"P2z_delay{delay:02d}m_advance_buffer"
    plan.description = (f"P2z с замороженным календарём Earth-New; задержка {delay} мес.; заблаговременный буфер Earth-Flex "
                        f"{volume:.3f} т, поставка {BUFFER_YEAR}-{BUFFER_MONTH:02d} (заказ до наблюдения задержки)")
    monthly = [volume if m == BUFFER_MONTH else 0.0 for m in range(1, 13)]
    plan.orders.append(Order("B", BUFFER_YEAR, volume, "monthly", monthly, False))
    plan.reservations.append(Reservation("B", BUFFER_YEAR, volume))
    plan.meta = dict(plan.meta, experiment="EXP-13", measure="advance_buffer", delay_months=delay,
                     decision_timing="заказ и резерв B до наблюдения; оплачивается и без задержки")
    return plan


def minimal_volume(build, case, scen, assumptions, upper):
    """Наименьший объём меры (бисекция, шаг 0,001 т), при котором последствия задержки исчезают."""
    def passes(volume):
        return not consequence_violations(simulate(case, build(volume), scen, assumptions))
    if passes(0.0):
        return 0.0
    if not passes(upper):
        raise ValueError(f"мера не устраняет последствия даже при {upper:.3f} т")
    lo, hi = 0.0, upper
    while hi - lo > TOLERANCE_T:
        mid = (lo + hi) / 2
        if passes(mid):
            hi = mid
        else:
            lo = mid
    return math.ceil(hi / TOLERANCE_T) * TOLERANCE_T


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def export_run(res, run_dir):
    write_results(res, run_dir, xlsx=False)
    case_hashes = {p.name: sha256(p) for p in sorted((run_dir / "case").glob("*.csv"))}
    core = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
    core.update(case_file_hash_format=HASH_FORMAT, case_file_sha256=case_hashes)
    write_json(run_dir / "run_manifest.json", core)
    return case_hashes


def summarize(res, reference, violations):
    reserve = [v for v in violations if v.rule_id == "RESERVE_45D"]
    first = violations[0] if violations else None
    return dict(shortage_t=res.kpi["shortage_total_t"], critical_shortage_t=res.kpi["shortage_critical_t"],
                min_service_total=res.kpi["min_service_level_total"], min_service_critical=res.kpi["min_service_level_critical"],
                reserve_failed_years=";".join(str(v.year) for v in reserve),
                max_reserve_gap_t=max(max(0.0, y.reserve_required_t - y.opening_t) for y in res.years),
                min_reserve_slack_t=min(y.opening_t - y.reserve_required_t for y in res.years),
                consequence_violations=len(violations),
                event_violations=sum(1 for v in failure_violations(res) if is_event(v)),
                total_cost_mln=res.kpi["total_cost_mln"], pv_cost_mln=res.kpi["pv_cost_mln"],
                delta_total_vs_reference_mln=res.kpi["total_cost_mln"] - reference.kpi["total_cost_mln"],
                delta_pv_vs_reference_mln=res.kpi["pv_cost_mln"] - reference.kpi["pv_cost_mln"],
                first_consequence_rule=first.rule_id if first else None, first_consequence_year=first.year if first else None,
                first_consequence_month=first.month if first else None, passes=not violations)


def run_experiment(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    case, assumptions = load_all()
    base = scenario("BASE")
    original = load_plan(PLAN_PATH, case)
    reference = simulate(case, original, base, assumptions)
    if failure_violations(reference):
        raise ValueError("исходный план P2z должен проходить BASE без нарушений")
    frozen = freeze_earth_new_schedule(original, reference)
    c_price = case.sources["C"].variable_cost_mln_per_t
    comparison, yearly, runs = [], [], []

    def run_variant(delay, measure, plan, run_dir, sizing_note):
        modified = copy_delayed_case(run_dir / "case", delay)
        sc = delay_scenario(base, delay)
        sc.scenario_id = f"TEAM_EXP13_DELAY_{delay:02d}M"
        sc.changes.append(dict(status="TEAM_ASSUMPTION", experiment="EXP-13", measure=measure, label=MEASURE_LABEL[measure],
                               sizing=sizing_note, observation_month=OBSERVATION_MONTH,
                               frozen_orders="оплата замороженных заказов Earth-New не возвращается (как в EXP-09)"))
        a = assumptions.with_overrides(earth_new_preparation_delay_months=delay)
        a.entries["earth_new_preparation_delay_months"].update(
            unit="месяцев", range=list(DELAYS), status="TEAM_ASSUMPTION",
            justification="EXP-13: наложение на сроки Earth-New в копии данных, как в EXP-09; не параметр ядра")
        res = simulate(modified, plan, sc, a)
        case_hashes = export_run(res, run_dir)
        violations = chronological_failures(res, reference)
        cons = [v for v in violations if not is_event(v)]
        row = dict(delay_months=delay, measure=measure, measure_label=MEASURE_LABEL[measure], plan_id=plan.plan_id,
                   flex_volume_t=sum(o.ordered_t for o in plan.orders if o.source_id == "B" and o.year in (2036, 2037)),
                   decision_timing=plan.meta.get("decision_timing", "—"),
                   missed_earth_new_t=sum(max(0.0, s.ordered_t - s.actual_delivery_t) for s in res.source_years if s.source_id == "C" and s.period == "year"),
                   **summarize(res, reference, cons))
        row["unpaid_if_contract_excludes_unavailable_mln"] = row["missed_earth_new_t"] * c_price  # справка, не расчёт движка
        for y in res.years:
            yearly.append(dict(delay_months=delay, measure=measure, year=y.year, opening_t=y.opening_t,
                               reserve_required_t=y.reserve_required_t, reserve_gap_t=max(0.0, y.reserve_required_t - y.opening_t),
                               reserve_ok=y.reserve_ok, closing_t=y.closing_t, shortage_t=y.shortage_total_t,
                               service_total=y.service_level_total, service_critical=y.service_level_critical,
                               storage_capacity_end_t=y.storage_capacity_end_t))
        runs.append(dict(**row, result_dir=str(run_dir.relative_to(out)), kpi=res.kpi, scenario=sc.to_dict(), assumptions=a.entries,
                         plan=plan.to_dict(), violations=[asdict(v) for v in violations], case_sha256=case_hashes))
        return res, row

    for delay in MEASURE_DELAYS:
        res_none, row_none = run_variant(delay, "none", frozen, out / f"delay_{delay:02d}m" / "none", "мера не применяется")
        missed = row_none["missed_earth_new_t"]
        # Копия данных для подбора объёма — та же, что и для итогового прогона.
        sizing_case = copy_delayed_case(out / f"delay_{delay:02d}m" / "_sizing_case", delay)
        sizing_scen = delay_scenario(base, delay)
        sizing_a = assumptions.with_overrides(earth_new_preparation_delay_months=delay)
        upper = 2.0 * missed + 1.0
        v_react = minimal_volume(lambda v: with_reactive_flex(frozen, v, delay), sizing_case, sizing_scen, sizing_a, upper)
        v_buffer = minimal_volume(lambda v: with_advance_buffer(frozen, v, delay), sizing_case, sizing_scen, sizing_a, upper)
        for p in sorted((out / f"delay_{delay:02d}m" / "_sizing_case").glob("*")):
            p.unlink()
        (out / f"delay_{delay:02d}m" / "_sizing_case").rmdir()
        _, row_react = run_variant(delay, "reactive_flex", with_reactive_flex(frozen, v_react, delay),
                                   out / f"delay_{delay:02d}m" / "reactive_flex", f"минимальный объём бисекцией, шаг {TOLERANCE_T} т")
        _, row_buffer = run_variant(delay, "advance_buffer", with_advance_buffer(frozen, v_buffer, delay),
                                    out / f"delay_{delay:02d}m" / "advance_buffer", f"минимальный объём бисекцией, шаг {TOLERANCE_T} т")
        # Страховая премия буфера, если задержки нет: тот же план в копии данных без задержки.
        _, row_premium = run_variant(0, "advance_buffer", with_advance_buffer(frozen, v_buffer, delay),
                                     out / f"delay_{delay:02d}m" / "advance_buffer_no_delay", "буфер оплачен, задержки не было")
        for row in (row_none, row_react, row_buffer):
            row["delta_pv_vs_no_measure_mln"] = row["pv_cost_mln"] - row_none["pv_cost_mln"]
            row["delta_total_vs_no_measure_mln"] = row["total_cost_mln"] - row_none["total_cost_mln"]
        row_buffer["premium_if_no_delay_pv_mln"] = row_premium["delta_pv_vs_reference_mln"]
        row_buffer["premium_run_passes"] = row_premium["passes"]
        row_react["premium_if_no_delay_pv_mln"] = 0.0
        row_react["premium_run_passes"] = True
        row_none["premium_if_no_delay_pv_mln"] = 0.0
        row_none["premium_run_passes"] = True
        comparison += [row_none, row_react, row_buffer]

    paths = [PLAN_PATH, ASSUMPTIONS, Path(base.source_file), Path(__file__), ROOT / "experiments/common.py",
             ROOT / "experiments/run_earth_new_delay.py", ROOT / "experiments/run_reverse_stress.py"]
    paths += sorted(CASE_DIR.glob("*.csv")) + sorted((ROOT / "src/terraplan").glob("*.py"))
    report = dict(experiment_id="EXP-13", python=platform.python_version(), random_seed=None,
                  schema_version=SCHEMA_VERSION, hash_format=HASH_FORMAT, input_sha256=input_hashes(paths),
                  method=dict(status="TEAM_ASSUMPTION", plan=original.plan_id, reference="BASE", delays_months=list(MEASURE_DELAYS),
                              event="задержка подготовки Earth-New на копии данных, календарь Earth-New заморожен (EXP-09)",
                              observation=f"задержка наблюдается в {OBSERVATION_MONTH} (первый пропущенный слот); срок реакции Earth-Flex 4 месяца",
                              reactive_flex="резерв B на 2037 заложен заранее; заказ reactive=true; поставки 2037-05…2037-12; проверка сроков реакции движком",
                              advance_buffer=f"заказ B до наблюдения (поставка {BUFFER_YEAR}-{BUFFER_MONTH:02d}); премия без задержки рассчитана отдельным прогоном",
                              sizing=f"бисекция минимального объёма с шагом {TOLERANCE_T} т; критерий — отсутствие последствий (все hard-нарушения и ориентиры сервиса, кроме недоступности и превышения пропорционального резерва самого Earth-New в год задержки)",
                              contracts="замороженные заказы Earth-New оплачиваются без возврата; экономия при договорном исключении недоступного объёма — арифметическая справка",
                              costs="только денежные потоки движка: закупка, резерв мощности, хранение; без неустоек и оценки ущерба миссиям"),
                  reference_kpi=reference.kpi, comparison=comparison, yearly=yearly, runs=runs)
    write_json(out / "report.json", report)
    write_csv(out / "comparison.csv", comparison)
    write_csv(out / "yearly.csv", yearly)
    lines = ["# EXP-13: защитные меры P2z от задержки ввода Earth-New (BASE, копия данных)", "",
             f"Задержка наблюдается в {OBSERVATION_MONTH}; реакция — заказ Earth-Flex со сроком 4 месяца, поставки 2037-05…2037-12; "
             f"заблаговременный буфер — поставка Earth-Flex {BUFFER_YEAR}-{BUFFER_MONTH:02d} до наблюдения. Объёмы — минимальные (бисекция, шаг {TOLERANCE_T} т).",
             "Замороженные заказы Earth-New оплачиваются без возврата (как в EXP-09). Деньги — млн у.е. в ценах 2035 г., PV по реальной ставке 8 %.", "",
             "| Задержка, мес. | Мера | Объём B, т | Дефицит, т | Мин. сервис общий / критический | Годы нарушения резерва | Макс. разрыв резерва, т | PV, млн | ΔPV к плану без задержки | ΔPV к «без мер» | Премия без задержки, ΔPV | Последствия устранены |",
             "|---:|---|---:|---:|---|---|---:|---:|---:|---:|---:|---|"]
    for r in comparison:
        lines.append(f"| {r['delay_months']} | {r['measure_label']} | {r['flex_volume_t']:.3f} | {r['shortage_t']:.3f} | "
                     f"{r['min_service_total']:.4f} / {r['min_service_critical']:.4f} | {r['reserve_failed_years'] or 'нет'} | {r['max_reserve_gap_t']:.3f} | "
                     f"{r['pv_cost_mln']:.3f} | {r['delta_pv_vs_reference_mln']:+.3f} | {r['delta_pv_vs_no_measure_mln']:+.3f} | "
                     f"{r['premium_if_no_delay_pv_mln']:+.3f} | {'да' if r['passes'] else 'нет'} |")
    lines += ["", "## Чтение результата", "",
              "- Без мер сервис остаётся 100 %, но 45-дневный резерв нарушен в 2038–2040: недопоставленное топливо Earth-New остаётся оплаченным, а физический запас ниже нормы.",
              "- Обе меры устраняют последствия; недоступность Earth-New и превышение его пропорционального резерва в год задержки остаются в матрице проверок как факт события (замороженный заказ).",
              "- Реакция дешевле ровно тогда, когда задержка происходит; буфер «заранее» дополнительно оплачивается и без задержки (столбец «Премия без задержки»).",
              "- Остаточный риск реакции: задержка, объявленная позже 2037-08, не оставляет 4 месяцев до проверки резерва 1 января 2038 г.; тогда работает только буфер или Emergency (6 недель).",
              f"- Справка: при договорном исключении недоступного объёма Earth-New из оплаты экономия составила бы объём × {c_price} млн/т (столбец unpaid_if_contract_excludes_unavailable_mln в comparison.csv); движок этого не считает.",
              "", "## Воспроизведение", "", "```bash",
              "python experiments/run_earth_new_delay_measures.py",
              "python -m terraplan verify results/earth_new_delay_measures/delay_03m/reactive_flex --case results/earth_new_delay_measures/delay_03m/reactive_flex/case",
              "python tests/independent_recalc.py results/earth_new_delay_measures/delay_03m/reactive_flex results/earth_new_delay_measures/delay_03m/reactive_flex/case",
              "python experiments/provenance.py results/earth_new_delay_measures", "```"]
    text = "\n".join(lines) + "\n"
    write_text(out / "summary.md", text)
    return report, text


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=RESULTS / "earth_new_delay_measures")
    args = parser.parse_args(argv)
    _, text = run_experiment(args.out)
    print(text)


if __name__ == "__main__":
    main()

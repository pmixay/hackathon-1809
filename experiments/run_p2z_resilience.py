"""EXP-12: P2z delay protection, sensitivity and conditional reverse stress.

Keep EXP-09's missed-slot and payment semantics. Compare purchased stock with
an ex-ante guarded C calendar. No online policy or probability is inferred.
"""
from __future__ import annotations

import argparse
import json
import math
import platform
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from common import ASSUMPTIONS, CASE_DIR, PLANS, RESULTS, ROOT, load_all, scenario
from provenance import HASH_FORMAT, SCHEMA_VERSION, input_hashes, sha256, write_json, write_text
from run_earth_new_delay import DELAYS, copy_delayed_case, delay_scenario, freeze_earth_new_schedule, write_csv
from run_reverse_stress import RAYS, YEARS, bisect_boundary, failure_violations
from terraplan.engine import EPS, TOL_T, simulate
from terraplan.export import write_results
from terraplan.plan import Order, Reservation, load_plan
from terraplan.scenario import scenario_from_dict

BASE_PLAN = PLANS / "P2z_earth_new_zbo.json"
STRESS_PLAN = PLANS / "P2z_earth_new_zbo_adapted.json"
TARGET_DELAY = 3
TOLERANCE = 1e-10
LABELS = {"without_measure": "Без защиты", "physical_stock": "Дополнительный запас",
          "guarded_calendar": "Защитный календарь", "adapted_stress": "Адаптированный стресс"}


def stock_plan(original, case, net_t):
    """Additional B deliveries Jul-Dec 2037, ordered Mar-Aug (four-month lead)."""
    if not math.isfinite(net_t) or net_t < 0:
        raise ValueError("net_t должен быть конечным неотрицательным числом")
    plan = deepcopy(original)
    plan.plan_id = f"P2z_stock_{net_t:g}t"
    if original.order("B", 2037) is not None:
        raise ValueError("EXP-12 ожидает отсутствие исходного заказа B в 2037")
    if net_t:
        gross_month = math.ceil(net_t / (6 * (1 - case.storage["ZBO"].loss_rate_on_throughput)) * 1e4 - 1e-9) / 1e4
        monthly = [0.0] * 6 + [gross_month] * 6
        plan.orders.append(Order("B", 2037, sum(monthly), "monthly", monthly))
        capacity = math.ceil(gross_month * 12 * 1e3 - 1e-9) / 1e3
        plan.reservations.append(Reservation("B", 2037, capacity))
    plan.meta.update(experiment="EXP-12", stock_target_net_t=net_t,
                     protection="Закупленный запас Flex; исходные обязательства C сохранены")
    return plan


def guarded_plan(original):
    """At the 2035 option decision reserve a 3-month commissioning margin.

    Same annual ordered tonnes; all 2037 C deliveries explicitly Apr-Dec.
    Increase annualized reservation to cover that monthly peak. This calendar
    is fixed in advance, including in the zero-delay control; no hindsight.
    """
    plan = deepcopy(original)
    plan.plan_id = "P2z_guarded_calendar_3m"
    order = plan.order("C", 2037)
    order.profile = "monthly"
    order.monthly_t = [0.0] * 3 + [order.ordered_t / 9] * 9
    order.ordered_t = sum(order.monthly_t)
    reservation = next(r for r in plan.reservations if (r.source_id, r.year) == ("C", 2037))
    reservation.reserved_capacity_t = math.ceil(max(order.monthly_t) * 12 * 1e3 - 1e-9) / 1e3
    plan.meta.update(experiment="EXP-12", calendar_committed_at="2035-01",
                     protection="Поставки C в апреле–декабре 2037; дополнительный резерв мощности оплачен")
    return plan


def physical_failures(result):
    """Operational fuel/storage checks, separate from the FULL failure predicate."""
    rules = {"RESERVE_45D", "STORAGE_OVERFLOW", "BASE_TOTAL_SERVICE", "BASE_CRITICAL_SERVICE", "STRESS_LOSS_LIMIT"}
    return [v for v in failure_violations(result) if v.rule_id in rules]


def metrics(result):
    failures = failure_violations(result)
    first = failures[0] if failures else None
    return dict(pv_cost_mln=result.kpi["pv_cost_mln"], total_cost_mln=result.kpi["total_cost_mln"],
                full_pass=not failures, physical_pass=not physical_failures(result),
                shortage_t=result.kpi["shortage_total_t"], critical_shortage_t=result.kpi["shortage_critical_t"],
                min_service_total=result.kpi["min_service_level_total"],
                min_service_critical=result.kpi["min_service_level_critical"],
                max_reserve_gap_t=max(max(0.0, y.reserve_required_t - y.opening_t) for y in result.years),
                reserve_failed_years=";".join(str(y.year) for y in result.years if not y.reserve_ok),
                hard_violations=result.kpi["hard_violations"],
                failure_rules=";".join(sorted({v.rule_id for v in failures})),
                first_rule=first.rule_id if first else None, first_year=first.year if first else None,
                first_month=first.month if first else None)


def p2z_shock(reference, case, demand=0.0, delivery_reduction=0.0, price=1.0):
    """Persistent relative demand/C-delivery shocks 2038-40; prices 2038-39."""
    if not all(math.isfinite(x) for x in (demand, delivery_reduction, price)) or demand < 0 or not 0 <= delivery_reduction <= 1 or price <= 0:
        raise ValueError("недопустимые параметры шока P2z")
    data = deepcopy(reference.to_dict())
    data.update(scenario_id=f"TEAM_P2Z_d{demand:.17g}_c{delivery_reduction:.17g}_p{price:.17g}",
                label="EXP-12: чувствительность P2z", status="TEAM_ASSUMPTION")
    data["demand_multiplier"] = {y: reference.demand_mult(y) * (1 + demand if y in YEARS else 1) for y in case.years}
    data["critical_demand_multiplier"] = {y: reference.critical_mult(y) * (1 + demand if y in YEARS else 1) for y in case.years}
    data["actual_delivery_share"] = {
        sid: {y: reference.delivery_share(source, y) * (1 - delivery_reduction if sid == "C" and y in YEARS else 1)
              for y in case.years} for sid, source in case.sources.items()}
    data["variable_price_multiplier"] = {
        sid: {y: reference.price_mult(source, y) * (price if sid in ("A", "B") and y in (2038, 2039) else 1)
              for y in case.years} for sid, source in case.sources.items()}
    data["changes"] += [dict(status="TEAM_ASSUMPTION", reference=reference.scenario_id,
                             demand_increase=demand, c_delivery_reduction=delivery_reduction,
                             core_flex_price_multiplier=price, physical_years=list(YEARS), price_years=[2038, 2039],
                             frozen="Все решения плана; шок C — доля поставки, не задержка ввода")]
    return scenario_from_dict(data)


def reverse_boundary(case, plan, reference, assumptions):
    rows = []
    for u, v in RAYS:
        def evaluate(t):
            return simulate(case, plan, p2z_shock(reference, case, u * t, v * t), assumptions)
        lo, hi = bisect_boundary(lambda t: bool(failure_violations(evaluate(t))), 0.5, TOLERANCE)
        passed = evaluate(lo)
        failed = evaluate(hi) if hi is not None else None
        rows.append(dict(demand_direction=u, earth_new_direction=v, pass_radius=lo, fail_radius=hi,
                         first_violation=asdict(failure_violations(failed)[0]) if failed else None,
                         passing_kpi=passed.kpi, failing_kpi=failed.kpi if failed else None))
    return rows


def run_experiment(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    case, a = load_all()
    base, stress = scenario("BASE"), scenario("MANDATORY_STRESS")
    original = load_plan(BASE_PLAN, case)
    reference = simulate(case, original, base, a)
    frozen = freeze_earth_new_schedule(original, reference)
    delayed_cases = {d: copy_delayed_case(out / "cases" / f"delay_{d:02d}m", d) for d in DELAYS}
    scenarios = {d: delay_scenario(base, d) for d in DELAYS}
    for sc in scenarios.values():
        sc.label = "EXP-12: задержка Earth-New на копии данных"
    # Evaluate every lower practical size; storage feasibility need not be monotone.
    sizing = []
    target_unprotected = simulate(delayed_cases[TARGET_DELAY], frozen, scenarios[TARGET_DELAY], a)
    max_steps = math.floor(case.sources["B"].capacity_t_per_year / 2 * (1 - case.storage["ZBO"].loss_rate_on_throughput) * 10)
    for step in range(max_steps + 1):
        plan = stock_plan(frozen, case, step / 10)
        control = simulate(case, plan, base, a)
        target = simulate(delayed_cases[TARGET_DELAY], plan, scenarios[TARGET_DELAY], a)
        sizing.append(dict(stock_target_net_t=step / 10, control_pass=not failure_violations(control),
                           target_physical_pass=not physical_failures(target), target_full_pass=not failure_violations(target),
                           target_max_reserve_gap_t=metrics(target)["max_reserve_gap_t"],
                           delta_pv_mln=target.kpi["pv_cost_mln"] - target_unprotected.kpi["pv_cost_mln"]))
        if sizing[-1]["control_pass"] and sizing[-1]["target_physical_pass"]:
            selected_stock = step / 10
            break
    else:
        raise ValueError("в заданном семействе не найдена защита физического резерва")
    plans = {"without_measure": frozen, "physical_stock": stock_plan(frozen, case, selected_stock),
             "guarded_calendar": guarded_plan(frozen)}
    comparison, yearly, runs = [], [], []
    for delay in DELAYS:
        delayed = delayed_cases[delay]
        sc = scenarios[delay]
        aa = a.with_overrides(earth_new_preparation_delay_months=delay, p2z_guard_months=3,
                              p2z_stock_target_net_t=selected_stock)
        for key, unit, bounds, why in (
            ("earth_new_preparation_delay_months", "месяц", list(DELAYS), "EXP-12: накладка сроков C на копии CASE_INPUT"),
            ("p2z_guard_months", "месяц", [3], "EXP-12: календарь C принят в 2035-01; не реактивное решение"),
            ("p2z_stock_target_net_t", "т нетто", [0, max_steps / 10], "EXP-12: сетка 0,1 т; физическая защита резерва, без отмены обязательств C"),
        ):
            aa.entries[key].update(status="TEAM_ASSUMPTION", unit=unit, range=bounds, justification=why)
        unprotected = simulate(delayed, frozen, sc, aa)
        for name, plan in plans.items():
            res = simulate(delayed, plan, sc, aa)
            relative = f"{name}_delay_{delay:02d}m"
            write_results(res, out / relative, xlsx=False)
            manifest_path = out / relative / "run_manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest.update(case_dir=f"../cases/delay_{delay:02d}m", case_dir_absolute_at_run="",
                            case_file_hash_format=HASH_FORMAT,
                            case_file_sha256={p.name: sha256(p) for p in sorted((out / "cases" / f"delay_{delay:02d}m").glob("*.csv"))})
            write_json(manifest_path, manifest)
            row = dict(variant=name, delay_months=delay, **metrics(res),
                       delta_pv_same_delay_mln=res.kpi["pv_cost_mln"] - unprotected.kpi["pv_cost_mln"],
                       delta_total_same_delay_mln=res.kpi["total_cost_mln"] - unprotected.kpi["total_cost_mln"],
                       delta_pv_original_base_mln=res.kpi["pv_cost_mln"] - reference.kpi["pv_cost_mln"])
            comparison.append(row)
            for y in res.years:
                yearly.append(dict(variant=name, delay_months=delay, **asdict(y)))
            runs.append(dict(**row, result_dir=relative, case_dir=f"cases/delay_{delay:02d}m",
                             failures=[asdict(v) for v in failure_violations(res)],
                             delta_components_mln={k: res.kpi[k] - unprotected.kpi[k] for k in
                                                   ("procurement_total_mln", "reservation_total_mln", "holding_total_mln", "fixed_opex_total_mln", "capex_total_mln")}))
    analysis_plans = {**{name: (plan, base) for name, plan in plans.items()},
                      "adapted_stress": (load_plan(STRESS_PLAN, case), stress)}
    boundaries, sensitivity = {}, []
    for name, (plan, environment) in analysis_plans.items():
        boundaries[name] = reverse_boundary(case, plan, environment, a)
        ref = simulate(case, plan, environment, a)
        for factor, values in (("demand", (0, 0.01, 0.02, 0.05, 0.1)),
                               ("delivery_reduction", (0, 0.01, 0.02, 0.05, 0.1)),
                               ("price", (0.8, 1.0, 1.25, 1.5))):
            for value in values:
                res = simulate(case, plan, p2z_shock(environment, case, **{factor: value}), a)
                sensitivity.append(dict(variant=name, reference=environment.scenario_id, factor=factor, value=value,
                                        **metrics(res), delta_pv_mln=res.kpi["pv_cost_mln"] - ref.kpi["pv_cost_mln"]))
    paths = [BASE_PLAN, STRESS_PLAN, ASSUMPTIONS, Path(base.source_file), Path(stress.source_file), Path(__file__),
             ROOT / "experiments/common.py", ROOT / "experiments/run_reverse_stress.py", ROOT / "experiments/run_earth_new_delay.py"]
    paths += sorted(CASE_DIR.glob("*.csv")) + sorted((ROOT / "src/terraplan").glob("*.py"))
    report = dict(experiment_id="EXP-12", schema_version=SCHEMA_VERSION, hash_format=HASH_FORMAT,
                  python=platform.python_version(), random_seed=None, input_sha256=input_hashes(paths),
                  method=dict(status="TEAM_ASSUMPTION", target_delay_months=3, delays_months=list(DELAYS),
                              stock_step_net_t=0.1, stock_max_net_t=max_steps / 10,
                              selected_stock_net_t=selected_stock, rounding="добавочный валовый месячный объём вверх до 0,0001 т",
                              stock_calendar="Flex июль–декабрь 2037, заказы март–август, срок 4 месяца; ZBO с июля, лаг 0",
                              guard_calendar="В 2035-01 зафиксировать C апрель–декабрь 2037; тот же годовой заказ, резерв >= пик * 12",
                              missed_slots="Как EXP-09: потеря слота без переноса/возврата; оплата заказанного, резерв по доступному периоду",
                              failure="Любое жёсткое нарушение или сервис ниже 97%/99%; физический результат не заменяет полный",
                              physical_rules=["RESERVE_45D", "STORAGE_OVERFLOW", "BASE_TOTAL_SERVICE", "BASE_CRITICAL_SERVICE", "STRESS_LOSS_LIMIT"],
                              reverse="Фиксированные планы при нулевой задержке; спрос и относительная недопоставка C в 2038–2040",
                              reverse_domain=[0, 0.5], metric="max(d,c)", tolerance=TOLERANCE,
                              physical_tolerance_t=TOL_T, service_tolerance=EPS,
                              limits="Не онлайн-политика, не прогноз вероятностей и не оптимум; меры BASE не доказывают защиту в обязательном стрессе"),
                  assumptions=a.entries, plans={name: plan.to_dict() for name, (plan, _) in analysis_plans.items()},
                  references={name: environment.to_dict() for name, (_, environment) in analysis_plans.items()},
                  sizing=sizing, comparison=comparison, yearly=yearly, runs=runs, boundary=boundaries, sensitivity=sensitivity)
    write_csv(out / "sizing.csv", sizing)
    write_csv(out / "comparison.csv", comparison)
    write_csv(out / "yearly.csv", yearly)
    write_csv(out / "sensitivity.csv", sensitivity)
    boundary_rows = []
    for name, rows in boundaries.items():
        for row in rows:
            first = row["first_violation"] or {}
            boundary_rows.append(dict(variant=name, **{k: row[k] for k in ("demand_direction", "earth_new_direction", "pass_radius", "fail_radius")},
                                      first_rule=first.get("rule_id"), first_year=first.get("year"), first_month=first.get("month")))
    write_csv(out / "boundary.csv", boundary_rows)
    for name, (plan, _) in analysis_plans.items():
        write_json(out / f"{name}.plan.json", plan.to_dict())
    write_json(out / "report.json", report)
    text = summary(report)
    write_text(out / "summary.md", text)
    # Standard result.json includes local paths and export_envelope contains time.
    # Hash portable CSVs/snapshots plus copied cases; CLI verify checks numerical replay.
    excluded = {"result.json", "export_envelope.json"}
    outputs = {p.relative_to(out).as_posix(): sha256(p) for p in sorted(out.rglob("*"))
               if p.is_file() and p.name not in excluded and p != out / "run_manifest.json"}
    write_json(out / "run_manifest.json", dict(experiment_id="EXP-12", schema_version=SCHEMA_VERSION,
               hash_format=HASH_FORMAT, input_sha256=report["input_sha256"], output_sha256=outputs))
    return report, text


def summary(report):
    lines = ["# EXP-12 — защита и устойчивость выбранного P2z", "",
             "## Задержка Earth-New: меры, стоимость и остаточный риск", "",
             f"Цель: задержка 3 месяца в BASE. Минимальный целевой запас на сетке 0,1 т: **{report['method']['selected_stock_net_t']:g} т нетто**.",
             "Запас поставляется Flex в июле–декабре 2037 после ввода ZBO; это оплаченная закупка, не резерв мощности.",
             "Вторая мера — заранее принятый в январе 2035 календарь C: апрель–декабрь 2037, прежний годовой объём, увеличенное резервирование.", "",
             "| Мера | Задержка, мес. | PV, млн | Доплата к тому же шоку, млн PV | Макс. нехватка резерва, т | Дефицит, т | Полностью проходит | Остаточные нарушения |",
             "|---|---:|---:|---:|---:|---:|---|---|"]
    for row in report["comparison"]:
        lines.append(f"| {LABELS[row['variant']]} | {row['delay_months']} | {row['pv_cost_mln']:.6f} | {row['delta_pv_same_delay_mln']:.6f} | "
                     f"{row['max_reserve_gap_t']:.6f} | {row['shortage_t']:.6f} | {'да' if row['full_pass'] else 'нет'} | {row['failure_rules'] or 'нет'} |")
    lines += ["", "Запас устраняет нехватку физического резерва при целевой задержке, но не отменяет сорванные слоты C и договорные ограничения.",
              "Защитный календарь проверен также без задержки; это заблаговременная мера, не перестановка уже сорванных поставок задним числом.",
              "При 6/12 месяцах защиты не хватает. Полная таблица затрат хранит доплату относительно исходного BASE отдельно от цены меры при том же шоке.",
              "Не оценены штрафы, стоимость срыва миссий и коммерческая согласуемость графика. Снижение расходов из-за недопоставки не считается выгодой риска.", "",
              "## Обратный стресс: спрос и недопоставка Earth-New", "",
              "Нулевая задержка ввода; постоянные дополнительные шоки в 2038–2040. Метрика max(d,c), диапазон 0–50%, 9 направлений.",
              "Цена Core/Flex исследуется отдельно: 0,8/1/1,25/1,5 в 2038–2039; физические шоки на сетке 0/1/2/5/10%.",
              "| План / фон | Последняя проходящая диагональ, % | Первая нарушающая, % | Первое нарушение |",
              "|---|---:|---:|---|"]
    for name, rows in report["boundary"].items():
        row = next(r for r in rows if r["demand_direction"] == r["earth_new_direction"])
        first = row["first_violation"]
        hi = f"{row['fail_radius'] * 100:.9f}" if row["fail_radius"] is not None else "в диапазоне нет"
        lines.append(f"| {LABELS[name]} / {report['references'][name]['scenario_id']} | {row['pass_radius'] * 100:.9f} | {hi} | "
                     f"{first['rule_id'] + ' @ ' + str(first['year']) if first else 'нет'} |")
    lines += ["", "Граница — интервал, не точный достигаемый минимум; микроскопический запас над ограничением не означает практической устойчивости.",
              "Для этих фиксированных планов рост спроса/снижение поставок понижает запас, ZBO уже работает: проходящая диагональ покрывает свой квадрат шоков.",
              "Это условный результат на выбранном фоне: планы BASE и адаптированного стресса различаются; единую политику он не доказывает.",
              "Распределений и вероятностного рейтинга нет. Детерминированный обратный стресс выбран вместо нового Монте-Карло без калибровки.", "",
              "## Воспроизведение", "", "```bash", "python experiments/run_p2z_resilience.py",
              "python experiments/provenance.py results/p2z_resilience",
              "python -m terraplan verify results/p2z_resilience/guarded_calendar_delay_03m --case results/p2z_resilience/cases/delay_03m",
              "```", "", "`sizing.csv`: все меньшие размеры запаса; `comparison.csv`, `yearly.csv`: затраты и остаточный риск;",
              "`sensitivity.csv`, `boundary.csv`: чувствительность и границы; `report.json`: планы, допущения и граничные KPI;",
              "`run_manifest.json`: нормализованные SHA-256 входов и переносимых выгрузок. CASE_INPUT не изменяется."]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=RESULTS / "p2z_resilience")
    args = parser.parse_args(argv)
    _, text = run_experiment(args.out)
    print(text)


if __name__ == "__main__":
    main()

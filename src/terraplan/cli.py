"""Интерфейс командной строки TerraPlan (вывод на русском; идентификаторы правил и файлов — как в форматах организатора).

  python -m terraplan run --plan configs/plans/P3.json --scenario BASE --out results/P3_BASE
  python -m terraplan run --plan ... --scenario configs/scenarios/mandatory_stress.yaml --out ...
  python -m terraplan compare results/P3_BASE results/P3_STRESS --out results/compare_P3
  python -m terraplan validate --plan configs/plans/P3.json
  python -m terraplan verify results/alternatives/P3_isru_zbo_BASE      # доказательство воспроизводимости
  python -m terraplan control-cases                                      # контрольные примеры организатора V01–V10
  python -m terraplan info

Коды выхода: 0 — план исполним; 2 — есть жёсткие нарушения (перечислены с правилом, годом, величиной и причиной);
3 — ошибочный ввод (сообщение называет файл, поле и значение); 1 — проверка verify / control-cases не пройдена.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .assumptions import load_assumptions
from .case import CaseError, load_case
from .compare import compare_results, write_comparison
from .engine import Result, simulate
from .export import load_result, write_results
from .plan import PlanError, load_plan
from .scenario import ScenarioError, resolve_scenario

SEVERITY_RU = {"hard": "жёсткое", "guideline": "ориентир", "warning": "предупреждение"}


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("--case", default="data/case", help="каталог с CSV-файлами CASE_INPUT")
    p.add_argument("--assumptions", default="configs/assumptions.yaml", help="YAML-реестр допущений TEAM_ASSUMPTION")
    p.add_argument("--scenarios-dir", default="configs/scenarios", help="каталог сценариев (BASE, MANDATORY_STRESS, TEAM_*)")


def cmd_run(args: argparse.Namespace) -> int:
    case = load_case(args.case)
    a = load_assumptions(args.assumptions)
    plan = load_plan(args.plan, case)
    scenario = resolve_scenario(args.scenario, args.scenarios_dir)
    res = simulate(case, plan, scenario, a)
    out = write_results(res, args.out, xlsx=not args.no_xlsx)
    _print_summary(res)
    print(f"\nрезультаты записаны в {out}")
    return 0 if res.feasible else 2


def _print_summary(res: Result) -> None:
    k = res.kpi
    print(f"план {res.plan_id} | сценарий {res.scenario_id} | исполним: {'ДА' if res.feasible else 'НЕТ'} "
          f"(жёстких нарушений {k['hard_violations']}, отклонений от ориентиров {k['guideline_violations']}, предупреждений {k['warnings']})")
    print(f"полные затраты {k['total_cost_mln']:.1f} млн | PV {k['pv_cost_mln']:.1f} млн при r={k['discount_rate_real']:.2%} | "
          f"затраты на обслуженную т {k['cost_per_served_t_mln']:.3f} млн | обслужено {k['served_total_t']:.1f} т из {k['demand_total_t']:.1f} т | "
          f"дефицит {k['shortage_total_t']:.1f} т | мин. уровень сервиса общий {k['min_service_level_total']:.3f} / критический {k['min_service_level_critical']:.3f}")
    for v in res.violations:
        if v.severity != "warning":
            print(f"  [{SEVERITY_RU.get(v.severity, v.severity)}] {v.rule_id}: {v.message}")


def cmd_compare(args: argparse.Namespace) -> int:
    a = load_result(args.dir_a)
    b = load_result(args.dir_b)
    rows = compare_results(a, b)
    out = Path(args.out)
    write_comparison(rows, out.with_suffix(".csv") if out.suffix else out / "comparison.csv",
                     out.with_suffix(".md") if out.suffix else out / "comparison.md")
    print(f"сравнение записано в {out}")
    return 0


def _resolve_case_dir(manifest: dict, result_dir: Path) -> Path:
    """Manifest path as given; else the same relative path from the repo root above the result dir; else data/case."""
    cand = [Path(manifest.get("case_dir", "data/case")), Path(manifest.get("case_dir_absolute_at_run", ""))]
    for anc in [result_dir.resolve()] + list(result_dir.resolve().parents):
        if (anc / "pyproject.toml").exists():
            cand.append(anc / manifest.get("case_dir", "data/case"))
            cand.append(anc / "data" / "case")
    cand.append(Path("data/case"))
    for p in cand:
        if str(p) and (p / "demand.csv").exists():
            return p
    raise CaseError(f"не удалось найти каталог исходных данных для {result_dir}; укажите --case")


def cmd_verify(args: argparse.Namespace) -> int:
    """Re-run a result directory from its own plan/scenario/assumptions and compare with what was exported."""
    from .assumptions import Assumptions
    from .export import kpi_hash
    from .plan import plan_from_dict
    from .scenario import scenario_from_dict
    d = Path(args.result_dir)
    manifest = json.loads((d / "run_manifest.json").read_text(encoding="utf-8"))
    stored = load_result(d)
    case_dir = args.case or _resolve_case_dir(manifest, d)
    case = load_case(case_dir)
    plan = plan_from_dict(json.loads((d / "plan.json").read_text(encoding="utf-8")), str(d / "plan.json"))
    scenario = scenario_from_dict(json.loads((d / "scenario.json").read_text(encoding="utf-8")), str(d / "scenario.json"))
    res = simulate(case, plan, scenario, Assumptions(stored.assumptions))
    tol = float(args.tolerance)
    problems = []
    if kpi_hash(res.kpi) != manifest["kpi_sha256"]:
        problems.append("kpi_sha256 не совпадает с run_manifest.json")
    for k, v in res.kpi.items():
        w = stored.kpi.get(k)
        if isinstance(v, float) and isinstance(w, float) and v == v and abs(v - w) > tol:
            problems.append(f"показатель {k}: пересчитано {v}, выгружено {w}")
    for a_, b_ in zip(res.years, stored.years):
        for f in ("served_total_t", "losses_t", "closing_t", "shortage_total_t"):
            if abs(getattr(a_, f) - getattr(b_, f)) > tol:
                problems.append(f"{a_.year} {f}: {getattr(a_, f)} против {getattr(b_, f)}")
    for a_, b_ in zip(res.finance, stored.finance):
        if abs(a_.total_mln - b_.total_mln) > tol:
            problems.append(f"{a_.year} total_mln: {a_.total_mln} против {b_.total_mln}")
    n_bal = sum(1 for m in res.months if abs(m.opening_t + m.throughput_t - m.losses_t - m.served_t - m.closing_t) > 1e-9)
    if n_bal:
        problems.append(f"тождество материального баланса нарушено в {n_bal} месяцах")
    print(f"verify {d}: план {res.plan_id} / сценарий {res.scenario_id}; месяцев {len(res.months)}, проверок {len(res.check_matrix)} "
          f"(выполнено {res.kpi['checks_passed']}); тождество баланса выполняется во всех месяцах; допуск {tol}")
    if problems:
        for p_ in problems:
            print("  ОШИБКА:", p_)
        return 1
    print("  ПРОЙДЕНО: пересчитанные результаты совпадают с выгруженными; kpi_sha256 совпадает с run_manifest.json")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    case = load_case(args.case)
    plan = load_plan(args.plan, case)
    print(f"план {plan.plan_id}: структура корректна ({len(plan.orders)} заказов, {len(plan.reservations)} резервирований, {len(plan.investments)} инвестиций)")
    return 0


def cmd_control_cases(args: argparse.Namespace) -> int:
    from .control_cases import run_control_cases
    rows = run_control_cases(Path(args.expected))
    ok = True
    for r in rows:
        ok &= r["passed"]
        print(f"{r['case_id']}: {'ПРОЙДЕН' if r['passed'] else 'НЕ ПРОЙДЕН'}  ожидалось={r['expected']} получено={r['actual']}")
    print("ВСЕ КОНТРОЛЬНЫЕ ПРИМЕРЫ ПРОЙДЕНЫ" if ok else "ЕСТЬ НЕПРОЙДЕННЫЕ КОНТРОЛЬНЫЕ ПРИМЕРЫ")
    return 0 if ok else 1


def cmd_info(args: argparse.Namespace) -> int:
    case = load_case(args.case)
    print(f"каталог данных: {case.source_dir}; горизонт {case.first_year}–{case.last_year}")
    print("спрос (т/год):")
    for d in case.demand:
        print(f"  {d.year}: всего {d.base_total_t:g}, критический {d.base_critical_t:g}, низкий {d.low_total_t:g}, высокий {d.high_total_t:g}")
    print("источники:")
    for s in case.sources.values():
        print(f"  {s.source_id} {s.name}: мощность {s.capacity_t_per_year:g} т/год, цена {s.variable_cost_mln_per_t:g}, резервирование {s.reservation_rate_mln_per_t_year:g}, "
              f"take-or-pay {s.take_or_pay_share:.0%}, срок поставки {s.lead_time_min_value:g}–{s.lead_time_max_value:g} {s.lead_time_unit}, доступен с {s.available_from_year}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="terraplan", description=f"TerraPlan {__version__} — цифровой контур планирования снабжения орбитального топливного узла")
    sub = p.add_subparsers(dest="cmd", required=True)
    ui = sub.add_parser("ui", help="запустить офлайн-интерфейс оператора на localhost (R4)")
    ui.add_argument("--root", default=".", help="корень проекта с data/ и configs/")
    ui.add_argument("--port", type=int, default=8765)
    def cmd_ui(args):
        from .web import serve
        serve(args.root, args.port)
        return 0
    ui.set_defaults(fn=cmd_ui)
    r = sub.add_parser("run", help="рассчитать план в сценарии и выгрузить результаты")
    r.add_argument("--plan", required=True, help="JSON-файл плана (TEAM_DECISION)"); r.add_argument("--scenario", required=True, help="идентификатор или файл сценария")
    r.add_argument("--out", required=True, help="каталог результатов")
    r.add_argument("--no-xlsx", action="store_true", help="не писать results.xlsx"); _common(r); r.set_defaults(fn=cmd_run)
    c = sub.add_parser("compare", help="сравнить два каталога результатов")
    c.add_argument("dir_a"); c.add_argument("dir_b"); c.add_argument("--out", required=True); c.set_defaults(fn=cmd_compare)
    v = sub.add_parser("validate", help="проверить структуру файла плана относительно данных кейса")
    v.add_argument("--plan", required=True); _common(v); v.set_defaults(fn=cmd_validate)
    vf = sub.add_parser("verify", help="повторно рассчитать выгруженный каталог результатов и подтвердить воспроизводимость")
    vf.add_argument("result_dir"); vf.add_argument("--case", default=None); vf.add_argument("--tolerance", default="1e-6"); vf.set_defaults(fn=cmd_verify)
    cc = sub.add_parser("control-cases", help="выполнить контрольные примеры организатора V01–V10")
    cc.add_argument("--expected", default="tests/fixtures/expected_checks.json"); cc.set_defaults(fn=cmd_control_cases)
    i = sub.add_parser("info", help="показать загруженные данные кейса"); _common(i); i.set_defaults(fn=cmd_info)
    args = p.parse_args(argv)
    try:
        return args.fn(args)
    except (CaseError, PlanError, ScenarioError) as exc:
        print(f"ОШИБКА ВВОДА: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())

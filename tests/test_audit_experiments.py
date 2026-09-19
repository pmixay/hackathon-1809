"""Эксперименты, добавленные по итогам независимого аудита 19.09.2026 (A3, A5, A6, A8).

Каждый тест проверяет не текст отчёта, а его числа: отчёт пересчитывается из опубликованного JSON
и сверяется с движком, поэтому устаревший вывод в Markdown не может остаться незамеченным.
"""
import json

import pytest

from conftest import ROOT
from terraplan.assumptions import load_assumptions
from terraplan.engine import intra_month_peak, simulate
from terraplan.plan import load_plan
from terraplan.scenario import resolve_scenario

RESULTS = ROOT / "results"


# ---------------------------------------------------------------- A3 / EXP-16
def test_intra_month_peak_formula_limits():
    """N = 1 — запас сразу после поступления; при росте N пик падает к max(начало, конец)."""
    opening, net, draw = 100.0, 40.0, 30.0
    assert intra_month_peak(opening, net, draw, 1) == pytest.approx(opening + net)
    peaks = [intra_month_peak(opening, net, draw, n) for n in (1, 2, 4, 12, 240)]
    assert peaks == sorted(peaks, reverse=True)                     # монотонно убывает по N
    limit = max(opening, opening + net - draw)
    for n in (12, 240):                                             # сходимость к пределу как draw/N
        assert intra_month_peak(opening, net, draw, n) == pytest.approx(limit + draw / n, abs=1e-9)
    # выдача больше поступления: пик достигается на первой партии и от N не зависит
    assert intra_month_peak(100.0, 5.0, 30.0, 4) == pytest.approx(100.0 + 5.0 / 4)


def test_accepted_plans_do_not_depend_on_the_batching_assumption(case, assumptions):
    """Ключевые планы проходят уже при самом строгом N = 1 — вывод не опирается на дробление поставок."""
    published = json.loads((RESULTS / "intra_month" / "classification.json").read_text(encoding="utf-8"))
    independent = {tuple(x) for x in published["independent"]}
    for plan_name, sid in (("P2z_earth_new_zbo", "BASE"), ("P2z_earth_new_zbo_adapted", "MANDATORY_STRESS"),
                           ("P3_isru_zbo", "BASE"), ("P4_full", "BASE")):
        assert (plan_name, sid) in independent
        a = load_assumptions(ROOT / "configs/assumptions.yaml").with_overrides(intra_month_delivery_batches=1)
        res = simulate(case, load_plan(ROOT / f"configs/plans/{plan_name}.json", case),
                       resolve_scenario(sid, ROOT / "configs/scenarios"), a)
        assert not [v for v in res.violations if v.rule_id == "INTRA_MONTH_PEAK"]
        assert all(m.peak_stock_t <= m.storage_capacity_t + 1e-9 for m in res.months)


# ---------------------------------------------------------------- A5 / EXP-14
def test_adaptive_policy_is_non_anticipative_and_holds_what_it_can_reach():
    detail = json.loads((RESULTS / "adaptive_policy" / "policy_detail.json").read_text(encoding="utf-8"))
    logs = json.loads((RESULTS / "adaptive_policy" / "policy_log.json").read_text(encoding="utf-8"))
    assert len(detail) == 4 and len(logs) == 4

    # решения, принятые до расхождения траекторий, обязаны совпадать во всех ветвях
    def early(log):
        return sorted((d["decided_in"], d["source_id"], d["delivery_month"], round(d["added_t"], 4))
                      for d in log if d["decided_in"] <= "2038-12")
    reference = early(next(iter(logs.values())))
    assert reference, "политика не приняла ни одного решения до расхождения траекторий"
    for key, log in logs.items():
        assert early(log) == reference, f"траектория {key} решает иначе до расхождения — политика видит будущее"

    for key, d in detail.items():
        assert d["in_reach"] == [], f"{key}: политика не удержала ограничение, на которое могла повлиять"
        assert d["out_of_reach"] == ["RESERVE_45D@2038-01"], key       # датировано до наблюдения
        # версия со знанием будущего — не оптимум и не нижняя граница: это то же жадное правило.
        # Проверяется лишь то, что разность мала и причинная политика не дороже (см. adaptive_policy.md).
        assert abs(d["policy"]["pv"] - d["oracle"]["pv"]) < 25.0, key
        assert d["policy"]["pv"] <= d["oracle"]["pv"] + 1e-6, key
        assert d["policy"]["shortage"] == pytest.approx(0.8664, abs=1e-3)   # окно реакции, апрель 2038


def test_reaction_report_claims_only_calendar_feasibility():
    """A5: отчёт EXP-06 больше не утверждает, что объёмы выбраны без знания будущего."""
    text = (RESULTS / "reaction" / "response_rule_check.md").read_text(encoding="utf-8")
    assert "Что НЕ проверяется" in text and "EXP-14" in text
    assert "не использует знание сценария заранее" not in text


# ---------------------------------------------------------------- A6 / EXP-15
def test_joint_schedule_impossibility_is_proved_from_the_case_data(case):
    """Необходимое условие R(y) + SS(<y) <= C + D_base(<y) пересчитывается здесь заново."""
    from terraplan import rules
    published = json.loads((RESULTS / "joint_feasibility" / "necessary_condition.json").read_text(encoding="utf-8"))
    base = resolve_scenario("BASE", ROOT / "configs/scenarios")
    stress = resolve_scenario("MANDATORY_STRESS", ROOT / "configs/scenarios")
    capacity = max(s.capacity_t for s in case.storage.values())
    for row in published:
        y = row["year"]
        prior = [k for k in case.years if k < y]
        d_base = sum(case.demand_row(k).total("base") * base.demand_mult(k) for k in prior)
        d_stress = sum(case.demand_row(k).total("base") * stress.demand_mult(k) for k in prior)
        r_stress = rules.reserve_45d(case.demand_row(y).total("base") * stress.demand_mult(y))
        assert row["required_t"] == pytest.approx(r_stress + d_stress, abs=1e-6)
        assert row["allowed_t"] == pytest.approx(capacity + d_base, abs=1e-6)
        assert row["holds"] == (row["required_t"] <= row["allowed_t"] + 1e-9)
    broken = [r for r in published if not r["holds"]]
    assert [r["year"] for r in broken] == [2040]
    assert broken[0]["gap_t"] == pytest.approx(20.795, abs=1e-3)
    assert broken[0]["max_stress_service_share"] == pytest.approx(0.9808, abs=1e-4)


def test_no_interpolated_schedule_passes_both_scenarios():
    import csv
    with (RESULTS / "joint_feasibility" / "search.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 11
    assert not [r for r in rows if r["base_feasible"] == "True" and r["stress_feasible"] == "True"]


# ---------------------------------------------------------------- A8 / EXP-17
def test_zbo_delay_cost_for_p2z_is_quantified(case):
    """Цена задержки ZBO для выбранного P2z посчитана и воспроизводится движком."""
    detail = json.loads((RESULTS / "zbo_delay" / "zbo_delay.json").read_text(encoding="utf-8"))
    assert {d["delay_months"] for d in detail} == {3, 6, 12}
    for d in detail:
        a = load_assumptions(ROOT / "configs/assumptions.yaml").with_overrides(zbo_commissioning_lag_months=d["delay_months"])
        res = simulate(case, load_plan(ROOT / f"configs/plans/{d['plan']}.json", case),
                       resolve_scenario(d["scenario"], ROOT / "configs/scenarios"), a)
        gaps = {str(v.year): round(v.excess, 3) for v in res.violations if v.rule_id == "RESERVE_45D"}
        assert gaps == d["reserve_gaps"]
        assert res.kpi["pv_cost_mln"] == pytest.approx(d["pv_without_measure"], abs=1e-3)
        assert res.kpi["shortage_total_t"] == pytest.approx(0.0, abs=1e-9)   # страдает резерв, не обслуживание
        # ловушка учёта: задержка СНИЖАЕТ PV, потому что CAPEX и OPEX платятся позже
        assert d["pv_without_measure"] < d["pv_reference"]

    # 12 месяцев в обязательном стрессе объёмом не лечится: мешает потолок потерь
    worst = next(d for d in detail if d["scenario"] == "MANDATORY_STRESS" and d["delay_months"] == 12)
    assert worst["flex_t"] is None and worst["reaction_blocked_by"] == ["STRESS_LOSS_LIMIT"]
    assert worst["price_of_early_mln"] == pytest.approx(12.346, abs=1e-2)


# ---------------------------------------------------------------- A8: объём поставляемых документов
def test_management_note_and_one_pager_have_the_required_length():
    """Кейс: записка 8–12 страниц, отдельное одностраничное резюме. Объём считается по фиксированной вёрстке."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_note", ROOT / "docs" / "build_note.py")
    build_note = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(build_note)

    note = (ROOT / "docs" / "management_note.md").read_text(encoding="utf-8")
    body, appendices = build_note.split_body_and_appendices(note)
    pages = build_note.paginate(build_note.layout_lines(body))
    lo, hi = build_note.NOTE_PAGES
    assert lo <= len(pages) <= hi, f"управленческая записка: {len(pages)} страниц, требуется {lo}–{hi}"

    one = (ROOT / "docs" / "one_pager_scenarios.md").read_text(encoding="utf-8")
    one_pages = build_note.paginate(build_note.layout_lines(one))
    assert len(one_pages) == 1, f"резюме сравнения сценариев: {len(one_pages)} страниц, требуется 1"

    # приложения существуют и на них есть ссылки из тела
    assert appendices.strip(), "приложения записки пусты"
    assert "Подробности — приложение" in body
    for page in pages:
        assert all(len(line) <= build_note.WIDTH for line in page)

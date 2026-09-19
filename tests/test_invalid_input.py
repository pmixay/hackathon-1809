"""Ошибочный ввод должен давать понятное сообщение с именем файла, поля и значением (критерии 5 и 19)."""
import json
from pathlib import Path

import pytest

from conftest import SOURCE_X, copy_case
from terraplan.case import CaseError, load_case
from terraplan.engine import simulate
from terraplan.plan import PlanError, load_plan, plan_from_dict
from terraplan.scenario import ScenarioError, load_scenario


def test_negative_reservation_is_rejected(root):
    with pytest.raises(PlanError) as e:
        plan_from_dict(json.loads((root / "tests/fixtures/invalid_plan_examples/negative_reservation.json").read_text()))
    assert "reserved_capacity_t" in str(e.value) and ">= 0" in str(e.value)


def test_malformed_scenario_without_id(root):
    with pytest.raises(ScenarioError) as e:
        load_scenario(root / "tests/fixtures/invalid_plan_examples/malformed_scenario.json")
    assert "scenario_id" in str(e.value)


def test_over_capacity_reports_excess(root, tmp_path, base, assumptions):
    case_dir = copy_case(tmp_path, extra_source=SOURCE_X)
    case = load_case(case_dir)
    d = json.loads((root / "tests/fixtures/invalid_plan_examples/over_capacity.json").read_text())
    d["decisions"]["capacity_reservations"][0]["source_id"] = "X"   # synthetic Source-X, capacity 10
    res = simulate(case, plan_from_dict(d), base, assumptions)
    v = [x for x in res.violations if x.rule_id == "CAPACITY_EXCEEDED"]
    assert len(v) == 1 and v[0].year == 2035 and v[0].source_id == "X"
    assert v[0].actual == pytest.approx(12) and v[0].limit == pytest.approx(10) and v[0].excess == pytest.approx(2)
    assert not res.feasible


def test_unknown_source_and_missing_keys(case):
    from terraplan.plan import validate_plan
    with pytest.raises(PlanError, match="неизвестный source_id"):
        plan = plan_from_dict({"plan_id": "p", "decisions": {"capacity_reservations": [{"source_id": "Z", "year": 2035, "reserved_capacity_t": 1}],
                                                             "supply_orders": [], "investments": [], "inventory_policy": {}}})
        validate_plan(plan, case)
    with pytest.raises(PlanError, match="decisions.investments обязателен"):
        plan_from_dict({"plan_id": "p", "decisions": {"capacity_reservations": [], "supply_orders": [], "inventory_policy": {}}})
    with pytest.raises(PlanError, match="вне горизонта"):
        validate_plan(plan_from_dict({"plan_id": "p", "decisions": {"capacity_reservations": [], "supply_orders": [{"source_id": "A", "year": 2050, "ordered_t": 1}],
                                                                    "investments": [], "inventory_policy": {}}}), case)


def test_missing_case_file(tmp_path):
    with pytest.raises(CaseError, match="отсутствует файл CASE_INPUT"):
        load_case(tmp_path)


def test_critical_exceeding_total_is_rejected(tmp_path):
    case_dir = copy_case(tmp_path, extra_demand=dict(year=2041, base_total_t=100, base_critical_t=150, low_total_t=80, high_total_t=120, status="TEAM_ASSUMPTION"))
    with pytest.raises(CaseError) as e:
        load_case(case_dir)
    assert "критический спрос 150 т превышает общий спрос 100 т в 2041 г." in str(e.value)
    assert "demand.csv" in str(e.value) and "строка" in str(e.value)


# A2: каждое из этих полей раньше принималось и молча считалось; теперь расчёт не начинается.
@pytest.mark.parametrize("table,column,row_key,value,expect", [
    ("demand.csv", "base_critical_t", "2035", "-80", "base_critical_t"),
    ("demand.csv", "base_total_t", "2035", "nan", "конечным"),
    ("supply_sources.csv", "lead_time_min_value", "A", "-12", "lead_time_min_value"),
    ("supply_sources.csv", "capacity_t_per_year", "A", "-190", "capacity_t_per_year"),
    ("supply_sources.csv", "take_or_pay_share", "A", "1.4", "take_or_pay_share"),
    ("investment_options.csv", "exercise_cost_mln", "ZBO", "-180", "exercise_cost_mln"),
    ("storage_options.csv", "holding_cost_mln_per_t_year", "BASE", "-0.72", "holding_cost_mln_per_t_year"),
    ("storage_options.csv", "capacity_t", "BASE", "-70", "capacity_t"),
])
def test_negative_or_non_finite_case_inputs_are_rejected(tmp_path, root, table, column, row_key, value, expect):
    import shutil
    dst = tmp_path / "case_copy"
    shutil.copytree(root / "data" / "case", dst)
    path = dst / table
    lines = path.read_text(encoding="utf-8").splitlines()
    header = lines[0].split(",")
    idx = header.index(column)
    for n, line in enumerate(lines[1:], 1):
        cells = line.split(",")
        if cells[0] == row_key:
            cells[idx] = value
            lines[n] = ",".join(cells)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(CaseError) as e:
        load_case(dst)
    message = str(e.value)
    assert table in message and expect in message and "строка" in message


def test_negative_capex_cannot_reach_the_engine(case, base, assumptions, root):
    """Движок пропускает нулевые платежи по условию `> 0`; отрицательный CAPEX уменьшил бы стоимость плана."""
    import dataclasses
    from terraplan.case import validate_case
    broken = dataclasses.replace(case, investments=dict(case.investments))
    broken.investments["ZBO"] = dataclasses.replace(case.investments["ZBO"], exercise_cost_mln=-180.0, total_capex_mln=-180.0)
    with pytest.raises(CaseError, match="должен быть >= 0"):
        validate_case(broken)
    with pytest.raises(CaseError):
        simulate(broken, load_plan(root / "configs/plans/P2z_earth_new_zbo.json", case), base, assumptions)


def test_plan_file_not_json(tmp_path, case):
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(PlanError, match="не является корректным JSON"):
        load_plan(p, case)


def test_monthly_profile_rounding_tolerance():
    """A hand-edited 4-decimal monthly profile reopens (ordered_t within 0.001 t of the sum); a real mismatch is rejected."""
    monthly = [round(48.87776 / 12, 4)] * 12
    d = {"plan_id": "p", "decisions": {"capacity_reservations": [], "investments": [], "inventory_policy": {},
                                       "supply_orders": [{"source_id": "B", "year": 2038, "profile": "monthly", "monthly_t": monthly, "ordered_t": round(48.87776, 4)}]}}
    plan = plan_from_dict(d)
    assert plan.orders[0].ordered_t == pytest.approx(sum(monthly))
    d["decisions"]["supply_orders"][0]["ordered_t"] = 49.0
    with pytest.raises(PlanError, match="не равен сумме monthly_t"):
        plan_from_dict(d)


def test_cli_reports_input_error_with_exit_code_3(tmp_path, capsys, root):
    from terraplan.cli import main
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"plan_id": "p", "decisions": {"capacity_reservations": [{"source_id": "A", "year": 2035, "reserved_capacity_t": -5}],
                                                            "supply_orders": [], "investments": [], "inventory_policy": {}}}), encoding="utf-8")
    rc = main(["run", "--plan", str(p), "--scenario", "BASE", "--out", str(tmp_path / "out"), "--case", str(root / "data/case"),
               "--assumptions", str(root / "configs/assumptions.yaml"), "--scenarios-dir", str(root / "configs/scenarios")])
    err = capsys.readouterr().err
    assert rc == 3 and "ОШИБКА ВВОДА" in err and "reserved_capacity_t" in err and "-5" in err


def _plan(orders=None, reservations=None, investments=None, policy=None) -> dict:
    return {"plan_id": "multi", "decisions": {"capacity_reservations": reservations or [], "supply_orders": orders or [],
                                              "investments": investments or [], "inventory_policy": policy or {}}}


def test_all_problems_of_a_plan_are_reported_in_one_pass():
    """Оператор должен увидеть все ошибки сразу, а не исправлять их по одной."""
    with pytest.raises(PlanError) as e:
        plan_from_dict(_plan(
            reservations=[{"source_id": "A", "year": 2035, "reserved_capacity_t": -5}],
            orders=[{"source_id": "B", "year": 2036, "ordered_t": -1},
                    {"source_id": "A", "year": 2037, "profile": "quarterly", "ordered_t": 10}],
            policy={"reserve_mode": "wishful", "allocation_rule": "random"}))
    details = e.value.details
    assert len(details) == 5, [d["message"] for d in details]
    joined = " | ".join(d["message"] for d in details)
    for fragment in ("reserved_capacity_t", "ordered_t", "quarterly", "reserve_mode", "allocation_rule"):
        assert fragment in joined
    assert all(d["path"] for d in details)
    # первое сообщение остаётся заголовком ошибки, поэтому старые обработчики продолжают работать
    assert details[0]["message"] in str(e.value)
    assert "и ещё 4" in str(e.value)


def test_cross_check_reports_every_mismatch_with_the_case(case):
    from terraplan.plan import validate_plan
    plan = plan_from_dict(_plan(
        reservations=[{"source_id": "NOPE", "year": 2035, "reserved_capacity_t": 10},
                      {"source_id": "A", "year": 2099, "reserved_capacity_t": 10}],
        orders=[{"source_id": "A", "year": 2035, "ordered_t": 1}, {"source_id": "A", "year": 2035, "ordered_t": 2}],
        investments=[{"investment_id": "UNKNOWN_OPTION", "decision_year": 2035}]))
    with pytest.raises(PlanError) as e:
        validate_plan(plan, case)
    messages = [d["message"] for d in e.value.details]
    assert len(messages) == 4, messages
    assert any("NOPE" in m for m in messages) and any("2099" in m for m in messages)
    assert any("повторный заказ" in m for m in messages) and any("UNKNOWN_OPTION" in m for m in messages)


def test_a_single_problem_still_reads_as_one_message():
    with pytest.raises(PlanError) as e:
        plan_from_dict(_plan(orders=[{"source_id": "A", "year": 2035, "ordered_t": -3}]))
    assert len(e.value.details) == 1
    assert "и ещё" not in str(e.value)
    assert str(e.value) == e.value.details[0]["message"]


def test_case_and_scenario_errors_expose_the_same_details_field(root, tmp_path):
    with pytest.raises(ScenarioError) as e:
        load_scenario(root / "tests/fixtures/invalid_plan_examples/malformed_scenario.json")
    assert e.value.details and e.value.details[0]["message"] == str(e.value)
    with pytest.raises(CaseError) as e:
        load_case(tmp_path / "missing_case_dir")
    assert e.value.details and e.value.details[0]["message"] == str(e.value)

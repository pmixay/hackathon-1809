"""Проверка правила реакции: план ответа не может использовать информацию, недоступную на момент решения."""
import sys
from dataclasses import replace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from check_stress_response import check, main as checker_main
from terraplan.plan import Investment, Order, load_plan

PLANS = ROOT / "configs" / "plans"


@pytest.fixture(scope="module")
def p3_pair():
    return load_plan(PLANS / "P3_isru_zbo.json"), load_plan(PLANS / "P3_isru_zbo_reactive.json")


def test_reactive_plan_passes_every_rule(p3_pair, case, assumptions):
    fixed, reactive = p3_pair
    viol, rows = check(fixed, reactive, case, assumptions, None, None)
    assert viol == [], [f"{v['rule']} {v['what']}: {v['why']}" for v in viol]
    assert rows, "план реакции должен отличаться от исходного"
    assert all(r["available"] for r in rows)
    # реакция начинается не раньше наблюдения: Emergency 2 мес. -> 2038-05, Earth-Flex 4 мес. -> 2038-07
    deliveries = {(r["source_id"], r["delivery_month"]) for r in rows if r["month"] > 0}
    assert min(m for s, m in deliveries if s == "E") == "2038-05"
    assert min(m for s, m in deliveries if s == "B") == "2038-07"
    assert not any(m < "2038-05" for _, m in deliveries)


def test_checker_exit_code_is_zero_for_the_reaction_benchmark():
    assert checker_main([str(PLANS / "P3_isru_zbo.json"), str(PLANS / "P3_isru_zbo_reactive.json")]) == 0


def test_advance_adapted_plan_is_rejected_as_a_reaction(case, assumptions):
    """Заблаговременно адаптированный план — это не реакция: он меняет решения, принятые до наблюдения."""
    fixed = load_plan(PLANS / "P2z_earth_new_zbo.json")
    adapted = load_plan(PLANS / "P2z_earth_new_zbo_adapted.json")
    viol, _ = check(fixed, adapted, case, assumptions, ["B", "E"], "2038-01")
    rules = {v["rule"] for v in viol}
    assert "I3" in rules and "I4" in rules
    assert any("2036" in v["why"] for v in viol if v["rule"] == "I3")


def test_delivery_one_month_too_early_is_named_with_its_order_month(p3_pair, case, assumptions):
    fixed, reactive = p3_pair
    early = [o for o in reactive.orders if not (o.source_id == "E" and o.year == 2038)]
    profile = [0.0] * 12
    profile[3] = 6.667                                    # поставка в апреле: заказ 2038-02, до наблюдения 2038-03
    early.append(Order("E", 2038, sum(profile), "monthly", profile, reactive=True))
    viol, rows = check(fixed, replace(reactive, orders=early), case, assumptions, None, None)
    i3 = [v for v in viol if v["rule"] == "I3"]
    assert i3 and any("2038-04" in v["what"] and "2038-02" in v["why"] for v in i3)
    assert any(r["delivery_month"] == "2038-04" and not r["available"] for r in rows)


def test_uniform_annual_order_cannot_pass_as_a_reaction_inside_the_observation_year(p3_pair, case, assumptions):
    """Без месячного профиля заказ считается равномерным с января — такую реакцию нельзя отличить от предвидения."""
    fixed, reactive = p3_pair
    orders = [o for o in reactive.orders if not (o.source_id == "B" and o.year == 2038)]
    orders.append(Order("B", 2038, 60.0, "uniform", None, reactive=True))
    viol, _ = check(fixed, replace(reactive, orders=orders), case, assumptions, None, None)
    assert any(v["rule"] == "I3" and "2038-01" in v["what"] for v in viol)


def test_changed_investment_is_rejected(p3_pair, case, assumptions):
    fixed, reactive = p3_pair
    moved = [replace(i, decision_year=i.decision_year + 1) if i.investment_id == "ZBO" else i
             for i in reactive.investments]
    assert moved != reactive.investments
    viol, _ = check(fixed, replace(reactive, investments=moved), case, assumptions, None, None)
    assert any(v["rule"] == "I1" for v in viol)


def test_reservation_for_a_finished_year_is_rejected(p3_pair, case, assumptions):
    """Договорной объём года, закончившегося до наблюдения, уже нельзя пересмотреть."""
    from terraplan.plan import Reservation
    fixed, reactive = p3_pair
    res = list(reactive.reservations) + [Reservation("B", 2036, 50.0)]
    viol, _ = check(fixed, replace(reactive, reservations=res), case, assumptions, None, None)
    assert any(v["rule"] == "I5" and "2036" in v["what"] for v in viol)


def test_missing_observation_month_is_refused(p3_pair, case, assumptions):
    fixed, reactive = p3_pair
    viol, rows = check(fixed, replace(reactive, observation_month=None), case, assumptions, None, None)
    assert rows == [] and viol and viol[0]["rule"] == "I0"

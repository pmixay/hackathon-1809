"""Порог смены победителя: при каких значениях параметров альтернатива становится дешевле рекомендации."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))

from run_sensitivity import (CHALLENGER, CROSSOVER_TOL, RECOMMENDED, case_with_isru_capex, crossover,
                             plan_pv, scaled_prices)


def test_crossover_finds_a_known_root():
    value, reason = crossover(lambda x: x - 1.25, 0.0, 3.0, 1e-4)
    assert reason is None and value == pytest.approx(1.25, abs=1e-4)


def test_crossover_reports_which_side_wins_when_there_is_no_sign_change():
    value, reason = crossover(lambda x: x + 1.0, 0.0, 3.0, 1e-4)
    assert value is None and "дороже" in reason
    value, reason = crossover(lambda x: -x - 1.0, 0.0, 3.0, 1e-4)
    assert value is None and "дешевле" in reason


def test_scaled_prices_multiplies_the_scenario_instead_of_replacing_it(case, stress):
    src = case.sources["A"]
    doubled = scaled_prices(stress, case, 2.0, case.years)
    for y in case.years:
        assert doubled.price_mult(src, y) == pytest.approx(stress.price_mult(src, y) * 2.0)
    assert stress.price_mult(src, 2038) > 1.0, "обязательный стресс поднимает цену 2038 года"
    unchanged = scaled_prices(stress, case, 1.0, case.years)
    assert [unchanged.price_mult(src, y) for y in case.years] == [stress.price_mult(src, y) for y in case.years]
    # каналы вне списка не затронуты
    assert doubled.price_mult(case.sources["E"], 2038) == pytest.approx(stress.price_mult(case.sources["E"], 2038))


def test_recommendation_stays_cheaper_on_the_decision_metric_across_the_price_range(case, assumptions, stress):
    """Метрика выбора — PV заблаговременно адаптированного обязательного стресса."""
    for x in (0.5, 1.0, 3.0):
        sc = scaled_prices(stress, case, x, case.years)
        pv_rec, ok_rec = plan_pv(case, assumptions, sc, RECOMMENDED, True)
        pv_cha, _ = plan_pv(case, assumptions, sc, CHALLENGER, True)
        assert ok_rec, f"рекомендация должна оставаться допустимой при множителе цены {x}"
        assert pv_rec < pv_cha, f"при множителе цены {x} рекомендация должна быть дешевле"


def test_isru_capex_crossover_is_the_only_one_found_on_the_decision_metric(case, assumptions, stress):
    def diff(x: float) -> float:
        c = case_with_isru_capex(case, x)
        return plan_pv(c, assumptions, stress, RECOMMENDED, True)[0] - plan_pv(c, assumptions, stress, CHALLENGER, True)[0]

    value, reason = crossover(diff, 100.0, 1250.0, CROSSOVER_TOL["isru_capex_mln"])
    assert reason is None
    assert 600 < value < 750, value
    assert abs(diff(value)) < 1.0                       # на пороге планы стоят одинаково с точностью до 1 млн
    assert diff(1250.0) < 0 < diff(100.0)               # дешёвый ISRU выигрывает, ISRU по цене кейса — нет


def test_hypothetical_isru_capex_changes_only_that_option(case):
    cheap = case_with_isru_capex(case, 500.0)
    assert cheap.investments["LUNAR_ISRU"].exercise_cost_mln == 500.0
    assert cheap.investments["LUNAR_ISRU"].status == "TEAM_ASSUMPTION"
    assert case.investments["LUNAR_ISRU"].exercise_cost_mln == 1250.0, "исходные данные кейса не изменяются"
    for key, opt in case.investments.items():
        if key != "LUNAR_ISRU":
            assert cheap.investments[key] == opt
    assert cheap.sources == case.sources and cheap.demand == case.demand

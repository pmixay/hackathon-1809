"""Случайные планы: инварианты баланса и отсутствие двойного учёта на произвольных решениях.

Проверка дополняет именованные сценарии: она не сравнивает с эталоном, а требует, чтобы на любом
принятом плане выполнялись тождества, из которых собран расчёт. Seed фиксирован, поэтому набор
планов воспроизводим.
"""
import random

import pytest

from terraplan.engine import simulate
from terraplan.plan import plan_from_dict
from terraplan.rules import take_or_pay_volume

SEED = 20260919
N_PLANS = 40


def random_plan(rng: random.Random, case, index: int) -> dict:
    sources = sorted(case.sources)
    years = case.years
    investments = []
    for inv_id in sorted(case.investments):
        if rng.random() < 0.5:
            investments.append({"investment_id": inv_id, "decision_year": rng.choice(years[:3]), "decision_month": rng.randint(1, 12)})
    reservations, orders = [], []
    for sid in sources:
        cap = case.sources[sid].capacity_t_per_year
        for y in years:
            if rng.random() < 0.6:
                reserved = round(rng.uniform(0, cap), 3)
                reservations.append({"source_id": sid, "year": y, "reserved_capacity_t": reserved})
                if rng.random() < 0.8:
                    orders.append({"source_id": sid, "year": y, "ordered_t": round(rng.uniform(0, reserved), 3)})
    return {"plan_id": f"random_{index}", "scenario_id": "BASE",
            "decisions": {"capacity_reservations": reservations, "supply_orders": orders,
                          "investments": investments,
                          "inventory_policy": {"reserve_mode": rng.choice(["physical", "emergency_contract"]),
                                               "allocation_rule": rng.choice(["critical_first", "proportional"])}}}


@pytest.fixture(scope="module")
def random_runs(case, base, stress, assumptions):
    rng = random.Random(SEED)
    runs = []
    for i in range(N_PLANS):
        plan = plan_from_dict(random_plan(rng, case, i))
        runs.append((plan, simulate(case, plan, base, assumptions), simulate(case, plan, stress, assumptions)))
    return runs


def test_random_plans_keep_the_material_balance(random_runs):
    for plan, *results in random_runs:
        for res in results:
            prev_close = None
            for m in res.months:
                opening = prev_close if prev_close is not None else m.opening_t
                assert m.opening_t == pytest.approx(opening, abs=1e-9), f"{plan.plan_id} {m.year}-{m.month}: разрыв между месяцами"
                assert m.closing_t == pytest.approx(m.opening_t + m.throughput_t - m.losses_t - m.served_t, abs=1e-6), \
                    f"{plan.plan_id} {m.year}-{m.month}: баланс не сходится"
                prev_close = m.closing_t


def test_random_plans_never_produce_negative_stock_or_service_above_one(random_runs):
    for plan, *results in random_runs:
        for res in results:
            assert all(m.closing_t >= -1e-9 for m in res.months), f"{plan.plan_id}: отрицательный запас"
            assert all(m.served_t <= m.demand_t + 1e-9 for m in res.months), f"{plan.plan_id}: обслужено больше спроса"
            for y in res.years:
                assert -1e-9 <= y.service_level_total <= 1 + 1e-9
                assert y.served_total_t + y.shortage_total_t == pytest.approx(y.demand_total_t, abs=1e-6)
                assert y.served_critical_t <= y.served_total_t + 1e-9


def test_random_plans_charge_losses_once_on_gross_throughput(random_runs):
    for plan, *results in random_runs:
        for res in results:
            for m in res.months:
                assert m.losses_t == pytest.approx(m.throughput_t * m.loss_rate, abs=1e-9), \
                    f"{plan.plan_id} {m.year}-{m.month}: потери начислены не один раз на валовой приход"


def test_random_plans_never_double_count_take_or_pay(random_runs, case):
    for plan, *results in random_runs:
        for res in results:
            for sy in res.source_years:
                if sy.period != "year":
                    continue
                expected = take_or_pay_volume(sy.ordered_t, sy.reserved_period_t, case.sources[sy.source_id].take_or_pay_share)
                assert sy.payable_volume_t == pytest.approx(expected, abs=1e-9)
                assert sy.procurement_mln == pytest.approx(sy.price_mln_per_t * sy.payable_volume_t, abs=1e-9)
                assert sy.take_or_pay_topup_mln == pytest.approx(sy.price_mln_per_t * max(0.0, sy.payable_volume_t - sy.ordered_t), abs=1e-6)


def test_random_plans_costs_decompose_and_stress_is_never_cheaper_physically(random_runs):
    for plan, res_base, res_stress in random_runs:
        for res in (res_base, res_stress):
            for f in res.finance:
                assert f.total_mln == pytest.approx(f.procurement_mln + f.reservation_mln + f.holding_mln + f.fixed_opex_mln + f.capex_mln, abs=1e-9)
                assert 0.0 <= f.take_or_pay_topup_mln <= f.procurement_mln + 1e-9
            assert sum(f.total_mln for f in res.finance) == pytest.approx(res.kpi["total_cost_mln"], abs=1e-6)
        # тот же план в обязательном стрессе не может поставить больше тонн, чем в BASE
        assert res_stress.kpi["served_total_t"] <= res_base.kpi["served_total_t"] + 1e-6
        assert res_base.kpi["capex_total_mln"] == pytest.approx(res_stress.kpi["capex_total_mln"], abs=1e-9)


def test_random_plans_are_reproducible_from_the_seed(case, base, assumptions):
    rng_a, rng_b = random.Random(SEED), random.Random(SEED)
    for i in range(5):
        pa, pb = random_plan(rng_a, case, i), random_plan(rng_b, case, i)
        assert pa == pb
        ka = simulate(case, plan_from_dict(pa), base, assumptions).kpi
        kb = simulate(case, plan_from_dict(pb), base, assumptions).kpi
        assert ka == kb

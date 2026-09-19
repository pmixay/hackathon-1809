"""Control formulas of the organizer (CALCULATION_RULES.md), as pure functions.

These primitives are used by the engine and are verified directly by the organizer
control vectors V01–V10 in tests/test_control_cases.py. Units: tonnes (t), mln units.
"""
from __future__ import annotations

DAYS_PER_YEAR = 365  # organizer control convention
RESERVE_DAYS = 45


def material_balance(opening_t: float, delivered_t: float, losses_t: float, served_t: float) -> float:
    """I_end = I_start + Q_delivered - Losses - Q_served  (V01)."""
    return opening_t + delivered_t - losses_t - served_t


def serve(available_t: float, demand_t: float) -> tuple[float, float]:
    """Return (served, shortage). Served never exceeds physical availability; inventory never negative (V02)."""
    served = min(max(available_t, 0.0), max(demand_t, 0.0))
    shortage = max(0.0, demand_t - served)
    return served, shortage


def losses_on_throughput(gross_inflow_t: float, loss_rate: float) -> float:
    """Losses = Throughput * loss_rate, applied once to gross inflow (V06)."""
    return gross_inflow_t * loss_rate


def reserve_45d(annual_total_demand_t: float, days: float = RESERVE_DAYS) -> float:
    """R_y = D_y * 45 / 365 (V07)."""
    return annual_total_demand_t * days / DAYS_PER_YEAR


def take_or_pay_volume(ordered_t: float, reserved_period_t: float, top_share: float) -> float:
    """Q_pay = max(Q_order, take_or_pay_share * Q_reserved_period) (V03/V04)."""
    return max(ordered_t, top_share * reserved_period_t)


def variable_payment(price_mln_per_t: float, ordered_t: float, reserved_period_t: float, top_share: float) -> float:
    """VariablePayment = price * Q_pay. Take-or-pay is inside max(); never added again (V04)."""
    return price_mln_per_t * take_or_pay_volume(ordered_t, reserved_period_t, top_share)


def take_or_pay_topup_payment(price_mln_per_t: float, ordered_t: float, reserved_period_t: float, top_share: float) -> float:
    """Premium share of the variable payment: price * (Q_pay - Q_order), i.e. volume paid but not ordered.

    This is a decomposition of `variable_payment`, not an extra charge: payment = price*Q_order + this premium.
    """
    return price_mln_per_t * max(0.0, take_or_pay_volume(ordered_t, reserved_period_t, top_share) - ordered_t)


def reservation_payment(rate_mln_per_t_year: float, annual_reserved_capacity_t: float, period_fraction: float) -> float:
    """ReservationPayment = rate * annual_reserved_capacity * period_fraction (V05)."""
    return rate_mln_per_t_year * annual_reserved_capacity_t * period_fraction


def capacity_check(reserved_t: float, capacity_t: float) -> float:
    """Return excess above capacity (0 if within). V08 expects excess 2 for 12 vs 10."""
    return max(0.0, reserved_t - capacity_t)


def total_demand_with_nested_critical(total_t: float, critical_t: float) -> float:
    """Critical demand is a subset of total demand; total stays total (V09)."""
    if critical_t > total_t:
        raise ValueError(f"critical demand {critical_t} exceeds total demand {total_t}")
    return total_t


def actual_delivery(planned_t: float, actual_delivery_share: float) -> float:
    """Stress delivery = planned * share. Reliability is NOT applied again (V10)."""
    return planned_t * actual_delivery_share


def service_level(served_t: float, demand_t: float) -> float:
    """SL = served / demand; defined as 1.0 when demand is zero (explicit boundary rule)."""
    if demand_t <= 0:
        return 1.0
    return served_t / demand_t


def present_value(cash_flow: float, rate: float, periods: float) -> float:
    """PV_t = CF_t / (1+r)^(t - t0)."""
    return cash_flow / (1.0 + rate) ** periods

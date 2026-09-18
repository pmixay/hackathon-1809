"""Organizer control vectors V01–V10 evaluated with the engine's primitive rules."""
from __future__ import annotations

import json
from pathlib import Path

from . import rules


def run_control_cases(expected_path: Path) -> list[dict]:
    expected = {e["case_id"]: e["expected"] for e in json.loads(Path(expected_path).read_text(encoding="utf-8"))}
    actual: dict[str, dict] = {}
    actual["V01"] = {"closing_inventory_t": rules.material_balance(10, 30, 2, 25)}
    served, shortage = rules.serve(0 + 8 - 0, 10)
    actual["V02"] = {"served_t": served, "shortage_t": shortage, "closing_inventory_t": rules.material_balance(0, 8, 0, served)}
    q_pay = rules.take_or_pay_volume(50, 100, 0.70)
    actual["V03"] = {"payable_volume_t": q_pay, "variable_payment_mln": rules.variable_payment(2, 50, 100, 0.70)}
    actual["V04"] = {"variable_payment_mln": rules.variable_payment(2, 50, 100, 0.70)}  # no second TOP line
    actual["V05"] = {"reservation_payment_mln": rules.reservation_payment(0.4, 100, 0.5)}
    actual["V06"] = {"losses_t": rules.losses_on_throughput(20, 0.05)}
    actual["V07"] = {"reserve_t": rules.reserve_45d(365)}
    excess = rules.capacity_check(12, 10)
    actual["V08"] = {"violation": "CAPACITY_EXCEEDED" if excess > 0 else "", "excess_t": excess}
    actual["V09"] = {"total_demand_t": rules.total_demand_with_nested_critical(100, 60)}
    actual["V10"] = {"actual_delivery_t": rules.actual_delivery(20, 0.50)}  # reliability 0.80 NOT applied
    rows = []
    for cid, exp in expected.items():
        got = actual.get(cid, {})
        ok = all(k in got and (got[k] == v if isinstance(v, str) else abs(float(got[k]) - float(v)) < 1e-9) for k, v in exp.items())
        rows.append({"case_id": cid, "expected": exp, "actual": got, "passed": ok})
    return rows

"""Independent recalculation of an exported result using ONLY the CSV files and the csv module.

No terraplan import: this is the organizer-required independent control calculation. It re-derives
yearly totals from the monthly trace, procurement/reservation from the source schedule and the case's
supply_sources.csv, finance totals from components, and PV from the disclosed rate, then compares with
the exported yearly_balance.csv / financial_breakdown.csv.  Usage: python tests/independent_recalc.py <results_dir> [case_dir]
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

TOL = 1e-5   # exported CSVs carry 6 decimals


def rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def recalc(result_dir: Path, case_dir: Path) -> list[str]:
    problems: list[str] = []
    trace = rows(result_dir / "inventory_trace.csv")
    yearly = {int(r["year"]): r for r in rows(result_dir / "yearly_balance.csv")}
    sched = rows(result_dir / "source_schedule.csv")
    fin = {int(r["year"]): r for r in rows(result_dir / "financial_breakdown.csv")}
    sources = {r["source_id"]: r for r in rows(case_dir / "supply_sources.csv")}
    assumptions = {r["key"]: json.loads(r["value"]) for r in rows(result_dir / "assumptions.csv")}
    r = float(assumptions["discount_rate_real"]); t0 = int(assumptions["discount_t0_year"])
    offset = {"start": 0.0, "mid": 0.5, "end": 1.0}[assumptions.get("discount_timing", "start")]
    paid_on_order = bool(assumptions.get("undelivered_volume_paid", True))

    # 1. monthly balance identity and non-negative stock
    for m in trace:
        o, thr, l, s, c = (float(m[k]) for k in ("opening_t", "throughput_t", "losses_t", "served_t", "closing_t"))
        if abs(o + thr - l - s - c) > TOL:
            problems.append(f"balance identity fails {m['year']}-{m['month']}")
        if c < -1e-9:
            problems.append(f"negative stock {m['year']}-{m['month']}")
        if abs(l - thr * float(m["loss_rate"])) > TOL:
            problems.append(f"losses != throughput*rate {m['year']}-{m['month']}")
    # 2. yearly totals from months
    for y, yr in yearly.items():
        ms = [m for m in trace if int(m["year"]) == y]
        for mk, yk in (("served_t", "served_total_t"), ("losses_t", "losses_t"), ("throughput_t", "throughput_t"), ("shortage_t", "shortage_total_t")):
            tot = sum(float(m[mk]) for m in ms)
            if abs(tot - float(yr[yk])) > TOL:
                problems.append(f"{y} {yk}: months sum {tot} vs yearly {yr[yk]}")
        if abs(float(ms[0]["opening_t"]) - float(yr["opening_t"])) > TOL or abs(float(ms[-1]["closing_t"]) - float(yr["closing_t"])) > TOL:
            problems.append(f"{y} opening/closing mismatch")
        D = float(yr["demand_total_t"]); served = float(yr["served_total_t"])
        sl = served / D if D > 0 else 1.0
        if abs(sl - float(yr["service_level_total"])) > TOL:
            problems.append(f"{y} service level {sl} vs {yr['service_level_total']}")
        if abs(D * 45 / 365 - float(yr["reserve_required_t"])) > TOL:
            problems.append(f"{y} reserve_required")
    # 3. contracts: payable volume and payments from the case's TOP shares and rates
    proc_by_year: dict[int, float] = {}; resv_by_year: dict[int, float] = {}
    for s_ in sched:
        y = int(s_["year"]); src = sources[s_["source_id"]]
        ordered = float(s_["ordered_t"]); reserved = float(s_["reserved_capacity_t"]); f = float(s_["period_fraction"])
        if s_["period"] == "year":
            base = ordered if paid_on_order else min(ordered, float(s_["actual_delivery_t"]))
            q_pay = max(base, float(src["take_or_pay_share"]) * reserved * f)
            price = float(src["variable_cost_mln_per_t"]) * float(s_["price_multiplier"])
        else:  # preparatory purchase: paid at price, reservation for the stated fraction of a year
            q_pay = ordered; price = float(src["variable_cost_mln_per_t"]) * float(s_["price_multiplier"])
        proc = price * q_pay
        resv = float(src["reservation_rate_mln_per_t_year_capacity"]) * reserved * f
        if abs(q_pay - float(s_["payable_volume_t"])) > TOL or abs(proc - float(s_["procurement_mln"])) > TOL or abs(resv - float(s_["reservation_payment_mln"])) > TOL:
            problems.append(f"{y} {s_['source_id']} contract payment mismatch: q_pay {q_pay} proc {proc} resv {resv}")
        fy = min(yearly) if s_["period"] != "year" else y
        proc_by_year[fy] = proc_by_year.get(fy, 0.0) + proc; resv_by_year[fy] = resv_by_year.get(fy, 0.0) + resv
    # 4. finance: components, totals, PV
    cum = 0.0
    for y, fr in fin.items():
        if abs(proc_by_year.get(y, 0.0) - float(fr["procurement_mln"])) > 1e-5:
            problems.append(f"{y} procurement {proc_by_year.get(y, 0.0)} vs {fr['procurement_mln']}")
        if abs(resv_by_year.get(y, 0.0) - float(fr["reservation_mln"])) > 1e-5:
            problems.append(f"{y} reservation {resv_by_year.get(y, 0.0)} vs {fr['reservation_mln']}")
        hold = sum(float(m["holding_cost_mln"]) for m in trace if int(m["year"]) == y)
        if abs(hold - float(fr["holding_mln"])) > TOL:
            problems.append(f"{y} holding {hold} vs {fr['holding_mln']}")
        total = sum(float(fr[k]) for k in ("procurement_mln", "reservation_mln", "holding_mln", "fixed_opex_mln", "capex_mln"))
        if abs(total - float(fr["total_mln"])) > TOL:
            problems.append(f"{y} total {total} vs {fr['total_mln']}")
        pv = total / (1 + r) ** (y - t0 + offset)
        if abs(pv - float(fr["pv_total_mln"])) > TOL:
            problems.append(f"{y} PV {pv} vs {fr['pv_total_mln']}")
        cum += float(fr["capex_mln"])
        if abs(cum - float(fr["cumulative_capex_mln"])) > TOL:
            problems.append(f"{y} cumulative capex")
    return problems


if __name__ == "__main__":
    rd = Path(sys.argv[1]); cd = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("data/case")
    probs = recalc(rd, cd)
    print(f"независимый пересчёт по CSV {rd}: {'ПРОЙДЕНО' if not probs else 'ОШИБКА'}")
    for p in probs:
        print("  ", p)
    sys.exit(1 if probs else 0)

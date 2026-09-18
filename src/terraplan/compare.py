"""Scenario / plan comparison on a common basis (same units, horizon, discount rate)."""
from __future__ import annotations

import csv
from pathlib import Path

from .engine import Result

YEAR_METRICS = [("demand_total_t", "Demand total, t"), ("served_total_t", "Served total, t"), ("service_level_total", "SL total"),
                ("service_level_critical", "SL critical"), ("shortage_total_t", "Shortage, t"), ("throughput_t", "Delivered (actual), t"),
                ("losses_t", "Losses, t"), ("loss_ratio", "Losses/throughput"), ("opening_t", "Opening stock, t"), ("closing_t", "Closing stock, t"),
                ("reserve_required_t", "45-day reserve, t")]
FIN_METRICS = [("procurement_mln", "Procurement, mln"), ("reservation_mln", "Reservation, mln"), ("holding_mln", "Holding, mln"),
               ("fixed_opex_mln", "Fixed OPEX, mln"), ("capex_mln", "CAPEX, mln"), ("total_mln", "Total, mln"), ("pv_total_mln", "PV total, mln")]
KPI_METRICS = ["total_cost_mln", "pv_cost_mln", "cost_per_served_t_mln", "pv_cost_per_served_t_mln", "served_total_t", "shortage_total_t",
               "shortage_critical_t", "min_service_level_total", "min_service_level_critical", "losses_total_t", "capex_total_mln",
               "take_or_pay_idle_t", "hard_violations", "guideline_violations"]


def compare_results(a: Result, b: Result, label_a: str | None = None, label_b: str | None = None) -> list[dict]:
    la = label_a or f"{a.plan_id}/{a.scenario_id}"
    lb = label_b or f"{b.plan_id}/{b.scenario_id}"
    rows: list[dict] = []
    for m in KPI_METRICS:
        va, vb = a.kpi.get(m), b.kpi.get(m)
        rows.append(dict(section="kpi", metric=m, year="", a=va, b=vb, delta=(vb - va) if isinstance(va, (int, float)) and isinstance(vb, (int, float)) else "", label_a=la, label_b=lb))
    ya = {y.year: y for y in a.years}
    yb = {y.year: y for y in b.years}
    for year in sorted(set(ya) | set(yb)):
        for key, name in YEAR_METRICS:
            va = getattr(ya[year], key) if year in ya else None
            vb = getattr(yb[year], key) if year in yb else None
            rows.append(dict(section="yearly", metric=name, year=year, a=va, b=vb, delta=(vb - va) if va is not None and vb is not None else "", label_a=la, label_b=lb))
    fa = {f.year: f for f in a.finance}
    fb = {f.year: f for f in b.finance}
    for year in sorted(set(fa) | set(fb)):
        for key, name in FIN_METRICS:
            va = getattr(fa[year], key) if year in fa else None
            vb = getattr(fb[year], key) if year in fb else None
            rows.append(dict(section="finance", metric=name, year=year, a=va, b=vb, delta=(vb - va) if va is not None and vb is not None else "", label_a=la, label_b=lb))
    # decisions that differ
    def orders(r: Result):
        return {(o["source_id"], o["year"]): o["ordered_t"] for o in r.plan["decisions"]["supply_orders"]}
    def resv(r: Result):
        return {(o["source_id"], o["year"]): o["reserved_capacity_t"] for o in r.plan["decisions"]["capacity_reservations"]}
    oa, ob, ra, rb = orders(a), orders(b), resv(a), resv(b)
    for key in sorted(set(oa) | set(ob)):
        if abs(oa.get(key, 0) - ob.get(key, 0)) > 1e-6:
            rows.append(dict(section="decision:order", metric=f"ordered_t {key[0]}", year=key[1], a=oa.get(key, 0), b=ob.get(key, 0), delta=ob.get(key, 0) - oa.get(key, 0), label_a=la, label_b=lb))
    for key in sorted(set(ra) | set(rb)):
        if abs(ra.get(key, 0) - rb.get(key, 0)) > 1e-6:
            rows.append(dict(section="decision:reservation", metric=f"reserved_t {key[0]}", year=key[1], a=ra.get(key, 0), b=rb.get(key, 0), delta=rb.get(key, 0) - ra.get(key, 0), label_a=la, label_b=lb))
    ia = {i["investment_id"]: i for i in a.plan["decisions"]["investments"]}
    ib = {i["investment_id"]: i for i in b.plan["decisions"]["investments"]}
    for key in sorted(set(ia) | set(ib)):
        da = f"{ia[key]['decision_year']}-{ia[key].get('decision_month', 1):02d}" if key in ia else "—"
        db = f"{ib[key]['decision_year']}-{ib[key].get('decision_month', 1):02d}" if key in ib else "—"
        if da != db:
            rows.append(dict(section="decision:investment", metric=key, year="", a=da, b=db, delta="", label_a=la, label_b=lb))
    va = {(v.rule_id, v.year) for v in a.violations if v.severity != "warning"}
    vb = {(v.rule_id, v.year) for v in b.violations if v.severity != "warning"}
    for key in sorted(va | vb, key=lambda k: (str(k[0]), k[1] or 0)):
        rows.append(dict(section="violation", metric=key[0], year=key[1] or "", a="yes" if key in va else "", b="yes" if key in vb else "", delta="", label_a=la, label_b=lb))
    return rows


def write_comparison(rows: list[dict], path_csv: str | Path, path_md: str | Path | None = None) -> None:
    p = Path(path_csv)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["section", "metric", "year", "a", "b", "delta"])
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})
    if path_md:
        fmt = lambda v: f"{v:,.3f}" if isinstance(v, float) else ("" if v is None else str(v))
        la, lb = (rows[0]["label_a"], rows[0]["label_b"]) if rows else ("A", "B")
        lines = [f"# Comparison: {la} vs {lb}", "", "| Section | Metric | Year | " + la + " | " + lb + " | Δ (B−A) |", "|---|---|---:|---:|---:|---:|"]
        for r in rows:
            lines.append(f"| {r['section']} | {r['metric']} | {r['year']} | {fmt(r['a'])} | {fmt(r['b'])} | {fmt(r['delta'])} |")
        Path(path_md).write_text("\n".join(lines) + "\n", encoding="utf-8")

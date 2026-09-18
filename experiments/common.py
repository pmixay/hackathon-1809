"""Shared strategy definitions and helpers for the experiment scripts.

All strategies are TEAM_DECISION drafts produced by the greedy merit-order builder (src/terraplan/planner.py).
They are saved to configs/plans/ so the jury can edit them by hand and re-run the engine.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from terraplan.assumptions import load_assumptions  # noqa: E402
from terraplan.case import load_case  # noqa: E402
from terraplan.engine import Result, simulate  # noqa: E402
from terraplan.export import write_results  # noqa: E402
from terraplan.plan import Plan, save_plan  # noqa: E402
from terraplan.planner import build_plan  # noqa: E402
from terraplan.scenario import resolve_scenario  # noqa: E402

CASE_DIR = ROOT / "data" / "case"
ASSUMPTIONS = ROOT / "configs" / "assumptions.yaml"
SCENARIOS = ROOT / "configs" / "scenarios"
PLANS = ROOT / "configs" / "plans"
RESULTS = ROOT / "results"

EARTH_NEW_2035 = dict(investment_id="EARTH_NEW", option_year=2035, option_month=1, decision_year=2035, decision_month=1)
ISRU_2036 = dict(investment_id="LUNAR_ISRU", decision_year=2036, decision_month=1)
ZBO_2037 = dict(investment_id="ZBO", decision_year=2037, decision_month=7)

STRATEGIES: dict[str, dict] = {
    "P1_earth_only": dict(plan_id="P1_earth_only", description="Earth-Core + Earth-Flex only, no investments (reference: shows capacity ceiling 300 t/yr)",
                          reservation_caps={"A": 190, "B": 110}, investments=[]),
    "P2_earth_new": dict(plan_id="P2_earth_new", description="Earth-Core + Earth-Flex + Earth-New option exercised 2035-01 (commissioned 2037-01); no ZBO, no ISRU",
                         reservation_caps={"A": 190, "B": 110, "C": 130}, investments=[EARTH_NEW_2035]),
    "P2z_earth_new_zbo": dict(plan_id="P2z_earth_new_zbo", description="P2 plus ZBO modernization 2037-07 (needed for the stress loss ceiling)",
                              reservation_caps={"A": 190, "B": 110, "C": 130}, investments=[EARTH_NEW_2035, ZBO_2037]),
    "P3_isru_zbo": dict(plan_id="P3_isru_zbo", description="Earth-Core + Earth-Flex + Lunar-ISRU pilot (CAPEX 2036-01, first delivery 2038-03) + ZBO 2037-07",
                        reservation_caps={"A": 190, "B": 110, "D": 120}, investments=[ISRU_2036, ZBO_2037]),
    "P4_full": dict(plan_id="P4_full", description="All options: Earth-New 2035-01, ISRU 2036-01, ZBO 2037-07; Emergency capped at 15 % of demand (CAPEX 1790 ≤ 1800 by 2037)",
                    reservation_caps={"A": 190, "B": 110, "C": 130, "D": 120, "E": 80}, investments=[EARTH_NEW_2035, ISRU_2036, ZBO_2037]),
}


def load_all():
    case = load_case(CASE_DIR)
    a = load_assumptions(ASSUMPTIONS)
    return case, a


def scenario(sid: str):
    return resolve_scenario(sid, SCENARIOS)


def run_and_save(case, plan: Plan, scen, a, out_dir: Path, xlsx: bool = True) -> Result:
    res = simulate(case, plan, scen, a)
    write_results(res, out_dir, xlsx=xlsx)
    return res


def kpi_row(res: Result, **extra) -> dict:
    k = res.kpi
    return dict(plan_id=res.plan_id, scenario_id=res.scenario_id, feasible=res.feasible, hard_violations=k["hard_violations"],
                guideline_violations=k["guideline_violations"], total_cost_mln=k["total_cost_mln"], pv_cost_mln=k["pv_cost_mln"],
                cost_per_served_t_mln=k["cost_per_served_t_mln"], pv_cost_per_served_t_mln=k["pv_cost_per_served_t_mln"],
                capex_total_mln=k["capex_total_mln"], procurement_total_mln=k["procurement_total_mln"], reservation_total_mln=k["reservation_total_mln"],
                holding_total_mln=k["holding_total_mln"], fixed_opex_total_mln=k["fixed_opex_total_mln"],
                served_total_t=k["served_total_t"], shortage_total_t=k["shortage_total_t"], shortage_critical_t=k["shortage_critical_t"],
                min_sl_total=k["min_service_level_total"], min_sl_critical=k["min_service_level_critical"], losses_total_t=k["losses_total_t"],
                take_or_pay_idle_t=k["take_or_pay_idle_t"],
                violations="; ".join(sorted({f"{v.rule_id}@{v.year}" for v in res.violations if v.severity != "warning"})), **extra)


def write_table(rows: list[dict], path_csv: Path, path_md: Path | None = None, title: str = "") -> None:
    path_csv.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with path_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in r.items()})
    if path_md:
        keys = list(rows[0].keys())
        fmt = lambda v: (f"{v:,.3f}" if isinstance(v, float) else str(v))
        lines = [f"# {title}", "", "| " + " | ".join(keys) + " |", "|" + "|".join("---" for _ in keys) + "|"]
        for r in rows:
            lines.append("| " + " | ".join(fmt(r[k]) for k in keys) + " |")
        path_md.write_text("\n".join(lines) + "\n", encoding="utf-8")

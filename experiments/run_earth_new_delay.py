"""EXP-09: Earth-New preparation delay 0/3/6/12 months, fixed P2z under BASE.

Copy case data, extend only C's preparation lead time, freeze its original monthly
delivery slots. Missed slots are not caught up. CAPEX and orders remain committed.
The engine is unchanged; every exported run can be replayed with its case copy.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import shutil
from copy import deepcopy
from dataclasses import asdict, replace
from pathlib import Path

from common import ASSUMPTIONS, CASE_DIR, PLANS, RESULTS, ROOT, load_all, scenario
from provenance import HASH_FORMAT, SCHEMA_VERSION, input_hashes, sha256, write_json, write_text
from run_reverse_stress import failure_violations
from terraplan.case import load_case
from terraplan.engine import simulate
from terraplan.export import write_results
from terraplan.plan import load_plan
from terraplan.scenario import scenario_from_dict

DELAYS = (0, 3, 6, 12)
PLAN_PATH = PLANS / "P2z_earth_new_zbo.json"


def freeze_earth_new_schedule(original, reference):
    """Fix planned delivery slots, avoiding uniform-profile compression after a delay."""
    plan = deepcopy(original)
    plan.plan_id = original.plan_id + "_fixed_calendar"
    scheduled = {(d["year"], d["month"]): d["planned_t"] for d in reference.deliveries if d["source_id"] == "C"}
    for order in plan.orders:
        if order.source_id == "C":
            order.profile = "monthly"
            order.monthly_t = [scheduled.get((order.year, m), 0.0) for m in range(1, 13)]
            # Keep the original contractual ordered_t; only its profile is explicit.
            if not math.isclose(sum(order.monthly_t), order.ordered_t, abs_tol=1e-6):
                raise ValueError("reference C calendar does not reproduce the committed annual order")
    plan.meta = dict(plan.meta, experiment="EXP-09", fixed_calendar=True,
                     missed_slot_policy="unavailable slots lost; no catch-up, refund or substitute orders")
    return plan


def copy_delayed_case(destination, delay):
    """Create an isolated CASE_INPUT copy; only Earth-New lead times are overlaid."""
    if delay not in DELAYS:
        raise ValueError(f"delay must be one of {DELAYS}")
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for path in sorted(CASE_DIR.glob("*.csv")):
        shutil.copyfile(path, destination / path.name)
    path = destination / "supply_sources.csv"
    if delay:
        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            fields, rows = reader.fieldnames, list(reader)
        for row in rows:
            if row["source_id"] == "C":
                if row["lead_time_unit"] != "month":
                    raise ValueError("EXP-09 requires Earth-New lead time in months")
                for key in ("lead_time_min_value", "lead_time_max_value"):
                    row[key] = str(float(row[key]) + delay)
                row["status"] = "TEAM_ASSUMPTION"
                row["notes"] += f"; EXP-09 preparation delay +{delay} months, original investment dates frozen"
        with path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    return load_case(destination)


def delay_scenario(base, delay):
    data = deepcopy(base.to_dict())
    data.update(scenario_id=f"TEAM_EARTH_NEW_DELAY_{delay:02d}M", status="TEAM_ASSUMPTION",
                label=f"Earth-New preparation delay {delay} months; BASE demand/prices")
    data["changes"] += [dict(status="TEAM_ASSUMPTION", source_id="C", delay_months=delay,
                             applied_to="case copy: C lead_time_min_value and lead_time_max_value",
                             original_preparation_months="18..24", frozen="investment dates, orders, reservations and delivery slots",
                             missed_slots="lost, no catch-up or compensation")]
    return scenario_from_dict(data)


def chronological_failures(result, reference):
    """Date year-only source-unavailable checks by the first frozen missed slot.

    When C is unavailable for an entire year, the engine emits an annual check
    without a month. The experiment can locate the first missed delivery exactly.
    Only report copies are annotated; standard engine exports remain untouched.
    """
    actual = {(m.year, m.month): m.inflow_by_source.get("C", 0.0) for m in result.months}
    first_missed = {}
    for d in reference.deliveries:
        if d["source_id"] == "C" and d["planned_t"] > 0 and actual[(d["year"], d["month"])] == 0:
            first_missed[d["year"]] = min(first_missed.get(d["year"], 12), d["month"])
    violations = []
    for v in result.violations:
        if v.rule_id == "SOURCE_NOT_AVAILABLE" and v.source_id == "C" and v.month is None and v.year in first_missed:
            v = replace(v, month=first_missed[v.year],
                        message=v.message + " [EXP-09: month dated from first missed frozen delivery slot]")
        violations.append(v)
    return failure_violations(replace(result, violations=violations))


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def run_experiment(out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    case, assumptions = load_all()
    base = scenario("BASE")
    original = load_plan(PLAN_PATH, case)
    reference = simulate(case, original, base, assumptions)
    if failure_violations(reference):
        raise ValueError("the reference P2z plan must pass before applying the delay")
    plan = freeze_earth_new_schedule(original, reference)
    comparison, yearly, runs = [], [], []
    for delay in DELAYS:
        relative = f"delay_{delay:02d}m"
        run_dir = out / relative
        modified = copy_delayed_case(run_dir / "case", delay)
        sc = delay_scenario(base, delay)
        a = assumptions.with_overrides(earth_new_preparation_delay_months=delay)
        a.entries["earth_new_preparation_delay_months"].update(
            unit="months", range=list(DELAYS), status="TEAM_ASSUMPTION",
            justification="EXP-09 overlay applied to Earth-New source lead times on a case copy; not a core-engine parameter")
        res = simulate(modified, plan, sc, a)
        write_results(res, run_dir, xlsx=False)
        # Adapt only the file-hash portion of this experiment's standard manifest.
        # Core semantic plan/scenario/assumption/KPI hashes retain their own format.
        case_hashes = {p.name: sha256(p) for p in sorted((run_dir / "case").glob("*.csv"))}
        core_manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))
        core_manifest.update(case_file_hash_format=HASH_FORMAT, case_file_sha256=case_hashes)
        write_json(run_dir / "run_manifest.json", core_manifest)
        violations = chronological_failures(res, reference)
        first = violations[0] if violations else None
        reserve_violations = [v for v in violations if v.rule_id == "RESERVE_45D"]
        commissioning = next(i.commissioning_date for i in res.investments if i.investment_id == "EARTH_NEW")
        c_rows = [s for s in res.source_years if s.source_id == "C" and s.period == "year"]
        delta_components = {key: res.kpi[key] - reference.kpi[key] for key in
                            ("procurement_total_mln", "reservation_total_mln", "holding_total_mln", "fixed_opex_total_mln", "capex_total_mln")}
        row = dict(delay_months=delay, commissioning=commissioning,
                   missed_earth_new_t=sum(max(0.0, s.ordered_t - s.actual_delivery_t) for s in c_rows),
                   shortage_t=res.kpi["shortage_total_t"], critical_shortage_t=res.kpi["shortage_critical_t"],
                   min_service_total=res.kpi["min_service_level_total"], min_service_critical=res.kpi["min_service_level_critical"],
                   reserve_failed_years=";".join(str(v.year) for v in reserve_violations),
                   max_reserve_gap_t=max(max(0.0, y.reserve_required_t - y.opening_t) for y in res.years),
                   total_cost_mln=res.kpi["total_cost_mln"], pv_cost_mln=res.kpi["pv_cost_mln"],
                   delta_total_mln=res.kpi["total_cost_mln"] - reference.kpi["total_cost_mln"],
                   delta_pv_mln=res.kpi["pv_cost_mln"] - reference.kpi["pv_cost_mln"],
                   hard_violations=res.kpi["hard_violations"], guideline_violations=res.kpi["guideline_violations"],
                   first_rule=first.rule_id if first else None, first_year=first.year if first else None,
                   first_month=first.month if first else None)
        comparison.append(row)
        for y in res.years:
            yearly.append(dict(delay_months=delay, year=y.year, demand_t=y.demand_total_t,
                               shortage_t=y.shortage_total_t, critical_shortage_t=y.shortage_critical_t,
                               service_total=y.service_level_total, service_critical=y.service_level_critical,
                               opening_t=y.opening_t, reserve_required_t=y.reserve_required_t, reserve_ok=y.reserve_ok,
                               reserve_gap_t=max(0.0, y.reserve_required_t - y.opening_t), closing_t=y.closing_t))
        runs.append(dict(**row, result_dir=relative, kpi=res.kpi, scenario=sc.to_dict(), assumptions=a.entries,
                         delta_components_mln=delta_components,
                         first_violation=asdict(first) if first else None,
                         first_reserve_violation=asdict(reserve_violations[0]) if reserve_violations else None,
                         violations=[asdict(v) for v in violations],
                         source_schedule=[asdict(s) for s in c_rows],
                          case_sha256=case_hashes))
    paths = [PLAN_PATH, ASSUMPTIONS, Path(base.source_file), Path(__file__), ROOT / "experiments/common.py",
             ROOT / "experiments/run_reverse_stress.py"]
    paths += sorted(CASE_DIR.glob("*.csv")) + sorted((ROOT / "src/terraplan").glob("*.py"))
    report = dict(experiment_id="EXP-09", python=platform.python_version(), random_seed=None,
                  schema_version=SCHEMA_VERSION, hash_format=HASH_FORMAT, input_sha256=input_hashes(paths),
                  method=dict(status="TEAM_ASSUMPTION", plan=original.plan_id, reference="BASE", delays_months=list(DELAYS),
                              factor="only Earth-New preparation lead time on a copy of case data",
                              scheduling="freeze original C monthly delivery slots; no catch-up or substitution",
                              contracts="original orders and investment payment dates frozen; no refund for missed fuel; reservation prorated by engine availability",
                              failure="hard violations or 97%/99% service guidelines; earliest year/month, annual checks at December",
                              first_violation_timing="year-only C unavailability is dated by the first missed frozen delivery; engine exports unchanged",
                              costs="engine cash costs only; no invented delay penalties, compensation or mission-loss valuation",
                              reproducibility="summary CSV/JSON deterministic; standard export envelope contains generation timestamps"),
                  original_plan=original.to_dict(), frozen_plan=plan.to_dict(), reference_kpi=reference.kpi,
                  comparison=comparison, yearly=yearly, runs=runs)
    write_json(out / "report.json", report)
    write_csv(out / "comparison.csv", comparison)
    write_csv(out / "yearly.csv", yearly)
    lines = ["# EXP-09 Earth-New preparation delay: fixed P2z / BASE", "",
             "Only Earth-New preparation is delayed; original CAPEX, orders, reservations and delivery slots are frozen.",
             "Missed slots are lost, not redistributed. Other sources do not substitute. Prices and demand are BASE.", "",
             "| Delay, mo | Commissioned | Missed C, t | Shortage, t | Min SL total / critical | Reserve failed years | Max reserve gap, t | PV cost, mln | Delta PV, mln | First violation |",
             "|---:|---|---:|---:|---|---|---:|---:|---:|---|"]
    for row in comparison:
        first = f"{row['first_rule']} @ {row['first_year']}-{row['first_month'] or 12:02d}" if row["first_rule"] else "none"
        lines.append(f"| {row['delay_months']} | {row['commissioning']} | {row['missed_earth_new_t']:.6f} | {row['shortage_t']:.6f} | "
                     f"{row['min_service_total']:.6f} / {row['min_service_critical']:.6f} | {row['reserve_failed_years'] or 'none'} | "
                     f"{row['max_reserve_gap_t']:.6f} | {row['pv_cost_mln']:.6f} | {row['delta_pv_mln']:.6f} | {first} |")
    lines += ["", "## Interpretation and reproduction", "",
              "- First operational failure is reported separately from the first reserve failure in report.json; yearly.csv gives all annual service and reserve values.",
              "  Year-only SOURCE_NOT_AVAILABLE checks are dated from the first missed frozen delivery in the experiment report; standard engine exports keep the original check.",
              "- A 100% service level does not mean compliance: stock can cover demand while the required 45-day reserve is violated.",
              "- Lower cash cost is not a risk benefit: missed fuel remains payable, but holding falls and reservation fees are prorated to availability.",
              "  No delay damages, refunds or recovery orders are priced. Unchanged annual orders may exceed the delayed channel's prorated reservation.",
              "- delay_XXm/ contains standard CSV/JSON exports and the actual case copy used for calculation.",
              "  Replay with: python -m terraplan verify results/earth_new_delay/delay_03m --case results/earth_new_delay/delay_03m/case",
              "- The scenario IDs are TEAM_*; service failures count in the experiment even when the engine labels them guidelines."]
    text = "\n".join(lines) + "\n"
    write_text(out / "summary.md", text)
    return report, text


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=RESULTS / "earth_new_delay")
    args = parser.parse_args(argv)
    _, text = run_experiment(args.out)
    print(text)


if __name__ == "__main__":
    main()

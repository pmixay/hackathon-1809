"""EXP-08: minimum practical P3 protections against the EXP-07 uncertainty set.

Search a 0.1 net-tonne stock grid and monthly ZBO dates for a default 1% square.
Reservation-only controls keep orders unchanged, including a full-headroom test.
All costs are engine-computed deltas against the same unprotected adapted P3.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import platform
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path

from common import ASSUMPTIONS, PLANS, RESULTS, ROOT, load_all, scenario
from run_reverse_stress import RAYS, YEARS, bisect_boundary, failure_violations, shocked_scenario
from terraplan.engine import simulate
from terraplan.plan import Reservation, load_plan

DEFAULT_TARGET = 0.01


def inventory_plan(original, case, net_t):
    """Pre-commit Flex deliveries in July-December 2037, after existing ZBO startup.

    Round EXTRA monthly deliveries up to 0.0001 t. Reserve enough annualized
    capacity for the monthly peak (a conservative experiment-specific convention).
    """
    plan = deepcopy(original)
    plan.plan_id = f"{original.plan_id}_stock_{net_t:g}t"
    order = plan.order("B", 2037)
    loss = case.storage["ZBO"].loss_rate_on_throughput
    extra_monthly = math.ceil(net_t / (6 * (1 - loss)) * 1e4 - 1e-9) / 1e4
    monthly = [order.ordered_t / 12] * 12
    for m in range(6, 12):
        monthly[m] += extra_monthly
    order.profile, order.monthly_t, order.ordered_t = "monthly", monthly, sum(monthly)
    for r in plan.reservations:
        if (r.source_id, r.year) == ("B", 2037):
            r.reserved_capacity_t = max(r.reserved_capacity_t, math.ceil(max(monthly) * 12 * 1e3 - 1e-9) / 1e3)
    return plan


def reservation_plan(original, case, extra_per_year=None):
    """Reserve cheapest available headroom B then E, 2038-2040; place no extra orders.

    None reserves ALL B/E headroom. Existing A/D are already fully reserved;
    Earth-New requires an investment and is outside this single-measure family.
    """
    plan = deepcopy(original)
    plan.plan_id = f"{original.plan_id}_reservation_{extra_per_year if extra_per_year is not None else 'full'}"
    for y in YEARS:
        remaining = math.inf if extra_per_year is None else extra_per_year
        for sid in ("B", "E"):
            old = plan.reserved(sid, y)
            extra = min(remaining, case.sources[sid].capacity_t_per_year - old)
            if extra <= 0:
                continue
            r = next((r for r in plan.reservations if (r.source_id, r.year) == (sid, y)), None)
            if r is None:
                plan.reservations.append(Reservation(sid, y, extra))
            else:
                r.reserved_capacity_t += extra
            remaining -= extra
    return plan


def early_zbo_plan(original, months_earlier):
    plan = deepcopy(original)
    plan.plan_id = f"{original.plan_id}_zbo_{months_earlier}mo_earlier"
    zbo = next(i for i in plan.investments if i.investment_id == "ZBO")
    idx = zbo.decision_year * 12 + zbo.decision_month - 1 - months_earlier
    zbo.decision_year, month = divmod(idx, 12)
    zbo.decision_month = month + 1
    return plan


def result_summary(result):
    return dict(kpi=result.kpi, failures=[asdict(v) for v in failure_violations(result)],
                finance=[asdict(f) for f in result.finance],
                reserves=[dict(year=y.year, opening_t=y.opening_t, required_t=y.reserve_required_t,
                               slack_t=y.opening_t - y.reserve_required_t) for y in result.years])


def frontier(case, plan, stress, assumptions):
    rows = []
    for u, v in RAYS:
        def evaluate(t):
            return simulate(case, plan, shocked_scenario(stress, case, u * t, v * t), assumptions)
        lo, hi = bisect_boundary(lambda t: bool(failure_violations(evaluate(t))))
        failed = evaluate(hi) if hi is not None else None
        rows.append(dict(demand_direction=u, isru_direction=v, pass_radius=lo, fail_radius=hi,
                         demand_fail=u * hi if hi is not None else None,
                         isru_reduction_fail=v * hi if hi is not None else None,
                         first_violation=asdict(failure_violations(failed)[0]) if failed else None))
    return rows


def analyze(target=DEFAULT_TARGET):
    if not math.isfinite(target) or not 0 < target <= 0.5:
        raise ValueError("target must be finite and in (0, 0.5]")
    case, a = load_all()
    stress = scenario("MANDATORY_STRESS")
    original = load_plan(PLANS / "P3_isru_zbo_adapted.json", case)
    baseline = simulate(case, original, stress, a)
    corner = shocked_scenario(stress, case, target, target)
    trials, selections = [], {}

    def trial(family, value, plan):
        ref = simulate(case, plan, stress, a)
        stressed = simulate(case, plan, corner, a)
        ref_fail, target_fail = failure_violations(ref), failure_violations(stressed)
        first = target_fail[0] if target_fail else None
        row = dict(family=family, value=value, reference_pass=not ref_fail, target_pass=not target_fail,
                   delta_pv_mln=ref.kpi["pv_cost_mln"] - baseline.kpi["pv_cost_mln"],
                   target_first_rule=first.rule_id if first else None,
                   target_first_year=first.year if first else None)
        trials.append(row)
        return row

    # All levels before the first success are evaluated; do not assume feasibility
    # is monotone in stock size (storage capacity could impose an upper bound).
    loss = case.storage["ZBO"].loss_rate_on_throughput
    monthly_room = case.sources["B"].capacity_t_per_year / 12 - original.order("B", 2037).ordered_t / 12
    stock_max_steps = math.floor(monthly_room * 6 * (1 - loss) * 10)
    stock_steps = list(range(stock_max_steps + 1))
    zbo = next(i for i in original.investments if i.investment_id == "ZBO")
    earliest_zbo_year = max(case.first_year, case.storage["ZBO"].available_from_year)
    zbo_steps = list(range((zbo.decision_year - earliest_zbo_year) * 12 + zbo.decision_month))
    for family, steps, make_plan in (
        ("physical_stock", stock_steps, lambda n: inventory_plan(original, case, n / 10)),
        ("early_zbo", zbo_steps, lambda n: early_zbo_plan(original, n)),
    ):
        found = None
        last_feasible = None
        for n in steps:
            value = n / 10 if family == "physical_stock" else n
            plan = make_plan(n)
            row = trial(family, value, plan)
            if row["reference_pass"]:
                last_feasible = (value, plan)
            if row["reference_pass"] and row["target_pass"]:
                found = (value, plan)
                break
        selected = found or last_feasible
        selections[family] = dict(minimum=found[0] if found else None,
                                  selected_value=selected[0], plan=selected[1],
                                  status="target_met" if found else "target_unreachable_in_family")

    # A 1 t/year practical unit and the maximum are sufficient: with fixed orders
    # reservations cannot change physical deliveries at ANY intermediate level.
    reserve_unit = reservation_plan(original, case, 1)
    reserve_full = reservation_plan(original, case)
    trial("reservation_only", 1, reserve_unit)
    trial("reservation_only", "full_headroom", reserve_full)
    selections["reservation_only"] = dict(minimum=None, status="no_physical_effect_at_any_level",
                                          selected_value="full_headroom", plan=reserve_full)

    # If early ZBO alone falls short, size only the residual stock requirement.
    # This is explicitly a combination, never credited to the ZBO-only row.
    early = selections["early_zbo"]["plan"]
    combined = None
    for n in stock_steps:
        plan = inventory_plan(early, case, n / 10)
        row = trial("early_zbo_plus_stock", n / 10, plan)
        if row["reference_pass"] and row["target_pass"]:
            combined = plan
            selections["early_zbo_plus_stock"] = dict(minimum=n / 10, selected_value=n / 10,
                                                       status="target_met", zbo_months_earlier=selections["early_zbo"]["selected_value"])
            break

    plans = [("without_measure", original), ("physical_stock", selections["physical_stock"]["plan"]),
             ("reservation_1t_per_year", reserve_unit), ("reservation_full", reserve_full),
             ("zbo_1month_earlier", early_zbo_plan(original, 1)), ("early_zbo", early)]
    if combined is not None:
        plans.append(("early_zbo_plus_stock", combined))
    variants = {}
    for name, plan in plans:
        ref = simulate(case, plan, stress, a)
        at_target = simulate(case, plan, corner, a)
        components = {}
        for key in ("procurement_total_mln", "reservation_total_mln", "holding_total_mln", "fixed_opex_total_mln", "capex_total_mln"):
            components[key] = ref.kpi[key] - baseline.kpi[key]
        variants[name] = dict(plan=plan.to_dict(), reference=result_summary(ref), target=result_summary(at_target),
                              delta_pv_mln=ref.kpi["pv_cost_mln"] - baseline.kpi["pv_cost_mln"],
                              delta_total_mln=ref.kpi["total_cost_mln"] - baseline.kpi["total_cost_mln"],
                              delta_components_mln=components, boundary=frontier(case, plan, stress, a),
                              delivery_calendar=ref.deliveries)
    paths = [PLANS / "P3_isru_zbo_adapted.json", ASSUMPTIONS, Path(stress.source_file), Path(__file__),
             ROOT / "experiments/run_reverse_stress.py", ROOT / "experiments/common.py"]
    paths += sorted((ROOT / "data/case").glob("*.csv")) + sorted((ROOT / "src/terraplan").glob("*.py"))
    return dict(experiment_id="EXP-08", python=platform.python_version(), random_seed=None,
                input_sha256={p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
                method=dict(status="TEAM_ASSUMPTION", target=target, uncertainty_set=f"0 <= d,s <= {target}",
                            reference="MANDATORY_STRESS; same shock definition and failure criterion as EXP-07",
                            rationale="operational protection target, not an empirical probability or a global cost optimum",
                            stock_step_net_t=0.1, reservation_step_t_per_year=1, zbo_step_months=1,
                            stock_schedule="extra Flex July-December 2037; orders March-August, 4 months lead",
                            stock_rounding="extra monthly gross tonnes rounded up to 0.0001; reserve >= monthly peak * 12",
                            zbo_range=f"2037-07 back to {earliest_zbo_year}-01 (CASE_INPUT availability); orders unchanged, saved losses retained as stock",
                            stock_range_net_t=[0, stock_max_steps / 10],
                            boundary_tolerance=1e-12, search_domain=[0, 0.5],
                            reservation_semantics="right to capacity only; no extra orders, no fictitious physical stock",
                            combination="selected early ZBO plus minimum residual stock; explicitly separate from single measures"),
                reference_scenario=stress.to_dict(), target_scenario=corner.to_dict(), assumptions=a.entries,
                selections={key: {k: v for k, v in sel.items() if k != "plan"} for key, sel in selections.items()},
                trials=trials, variants=variants)


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_report(report, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    write_csv(out / "sizing.csv", report["trials"])
    rows, boundaries = [], []
    for name, variant in report["variants"].items():
        diagonal = next(b for b in variant["boundary"] if b["demand_direction"] == b["isru_direction"])
        first = diagonal["first_violation"]
        rows.append(dict(variant=name, delta_pv_mln=variant["delta_pv_mln"], delta_total_mln=variant["delta_total_mln"],
                         reference_pv_mln=variant["reference"]["kpi"]["pv_cost_mln"],
                         target_pass=not variant["target"]["failures"],
                         pass_radius=diagonal["pass_radius"], fail_radius=diagonal["fail_radius"],
                         first_rule=first["rule_id"] if first else None, first_year=first["year"] if first else None))
        for b in variant["boundary"]:
            first = b["first_violation"] or {}
            boundaries.append(dict(variant=name, **{k: v for k, v in b.items() if k != "first_violation"},
                                   first_rule=first.get("rule_id"), first_year=first.get("year"), first_month=first.get("month"),
                                   actual=first.get("actual"), limit=first.get("limit"), excess=first.get("excess")))
        # Standalone plans can be reopened with the existing CLI and any scenario.
        (out / f"{name}.plan.json").write_text(json.dumps(variant["plan"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_csv(out / "comparison.csv", rows)
    write_csv(out / "boundary.csv", boundaries)
    lines = ["# EXP-08 P3 protection measures: without -> with", "",
             f"Target: additional demand +{report['method']['target']:.2%} and ISRU relative reduction {report['method']['target']:.2%}, 2038-2040.",
             "Reference environment is MANDATORY_STRESS. Costs are deltas against the same adapted P3, mln constant-2035 units.",
             "Practical minima within defined measure families: stock 0.1 net t, capacity 1 t/year, ZBO 1 month.", "",
             "| Variant | Extra PV, mln | Extra nominal total, mln | Target passes | Failure radius, % | First failure |",
             "|---|---:|---:|---|---:|---|"]
    for row in rows:
        radius = "none in domain" if row["fail_radius"] is None else f"{row['fail_radius'] * 100:.9f}"
        lines.append(f"| {row['variant']} | {row['delta_pv_mln']:.6f} | {row['delta_total_mln']:.6f} | "
                     f"{row['target_pass']} | {radius} | {row['first_rule']} @ {row['first_year']} |")
    lines += ["", "## Sizing", ""]
    for family, sel in report["selections"].items():
        lines.append(f"- {family}: minimum={sel['minimum']}; reported level={sel['selected_value']}; {sel['status']}.")
    lines += ["", "## Interpretation", "",
              "- Stock is actually purchased and delivered before 2038. Its price includes procurement, additional peak-capacity reservation and holding.",
              "- Capacity-only has no finite protective minimum for this fixed-order test: even all available B/E headroom leaves deliveries and the boundary unchanged.",
              "  The 1 t/year row is a cost diagnostic, not a recommended protection. Activation would require extra orders, lead times and a separate response policy.",
              "- Early ZBO retains the fuel saved from lower pre-2038 losses. Orders are held fixed; reducing procurement by the same amount would remove this buffer.",
              "  Additional costs include earlier CAPEX in PV, extra fixed OPEX and holding. Nominal CAPEX is unchanged; lag stays at the original 0-month assumption.",
              "- Every smaller stock/ZBO level is recorded in sizing.csv. Both the no-additional-shock reference and the target must pass.",
              "  For fixed plans, the diagonal is the worst point of the uncertainty square; boundary.csv includes all nine EXP-07 directions.",
              "- report.json contains input/code hashes, assumptions, plans, yearly finance/reserves, target violations and delivery calendars.",
              "  Units of shock coordinates in CSV/JSON are fractions, not percent. No probability model is used."]
    text = "\n".join(lines) + "\n"
    (out / "summary.md").write_text(text, encoding="utf-8")
    return text


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=float, default=DEFAULT_TARGET)
    parser.add_argument("--out", type=Path, default=RESULTS / "protection_measures")
    args = parser.parse_args(argv)
    try:
        report = analyze(args.target)
    except ValueError as exc:
        parser.error(str(exc))
    print(write_report(report, args.out))


if __name__ == "__main__":
    main()

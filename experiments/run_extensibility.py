"""EXP-05: extensibility check on a COPY of the dataset — add synthetic Source-X and year 2041 (TEAM_ASSUMPTION).

The engine is not modified. Outputs: results/extensibility/case_copy/ (the edited copy), results/extensibility/run/.
"""
import csv
import shutil

from common import CASE_DIR, RESULTS, STRATEGIES, load_all, run_and_save
from terraplan.case import load_case
from terraplan.planner import build_plan
from terraplan.scenario import scenario_from_dict

SOURCE_X = dict(source_id="X", name="Source-X", capacity_t_per_year=60, variable_cost_mln_per_t=5.5, reservation_rate_mln_per_t_year_capacity=0.2,
                take_or_pay_share=0.3, lead_time_min_value=3, lead_time_max_value=3, lead_time_unit="month", reliability_profile="constant:0.95",
                available_from_year=2039, status="TEAM_ASSUMPTION", notes="синтетический шестой источник для проверки расширяемости; не данные организатора")
DEMAND_2041 = dict(year=2041, base_total_t=450, base_critical_t=290, low_total_t=360, high_total_t=562.5, status="TEAM_ASSUMPTION")


def append_row(path, row):
    with path.open(encoding="utf-8", newline="") as f:
        r = csv.DictReader(f)
        fields, rows = r.fieldnames, list(r)
    rows.append({k: str(row.get(k, "")) for k in fields})
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    _, a = load_all()
    copy = RESULTS / "extensibility" / "case_copy"
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(CASE_DIR, copy)
    append_row(copy / "supply_sources.csv", SOURCE_X)
    append_row(copy / "demand.csv", DEMAND_2041)
    (copy / "README_COPY.md").write_text("Копия data/case со строками TEAM_ASSUMPTION: Source-X (60 т/год, 5,5 млн/т, с 2039 г.) и спрос 2041 г. "
                                         "(450 т всего / 290 т критического: экстраполяция роста 2040 г. на +15 %). Контрольные расчёты эту копию не используют.\n", encoding="utf-8")
    case = load_case(copy)
    sc = scenario_from_dict({"scenario_id": "TEAM_2041_SOURCE_X", "status": "TEAM_ASSUMPTION",
                             "changes": ["+Source-X 60 т/год с 2039 г. (5,5 млн/т, резервирование 0,2, take-or-pay 30 %)", "+спрос 2041 г. 450/290 т (экстраполяция)",
                                         "лимиты CAPEX и правило 45 дней сохранены как в исходном наборе (лимит CAPEX через 2041 г. не добавлялся)"]})
    strat = dict(STRATEGIES["P3_isru_zbo"], plan_id="P3_isru_zbo_ext2041", reservation_caps={"A": 190, "B": 110, "D": 120, "X": 60})
    plan = build_plan(case, sc, strat, a)
    res = run_and_save(case, plan, sc, a, RESULTS / "extensibility" / "run")
    print(f"extensibility run: years={len(res.years)} sources={sorted(case.sources)} feasible={res.feasible} PV={res.kpi['pv_cost_mln']:.1f}")
    for s in res.source_years:
        if s.source_id == "X" and s.ordered_t > 0:
            print(f"  Source-X {s.year}: ordered {s.ordered_t:.1f} t, delivered {s.actual_delivery_t:.1f} t, procurement {s.procurement_mln:.1f} mln")
    for v in res.violations:
        if v.severity != "warning":
            print("  ", v.severity, v.rule_id, v.message)


if __name__ == "__main__":
    main()

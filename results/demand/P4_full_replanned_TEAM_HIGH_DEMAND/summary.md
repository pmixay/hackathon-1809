# P4_full_team_high_demand — TEAM_HIGH_DEMAND (Высокий спрос (проверка чувствительности, данные организатора))

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 13,113.254 |
| pv_cost_mln | 10,594.783 |
| cost_per_served_t_mln | 7.838 |
| pv_cost_per_served_t_mln | 6.333 |
| served_total_t | 1,673.000 |
| demand_total_t | 1,673.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 34.357 |
| capex_total_mln | 1,790.000 |
| procurement_total_mln | 10,336.927 |
| reservation_total_mln | 575.670 |
| holding_total_mln | 158.657 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 110.0 | 88.0 | 110.0 | 1.000 | 1.000 | 0.0 | 120.9 | 5.44 | 13.6 | 19.0 | 13.6 | yes | BASE |
| 2036 | 154.0 | 115.5 | 154.0 | 1.000 | 1.000 | 0.0 | 168.4 | 7.58 | 19.0 | 25.8 | 19.0 | yes | BASE |
| 2037 | 209.0 | 148.5 | 209.0 | 1.000 | 1.000 | 0.0 | 228.3 | 6.51 | 25.8 | 38.5 | 25.8 | yes | ZBO |
| 2038 | 312.5 | 212.5 | 312.5 | 1.000 | 1.000 | 0.0 | 327.2 | 3.93 | 38.5 | 49.3 | 38.5 | yes | ZBO |
| 2039 | 400.0 | 262.5 | 400.0 | 1.000 | 1.000 | 0.0 | 415.8 | 4.99 | 49.3 | 60.1 | 49.3 | yes | ZBO |
| 2040 | 487.5 | 312.5 | 487.5 | 1.000 | 1.000 | 0.0 | 493.4 | 5.92 | 60.1 | 60.1 | 60.1 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 875.7 | 56.5 | 11.7 | 0.0 | 360.0 | 1304.0 | 1304.0 |
| 2036 | 1043.8 | 75.8 | 16.1 | 0.0 | 1250.0 | 2385.7 | 2209.0 |
| 2037 | 1449.7 | 97.0 | 22.5 | 6.0 | 180.0 | 1755.1 | 1504.7 |
| 2038 | 1742.2 | 96.7 | 25.7 | 82.0 | 0.0 | 1946.6 | 1545.3 |
| 2039 | 2289.0 | 117.2 | 39.4 | 82.0 | 0.0 | 2527.6 | 1857.9 |
| 2040 | 2936.4 | 132.5 | 43.3 | 82.0 | 0.0 | 3194.2 | 2173.9 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 120.9 | 120.9 | 120.9 | 6.20 | 120.9 | 749.4 | 54.4 |
| 2036 | Earth-Core | 168.4 | 168.4 | 168.4 | 6.20 | 168.4 | 1043.8 | 75.8 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 38.3 | 38.3 | 38.3 | 7.10 | 38.3 | 271.7 | 11.5 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2038 | Earth-New | 37.2 | 37.2 | 37.2 | 7.10 | 37.2 | 264.2 | 11.2 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-New | 105.8 | 105.8 | 105.8 | 7.10 | 105.8 | 751.0 | 31.7 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 53.4 | 53.4 | 53.4 | 8.90 | 53.4 | 475.4 | 8.0 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |

## Check matrix (every rule x year)

| Rule | Year | Metric | Actual | Limit | Op | Result | Severity |
|---|---:|---|---:|---:|---|:---:|---|
| BASE_CRITICAL_SERVICE | 2035 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2036 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2037 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2038 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2039 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2040 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2035 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2036 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2037 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2038 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2039 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2040 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| CAPEX_2037 | 2035 | cumulative_capex | 360.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2036 | cumulative_capex | 1610.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2037 | cumulative_capex | 1790.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2040 | 2035 | cumulative_capex | 360.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2036 | cumulative_capex | 1610.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2037 | cumulative_capex | 1790.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2038 | cumulative_capex | 1790.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2039 | cumulative_capex | 1790.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2040 | cumulative_capex | 1790.0000 | 2800.0000 | <= | OK | hard |
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 13.5617 | 13.5616 | >= | OK | hard |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 18.9864 | 18.9863 | >= | OK | hard |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 25.7672 | 25.7671 | >= | OK | hard |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 38.5276 | 38.5274 | >= | OK | hard |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 49.3153 | 49.3151 | >= | OK | hard |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 60.1030 | 60.1027 | >= | OK | hard |
| EMERGENCY_BASE_STREAK | 2035 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2036 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2037 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2038 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2039 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2040 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| STORAGE_OVERFLOW | 2035 | max_end_of_month_stock_t | 18.9864 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2035 | reserved_A_t_per_year | 120.8640 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2035 | ordered_A_t | 120.8636 | 120.8640 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2035 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2035 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2036 | max_end_of_month_stock_t | 25.7672 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2036 | reserved_A_t_per_year | 168.3570 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2036 | ordered_A_t | 168.3569 | 168.3570 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2036 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2036 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2037 | max_end_of_month_stock_t | 38.5276 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_C_t_per_year | 38.2660 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_C_t | 38.2659 | 38.2660 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 0.0000 | 1.0000 | == | VIOLATED | hard |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2038 | max_end_of_month_stock_t | 49.3153 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_C_t_per_year | 37.2150 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_C_t | 37.2143 | 37.2150 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_D_t | 100.0000 | 100.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 0.0000 | 1.0000 | == | VIOLATED | hard |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2039 | max_end_of_month_stock_t | 60.1030 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_C_t_per_year | 105.7770 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_C_t | 105.7770 | 105.7770 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_D_t | 120.0000 | 120.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2040 | max_end_of_month_stock_t | 60.1030 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 53.4220 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 53.4211 | 53.4220 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_C_t_per_year | 130.0000 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_C_t | 130.0000 | 130.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_D_t | 120.0000 | 120.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |

## Constraint checks

No violations.

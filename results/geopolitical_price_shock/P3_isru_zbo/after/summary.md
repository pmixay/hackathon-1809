# P3_isru_zbo — TEAM_GEOPOLITICAL_PRICE_SHOCK (EXP-11: геополитический ценовой шок Core/Flex +25% в 2038–2039)

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 11,249.838 |
| pv_cost_mln | 9,091.370 |
| cost_per_served_t_mln | 8.093 |
| pv_cost_per_served_t_mln | 6.541 |
| served_total_t | 1,390.000 |
| demand_total_t | 1,390.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 29.492 |
| capex_total_mln | 1,430.000 |
| procurement_total_mln | 8,970.477 |
| reservation_total_mln | 467.634 |
| holding_total_mln | 129.727 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 203.2 | 5.79 | 23.4 | 30.8 | 23.4 | yes | ZBO |
| 2038 | 250.0 | 170.0 | 250.0 | 1.000 | 1.000 | 0.0 | 261.8 | 3.14 | 30.8 | 39.5 | 30.8 | yes | ZBO |
| 2039 | 320.0 | 210.0 | 320.0 | 1.000 | 1.000 | 0.0 | 332.6 | 3.99 | 39.5 | 48.1 | 39.5 | yes | ZBO |
| 2040 | 390.0 | 250.0 | 390.0 | 1.000 | 1.000 | 0.0 | 394.7 | 4.74 | 48.1 | 48.1 | 48.1 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 0.0 | 858.2 | 858.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 1250.0 | 2282.4 | 2113.4 |
| 2037 | 1295.4 | 87.5 | 18.9 | 6.0 | 180.0 | 1587.8 | 1361.3 |
| 2038 | 1553.7 | 72.8 | 19.4 | 82.0 | 0.0 | 1727.9 | 1371.7 |
| 2039 | 2084.2 | 88.9 | 31.5 | 82.0 | 0.0 | 2286.6 | 1680.7 |
| 2040 | 2292.2 | 98.2 | 34.6 | 82.0 | 0.0 | 2507.0 | 1706.2 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-Flex | 13.2 | 13.2 | 13.2 | 8.90 | 13.2 | 117.4 | 2.0 |
| 2038 | Earth-Core | 161.8 | 161.8 | 161.8 | 7.75 | 161.8 | 1253.7 | 72.8 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2039 | Earth-Flex | 22.6 | 22.6 | 22.6 | 11.12 | 22.6 | 251.7 | 3.4 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 84.7 | 84.7 | 84.7 | 8.90 | 84.7 | 754.2 | 12.7 |
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
| CAPEX_2037 | 2035 | cumulative_capex | 0.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2036 | cumulative_capex | 1250.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2037 | cumulative_capex | 1430.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2040 | 2035 | cumulative_capex | 0.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2036 | cumulative_capex | 1250.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2037 | cumulative_capex | 1430.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2038 | cumulative_capex | 1430.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2039 | cumulative_capex | 1430.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2040 | cumulative_capex | 1430.0000 | 2800.0000 | <= | OK | hard |
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 12.3289 | 12.3288 | >= | OK | hard |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 17.2604 | 17.2603 | >= | OK | hard |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 23.4249 | 23.4247 | >= | OK | hard |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 30.8222 | 30.8219 | >= | OK | hard |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 39.4524 | 39.4521 | >= | OK | hard |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 48.0825 | 48.0822 | >= | OK | hard |
| EMERGENCY_BASE_STREAK | 2035 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2036 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2037 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2038 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2039 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2040 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| STORAGE_OVERFLOW | 2035 | max_end_of_month_stock_t | 17.2604 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2035 | reserved_A_t_per_year | 109.8760 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2035 | ordered_A_t | 109.8760 | 109.8760 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2035 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2035 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2036 | max_end_of_month_stock_t | 23.4249 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2036 | reserved_A_t_per_year | 153.0520 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2036 | ordered_A_t | 153.0518 | 153.0520 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2036 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2036 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2037 | max_end_of_month_stock_t | 30.8222 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_B_t_per_year | 13.1890 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_B_t | 13.1882 | 13.1890 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2038 | max_end_of_month_stock_t | 39.4524 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 161.7720 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 161.7714 | 161.7720 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_D_t | 100.0000 | 100.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2039 | max_end_of_month_stock_t | 48.0825 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_B_t_per_year | 22.6220 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_B_t | 22.6216 | 22.6220 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_D_t | 120.0000 | 120.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2040 | max_end_of_month_stock_t | 48.0826 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 84.7370 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 84.7369 | 84.7370 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_D_t | 120.0000 | 120.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |

## Constraint checks

No violations.

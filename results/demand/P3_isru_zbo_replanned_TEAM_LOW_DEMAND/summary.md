# P3_isru_zbo_team_low_demand — TEAM_LOW_DEMAND (Низкий спрос (проверка чувствительности, данные организатора))

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 8,392.867 |
| pv_cost_mln | 6,872.892 |
| cost_per_served_t_mln | 7.548 |
| pv_cost_per_served_t_mln | 6.181 |
| served_total_t | 1,112.000 |
| demand_total_t | 1,112.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 23.594 |
| capex_total_mln | 1,430.000 |
| procurement_total_mln | 6,237.569 |
| reservation_total_mln | 370.702 |
| holding_total_mln | 102.596 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 80.0 | 64.0 | 80.0 | 1.000 | 1.000 | 0.0 | 87.9 | 3.96 | 9.9 | 13.8 | 9.9 | yes | BASE |
| 2036 | 112.0 | 84.0 | 112.0 | 1.000 | 1.000 | 0.0 | 122.4 | 5.51 | 13.8 | 18.7 | 13.8 | yes | BASE |
| 2037 | 152.0 | 108.0 | 152.0 | 1.000 | 1.000 | 0.0 | 162.6 | 4.63 | 18.7 | 24.7 | 18.7 | yes | ZBO |
| 2038 | 200.0 | 136.0 | 200.0 | 1.000 | 1.000 | 0.0 | 209.4 | 2.51 | 24.7 | 31.6 | 24.7 | yes | ZBO |
| 2039 | 256.0 | 168.0 | 256.0 | 1.000 | 1.000 | 0.0 | 266.1 | 3.19 | 31.6 | 38.5 | 31.6 | yes | ZBO |
| 2040 | 312.0 | 200.0 | 312.0 | 1.000 | 1.000 | 0.0 | 315.8 | 3.79 | 38.5 | 38.5 | 38.5 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 636.9 | 41.1 | 8.5 | 0.0 | 0.0 | 686.5 | 686.5 |
| 2036 | 759.1 | 55.1 | 11.7 | 0.0 | 1250.0 | 2076.0 | 1922.2 |
| 2037 | 1007.8 | 73.1 | 15.1 | 6.0 | 180.0 | 1282.1 | 1099.2 |
| 2038 | 978.4 | 49.2 | 14.3 | 82.0 | 0.0 | 1123.9 | 892.2 |
| 2039 | 1265.8 | 65.7 | 25.2 | 82.0 | 0.0 | 1438.8 | 1057.5 |
| 2040 | 1589.5 | 86.4 | 27.7 | 82.0 | 0.0 | 1785.6 | 1215.2 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 87.9 | 87.9 | 87.9 | 6.20 | 87.9 | 545.0 | 39.6 |
| 2036 | Earth-Core | 122.4 | 122.4 | 122.4 | 6.20 | 122.4 | 759.1 | 55.1 |
| 2037 | Earth-Core | 162.6 | 162.6 | 162.6 | 6.20 | 162.6 | 1007.8 | 73.1 |
| 2038 | Earth-Core | 109.4 | 109.4 | 109.4 | 6.20 | 109.4 | 678.4 | 49.2 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 146.1 | 146.1 | 146.1 | 6.20 | 146.1 | 905.8 | 65.7 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 5.8 | 5.8 | 5.8 | 8.90 | 5.8 | 51.5 | 0.9 |
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
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 9.8630 | 9.8630 | >= | OK | hard |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 13.8083 | 13.8082 | >= | OK | hard |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 18.7399 | 18.7397 | >= | OK | hard |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 24.6577 | 24.6575 | >= | OK | hard |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 31.5619 | 31.5616 | >= | OK | hard |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 38.4660 | 38.4658 | >= | OK | hard |
| EMERGENCY_BASE_STREAK | 2035 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2036 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2037 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2038 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2039 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2040 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| STORAGE_OVERFLOW | 2035 | max_end_of_month_stock_t | 13.8083 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2035 | reserved_A_t_per_year | 87.9010 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2035 | ordered_A_t | 87.9008 | 87.9010 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2035 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2035 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2036 | max_end_of_month_stock_t | 18.7399 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2036 | reserved_A_t_per_year | 122.4420 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2036 | ordered_A_t | 122.4414 | 122.4420 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2036 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2036 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2037 | max_end_of_month_stock_t | 24.6577 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 162.5510 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 162.5505 | 162.5510 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2038 | max_end_of_month_stock_t | 31.5619 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 109.4180 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 109.4172 | 109.4180 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_D_t | 100.0000 | 100.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2039 | max_end_of_month_stock_t | 38.4660 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 146.0980 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 146.0973 | 146.0980 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_D_t | 120.0000 | 120.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2040 | max_end_of_month_stock_t | 38.4660 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 5.7900 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 5.7895 | 5.7900 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_D_t | 120.0000 | 120.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |

## Constraint checks

No violations.

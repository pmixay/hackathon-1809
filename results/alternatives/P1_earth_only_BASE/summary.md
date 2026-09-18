# P1_earth_only — BASE (Стандартный сценарий)

Feasible: **NO** — hard violations: 2, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 9,879.472 |
| pv_cost_mln | 7,857.380 |
| cost_per_served_t_mln | 7.644 |
| pv_cost_per_served_t_mln | 6.079 |
| served_total_t | 1,292.452 |
| demand_total_t | 1,390.000 |
| shortage_total_t | 97.548 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 0.750 |
| min_service_level_critical | 1.000 |
| losses_total_t | 60.320 |
| capex_total_mln | 0.000 |
| procurement_total_mln | 9,282.939 |
| reservation_total_mln | 509.881 |
| holding_total_mln | 86.651 |
| fixed_opex_total_mln | 0.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 206.7 | 9.30 | 23.4 | 30.8 | 23.4 | yes | BASE |
| 2038 | 250.0 | 170.0 | 250.0 | 1.000 | 1.000 | 0.0 | 270.8 | 12.19 | 30.8 | 39.5 | 30.8 | yes | BASE |
| 2039 | 320.0 | 210.0 | 320.0 | 1.000 | 1.000 | 0.0 | 300.0 | 13.50 | 39.5 | 6.0 | 39.5 | yes | BASE |
| 2040 | 390.0 | 250.0 | 292.5 | 0.750 | 1.000 | 97.5 | 300.0 | 13.50 | 6.0 | 0.0 | 48.1 | NO | BASE |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 0.0 | 858.2 | 858.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1326.6 | 88.0 | 19.5 | 0.0 | 0.0 | 1434.2 | 1229.6 |
| 2038 | 1897.3 | 97.6 | 25.3 | 0.0 | 0.0 | 2020.2 | 1603.7 |
| 2039 | 2157.0 | 102.0 | 16.3 | 0.0 | 0.0 | 2275.3 | 1672.4 |
| 2040 | 2157.0 | 102.0 | 0.2 | 0.0 | 0.0 | 2259.2 | 1537.6 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-Flex | 16.7 | 16.7 | 16.7 | 8.90 | 16.7 | 148.6 | 2.5 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2038 | Earth-Flex | 80.8 | 80.8 | 80.8 | 8.90 | 80.8 | 719.3 | 12.1 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |

## Check matrix (every rule x year)

| Rule | Year | Metric | Actual | Limit | Op | Result | Severity |
|---|---:|---|---:|---:|---|:---:|---|
| BASE_CRITICAL_SERVICE | 2035 | critical_service_level | 1.0000 | 0.9900 | >= | OK | hard |
| BASE_CRITICAL_SERVICE | 2036 | critical_service_level | 1.0000 | 0.9900 | >= | OK | hard |
| BASE_CRITICAL_SERVICE | 2037 | critical_service_level | 1.0000 | 0.9900 | >= | OK | hard |
| BASE_CRITICAL_SERVICE | 2038 | critical_service_level | 1.0000 | 0.9900 | >= | OK | hard |
| BASE_CRITICAL_SERVICE | 2039 | critical_service_level | 1.0000 | 0.9900 | >= | OK | hard |
| BASE_CRITICAL_SERVICE | 2040 | critical_service_level | 1.0000 | 0.9900 | >= | OK | hard |
| BASE_TOTAL_SERVICE | 2035 | total_service_level | 1.0000 | 0.9700 | >= | OK | hard |
| BASE_TOTAL_SERVICE | 2036 | total_service_level | 1.0000 | 0.9700 | >= | OK | hard |
| BASE_TOTAL_SERVICE | 2037 | total_service_level | 1.0000 | 0.9700 | >= | OK | hard |
| BASE_TOTAL_SERVICE | 2038 | total_service_level | 1.0000 | 0.9700 | >= | OK | hard |
| BASE_TOTAL_SERVICE | 2039 | total_service_level | 1.0000 | 0.9700 | >= | OK | hard |
| BASE_TOTAL_SERVICE | 2040 | total_service_level | 0.7499 | 0.9700 | >= | VIOLATED | hard |
| CAPEX_2037 | 2035 | cumulative_capex | 0.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2036 | cumulative_capex | 0.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2037 | cumulative_capex | 0.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2040 | 2035 | cumulative_capex | 0.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2036 | cumulative_capex | 0.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2037 | cumulative_capex | 0.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2038 | cumulative_capex | 0.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2039 | cumulative_capex | 0.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2040 | cumulative_capex | 0.0000 | 2800.0000 | <= | OK | hard |
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 12.3289 | 12.3288 | >= | OK | hard |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 17.2604 | 17.2603 | >= | OK | hard |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 23.4249 | 23.4247 | >= | OK | hard |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 30.8223 | 30.8219 | >= | OK | hard |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 39.4524 | 39.4521 | >= | OK | hard |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 5.9524 | 48.0822 | >= | VIOLATED | hard |
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
| STORAGE_OVERFLOW | 2037 | max_end_of_month_stock_t | 30.8223 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_B_t_per_year | 16.6990 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_B_t | 16.6988 | 16.6990 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2038 | max_end_of_month_stock_t | 39.4524 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_B_t_per_year | 80.8170 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_B_t | 80.8169 | 80.8170 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2039 | max_end_of_month_stock_t | 36.6607 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_B_t_per_year | 110.0000 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_B_t | 110.0000 | 110.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2040 | max_end_of_month_stock_t | 0.0000 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 110.0000 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 110.0000 | 110.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| BASE_TOTAL_SERVICE | hard | 2040 |  |  | 0.750 | 0.970 | 0.220 | 2040: total service level 0.7499 < 0.97 (shortage 97.548 t) |
| RESERVE_45D | hard | 2040 | 1 |  | 5.952 | 48.082 | 42.130 | 2040-01: physical stock 5.952 t < 45-day reserve 48.082 t |

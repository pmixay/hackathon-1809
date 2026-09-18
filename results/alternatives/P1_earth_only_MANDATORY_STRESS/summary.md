# P1_earth_only — MANDATORY_STRESS (Обязательный стрессовый сценарий)

Feasible: **NO** — hard violations: 6, guideline: 2, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 10,863.074 |
| pv_cost_mln | 8,607.464 |
| cost_per_served_t_mln | 8.405 |
| pv_cost_per_served_t_mln | 6.660 |
| served_total_t | 1,292.452 |
| demand_total_t | 1,534.000 |
| shortage_total_t | 241.548 |
| shortage_critical_t | 1.000 |
| min_service_level_total | 0.639 |
| min_service_level_critical | 0.997 |
| losses_total_t | 60.320 |
| capex_total_mln | 0.000 |
| procurement_total_mln | 10,296.507 |
| reservation_total_mln | 509.881 |
| holding_total_mln | 56.685 |
| fixed_opex_total_mln | 0.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 206.7 | 9.30 | 23.4 | 30.8 | 23.4 | yes | BASE |
| 2038 | 287.5 | 195.5 | 287.5 | 1.000 | 1.000 | 0.0 | 270.8 | 12.19 | 30.8 | 2.0 | 35.4 | NO | BASE |
| 2039 | 368.0 | 241.5 | 288.5 | 0.784 | 1.000 | 79.5 | 300.0 | 13.50 | 2.0 | 0.0 | 45.4 | NO | BASE |
| 2040 | 448.5 | 287.5 | 286.5 | 0.639 | 0.997 | 162.0 | 300.0 | 13.50 | 0.0 | 0.0 | 55.3 | NO | BASE |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 0.0 | 858.2 | 858.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1326.6 | 88.0 | 19.5 | 0.0 | 0.0 | 1434.2 | 1229.6 |
| 2038 | 2371.6 | 97.6 | 11.8 | 0.0 | 0.0 | 2481.0 | 1969.5 |
| 2039 | 2696.2 | 102.0 | 0.1 | 0.0 | 0.0 | 2798.3 | 2056.8 |
| 2040 | 2157.0 | 102.0 | 0.0 | 0.0 | 0.0 | 2259.0 | 1537.4 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-Flex | 16.7 | 16.7 | 16.7 | 8.90 | 16.7 | 148.6 | 2.5 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2038 | Earth-Flex | 80.8 | 80.8 | 80.8 | 11.12 | 80.8 | 899.1 | 12.1 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2039 | Earth-Flex | 110.0 | 110.0 | 110.0 | 11.12 | 110.0 | 1223.8 | 16.5 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |

## Check matrix (every rule x year)

| Rule | Year | Metric | Actual | Limit | Op | Result | Severity |
|---|---:|---|---:|---:|---|:---:|---|
| BASE_CRITICAL_SERVICE | 2035 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2036 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2037 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2038 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2039 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2040 | critical_service_level | 0.9965 | 0.9900 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2035 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2036 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2037 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2038 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2039 | total_service_level | 0.7838 | 0.9700 | >= | VIOLATED | guideline |
| BASE_TOTAL_SERVICE | 2040 | total_service_level | 0.6388 | 0.9700 | >= | VIOLATED | guideline |
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
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 30.8223 | 35.4452 | >= | VIOLATED | hard |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 1.9524 | 45.3699 | >= | VIOLATED | hard |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 0.0000 | 55.2945 | >= | VIOLATED | hard |
| EMERGENCY_BASE_STREAK | 2035 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2036 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2037 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2038 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2039 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2040 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| STRESS_LOSS_LIMIT | 2038 | losses_divided_by_throughput | 0.0450 | 0.0200 | <= | VIOLATED | hard |
| STRESS_LOSS_LIMIT | 2039 | losses_divided_by_throughput | 0.0450 | 0.0200 | <= | VIOLATED | hard |
| STRESS_LOSS_LIMIT | 2040 | losses_divided_by_throughput | 0.0450 | 0.0200 | <= | VIOLATED | hard |
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
| STORAGE_OVERFLOW | 2038 | max_end_of_month_stock_t | 28.4164 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_B_t_per_year | 80.8170 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_B_t | 80.8169 | 80.8170 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2039 | max_end_of_month_stock_t | 0.0000 | 70.0000 | <= | OK | hard |
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
| BASE_TOTAL_SERVICE | guideline | 2039 |  |  | 0.784 | 0.970 | 0.186 | 2039: total service level 0.7838 < 0.97 (shortage 79.548 t) [guideline in this scenario] |
| BASE_TOTAL_SERVICE | guideline | 2040 |  |  | 0.639 | 0.970 | 0.331 | 2040: total service level 0.6388 < 0.97 (shortage 162.000 t) [guideline in this scenario] |
| RESERVE_45D | hard | 2038 | 1 |  | 30.822 | 35.445 | 4.623 | 2038-01: physical stock 30.822 t < 45-day reserve 35.445 t |
| RESERVE_45D | hard | 2039 | 1 |  | 1.952 | 45.370 | 43.417 | 2039-01: physical stock 1.952 t < 45-day reserve 45.370 t |
| RESERVE_45D | hard | 2040 | 1 |  | 0.000 | 55.295 | 55.295 | 2040-01: physical stock 0.000 t < 45-day reserve 55.295 t |
| STRESS_LOSS_LIMIT | hard | 2038 |  |  | 0.045 | 0.020 | 0.025 | 2038: losses/throughput 0.0450 > 0.02 (12.187 t of 270.817 t) |
| STRESS_LOSS_LIMIT | hard | 2039 |  |  | 0.045 | 0.020 | 0.025 | 2039: losses/throughput 0.0450 > 0.02 (13.500 t of 300.000 t) |
| STRESS_LOSS_LIMIT | hard | 2040 |  |  | 0.045 | 0.020 | 0.025 | 2040: losses/throughput 0.0450 > 0.02 (13.500 t of 300.000 t) |

# P2_earth_new — BASE (Стандартный сценарий)

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 19

| KPI | Value |
|---|---:|
| total_cost_mln | 11,079.235 |
| pv_cost_mln | 8,779.822 |
| cost_per_served_t_mln | 7.971 |
| pv_cost_per_served_t_mln | 6.316 |
| served_total_t | 1,390.000 |
| demand_total_t | 1,390.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 67.182 |
| capex_total_mln | 360.000 |
| procurement_total_mln | 9,996.593 |
| reservation_total_mln | 586.383 |
| holding_total_mln | 136.259 |
| fixed_opex_total_mln | 0.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 206.7 | 9.30 | 23.4 | 30.8 | 23.4 | yes | BASE |
| 2038 | 250.0 | 170.0 | 250.0 | 1.000 | 1.000 | 0.0 | 270.8 | 12.19 | 30.8 | 39.5 | 30.8 | yes | BASE |
| 2039 | 320.0 | 210.0 | 320.0 | 1.000 | 1.000 | 0.0 | 344.1 | 15.49 | 39.5 | 48.1 | 39.5 | yes | BASE |
| 2040 | 390.0 | 250.0 | 390.0 | 1.000 | 1.000 | 0.0 | 408.4 | 18.38 | 48.1 | 48.1 | 48.1 | yes | BASE |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 360.0 | 1218.2 | 1218.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1296.6 | 90.5 | 19.5 | 0.0 | 0.0 | 1406.6 | 1205.9 |
| 2038 | 1751.8 | 109.7 | 25.3 | 0.0 | 0.0 | 1886.8 | 1497.8 |
| 2039 | 2315.6 | 128.1 | 31.5 | 0.0 | 0.0 | 2475.3 | 1819.4 |
| 2040 | 2887.6 | 137.8 | 34.6 | 0.0 | 0.0 | 3059.9 | 2082.5 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 16.7 | 16.7 | 16.7 | 7.10 | 16.7 | 118.6 | 5.0 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2038 | Earth-New | 80.8 | 80.8 | 80.8 | 7.10 | 80.8 | 573.8 | 24.2 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-Flex | 24.1 | 24.1 | 24.1 | 8.90 | 24.1 | 214.6 | 3.6 |
| 2039 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 88.4 | 88.4 | 88.4 | 8.90 | 88.4 | 786.6 | 13.3 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |

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
| BASE_TOTAL_SERVICE | 2040 | total_service_level | 1.0000 | 0.9700 | >= | OK | hard |
| CAPEX_2037 | 2035 | cumulative_capex | 360.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2036 | cumulative_capex | 360.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2037 | cumulative_capex | 360.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2040 | 2035 | cumulative_capex | 360.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2036 | cumulative_capex | 360.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2037 | cumulative_capex | 360.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2038 | cumulative_capex | 360.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2039 | cumulative_capex | 360.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2040 | cumulative_capex | 360.0000 | 2800.0000 | <= | OK | hard |
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 12.3289 | 12.3288 | >= | OK | hard |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 17.2604 | 17.2603 | >= | OK | hard |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 23.4249 | 23.4247 | >= | OK | hard |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 30.8223 | 30.8219 | >= | OK | hard |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 39.4524 | 39.4521 | >= | OK | hard |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 48.0826 | 48.0822 | >= | OK | hard |
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
| CAPACITY_EXCEEDED | 2037 | reserved_C_t_per_year | 16.6990 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_C_t | 16.6988 | 16.6990 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 0.0000 | 1.0000 | == | VIOLATED | hard |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2038 | max_end_of_month_stock_t | 39.4524 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_C_t_per_year | 80.8170 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_C_t | 80.8169 | 80.8170 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 0.0000 | 1.0000 | == | VIOLATED | hard |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2039 | max_end_of_month_stock_t | 48.0826 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_B_t_per_year | 24.1160 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_B_t | 24.1154 | 24.1160 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_C_t_per_year | 130.0000 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_C_t | 130.0000 | 130.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2040 | max_end_of_month_stock_t | 48.0826 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 88.3770 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 88.3770 | 88.3770 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_C_t_per_year | 130.0000 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_C_t | 130.0000 | 130.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| INTRA_MONTH_PEAK | warning | 2039 | 6 |  | 70.434 | 70.000 | 0.434 | stock after inflow 70.434 t exceeds Base storage capacity 70.0 t within 2039-06 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2039 | 7 |  | 71.153 | 70.000 | 1.153 | stock after inflow 71.153 t exceeds Base storage capacity 70.0 t within 2039-07 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2039 | 8 |  | 71.873 | 70.000 | 1.873 | stock after inflow 71.873 t exceeds Base storage capacity 70.0 t within 2039-08 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2039 | 9 |  | 72.592 | 70.000 | 2.592 | stock after inflow 72.592 t exceeds Base storage capacity 70.0 t within 2039-09 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2039 | 10 |  | 73.311 | 70.000 | 3.311 | stock after inflow 73.311 t exceeds Base storage capacity 70.0 t within 2039-10 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2039 | 11 |  | 74.030 | 70.000 | 4.030 | stock after inflow 74.030 t exceeds Base storage capacity 70.0 t within 2039-11 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2039 | 12 |  | 74.749 | 70.000 | 4.749 | stock after inflow 74.749 t exceeds Base storage capacity 70.0 t within 2039-12 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 1 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-01 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 2 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-02 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 3 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-03 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 4 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-04 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 5 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-05 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 6 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-06 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 7 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-07 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 8 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-08 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 9 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-09 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 10 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-10 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 11 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-11 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2040 | 12 |  | 80.583 | 70.000 | 10.583 | stock after inflow 80.583 t exceeds Base storage capacity 70.0 t within 2040-12 (before withdrawals) |

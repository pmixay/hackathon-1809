# P3_isru_zbo_adapted — BASE (Стандартный сценарий)

Feasible: **NO** — hard violations: 25, guideline: 0, warnings: 3

| KPI | Value |
|---|---:|
| total_cost_mln | 12,599.579 |
| pv_cost_mln | 10,097.535 |
| cost_per_served_t_mln | 9.064 |
| pv_cost_per_served_t_mln | 7.264 |
| served_total_t | 1,390.000 |
| demand_total_t | 1,390.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 31.901 |
| capex_total_mln | 1,430.000 |
| procurement_total_mln | 10,026.892 |
| reservation_total_mln | 505.229 |
| holding_total_mln | 385.457 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 207.9 | 5.93 | 23.4 | 35.4 | 23.4 | yes | ZBO |
| 2038 | 250.0 | 170.0 | 250.0 | 1.000 | 1.000 | 0.0 | 346.0 | 4.15 | 35.4 | 127.3 | 30.8 | yes | ZBO |
| 2039 | 320.0 | 210.0 | 320.0 | 1.000 | 1.000 | 0.0 | 412.5 | 4.95 | 127.3 | 214.9 | 39.5 | yes | ZBO |
| 2040 | 390.0 | 250.0 | 390.0 | 1.000 | 1.000 | 0.0 | 420.0 | 5.04 | 214.9 | 239.9 | 48.1 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 0.0 | 858.2 | 858.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 1250.0 | 2282.4 | 2113.4 |
| 2037 | 1337.7 | 88.2 | 20.6 | 6.0 | 180.0 | 1632.5 | 1399.6 |
| 2038 | 1976.7 | 93.9 | 52.7 | 82.0 | 0.0 | 2205.3 | 1750.6 |
| 2039 | 2450.4 | 100.9 | 123.2 | 82.0 | 0.0 | 2756.5 | 2026.1 |
| 2040 | 2517.0 | 102.0 | 163.7 | 82.0 | 0.0 | 2864.7 | 1949.7 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-Flex | 17.9 | 17.9 | 17.9 | 8.90 | 17.9 | 159.7 | 2.7 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2038 | Earth-Flex | 56.0 | 56.0 | 56.0 | 8.90 | 56.0 | 498.7 | 8.4 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-Flex | 102.5 | 102.5 | 102.5 | 8.90 | 102.5 | 912.4 | 15.4 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |

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
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 35.4455 | 30.8219 | >= | OK | hard |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 127.3303 | 39.4521 | >= | OK | hard |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 214.8950 | 48.0822 | >= | OK | hard |
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
| STORAGE_OVERFLOW | 2037 | max_end_of_month_stock_t | 35.4455 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_B_t_per_year | 17.9480 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_B_t | 17.9471 | 17.9480 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2038 | max_end_of_month_stock_t | 127.3303 | 120.0000 | <= | VIOLATED | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_B_t_per_year | 56.0380 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_B_t | 56.0372 | 56.0380 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_D_t | 100.0000 | 100.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2039 | max_end_of_month_stock_t | 214.8950 | 120.0000 | <= | VIOLATED | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_B_t_per_year | 102.5150 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_B_t | 102.5149 | 102.5150 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_D_t | 120.0000 | 120.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2040 | max_end_of_month_stock_t | 239.8550 | 120.0000 | <= | VIOLATED | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 110.0000 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 110.0000 | 110.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_D_t | 120.0000 | 120.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| INTRA_MONTH_PEAK | warning | 2038 | 9 |  | 120.252 | 120.000 | 0.252 | stock after inflow 120.252 t exceeds ZBO modernization capacity 120.0 t within 2038-09 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2038 | 10 |  | 129.556 | 120.000 | 9.556 | stock after inflow 129.556 t exceeds ZBO modernization capacity 120.0 t within 2038-10 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2038 | 11 |  | 138.860 | 120.000 | 18.860 | stock after inflow 138.860 t exceeds ZBO modernization capacity 120.0 t within 2038-11 (before withdrawals) |
| STORAGE_OVERFLOW | hard | 2038 | 12 |  | 127.330 | 120.000 | 7.330 | end-of-month stock 127.330 t exceeds ZBO modernization capacity 120.0 t in 2038-12 |
| STORAGE_OVERFLOW | hard | 2039 | 1 |  | 134.627 | 120.000 | 14.627 | end-of-month stock 134.627 t exceeds ZBO modernization capacity 120.0 t in 2039-01 |
| STORAGE_OVERFLOW | hard | 2039 | 2 |  | 141.924 | 120.000 | 21.924 | end-of-month stock 141.924 t exceeds ZBO modernization capacity 120.0 t in 2039-02 |
| STORAGE_OVERFLOW | hard | 2039 | 3 |  | 149.221 | 120.000 | 29.221 | end-of-month stock 149.221 t exceeds ZBO modernization capacity 120.0 t in 2039-03 |
| STORAGE_OVERFLOW | hard | 2039 | 4 |  | 156.519 | 120.000 | 36.519 | end-of-month stock 156.519 t exceeds ZBO modernization capacity 120.0 t in 2039-04 |
| STORAGE_OVERFLOW | hard | 2039 | 5 |  | 163.816 | 120.000 | 43.816 | end-of-month stock 163.816 t exceeds ZBO modernization capacity 120.0 t in 2039-05 |
| STORAGE_OVERFLOW | hard | 2039 | 6 |  | 171.113 | 120.000 | 51.113 | end-of-month stock 171.113 t exceeds ZBO modernization capacity 120.0 t in 2039-06 |
| STORAGE_OVERFLOW | hard | 2039 | 7 |  | 178.410 | 120.000 | 58.410 | end-of-month stock 178.410 t exceeds ZBO modernization capacity 120.0 t in 2039-07 |
| STORAGE_OVERFLOW | hard | 2039 | 8 |  | 185.707 | 120.000 | 65.707 | end-of-month stock 185.707 t exceeds ZBO modernization capacity 120.0 t in 2039-08 |
| STORAGE_OVERFLOW | hard | 2039 | 9 |  | 193.004 | 120.000 | 73.004 | end-of-month stock 193.004 t exceeds ZBO modernization capacity 120.0 t in 2039-09 |
| STORAGE_OVERFLOW | hard | 2039 | 10 |  | 200.301 | 120.000 | 80.301 | end-of-month stock 200.301 t exceeds ZBO modernization capacity 120.0 t in 2039-10 |
| STORAGE_OVERFLOW | hard | 2039 | 11 |  | 207.598 | 120.000 | 87.598 | end-of-month stock 207.598 t exceeds ZBO modernization capacity 120.0 t in 2039-11 |
| STORAGE_OVERFLOW | hard | 2039 | 12 |  | 214.895 | 120.000 | 94.895 | end-of-month stock 214.895 t exceeds ZBO modernization capacity 120.0 t in 2039-12 |
| STORAGE_OVERFLOW | hard | 2040 | 1 |  | 216.975 | 120.000 | 96.975 | end-of-month stock 216.975 t exceeds ZBO modernization capacity 120.0 t in 2040-01 |
| STORAGE_OVERFLOW | hard | 2040 | 2 |  | 219.055 | 120.000 | 99.055 | end-of-month stock 219.055 t exceeds ZBO modernization capacity 120.0 t in 2040-02 |
| STORAGE_OVERFLOW | hard | 2040 | 3 |  | 221.135 | 120.000 | 101.135 | end-of-month stock 221.135 t exceeds ZBO modernization capacity 120.0 t in 2040-03 |
| STORAGE_OVERFLOW | hard | 2040 | 4 |  | 223.215 | 120.000 | 103.215 | end-of-month stock 223.215 t exceeds ZBO modernization capacity 120.0 t in 2040-04 |
| STORAGE_OVERFLOW | hard | 2040 | 5 |  | 225.295 | 120.000 | 105.295 | end-of-month stock 225.295 t exceeds ZBO modernization capacity 120.0 t in 2040-05 |
| STORAGE_OVERFLOW | hard | 2040 | 6 |  | 227.375 | 120.000 | 107.375 | end-of-month stock 227.375 t exceeds ZBO modernization capacity 120.0 t in 2040-06 |
| STORAGE_OVERFLOW | hard | 2040 | 7 |  | 229.455 | 120.000 | 109.455 | end-of-month stock 229.455 t exceeds ZBO modernization capacity 120.0 t in 2040-07 |
| STORAGE_OVERFLOW | hard | 2040 | 8 |  | 231.535 | 120.000 | 111.535 | end-of-month stock 231.535 t exceeds ZBO modernization capacity 120.0 t in 2040-08 |
| STORAGE_OVERFLOW | hard | 2040 | 9 |  | 233.615 | 120.000 | 113.615 | end-of-month stock 233.615 t exceeds ZBO modernization capacity 120.0 t in 2040-09 |
| STORAGE_OVERFLOW | hard | 2040 | 10 |  | 235.695 | 120.000 | 115.695 | end-of-month stock 235.695 t exceeds ZBO modernization capacity 120.0 t in 2040-10 |
| STORAGE_OVERFLOW | hard | 2040 | 11 |  | 237.775 | 120.000 | 117.775 | end-of-month stock 237.775 t exceeds ZBO modernization capacity 120.0 t in 2040-11 |
| STORAGE_OVERFLOW | hard | 2040 | 12 |  | 239.855 | 120.000 | 119.855 | end-of-month stock 239.855 t exceeds ZBO modernization capacity 120.0 t in 2040-12 |

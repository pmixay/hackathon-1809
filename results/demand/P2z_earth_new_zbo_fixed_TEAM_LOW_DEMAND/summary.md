# P2z_earth_new_zbo — TEAM_LOW_DEMAND (Низкий спрос (проверка чувствительности, данные организатора))

Feasible: **NO** — hard violations: 43, guideline: 0, warnings: 6

| KPI | Value |
|---|---:|
| total_cost_mln | 11,433.135 |
| pv_cost_mln | 9,070.095 |
| cost_per_served_t_mln | 10.282 |
| pv_cost_per_served_t_mln | 8.157 |
| served_total_t | 1,112.000 |
| demand_total_t | 1,112.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 29.492 |
| capex_total_mln | 540.000 |
| procurement_total_mln | 9,683.753 |
| reservation_total_mln | 578.846 |
| holding_total_mln | 588.535 |
| fixed_opex_total_mln | 42.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 80.0 | 64.0 | 80.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 37.3 | 9.9 | yes | BASE |
| 2036 | 112.0 | 84.0 | 112.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 37.3 | 71.4 | 13.8 | yes | BASE |
| 2037 | 152.0 | 108.0 | 152.0 | 1.000 | 1.000 | 0.0 | 203.2 | 5.79 | 71.4 | 116.8 | 18.7 | yes | ZBO |
| 2038 | 200.0 | 136.0 | 200.0 | 1.000 | 1.000 | 0.0 | 261.8 | 3.14 | 116.8 | 175.5 | 24.7 | yes | ZBO |
| 2039 | 256.0 | 168.0 | 256.0 | 1.000 | 1.000 | 0.0 | 332.6 | 3.99 | 175.5 | 248.1 | 31.6 | yes | ZBO |
| 2040 | 312.0 | 200.0 | 312.0 | 1.000 | 1.000 | 0.0 | 394.7 | 4.74 | 248.1 | 326.1 | 38.5 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 17.9 | 0.0 | 360.0 | 1225.4 | 1225.4 |
| 2036 | 948.9 | 68.9 | 39.1 | 0.0 | 0.0 | 1056.9 | 978.6 |
| 2037 | 1271.6 | 89.5 | 67.2 | 6.0 | 180.0 | 1614.3 | 1384.0 |
| 2038 | 1687.6 | 107.0 | 105.2 | 12.0 | 0.0 | 1911.8 | 1517.7 |
| 2039 | 2213.3 | 126.4 | 152.5 | 12.0 | 0.0 | 2504.2 | 1840.7 |
| 2040 | 2766.2 | 135.7 | 206.7 | 12.0 | 0.0 | 3120.6 | 2123.8 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 13.2 | 13.2 | 13.2 | 7.10 | 13.2 | 93.6 | 4.0 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2038 | Earth-New | 71.8 | 71.8 | 71.8 | 7.10 | 71.8 | 509.6 | 21.5 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-Flex | 12.6 | 12.6 | 12.6 | 8.90 | 12.6 | 112.3 | 1.9 |
| 2039 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 74.7 | 74.7 | 74.7 | 8.90 | 74.7 | 665.2 | 11.2 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |

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
| CAPEX_2037 | 2036 | cumulative_capex | 360.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2037 | cumulative_capex | 540.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2040 | 2035 | cumulative_capex | 360.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2036 | cumulative_capex | 360.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2037 | cumulative_capex | 540.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2038 | cumulative_capex | 540.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2039 | cumulative_capex | 540.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2040 | cumulative_capex | 540.0000 | 2800.0000 | <= | OK | hard |
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 12.3289 | 9.8630 | >= | OK | hard |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 37.2604 | 13.8082 | >= | OK | hard |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 71.4249 | 18.7397 | >= | OK | hard |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 116.8222 | 24.6575 | >= | OK | hard |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 175.4524 | 31.5616 | >= | OK | hard |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 248.0825 | 38.4658 | >= | OK | hard |
| EMERGENCY_BASE_STREAK | 2035 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2036 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2037 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2038 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2039 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2040 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| STORAGE_OVERFLOW | 2035 | max_end_of_month_stock_t | 37.2604 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2035 | reserved_A_t_per_year | 109.8760 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2035 | ordered_A_t | 109.8760 | 109.8760 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2035 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2035 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2036 | max_end_of_month_stock_t | 71.4249 | 70.0000 | <= | VIOLATED | hard |
| CAPACITY_EXCEEDED | 2036 | reserved_A_t_per_year | 153.0520 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2036 | ordered_A_t | 153.0518 | 153.0520 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2036 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2036 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2037 | max_end_of_month_stock_t | 116.8222 | 70.0000 | <= | VIOLATED | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_C_t_per_year | 13.1890 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_C_t | 13.1882 | 13.1890 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 0.0000 | 1.0000 | == | VIOLATED | hard |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2038 | max_end_of_month_stock_t | 175.4524 | 120.0000 | <= | VIOLATED | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_C_t_per_year | 71.7720 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_C_t | 71.7714 | 71.7720 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 0.0000 | 1.0000 | == | VIOLATED | hard |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2039 | max_end_of_month_stock_t | 248.0825 | 120.0000 | <= | VIOLATED | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_B_t_per_year | 12.6220 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_B_t | 12.6216 | 12.6220 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_C_t_per_year | 130.0000 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_C_t | 130.0000 | 130.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2040 | max_end_of_month_stock_t | 326.0826 | 120.0000 | <= | VIOLATED | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_B_t_per_year | 74.7370 | 110.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_B_t | 74.7369 | 74.7370 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_C_t_per_year | 130.0000 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_C_t | 130.0000 | 130.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| INTRA_MONTH_PEAK | warning | 2036 | 9 |  | 72.217 | 70.000 | 2.217 | stock after inflow 72.217 t exceeds Base storage capacity 70.0 t within 2036-09 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2036 | 10 |  | 75.064 | 70.000 | 5.064 | stock after inflow 75.064 t exceeds Base storage capacity 70.0 t within 2036-10 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2036 | 11 |  | 77.911 | 70.000 | 7.911 | stock after inflow 77.911 t exceeds Base storage capacity 70.0 t within 2036-11 (before withdrawals) |
| STORAGE_OVERFLOW | hard | 2036 | 12 |  | 71.425 | 70.000 | 1.425 | end-of-month stock 71.425 t exceeds Base storage capacity 70.0 t in 2036-12 |
| STORAGE_OVERFLOW | hard | 2037 | 1 |  | 74.929 | 70.000 | 4.929 | end-of-month stock 74.929 t exceeds Base storage capacity 70.0 t in 2037-01 |
| STORAGE_OVERFLOW | hard | 2037 | 2 |  | 78.432 | 70.000 | 8.432 | end-of-month stock 78.432 t exceeds Base storage capacity 70.0 t in 2037-02 |
| STORAGE_OVERFLOW | hard | 2037 | 3 |  | 81.936 | 70.000 | 11.936 | end-of-month stock 81.936 t exceeds Base storage capacity 70.0 t in 2037-03 |
| STORAGE_OVERFLOW | hard | 2037 | 4 |  | 85.440 | 70.000 | 15.440 | end-of-month stock 85.440 t exceeds Base storage capacity 70.0 t in 2037-04 |
| STORAGE_OVERFLOW | hard | 2037 | 5 |  | 88.944 | 70.000 | 18.944 | end-of-month stock 88.944 t exceeds Base storage capacity 70.0 t in 2037-05 |
| STORAGE_OVERFLOW | hard | 2037 | 6 |  | 92.447 | 70.000 | 22.447 | end-of-month stock 92.447 t exceeds Base storage capacity 70.0 t in 2037-06 |
| INTRA_MONTH_PEAK | warning | 2037 | 10 |  | 121.364 | 120.000 | 1.364 | stock after inflow 121.364 t exceeds ZBO modernization capacity 120.0 t within 2037-10 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2037 | 11 |  | 125.426 | 120.000 | 5.426 | stock after inflow 125.426 t exceeds ZBO modernization capacity 120.0 t within 2037-11 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2037 | 12 |  | 129.489 | 120.000 | 9.489 | stock after inflow 129.489 t exceeds ZBO modernization capacity 120.0 t within 2037-12 (before withdrawals) |
| STORAGE_OVERFLOW | hard | 2038 | 1 |  | 121.708 | 120.000 | 1.708 | end-of-month stock 121.708 t exceeds ZBO modernization capacity 120.0 t in 2038-01 |
| STORAGE_OVERFLOW | hard | 2038 | 2 |  | 126.594 | 120.000 | 6.594 | end-of-month stock 126.594 t exceeds ZBO modernization capacity 120.0 t in 2038-02 |
| STORAGE_OVERFLOW | hard | 2038 | 3 |  | 131.480 | 120.000 | 11.480 | end-of-month stock 131.480 t exceeds ZBO modernization capacity 120.0 t in 2038-03 |
| STORAGE_OVERFLOW | hard | 2038 | 4 |  | 136.366 | 120.000 | 16.366 | end-of-month stock 136.366 t exceeds ZBO modernization capacity 120.0 t in 2038-04 |
| STORAGE_OVERFLOW | hard | 2038 | 5 |  | 141.251 | 120.000 | 21.251 | end-of-month stock 141.251 t exceeds ZBO modernization capacity 120.0 t in 2038-05 |
| STORAGE_OVERFLOW | hard | 2038 | 6 |  | 146.137 | 120.000 | 26.137 | end-of-month stock 146.137 t exceeds ZBO modernization capacity 120.0 t in 2038-06 |
| STORAGE_OVERFLOW | hard | 2038 | 7 |  | 151.023 | 120.000 | 31.023 | end-of-month stock 151.023 t exceeds ZBO modernization capacity 120.0 t in 2038-07 |
| STORAGE_OVERFLOW | hard | 2038 | 8 |  | 155.909 | 120.000 | 35.909 | end-of-month stock 155.909 t exceeds ZBO modernization capacity 120.0 t in 2038-08 |
| STORAGE_OVERFLOW | hard | 2038 | 9 |  | 160.795 | 120.000 | 40.795 | end-of-month stock 160.795 t exceeds ZBO modernization capacity 120.0 t in 2038-09 |
| STORAGE_OVERFLOW | hard | 2038 | 10 |  | 165.681 | 120.000 | 45.681 | end-of-month stock 165.681 t exceeds ZBO modernization capacity 120.0 t in 2038-10 |
| STORAGE_OVERFLOW | hard | 2038 | 11 |  | 170.567 | 120.000 | 50.567 | end-of-month stock 170.567 t exceeds ZBO modernization capacity 120.0 t in 2038-11 |
| STORAGE_OVERFLOW | hard | 2038 | 12 |  | 175.452 | 120.000 | 55.452 | end-of-month stock 175.452 t exceeds ZBO modernization capacity 120.0 t in 2038-12 |
| STORAGE_OVERFLOW | hard | 2039 | 1 |  | 181.505 | 120.000 | 61.505 | end-of-month stock 181.505 t exceeds ZBO modernization capacity 120.0 t in 2039-01 |
| STORAGE_OVERFLOW | hard | 2039 | 2 |  | 187.557 | 120.000 | 67.557 | end-of-month stock 187.557 t exceeds ZBO modernization capacity 120.0 t in 2039-02 |
| STORAGE_OVERFLOW | hard | 2039 | 3 |  | 193.610 | 120.000 | 73.610 | end-of-month stock 193.610 t exceeds ZBO modernization capacity 120.0 t in 2039-03 |
| STORAGE_OVERFLOW | hard | 2039 | 4 |  | 199.662 | 120.000 | 79.662 | end-of-month stock 199.662 t exceeds ZBO modernization capacity 120.0 t in 2039-04 |
| STORAGE_OVERFLOW | hard | 2039 | 5 |  | 205.715 | 120.000 | 85.715 | end-of-month stock 205.715 t exceeds ZBO modernization capacity 120.0 t in 2039-05 |
| STORAGE_OVERFLOW | hard | 2039 | 6 |  | 211.767 | 120.000 | 91.767 | end-of-month stock 211.767 t exceeds ZBO modernization capacity 120.0 t in 2039-06 |
| STORAGE_OVERFLOW | hard | 2039 | 7 |  | 217.820 | 120.000 | 97.820 | end-of-month stock 217.820 t exceeds ZBO modernization capacity 120.0 t in 2039-07 |
| STORAGE_OVERFLOW | hard | 2039 | 8 |  | 223.872 | 120.000 | 103.872 | end-of-month stock 223.872 t exceeds ZBO modernization capacity 120.0 t in 2039-08 |
| STORAGE_OVERFLOW | hard | 2039 | 9 |  | 229.925 | 120.000 | 109.925 | end-of-month stock 229.925 t exceeds ZBO modernization capacity 120.0 t in 2039-09 |
| STORAGE_OVERFLOW | hard | 2039 | 10 |  | 235.978 | 120.000 | 115.978 | end-of-month stock 235.978 t exceeds ZBO modernization capacity 120.0 t in 2039-10 |
| STORAGE_OVERFLOW | hard | 2039 | 11 |  | 242.030 | 120.000 | 122.030 | end-of-month stock 242.030 t exceeds ZBO modernization capacity 120.0 t in 2039-11 |
| STORAGE_OVERFLOW | hard | 2039 | 12 |  | 248.083 | 120.000 | 128.083 | end-of-month stock 248.083 t exceeds ZBO modernization capacity 120.0 t in 2039-12 |
| STORAGE_OVERFLOW | hard | 2040 | 1 |  | 254.583 | 120.000 | 134.583 | end-of-month stock 254.583 t exceeds ZBO modernization capacity 120.0 t in 2040-01 |
| STORAGE_OVERFLOW | hard | 2040 | 2 |  | 261.083 | 120.000 | 141.083 | end-of-month stock 261.083 t exceeds ZBO modernization capacity 120.0 t in 2040-02 |
| STORAGE_OVERFLOW | hard | 2040 | 3 |  | 267.583 | 120.000 | 147.583 | end-of-month stock 267.583 t exceeds ZBO modernization capacity 120.0 t in 2040-03 |
| STORAGE_OVERFLOW | hard | 2040 | 4 |  | 274.083 | 120.000 | 154.083 | end-of-month stock 274.083 t exceeds ZBO modernization capacity 120.0 t in 2040-04 |
| STORAGE_OVERFLOW | hard | 2040 | 5 |  | 280.583 | 120.000 | 160.583 | end-of-month stock 280.583 t exceeds ZBO modernization capacity 120.0 t in 2040-05 |
| STORAGE_OVERFLOW | hard | 2040 | 6 |  | 287.083 | 120.000 | 167.083 | end-of-month stock 287.083 t exceeds ZBO modernization capacity 120.0 t in 2040-06 |
| STORAGE_OVERFLOW | hard | 2040 | 7 |  | 293.583 | 120.000 | 173.583 | end-of-month stock 293.583 t exceeds ZBO modernization capacity 120.0 t in 2040-07 |
| STORAGE_OVERFLOW | hard | 2040 | 8 |  | 300.083 | 120.000 | 180.083 | end-of-month stock 300.083 t exceeds ZBO modernization capacity 120.0 t in 2040-08 |
| STORAGE_OVERFLOW | hard | 2040 | 9 |  | 306.583 | 120.000 | 186.583 | end-of-month stock 306.583 t exceeds ZBO modernization capacity 120.0 t in 2040-09 |
| STORAGE_OVERFLOW | hard | 2040 | 10 |  | 313.083 | 120.000 | 193.083 | end-of-month stock 313.083 t exceeds ZBO modernization capacity 120.0 t in 2040-10 |
| STORAGE_OVERFLOW | hard | 2040 | 11 |  | 319.583 | 120.000 | 199.583 | end-of-month stock 319.583 t exceeds ZBO modernization capacity 120.0 t in 2040-11 |
| STORAGE_OVERFLOW | hard | 2040 | 12 |  | 326.083 | 120.000 | 206.083 | end-of-month stock 326.083 t exceeds ZBO modernization capacity 120.0 t in 2040-12 |

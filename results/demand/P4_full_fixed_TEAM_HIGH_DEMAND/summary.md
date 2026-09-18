# P4_full — TEAM_HIGH_DEMAND (Высокий спрос (проверка чувствительности, данные организатора))

Feasible: **NO** — hard violations: 6, guideline: 5, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 10,695.106 |
| pv_cost_mln | 8,764.365 |
| cost_per_served_t_mln | 7.437 |
| pv_cost_per_served_t_mln | 6.094 |
| served_total_t | 1,438.083 |
| demand_total_t | 1,673.000 |
| shortage_total_t | 234.917 |
| shortage_critical_t | 8.778 |
| min_service_level_total | 0.800 |
| min_service_level_critical | 0.959 |
| losses_total_t | 29.492 |
| capex_total_mln | 1,790.000 |
| procurement_total_mln | 8,157.914 |
| reservation_total_mln | 485.716 |
| holding_total_mln | 9.476 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 110.0 | 88.0 | 110.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 7.3 | 13.6 | NO | BASE |
| 2036 | 154.0 | 115.5 | 153.4 | 0.996 | 1.000 | 0.6 | 153.1 | 6.89 | 7.3 | 0.0 | 19.0 | NO | BASE |
| 2037 | 209.0 | 148.5 | 197.4 | 0.944 | 1.000 | 11.6 | 203.2 | 5.79 | 0.0 | 0.0 | 25.8 | NO | ZBO |
| 2038 | 312.5 | 212.5 | 258.6 | 0.828 | 0.959 | 53.9 | 261.8 | 3.14 | 0.0 | 0.0 | 38.5 | NO | ZBO |
| 2039 | 400.0 | 262.5 | 328.6 | 0.822 | 1.000 | 71.4 | 332.6 | 3.99 | 0.0 | 0.0 | 49.3 | NO | ZBO |
| 2040 | 487.5 | 312.5 | 390.0 | 0.800 | 1.000 | 97.5 | 394.7 | 4.74 | 0.0 | 0.0 | 60.1 | NO | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 7.1 | 0.0 | 360.0 | 1214.6 | 1214.6 |
| 2036 | 948.9 | 68.9 | 2.4 | 0.0 | 1250.0 | 2270.2 | 2102.1 |
| 2037 | 1271.6 | 89.5 | 0.0 | 6.0 | 180.0 | 1547.1 | 1326.4 |
| 2038 | 1303.0 | 72.8 | 0.0 | 82.0 | 0.0 | 1457.8 | 1157.2 |
| 2039 | 1698.6 | 92.3 | 0.0 | 82.0 | 0.0 | 1872.9 | 1376.6 |
| 2040 | 2139.6 | 110.9 | 0.0 | 82.0 | 0.0 | 2332.6 | 1587.5 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 13.2 | 13.2 | 13.2 | 7.10 | 13.2 | 93.6 | 4.0 |
| 2038 | Earth-Core | 161.8 | 161.8 | 161.8 | 6.20 | 161.8 | 1003.0 | 72.8 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-New | 22.6 | 22.6 | 22.6 | 7.10 | 22.6 | 160.6 | 6.8 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-New | 84.7 | 84.7 | 84.7 | 7.10 | 84.7 | 601.6 | 25.4 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |

## Check matrix (every rule x year)

| Rule | Year | Metric | Actual | Limit | Op | Result | Severity |
|---|---:|---|---:|---:|---|:---:|---|
| BASE_CRITICAL_SERVICE | 2035 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2036 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2037 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2038 | critical_service_level | 0.9587 | 0.9900 | >= | VIOLATED | guideline |
| BASE_CRITICAL_SERVICE | 2039 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_CRITICAL_SERVICE | 2040 | critical_service_level | 1.0000 | 0.9900 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2035 | total_service_level | 1.0000 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2036 | total_service_level | 0.9963 | 0.9700 | >= | OK | guideline |
| BASE_TOTAL_SERVICE | 2037 | total_service_level | 0.9445 | 0.9700 | >= | VIOLATED | guideline |
| BASE_TOTAL_SERVICE | 2038 | total_service_level | 0.8276 | 0.9700 | >= | VIOLATED | guideline |
| BASE_TOTAL_SERVICE | 2039 | total_service_level | 0.8216 | 0.9700 | >= | VIOLATED | guideline |
| BASE_TOTAL_SERVICE | 2040 | total_service_level | 0.8000 | 0.9700 | >= | VIOLATED | guideline |
| CAPEX_2037 | 2035 | cumulative_capex | 360.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2036 | cumulative_capex | 1610.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2037 | 2037 | cumulative_capex | 1790.0000 | 1800.0000 | <= | OK | hard |
| CAPEX_2040 | 2035 | cumulative_capex | 360.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2036 | cumulative_capex | 1610.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2037 | cumulative_capex | 1790.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2038 | cumulative_capex | 1790.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2039 | cumulative_capex | 1790.0000 | 2800.0000 | <= | OK | hard |
| CAPEX_2040 | 2040 | cumulative_capex | 1790.0000 | 2800.0000 | <= | OK | hard |
| RESERVE_45D | 2035 | opening_stock_vs_45d_reserve_t | 12.3289 | 13.5616 | >= | VIOLATED | hard |
| RESERVE_45D | 2036 | opening_stock_vs_45d_reserve_t | 7.2604 | 18.9863 | >= | VIOLATED | hard |
| RESERVE_45D | 2037 | opening_stock_vs_45d_reserve_t | 0.0000 | 25.7671 | >= | VIOLATED | hard |
| RESERVE_45D | 2038 | opening_stock_vs_45d_reserve_t | 0.0000 | 38.5274 | >= | VIOLATED | hard |
| RESERVE_45D | 2039 | opening_stock_vs_45d_reserve_t | 0.0000 | 49.3151 | >= | VIOLATED | hard |
| RESERVE_45D | 2040 | opening_stock_vs_45d_reserve_t | 0.0000 | 60.1027 | >= | VIOLATED | hard |
| EMERGENCY_BASE_STREAK | 2035 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2036 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2037 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2038 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2039 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| EMERGENCY_BASE_STREAK | 2040 | emergency_share_of_demand | 0.0000 | 0.2000 | <= (else counts as base year) | OK | hard |
| STORAGE_OVERFLOW | 2035 | max_end_of_month_stock_t | 11.9065 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2035 | reserved_A_t_per_year | 109.8760 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2035 | ordered_A_t | 109.8760 | 109.8760 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2035 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2035 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2036 | max_end_of_month_stock_t | 6.6075 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2036 | reserved_A_t_per_year | 153.0520 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2036 | ordered_A_t | 153.0518 | 153.0520 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2036 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2036 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2037 | max_end_of_month_stock_t | 0.0000 | 70.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2037 | reserved_C_t_per_year | 13.1890 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2037 | ordered_C_t | 13.1882 | 13.1890 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2037 | all_deliveries_ordered_within_lead_time | 0.0000 | 1.0000 | == | VIOLATED | hard |
| SOURCE_NOT_AVAILABLE | 2037 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2038 | max_end_of_month_stock_t | 0.0000 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_A_t_per_year | 161.7720 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_A_t | 161.7714 | 161.7720 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2038 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2038 | ordered_D_t | 100.0000 | 100.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2038 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2038 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2039 | max_end_of_month_stock_t | 0.0000 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_C_t_per_year | 22.6220 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_C_t | 22.6216 | 22.6220 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2039 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2039 | ordered_D_t | 120.0000 | 120.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2039 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2039 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |
| STORAGE_OVERFLOW | 2040 | max_end_of_month_stock_t | 0.0000 | 120.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_A_t_per_year | 190.0000 | 190.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_A_t | 190.0000 | 190.0000 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_C_t_per_year | 84.7370 | 130.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_C_t | 84.7369 | 84.7370 | <= | OK | hard |
| CAPACITY_EXCEEDED | 2040 | reserved_D_t_per_year | 120.0000 | 120.0000 | <= | OK | hard |
| ORDER_EXCEEDS_RESERVATION | 2040 | ordered_D_t | 120.0000 | 120.0000 | <= | OK | hard |
| LEAD_TIME_VIOLATED | 2040 | all_deliveries_ordered_within_lead_time | 1.0000 | 1.0000 | == | OK | hard |
| SOURCE_NOT_AVAILABLE | 2040 | all_orders_from_available_sources | 1.0000 | 1.0000 | == | OK | hard |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| BASE_CRITICAL_SERVICE | guideline | 2038 |  |  | 0.959 | 0.990 | 0.031 | 2038: critical service level 0.9587 < 0.99 (shortage 8.778 t) [guideline in this scenario] |
| BASE_TOTAL_SERVICE | guideline | 2037 |  |  | 0.944 | 0.970 | 0.026 | 2037: total service level 0.9445 < 0.97 (shortage 11.603 t) [guideline in this scenario] |
| BASE_TOTAL_SERVICE | guideline | 2038 |  |  | 0.828 | 0.970 | 0.142 | 2038: total service level 0.8276 < 0.97 (shortage 53.870 t) [guideline in this scenario] |
| BASE_TOTAL_SERVICE | guideline | 2039 |  |  | 0.822 | 0.970 | 0.148 | 2039: total service level 0.8216 < 0.97 (shortage 71.370 t) [guideline in this scenario] |
| BASE_TOTAL_SERVICE | guideline | 2040 |  |  | 0.800 | 0.970 | 0.170 | 2040: total service level 0.8000 < 0.97 (shortage 97.500 t) [guideline in this scenario] |
| RESERVE_45D | hard | 2035 | 1 |  | 12.329 | 13.562 | 1.233 | 2035-01: physical stock 12.329 t < 45-day reserve 13.562 t |
| RESERVE_45D | hard | 2036 | 1 |  | 7.260 | 18.986 | 11.726 | 2036-01: physical stock 7.260 t < 45-day reserve 18.986 t |
| RESERVE_45D | hard | 2037 | 1 |  | 0.000 | 25.767 | 25.767 | 2037-01: physical stock 0.000 t < 45-day reserve 25.767 t |
| RESERVE_45D | hard | 2038 | 1 |  | 0.000 | 38.527 | 38.527 | 2038-01: physical stock 0.000 t < 45-day reserve 38.527 t |
| RESERVE_45D | hard | 2039 | 1 |  | 0.000 | 49.315 | 49.315 | 2039-01: physical stock 0.000 t < 45-day reserve 49.315 t |
| RESERVE_45D | hard | 2040 | 1 |  | 0.000 | 60.103 | 60.103 | 2040-01: physical stock 0.000 t < 45-day reserve 60.103 t |

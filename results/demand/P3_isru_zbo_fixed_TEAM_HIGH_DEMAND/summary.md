# P3_isru_zbo — TEAM_HIGH_DEMAND (Высокий спрос (проверка чувствительности, данные организатора))

Feasible: **NO** — hard violations: 6, guideline: 5, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 10,534.008 |
| pv_cost_mln | 8,545.613 |
| cost_per_served_t_mln | 7.325 |
| pv_cost_per_served_t_mln | 5.942 |
| served_total_t | 1,438.083 |
| demand_total_t | 1,673.000 |
| shortage_total_t | 234.917 |
| shortage_critical_t | 8.778 |
| min_service_level_total | 0.800 |
| min_service_level_critical | 0.959 |
| losses_total_t | 29.492 |
| capex_total_mln | 1,430.000 |
| procurement_total_mln | 8,374.898 |
| reservation_total_mln | 467.634 |
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
| 2035 | 796.1 | 51.4 | 7.1 | 0.0 | 0.0 | 854.6 | 854.6 |
| 2036 | 948.9 | 68.9 | 2.4 | 0.0 | 1250.0 | 2270.2 | 2102.1 |
| 2037 | 1295.4 | 87.5 | 0.0 | 6.0 | 180.0 | 1568.9 | 1345.0 |
| 2038 | 1303.0 | 72.8 | 0.0 | 82.0 | 0.0 | 1457.8 | 1157.2 |
| 2039 | 1739.3 | 88.9 | 0.0 | 82.0 | 0.0 | 1910.2 | 1404.1 |
| 2040 | 2292.2 | 98.2 | 0.0 | 82.0 | 0.0 | 2472.4 | 1682.7 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-Flex | 13.2 | 13.2 | 13.2 | 8.90 | 13.2 | 117.4 | 2.0 |
| 2038 | Earth-Core | 161.8 | 161.8 | 161.8 | 6.20 | 161.8 | 1003.0 | 72.8 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-Flex | 22.6 | 22.6 | 22.6 | 8.90 | 22.6 | 201.3 | 3.4 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 84.7 | 84.7 | 84.7 | 8.90 | 84.7 | 754.2 | 12.7 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |

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

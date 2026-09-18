# P3_isru_zbo — MANDATORY_STRESS (Обязательный стрессовый сценарий)

Feasible: **NO** — hard violations: 3, guideline: 3, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 11,167.303 |
| pv_cost_mln | 9,031.625 |
| cost_per_served_t_mln | 8.187 |
| pv_cost_per_served_t_mln | 6.622 |
| served_total_t | 1,363.983 |
| demand_total_t | 1,534.000 |
| shortage_total_t | 170.017 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 0.812 |
| min_service_level_critical | 1.000 |
| losses_total_t | 28.592 |
| capex_total_mln | 1,430.000 |
| procurement_total_mln | 8,970.477 |
| reservation_total_mln | 467.634 |
| holding_total_mln | 47.193 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 203.2 | 5.79 | 23.4 | 30.8 | 23.4 | yes | ZBO |
| 2038 | 287.5 | 195.5 | 245.0 | 0.852 | 1.000 | 42.5 | 216.8 | 2.60 | 30.8 | 0.0 | 35.4 | NO | ZBO |
| 2039 | 368.0 | 241.5 | 299.0 | 0.812 | 1.000 | 69.0 | 302.6 | 3.63 | 0.0 | 0.0 | 45.4 | NO | ZBO |
| 2040 | 448.5 | 287.5 | 390.0 | 0.870 | 1.000 | 58.5 | 394.7 | 4.74 | 0.0 | 0.0 | 55.3 | NO | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 0.0 | 858.2 | 858.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 1250.0 | 2282.4 | 2113.4 |
| 2037 | 1295.4 | 87.5 | 18.9 | 6.0 | 180.0 | 1587.8 | 1361.3 |
| 2038 | 1553.7 | 72.8 | 3.0 | 82.0 | 0.0 | 1711.5 | 1358.6 |
| 2039 | 2084.2 | 88.9 | 0.0 | 82.0 | 0.0 | 2255.1 | 1657.5 |
| 2040 | 2292.2 | 98.2 | 0.0 | 82.0 | 0.0 | 2472.4 | 1682.7 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-Flex | 13.2 | 13.2 | 13.2 | 8.90 | 13.2 | 117.4 | 2.0 |
| 2038 | Earth-Core | 161.8 | 161.8 | 161.8 | 7.75 | 161.8 | 1253.7 | 72.8 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 55.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2039 | Earth-Flex | 22.6 | 22.6 | 22.6 | 11.12 | 22.6 | 251.7 | 3.4 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 90.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 84.7 | 84.7 | 84.7 | 8.90 | 84.7 | 754.2 | 12.7 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| BASE_TOTAL_SERVICE | guideline | 2038 |  |  | 0.852 | 0.970 | 0.118 | 2038: total service level 0.8521 < 0.97 (shortage 42.508 t) [guideline in this scenario] |
| BASE_TOTAL_SERVICE | guideline | 2039 |  |  | 0.812 | 0.970 | 0.158 | 2039: total service level 0.8125 < 0.97 (shortage 69.010 t) [guideline in this scenario] |
| BASE_TOTAL_SERVICE | guideline | 2040 |  |  | 0.870 | 0.970 | 0.100 | 2040: total service level 0.8696 < 0.97 (shortage 58.500 t) [guideline in this scenario] |
| RESERVE_45D | hard | 2038 | 1 |  | 30.822 | 35.445 | 4.623 | 2038-01: physical stock 30.822 t < 45-day reserve 35.445 t |
| RESERVE_45D | hard | 2039 | 1 |  | 0.000 | 45.370 | 45.370 | 2039-01: physical stock 0.000 t < 45-day reserve 45.370 t |
| RESERVE_45D | hard | 2040 | 1 |  | 0.000 | 55.295 | 55.295 | 2040-01: physical stock 0.000 t < 45-day reserve 55.295 t |

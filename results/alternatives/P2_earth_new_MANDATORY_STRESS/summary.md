# P2_earth_new — MANDATORY_STRESS (Обязательный стрессовый сценарий)

Feasible: **NO** — hard violations: 6, guideline: 2, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 11,642.318 |
| pv_cost_mln | 9,212.113 |
| cost_per_served_t_mln | 8.096 |
| pv_cost_per_served_t_mln | 6.406 |
| served_total_t | 1,438.083 |
| demand_total_t | 1,534.000 |
| shortage_total_t | 95.917 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 0.870 |
| min_service_level_critical | 1.000 |
| losses_total_t | 67.182 |
| capex_total_mln | 360.000 |
| procurement_total_mln | 10,639.250 |
| reservation_total_mln | 586.383 |
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
| 2039 | 368.0 | 241.5 | 330.6 | 0.898 | 1.000 | 37.4 | 344.1 | 15.49 | 2.0 | 0.0 | 45.4 | NO | BASE |
| 2040 | 448.5 | 287.5 | 390.0 | 0.870 | 1.000 | 58.5 | 408.4 | 18.38 | 0.0 | 0.0 | 55.3 | NO | BASE |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 360.0 | 1218.2 | 1218.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1296.6 | 90.5 | 19.5 | 0.0 | 0.0 | 1406.6 | 1205.9 |
| 2038 | 2046.3 | 109.7 | 11.8 | 0.0 | 0.0 | 2167.8 | 1720.9 |
| 2039 | 2663.8 | 128.1 | 0.1 | 0.0 | 0.0 | 2792.0 | 2052.2 |
| 2040 | 2887.6 | 137.8 | 0.0 | 0.0 | 0.0 | 3025.3 | 2059.0 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 16.7 | 16.7 | 16.7 | 7.10 | 16.7 | 118.6 | 5.0 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2038 | Earth-New | 80.8 | 80.8 | 80.8 | 7.10 | 80.8 | 573.8 | 24.2 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2039 | Earth-Flex | 24.1 | 24.1 | 24.1 | 11.12 | 24.1 | 268.3 | 3.6 |
| 2039 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 88.4 | 88.4 | 88.4 | 8.90 | 88.4 | 786.6 | 13.3 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| BASE_TOTAL_SERVICE | guideline | 2039 |  |  | 0.898 | 0.970 | 0.072 | 2039: total service level 0.8983 < 0.97 (shortage 37.417 t) [guideline in this scenario] |
| BASE_TOTAL_SERVICE | guideline | 2040 |  |  | 0.870 | 0.970 | 0.100 | 2040: total service level 0.8696 < 0.97 (shortage 58.500 t) [guideline in this scenario] |
| RESERVE_45D | hard | 2038 | 1 |  | 30.822 | 35.445 | 4.623 | 2038-01: physical stock 30.822 t < 45-day reserve 35.445 t |
| RESERVE_45D | hard | 2039 | 1 |  | 1.952 | 45.370 | 43.417 | 2039-01: physical stock 1.952 t < 45-day reserve 45.370 t |
| RESERVE_45D | hard | 2040 | 1 |  | 0.000 | 55.295 | 55.295 | 2040-01: physical stock 0.000 t < 45-day reserve 55.295 t |
| STRESS_LOSS_LIMIT | hard | 2038 |  |  | 0.045 | 0.020 | 0.025 | 2038: losses/throughput 0.0450 > 0.02 (12.187 t of 270.817 t) |
| STRESS_LOSS_LIMIT | hard | 2039 |  |  | 0.045 | 0.020 | 0.025 | 2039: losses/throughput 0.0450 > 0.02 (15.485 t of 344.115 t) |
| STRESS_LOSS_LIMIT | hard | 2040 |  |  | 0.045 | 0.020 | 0.025 | 2040: losses/throughput 0.0450 > 0.02 (18.377 t of 408.377 t) |

# P2z_earth_new_zbo — MANDATORY_STRESS (Обязательный стрессовый сценарий)

Feasible: **NO** — hard violations: 3, guideline: 2, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 11,517.764 |
| pv_cost_mln | 9,142.898 |
| cost_per_served_t_mln | 8.009 |
| pv_cost_per_served_t_mln | 6.358 |
| served_total_t | 1,438.083 |
| demand_total_t | 1,534.000 |
| shortage_total_t | 95.917 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 0.870 |
| min_service_level_critical | 1.000 |
| losses_total_t | 29.492 |
| capex_total_mln | 540.000 |
| procurement_total_mln | 10,300.836 |
| reservation_total_mln | 578.846 |
| holding_total_mln | 56.082 |
| fixed_opex_total_mln | 42.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 203.2 | 5.79 | 23.4 | 30.8 | 23.4 | yes | ZBO |
| 2038 | 287.5 | 195.5 | 287.5 | 1.000 | 1.000 | 0.0 | 261.8 | 3.14 | 30.8 | 2.0 | 35.4 | NO | ZBO |
| 2039 | 368.0 | 241.5 | 330.6 | 0.898 | 1.000 | 37.4 | 332.6 | 3.99 | 2.0 | 0.0 | 45.4 | NO | ZBO |
| 2040 | 448.5 | 287.5 | 390.0 | 0.870 | 1.000 | 58.5 | 394.7 | 4.74 | 0.0 | 0.0 | 55.3 | NO | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 360.0 | 1218.2 | 1218.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1271.6 | 89.5 | 18.9 | 6.0 | 180.0 | 1566.0 | 1342.6 |
| 2038 | 1982.1 | 107.0 | 11.8 | 12.0 | 0.0 | 2112.9 | 1677.3 |
| 2039 | 2535.9 | 126.4 | 0.1 | 12.0 | 0.0 | 2674.4 | 1965.7 |
| 2040 | 2766.2 | 135.7 | 0.0 | 12.0 | 0.0 | 2913.9 | 1983.1 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 13.2 | 13.2 | 13.2 | 7.10 | 13.2 | 93.6 | 4.0 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2038 | Earth-New | 71.8 | 71.8 | 71.8 | 7.10 | 71.8 | 509.6 | 21.5 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2039 | Earth-Flex | 12.6 | 12.6 | 12.6 | 11.12 | 12.6 | 140.4 | 1.9 |
| 2039 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 74.7 | 74.7 | 74.7 | 8.90 | 74.7 | 665.2 | 11.2 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| BASE_TOTAL_SERVICE | guideline | 2039 |  |  | 0.898 | 0.970 | 0.072 | 2039: total service level 0.8983 < 0.97 (shortage 37.417 t) [guideline in this scenario] |
| BASE_TOTAL_SERVICE | guideline | 2040 |  |  | 0.870 | 0.970 | 0.100 | 2040: total service level 0.8696 < 0.97 (shortage 58.500 t) [guideline in this scenario] |
| RESERVE_45D | hard | 2038 | 1 |  | 30.822 | 35.445 | 4.623 | 2038-01: physical stock 30.822 t < 45-day reserve 35.445 t |
| RESERVE_45D | hard | 2039 | 1 |  | 1.952 | 45.370 | 43.417 | 2039-01: physical stock 1.952 t < 45-day reserve 45.370 t |
| RESERVE_45D | hard | 2040 | 1 |  | 0.000 | 55.295 | 55.295 | 2040-01: physical stock 0.000 t < 45-day reserve 55.295 t |

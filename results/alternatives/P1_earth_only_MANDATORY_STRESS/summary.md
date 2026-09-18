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

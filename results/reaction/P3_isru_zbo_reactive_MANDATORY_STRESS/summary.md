# P3_isru_zbo_reactive — MANDATORY_STRESS (Обязательный стрессовый сценарий)

Feasible: **NO** — hard violations: 1, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 13,993.388 |
| pv_cost_mln | 11,135.161 |
| cost_per_served_t_mln | 9.127 |
| pv_cost_per_served_t_mln | 7.263 |
| served_total_t | 1,533.134 |
| demand_total_t | 1,534.000 |
| shortage_total_t | 0.866 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 0.997 |
| min_service_level_critical | 1.000 |
| losses_total_t | 31.318 |
| capex_total_mln | 1,430.000 |
| procurement_total_mln | 11,637.194 |
| reservation_total_mln | 539.789 |
| holding_total_mln | 134.405 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 203.2 | 5.79 | 23.4 | 30.8 | 23.4 | yes | ZBO |
| 2038 | 287.5 | 195.5 | 286.6 | 0.997 | 1.000 | 0.9 | 304.8 | 3.66 | 30.8 | 45.4 | 35.4 | NO | ZBO |
| 2039 | 368.0 | 241.5 | 368.0 | 1.000 | 1.000 | 0.0 | 382.5 | 4.59 | 45.4 | 55.3 | 45.4 | yes | ZBO |
| 2040 | 448.5 | 287.5 | 448.5 | 1.000 | 1.000 | 0.0 | 453.9 | 5.45 | 55.3 | 55.3 | 55.3 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 0.0 | 858.2 | 858.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 1250.0 | 2282.4 | 2113.4 |
| 2037 | 1295.4 | 87.5 | 18.9 | 6.0 | 180.0 | 1587.8 | 1361.3 |
| 2038 | 2638.3 | 117.3 | 14.1 | 82.0 | 0.0 | 2851.7 | 2263.8 |
| 2039 | 2973.0 | 100.9 | 36.2 | 82.0 | 0.0 | 3192.1 | 2346.3 |
| 2040 | 2985.5 | 113.9 | 39.8 | 82.0 | 0.0 | 3221.2 | 2192.3 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-Flex | 13.2 | 13.2 | 13.2 | 8.90 | 13.2 | 117.4 | 2.0 |
| 2038 | Earth-Core | 161.8 | 161.8 | 161.8 | 7.75 | 161.8 | 1253.7 | 72.8 |
| 2038 | Earth-Flex | 110.0 | 48.9 | 48.9 | 11.12 | 48.9 | 543.8 | 16.5 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 55.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2038 | Emergency | 80.0 | 39.2 | 39.2 | 13.80 | 39.2 | 540.8 | 28.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2039 | Earth-Flex | 102.5 | 102.5 | 102.5 | 11.12 | 102.5 | 1140.5 | 15.4 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 90.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Emergency | 33.9 | 33.9 | 33.9 | 13.80 | 33.9 | 468.5 | 11.9 |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| RESERVE_45D | hard | 2038 | 1 |  | 30.822 | 35.445 | 4.623 | 2038-01: physical stock 30.822 t < 45-day reserve 35.445 t |

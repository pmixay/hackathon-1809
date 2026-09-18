# P3_isru_zbo_adapted — MANDATORY_STRESS (Обязательный стрессовый сценарий)

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 13,291.585 |
| pv_cost_mln | 10,636.655 |
| cost_per_served_t_mln | 8.665 |
| pv_cost_per_served_t_mln | 6.934 |
| served_total_t | 1,534.000 |
| demand_total_t | 1,534.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 31.001 |
| capex_total_mln | 1,430.000 |
| procurement_total_mln | 10,968.671 |
| reservation_total_mln | 505.229 |
| holding_total_mln | 135.685 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 207.9 | 5.93 | 23.4 | 35.4 | 23.4 | yes | ZBO |
| 2038 | 287.5 | 195.5 | 287.5 | 1.000 | 1.000 | 0.0 | 301.0 | 3.61 | 35.4 | 45.4 | 35.4 | yes | ZBO |
| 2039 | 368.0 | 241.5 | 368.0 | 1.000 | 1.000 | 0.0 | 382.5 | 4.59 | 45.4 | 55.3 | 45.4 | yes | ZBO |
| 2040 | 448.5 | 287.5 | 448.5 | 1.000 | 1.000 | 0.0 | 420.0 | 5.04 | 55.3 | 21.8 | 55.3 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 0.0 | 858.2 | 858.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 1250.0 | 2282.4 | 2113.4 |
| 2037 | 1337.7 | 88.2 | 20.6 | 6.0 | 180.0 | 1632.5 | 1399.6 |
| 2038 | 2395.9 | 93.9 | 25.8 | 82.0 | 0.0 | 2597.7 | 2062.1 |
| 2039 | 2973.0 | 100.9 | 36.2 | 82.0 | 0.0 | 3192.1 | 2346.3 |
| 2040 | 2517.0 | 102.0 | 27.7 | 82.0 | 0.0 | 2728.7 | 1857.1 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-Flex | 17.9 | 17.9 | 17.9 | 8.90 | 17.9 | 159.7 | 2.7 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2038 | Earth-Flex | 56.0 | 56.0 | 56.0 | 11.12 | 56.0 | 623.4 | 8.4 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 55.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2039 | Earth-Flex | 102.5 | 102.5 | 102.5 | 11.12 | 102.5 | 1140.5 | 15.4 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 90.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |

## Constraint checks

No violations.

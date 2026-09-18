# P2z_earth_new_zbo_adapted — MANDATORY_STRESS (Обязательный стрессовый сценарий)

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 12,811.646 |
| pv_cost_mln | 10,097.472 |
| cost_per_served_t_mln | 8.352 |
| pv_cost_per_served_t_mln | 6.582 |
| served_total_t | 1,534.000 |
| demand_total_t | 1,534.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 31.121 |
| capex_total_mln | 540.000 |
| procurement_total_mln | 11,482.316 |
| reservation_total_mln | 604.827 |
| holding_total_mln | 142.503 |
| fixed_opex_total_mln | 42.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 207.9 | 5.93 | 23.4 | 35.4 | 23.4 | yes | ZBO |
| 2038 | 287.5 | 195.5 | 287.5 | 1.000 | 1.000 | 0.0 | 301.0 | 3.61 | 35.4 | 45.4 | 35.4 | yes | ZBO |
| 2039 | 368.0 | 241.5 | 368.0 | 1.000 | 1.000 | 0.0 | 382.5 | 4.59 | 45.4 | 55.3 | 45.4 | yes | ZBO |
| 2040 | 448.5 | 287.5 | 448.5 | 1.000 | 1.000 | 0.0 | 430.0 | 5.16 | 55.3 | 31.6 | 55.3 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 360.0 | 1218.2 | 1218.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1305.4 | 90.9 | 20.6 | 6.0 | 180.0 | 1602.9 | 1374.2 |
| 2038 | 2260.9 | 118.8 | 29.1 | 12.0 | 0.0 | 2420.8 | 1921.7 |
| 2039 | 3091.0 | 133.9 | 36.2 | 12.0 | 0.0 | 3273.1 | 2405.8 |
| 2040 | 3080.0 | 141.0 | 31.3 | 12.0 | 0.0 | 3264.3 | 2221.6 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 17.9 | 17.9 | 17.9 | 7.10 | 17.9 | 127.4 | 5.4 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2038 | Earth-New | 111.0 | 111.0 | 111.0 | 7.10 | 111.0 | 788.4 | 33.3 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2039 | Earth-Flex | 62.5 | 62.5 | 62.5 | 11.12 | 62.5 | 695.5 | 9.4 |
| 2039 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |

## Constraint checks

No violations.

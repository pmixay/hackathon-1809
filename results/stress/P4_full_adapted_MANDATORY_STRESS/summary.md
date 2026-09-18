# P4_full_adapted — MANDATORY_STRESS (Обязательный стрессовый сценарий)

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 13,112.382 |
| pv_cost_mln | 10,578.228 |
| cost_per_served_t_mln | 8.548 |
| pv_cost_per_served_t_mln | 6.896 |
| served_total_t | 1,534.000 |
| demand_total_t | 1,534.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 31.408 |
| capex_total_mln | 1,790.000 |
| procurement_total_mln | 10,366.326 |
| reservation_total_mln | 556.297 |
| holding_total_mln | 147.760 |
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
| 2040 | 448.5 | 287.5 | 448.5 | 1.000 | 1.000 | 0.0 | 453.9 | 5.45 | 55.3 | 55.3 | 55.3 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 360.0 | 1218.2 | 1218.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 1250.0 | 2282.4 | 2113.4 |
| 2037 | 1305.4 | 90.9 | 20.6 | 6.0 | 180.0 | 1602.9 | 1374.2 |
| 2038 | 2170.4 | 102.3 | 25.8 | 82.0 | 0.0 | 2380.5 | 1889.7 |
| 2039 | 2560.4 | 116.3 | 36.2 | 82.0 | 0.0 | 2794.8 | 2054.3 |
| 2040 | 2585.1 | 126.6 | 39.8 | 82.0 | 0.0 | 2833.5 | 1928.5 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 17.9 | 17.9 | 17.9 | 7.10 | 17.9 | 127.4 | 5.4 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2038 | Earth-New | 56.0 | 56.0 | 56.0 | 7.10 | 56.0 | 397.9 | 16.8 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 55.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 7.75 | 190.0 | 1472.5 | 85.5 |
| 2039 | Earth-New | 102.5 | 102.5 | 102.5 | 7.10 | 102.5 | 727.9 | 30.8 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 90.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 13.9 | 13.9 | 13.9 | 8.90 | 13.9 | 124.1 | 2.1 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |

## Constraint checks

No violations.

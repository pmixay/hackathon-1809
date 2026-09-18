# P3_isru_zbo_team_high_demand — TEAM_HIGH_DEMAND (Высокий спрос (проверка чувствительности, данные организатора))

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 12,577.031 |
| pv_cost_mln | 10,142.465 |
| cost_per_served_t_mln | 7.574 |
| pv_cost_per_served_t_mln | 6.108 |
| served_total_t | 1,660.563 |
| demand_total_t | 1,673.000 |
| shortage_total_t | 12.437 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 0.974 |
| min_service_level_critical | 1.000 |
| losses_total_t | 33.476 |
| capex_total_mln | 1,430.000 |
| procurement_total_mln | 10,243.742 |
| reservation_total_mln | 517.968 |
| holding_total_mln | 133.320 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 110.0 | 88.0 | 110.0 | 1.000 | 1.000 | 0.0 | 120.9 | 5.44 | 13.6 | 19.0 | 13.6 | yes | BASE |
| 2036 | 154.0 | 115.5 | 154.0 | 1.000 | 1.000 | 0.0 | 168.4 | 7.58 | 19.0 | 25.8 | 19.0 | yes | BASE |
| 2037 | 209.0 | 148.5 | 209.0 | 1.000 | 1.000 | 0.0 | 228.3 | 6.51 | 25.8 | 38.5 | 25.8 | yes | ZBO |
| 2038 | 312.5 | 212.5 | 312.5 | 1.000 | 1.000 | 0.0 | 327.2 | 3.93 | 38.5 | 49.3 | 38.5 | yes | ZBO |
| 2039 | 400.0 | 262.5 | 400.0 | 1.000 | 1.000 | 0.0 | 415.8 | 4.99 | 49.3 | 60.1 | 49.3 | yes | ZBO |
| 2040 | 487.5 | 312.5 | 475.1 | 0.974 | 1.000 | 12.4 | 420.0 | 5.04 | 60.1 | 0.0 | 60.1 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 875.7 | 56.5 | 11.7 | 0.0 | 0.0 | 944.0 | 944.0 |
| 2036 | 1043.8 | 75.8 | 16.1 | 0.0 | 1250.0 | 2385.7 | 2209.0 |
| 2037 | 1518.6 | 91.2 | 22.5 | 6.0 | 180.0 | 1818.3 | 1558.9 |
| 2038 | 1809.2 | 91.1 | 25.7 | 82.0 | 0.0 | 2008.0 | 1594.0 |
| 2039 | 2479.4 | 101.4 | 39.4 | 82.0 | 0.0 | 2702.2 | 1986.2 |
| 2040 | 2517.0 | 102.0 | 17.9 | 82.0 | 0.0 | 2718.9 | 1850.5 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 120.9 | 120.9 | 120.9 | 6.20 | 120.9 | 749.4 | 54.4 |
| 2036 | Earth-Core | 168.4 | 168.4 | 168.4 | 6.20 | 168.4 | 1043.8 | 75.8 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-Flex | 38.3 | 38.3 | 38.3 | 8.90 | 38.3 | 340.6 | 5.7 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2038 | Earth-Flex | 37.2 | 37.2 | 37.2 | 8.90 | 37.2 | 331.2 | 5.6 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-Flex | 105.8 | 105.8 | 105.8 | 8.90 | 105.8 | 941.4 | 15.9 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |

## Constraint checks

No violations.

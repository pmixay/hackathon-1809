# P2z_earth_new_zbo_team_high_demand — TEAM_HIGH_DEMAND (Высокий спрос (проверка чувствительности, данные организатора))

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 12,926.676 |
| pv_cost_mln | 10,238.585 |
| cost_per_served_t_mln | 7.738 |
| pv_cost_per_served_t_mln | 6.129 |
| served_total_t | 1,670.443 |
| demand_total_t | 1,673.000 |
| shortage_total_t | 2.557 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 0.995 |
| min_service_level_critical | 1.000 |
| losses_total_t | 33.596 |
| capex_total_mln | 540.000 |
| procurement_total_mln | 11,567.864 |
| reservation_total_mln | 634.708 |
| holding_total_mln | 142.104 |
| fixed_opex_total_mln | 42.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 110.0 | 88.0 | 110.0 | 1.000 | 1.000 | 0.0 | 120.9 | 5.44 | 13.6 | 19.0 | 13.6 | yes | BASE |
| 2036 | 154.0 | 115.5 | 154.0 | 1.000 | 1.000 | 0.0 | 168.4 | 7.58 | 19.0 | 25.8 | 19.0 | yes | BASE |
| 2037 | 209.0 | 148.5 | 209.0 | 1.000 | 1.000 | 0.0 | 228.3 | 6.51 | 25.8 | 38.5 | 25.8 | yes | ZBO |
| 2038 | 312.5 | 212.5 | 312.5 | 1.000 | 1.000 | 0.0 | 327.2 | 3.93 | 38.5 | 49.3 | 38.5 | yes | ZBO |
| 2039 | 400.0 | 262.5 | 400.0 | 1.000 | 1.000 | 0.0 | 415.8 | 4.99 | 49.3 | 60.1 | 49.3 | yes | ZBO |
| 2040 | 487.5 | 312.5 | 484.9 | 0.995 | 1.000 | 2.6 | 430.0 | 5.16 | 60.1 | 0.0 | 60.1 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 875.7 | 56.5 | 11.7 | 0.0 | 360.0 | 1304.0 | 1304.0 |
| 2036 | 1043.8 | 75.8 | 16.1 | 0.0 | 0.0 | 1135.7 | 1051.6 |
| 2037 | 1449.7 | 97.0 | 22.5 | 6.0 | 180.0 | 1755.1 | 1504.7 |
| 2038 | 2165.2 | 125.6 | 31.6 | 12.0 | 0.0 | 2334.4 | 1853.1 |
| 2039 | 2953.4 | 138.9 | 39.4 | 12.0 | 0.0 | 3143.7 | 2310.7 |
| 2040 | 3080.0 | 141.0 | 20.8 | 12.0 | 0.0 | 3253.8 | 2214.5 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 120.9 | 120.9 | 120.9 | 6.20 | 120.9 | 749.4 | 54.4 |
| 2036 | Earth-Core | 168.4 | 168.4 | 168.4 | 6.20 | 168.4 | 1043.8 | 75.8 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 38.3 | 38.3 | 38.3 | 7.10 | 38.3 | 271.7 | 11.5 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2038 | Earth-Flex | 7.2 | 7.2 | 7.2 | 8.90 | 7.2 | 64.2 | 1.1 |
| 2038 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-Flex | 95.8 | 95.8 | 95.8 | 8.90 | 95.8 | 852.4 | 14.4 |
| 2039 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |

## Constraint checks

No violations.

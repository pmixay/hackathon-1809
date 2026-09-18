# P4_full_team_low_demand — TEAM_LOW_DEMAND (Низкий спрос (проверка чувствительности, данные организатора))

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 8,743.314 |
| pv_cost_mln | 7,226.390 |
| cost_per_served_t_mln | 7.863 |
| pv_cost_per_served_t_mln | 6.499 |
| served_total_t | 1,112.000 |
| demand_total_t | 1,112.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 23.594 |
| capex_total_mln | 1,790.000 |
| procurement_total_mln | 6,227.148 |
| reservation_total_mln | 371.571 |
| holding_total_mln | 102.596 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 80.0 | 64.0 | 80.0 | 1.000 | 1.000 | 0.0 | 87.9 | 3.96 | 9.9 | 13.8 | 9.9 | yes | BASE |
| 2036 | 112.0 | 84.0 | 112.0 | 1.000 | 1.000 | 0.0 | 122.4 | 5.51 | 13.8 | 18.7 | 13.8 | yes | BASE |
| 2037 | 152.0 | 108.0 | 152.0 | 1.000 | 1.000 | 0.0 | 162.6 | 4.63 | 18.7 | 24.7 | 18.7 | yes | ZBO |
| 2038 | 200.0 | 136.0 | 200.0 | 1.000 | 1.000 | 0.0 | 209.4 | 2.51 | 24.7 | 31.6 | 24.7 | yes | ZBO |
| 2039 | 256.0 | 168.0 | 256.0 | 1.000 | 1.000 | 0.0 | 266.1 | 3.19 | 31.6 | 38.5 | 31.6 | yes | ZBO |
| 2040 | 312.0 | 200.0 | 312.0 | 1.000 | 1.000 | 0.0 | 315.8 | 3.79 | 38.5 | 38.5 | 38.5 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 636.9 | 41.1 | 8.5 | 0.0 | 360.0 | 1046.5 | 1046.5 |
| 2036 | 759.1 | 55.1 | 11.7 | 0.0 | 1250.0 | 2076.0 | 1922.2 |
| 2037 | 1007.8 | 73.1 | 15.1 | 6.0 | 180.0 | 1282.1 | 1099.2 |
| 2038 | 978.4 | 49.2 | 14.3 | 82.0 | 0.0 | 1123.9 | 892.2 |
| 2039 | 1265.8 | 65.7 | 25.2 | 82.0 | 0.0 | 1438.8 | 1057.5 |
| 2040 | 1579.1 | 87.2 | 27.7 | 82.0 | 0.0 | 1776.0 | 1208.7 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 87.9 | 87.9 | 87.9 | 6.20 | 87.9 | 545.0 | 39.6 |
| 2036 | Earth-Core | 122.4 | 122.4 | 122.4 | 6.20 | 122.4 | 759.1 | 55.1 |
| 2037 | Earth-Core | 162.6 | 162.6 | 162.6 | 6.20 | 162.6 | 1007.8 | 73.1 |
| 2038 | Earth-Core | 109.4 | 109.4 | 109.4 | 6.20 | 109.4 | 678.4 | 49.2 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 146.1 | 146.1 | 146.1 | 6.20 | 146.1 | 905.8 | 65.7 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-New | 5.8 | 5.8 | 5.8 | 7.10 | 5.8 | 41.1 | 1.7 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |

## Constraint checks

No violations.

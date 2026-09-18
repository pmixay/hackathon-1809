# P2z_earth_new_zbo — BASE (Стандартный сценарий)

Feasible: **YES** — hard violations: 0, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 10,980.255 |
| pv_cost_mln | 8,729.404 |
| cost_per_served_t_mln | 7.899 |
| pv_cost_per_served_t_mln | 6.280 |
| served_total_t | 1,390.000 |
| demand_total_t | 1,390.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 29.492 |
| capex_total_mln | 540.000 |
| procurement_total_mln | 9,683.753 |
| reservation_total_mln | 578.846 |
| holding_total_mln | 135.655 |
| fixed_opex_total_mln | 42.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 203.2 | 5.79 | 23.4 | 30.8 | 23.4 | yes | ZBO |
| 2038 | 250.0 | 170.0 | 250.0 | 1.000 | 1.000 | 0.0 | 261.8 | 3.14 | 30.8 | 39.5 | 30.8 | yes | ZBO |
| 2039 | 320.0 | 210.0 | 320.0 | 1.000 | 1.000 | 0.0 | 332.6 | 3.99 | 39.5 | 48.1 | 39.5 | yes | ZBO |
| 2040 | 390.0 | 250.0 | 390.0 | 1.000 | 1.000 | 0.0 | 394.7 | 4.74 | 48.1 | 48.1 | 48.1 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 360.0 | 1218.2 | 1218.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1271.6 | 89.5 | 18.9 | 6.0 | 180.0 | 1566.0 | 1342.6 |
| 2038 | 1687.6 | 107.0 | 25.3 | 12.0 | 0.0 | 1831.9 | 1454.2 |
| 2039 | 2213.3 | 126.4 | 31.5 | 12.0 | 0.0 | 2383.2 | 1751.8 |
| 2040 | 2766.2 | 135.7 | 34.6 | 12.0 | 0.0 | 2948.5 | 2006.7 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 13.2 | 13.2 | 13.2 | 7.10 | 13.2 | 93.6 | 4.0 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2038 | Earth-New | 71.8 | 71.8 | 71.8 | 7.10 | 71.8 | 509.6 | 21.5 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-Flex | 12.6 | 12.6 | 12.6 | 8.90 | 12.6 | 112.3 | 1.9 |
| 2039 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 74.7 | 74.7 | 74.7 | 8.90 | 74.7 | 665.2 | 11.2 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |

## Constraint checks

No violations.

# P1_earth_only — BASE (Стандартный сценарий)

Feasible: **NO** — hard violations: 2, guideline: 0, warnings: 0

| KPI | Value |
|---|---:|
| total_cost_mln | 9,879.472 |
| pv_cost_mln | 7,857.380 |
| cost_per_served_t_mln | 7.644 |
| pv_cost_per_served_t_mln | 6.079 |
| served_total_t | 1,292.452 |
| demand_total_t | 1,390.000 |
| shortage_total_t | 97.548 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 0.750 |
| min_service_level_critical | 1.000 |
| losses_total_t | 60.320 |
| capex_total_mln | 0.000 |
| procurement_total_mln | 9,282.939 |
| reservation_total_mln | 509.881 |
| holding_total_mln | 86.651 |
| fixed_opex_total_mln | 0.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 206.7 | 9.30 | 23.4 | 30.8 | 23.4 | yes | BASE |
| 2038 | 250.0 | 170.0 | 250.0 | 1.000 | 1.000 | 0.0 | 270.8 | 12.19 | 30.8 | 39.5 | 30.8 | yes | BASE |
| 2039 | 320.0 | 210.0 | 320.0 | 1.000 | 1.000 | 0.0 | 300.0 | 13.50 | 39.5 | 6.0 | 39.5 | yes | BASE |
| 2040 | 390.0 | 250.0 | 292.5 | 0.750 | 1.000 | 97.5 | 300.0 | 13.50 | 6.0 | 0.0 | 48.1 | NO | BASE |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 0.0 | 858.2 | 858.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1326.6 | 88.0 | 19.5 | 0.0 | 0.0 | 1434.2 | 1229.6 |
| 2038 | 1897.3 | 97.6 | 25.3 | 0.0 | 0.0 | 2020.2 | 1603.7 |
| 2039 | 2157.0 | 102.0 | 16.3 | 0.0 | 0.0 | 2275.3 | 1672.4 |
| 2040 | 2157.0 | 102.0 | 0.2 | 0.0 | 0.0 | 2259.2 | 1537.6 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-Flex | 16.7 | 16.7 | 16.7 | 8.90 | 16.7 | 148.6 | 2.5 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2038 | Earth-Flex | 80.8 | 80.8 | 80.8 | 8.90 | 80.8 | 719.3 | 12.1 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| BASE_TOTAL_SERVICE | hard | 2040 |  |  | 0.750 | 0.970 | 0.220 | 2040: total service level 0.7499 < 0.97 (shortage 97.548 t) |
| RESERVE_45D | hard | 2040 | 1 |  | 5.952 | 48.082 | 42.130 | 2040-01: physical stock 5.952 t < 45-day reserve 48.082 t |

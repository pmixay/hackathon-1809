# P2z_earth_new_zbo_adapted — BASE (Стандартный сценарий)

Feasible: **NO** — hard violations: 17, guideline: 0, warnings: 5

| KPI | Value |
|---|---:|
| total_cost_mln | 12,223.950 |
| pv_cost_mln | 9,644.476 |
| cost_per_served_t_mln | 8.794 |
| pv_cost_per_served_t_mln | 6.938 |
| served_total_t | 1,390.000 |
| demand_total_t | 1,390.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 31.121 |
| capex_total_mln | 540.000 |
| procurement_total_mln | 10,754.221 |
| reservation_total_mln | 604.827 |
| holding_total_mln | 282.903 |
| fixed_opex_total_mln | 42.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 100.0 | 80.0 | 100.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 17.3 | 12.3 | yes | BASE |
| 2036 | 140.0 | 105.0 | 140.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 17.3 | 23.4 | 17.3 | yes | BASE |
| 2037 | 190.0 | 135.0 | 190.0 | 1.000 | 1.000 | 0.0 | 207.9 | 5.93 | 23.4 | 35.4 | 23.4 | yes | ZBO |
| 2038 | 250.0 | 170.0 | 250.0 | 1.000 | 1.000 | 0.0 | 301.0 | 3.61 | 35.4 | 82.9 | 30.8 | yes | ZBO |
| 2039 | 320.0 | 210.0 | 320.0 | 1.000 | 1.000 | 0.0 | 382.5 | 4.59 | 82.9 | 140.8 | 39.5 | yes | ZBO |
| 2040 | 390.0 | 250.0 | 390.0 | 1.000 | 1.000 | 0.0 | 430.0 | 5.16 | 140.8 | 175.6 | 48.1 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 360.0 | 1218.2 | 1218.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1032.4 | 956.0 |
| 2037 | 1305.4 | 90.9 | 20.6 | 6.0 | 180.0 | 1602.9 | 1374.2 |
| 2038 | 1966.4 | 118.8 | 42.6 | 12.0 | 0.0 | 2139.8 | 1698.6 |
| 2039 | 2657.4 | 133.9 | 80.5 | 12.0 | 0.0 | 2883.8 | 2119.7 |
| 2040 | 3080.0 | 141.0 | 113.9 | 12.0 | 0.0 | 3346.9 | 2277.9 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 17.9 | 17.9 | 17.9 | 7.10 | 17.9 | 127.4 | 5.4 |
| 2038 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2038 | Earth-New | 111.0 | 111.0 | 111.0 | 7.10 | 111.0 | 788.4 | 33.3 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-Flex | 62.5 | 62.5 | 62.5 | 8.90 | 62.5 | 556.4 | 9.4 |
| 2039 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-Flex | 110.0 | 110.0 | 110.0 | 8.90 | 110.0 | 979.0 | 16.5 |
| 2040 | Earth-New | 130.0 | 130.0 | 130.0 | 7.10 | 130.0 | 923.0 | 39.0 |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| INTRA_MONTH_PEAK | warning | 2039 | 3 |  | 124.018 | 120.000 | 4.018 | stock after inflow 124.018 t exceeds ZBO modernization capacity 120.0 t within 2039-03 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2039 | 4 |  | 128.845 | 120.000 | 8.845 | stock after inflow 128.845 t exceeds ZBO modernization capacity 120.0 t within 2039-04 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2039 | 5 |  | 133.672 | 120.000 | 13.672 | stock after inflow 133.672 t exceeds ZBO modernization capacity 120.0 t within 2039-05 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2039 | 6 |  | 138.499 | 120.000 | 18.499 | stock after inflow 138.499 t exceeds ZBO modernization capacity 120.0 t within 2039-06 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2039 | 7 |  | 143.326 | 120.000 | 23.326 | stock after inflow 143.326 t exceeds ZBO modernization capacity 120.0 t within 2039-07 (before withdrawals) |
| STORAGE_OVERFLOW | hard | 2039 | 8 |  | 121.487 | 120.000 | 1.487 | end-of-month stock 121.487 t exceeds ZBO modernization capacity 120.0 t in 2039-08 |
| STORAGE_OVERFLOW | hard | 2039 | 9 |  | 126.314 | 120.000 | 6.314 | end-of-month stock 126.314 t exceeds ZBO modernization capacity 120.0 t in 2039-09 |
| STORAGE_OVERFLOW | hard | 2039 | 10 |  | 131.141 | 120.000 | 11.141 | end-of-month stock 131.141 t exceeds ZBO modernization capacity 120.0 t in 2039-10 |
| STORAGE_OVERFLOW | hard | 2039 | 11 |  | 135.968 | 120.000 | 15.968 | end-of-month stock 135.968 t exceeds ZBO modernization capacity 120.0 t in 2039-11 |
| STORAGE_OVERFLOW | hard | 2039 | 12 |  | 140.795 | 120.000 | 20.795 | end-of-month stock 140.795 t exceeds ZBO modernization capacity 120.0 t in 2039-12 |
| STORAGE_OVERFLOW | hard | 2040 | 1 |  | 143.698 | 120.000 | 23.698 | end-of-month stock 143.698 t exceeds ZBO modernization capacity 120.0 t in 2040-01 |
| STORAGE_OVERFLOW | hard | 2040 | 2 |  | 146.602 | 120.000 | 26.602 | end-of-month stock 146.602 t exceeds ZBO modernization capacity 120.0 t in 2040-02 |
| STORAGE_OVERFLOW | hard | 2040 | 3 |  | 149.505 | 120.000 | 29.505 | end-of-month stock 149.505 t exceeds ZBO modernization capacity 120.0 t in 2040-03 |
| STORAGE_OVERFLOW | hard | 2040 | 4 |  | 152.408 | 120.000 | 32.408 | end-of-month stock 152.408 t exceeds ZBO modernization capacity 120.0 t in 2040-04 |
| STORAGE_OVERFLOW | hard | 2040 | 5 |  | 155.312 | 120.000 | 35.312 | end-of-month stock 155.312 t exceeds ZBO modernization capacity 120.0 t in 2040-05 |
| STORAGE_OVERFLOW | hard | 2040 | 6 |  | 158.215 | 120.000 | 38.215 | end-of-month stock 158.215 t exceeds ZBO modernization capacity 120.0 t in 2040-06 |
| STORAGE_OVERFLOW | hard | 2040 | 7 |  | 161.118 | 120.000 | 41.118 | end-of-month stock 161.118 t exceeds ZBO modernization capacity 120.0 t in 2040-07 |
| STORAGE_OVERFLOW | hard | 2040 | 8 |  | 164.022 | 120.000 | 44.022 | end-of-month stock 164.022 t exceeds ZBO modernization capacity 120.0 t in 2040-08 |
| STORAGE_OVERFLOW | hard | 2040 | 9 |  | 166.925 | 120.000 | 46.925 | end-of-month stock 166.925 t exceeds ZBO modernization capacity 120.0 t in 2040-09 |
| STORAGE_OVERFLOW | hard | 2040 | 10 |  | 169.828 | 120.000 | 49.828 | end-of-month stock 169.828 t exceeds ZBO modernization capacity 120.0 t in 2040-10 |
| STORAGE_OVERFLOW | hard | 2040 | 11 |  | 172.732 | 120.000 | 52.732 | end-of-month stock 172.732 t exceeds ZBO modernization capacity 120.0 t in 2040-11 |
| STORAGE_OVERFLOW | hard | 2040 | 12 |  | 175.635 | 120.000 | 55.635 | end-of-month stock 175.635 t exceeds ZBO modernization capacity 120.0 t in 2040-12 |

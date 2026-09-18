# P4_full — TEAM_LOW_DEMAND (Низкий спрос (проверка чувствительности, данные организатора))

Feasible: **NO** — hard violations: 40, guideline: 0, warnings: 9

| KPI | Value |
|---|---:|
| total_cost_mln | 11,268.237 |
| pv_cost_mln | 9,198.301 |
| cost_per_served_t_mln | 10.133 |
| pv_cost_per_served_t_mln | 8.272 |
| served_total_t | 1,112.000 |
| demand_total_t | 1,112.000 |
| shortage_total_t | 0.000 |
| shortage_critical_t | 0.000 |
| min_service_level_total | 1.000 |
| min_service_level_critical | 1.000 |
| losses_total_t | 29.492 |
| capex_total_mln | 1,790.000 |
| procurement_total_mln | 8,157.914 |
| reservation_total_mln | 485.716 |
| holding_total_mln | 582.607 |
| fixed_opex_total_mln | 252.000 |
| take_or_pay_idle_t | 0.000 |

## Yearly balance

| Year | Demand | Critical | Served | SL total | SL crit | Shortage | Inflow (actual) | Losses | Open | Close | R45 | Reserve OK | Storage |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:---:|---|
| 2035 | 80.0 | 64.0 | 80.0 | 1.000 | 1.000 | 0.0 | 109.9 | 4.94 | 12.3 | 37.3 | 9.9 | yes | BASE |
| 2036 | 112.0 | 84.0 | 112.0 | 1.000 | 1.000 | 0.0 | 153.1 | 6.89 | 37.3 | 71.4 | 13.8 | yes | BASE |
| 2037 | 152.0 | 108.0 | 152.0 | 1.000 | 1.000 | 0.0 | 203.2 | 5.79 | 71.4 | 116.8 | 18.7 | yes | ZBO |
| 2038 | 200.0 | 136.0 | 200.0 | 1.000 | 1.000 | 0.0 | 261.8 | 3.14 | 116.8 | 175.5 | 24.7 | yes | ZBO |
| 2039 | 256.0 | 168.0 | 256.0 | 1.000 | 1.000 | 0.0 | 332.6 | 3.99 | 175.5 | 248.1 | 31.6 | yes | ZBO |
| 2040 | 312.0 | 200.0 | 312.0 | 1.000 | 1.000 | 0.0 | 394.7 | 4.74 | 248.1 | 326.1 | 38.5 | yes | ZBO |

## Finance (mln, constant 2035 prices)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 17.9 | 0.0 | 360.0 | 1225.4 | 1225.4 |
| 2036 | 948.9 | 68.9 | 39.1 | 0.0 | 1250.0 | 2306.9 | 2136.0 |
| 2037 | 1271.6 | 89.5 | 67.2 | 6.0 | 180.0 | 1614.3 | 1384.0 |
| 2038 | 1303.0 | 72.8 | 99.3 | 82.0 | 0.0 | 1557.1 | 1236.1 |
| 2039 | 1698.6 | 92.3 | 152.5 | 82.0 | 0.0 | 2025.4 | 1488.7 |
| 2040 | 2139.6 | 110.9 | 206.7 | 82.0 | 0.0 | 2539.3 | 1728.2 |

## Source schedule (t)

| Year | Source | Reserved t/yr | Ordered | Delivered | Price | Payable | Procurement | Reservation |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2035 | Earth-Core | 109.9 | 109.9 | 109.9 | 6.20 | 109.9 | 681.2 | 49.4 |
| 2036 | Earth-Core | 153.1 | 153.1 | 153.1 | 6.20 | 153.1 | 948.9 | 68.9 |
| 2037 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2037 | Earth-New | 13.2 | 13.2 | 13.2 | 7.10 | 13.2 | 93.6 | 4.0 |
| 2038 | Earth-Core | 161.8 | 161.8 | 161.8 | 6.20 | 161.8 | 1003.0 | 72.8 |
| 2038 | Lunar-ISRU | 120.0 | 100.0 | 100.0 | 3.00 | 100.0 | 300.0 | 0.0 |
| 2039 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2039 | Earth-New | 22.6 | 22.6 | 22.6 | 7.10 | 22.6 | 160.6 | 6.8 |
| 2039 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |
| 2040 | Earth-Core | 190.0 | 190.0 | 190.0 | 6.20 | 190.0 | 1178.0 | 85.5 |
| 2040 | Earth-New | 84.7 | 84.7 | 84.7 | 7.10 | 84.7 | 601.6 | 25.4 |
| 2040 | Lunar-ISRU | 120.0 | 120.0 | 120.0 | 3.00 | 120.0 | 360.0 | 0.0 |

## Constraint checks

| Rule | Severity | Year | Month | Source | Actual | Limit | Excess | Message |
|---|---|---:|---:|---|---:|---:|---:|---|
| INTRA_MONTH_PEAK | warning | 2036 | 9 |  | 72.217 | 70.000 | 2.217 | stock after inflow 72.217 t exceeds Base storage capacity 70.0 t within 2036-09 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2036 | 10 |  | 75.064 | 70.000 | 5.064 | stock after inflow 75.064 t exceeds Base storage capacity 70.0 t within 2036-10 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2036 | 11 |  | 77.911 | 70.000 | 7.911 | stock after inflow 77.911 t exceeds Base storage capacity 70.0 t within 2036-11 (before withdrawals) |
| STORAGE_OVERFLOW | hard | 2036 | 12 |  | 71.425 | 70.000 | 1.425 | end-of-month stock 71.425 t exceeds Base storage capacity 70.0 t in 2036-12 |
| STORAGE_OVERFLOW | hard | 2037 | 1 |  | 74.929 | 70.000 | 4.929 | end-of-month stock 74.929 t exceeds Base storage capacity 70.0 t in 2037-01 |
| STORAGE_OVERFLOW | hard | 2037 | 2 |  | 78.432 | 70.000 | 8.432 | end-of-month stock 78.432 t exceeds Base storage capacity 70.0 t in 2037-02 |
| STORAGE_OVERFLOW | hard | 2037 | 3 |  | 81.936 | 70.000 | 11.936 | end-of-month stock 81.936 t exceeds Base storage capacity 70.0 t in 2037-03 |
| STORAGE_OVERFLOW | hard | 2037 | 4 |  | 85.440 | 70.000 | 15.440 | end-of-month stock 85.440 t exceeds Base storage capacity 70.0 t in 2037-04 |
| STORAGE_OVERFLOW | hard | 2037 | 5 |  | 88.944 | 70.000 | 18.944 | end-of-month stock 88.944 t exceeds Base storage capacity 70.0 t in 2037-05 |
| STORAGE_OVERFLOW | hard | 2037 | 6 |  | 92.447 | 70.000 | 22.447 | end-of-month stock 92.447 t exceeds Base storage capacity 70.0 t in 2037-06 |
| INTRA_MONTH_PEAK | warning | 2037 | 10 |  | 121.364 | 120.000 | 1.364 | stock after inflow 121.364 t exceeds ZBO modernization capacity 120.0 t within 2037-10 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2037 | 11 |  | 125.426 | 120.000 | 5.426 | stock after inflow 125.426 t exceeds ZBO modernization capacity 120.0 t within 2037-11 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2037 | 12 |  | 129.489 | 120.000 | 9.489 | stock after inflow 129.489 t exceeds ZBO modernization capacity 120.0 t within 2037-12 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2038 | 1 |  | 130.141 | 120.000 | 10.141 | stock after inflow 130.141 t exceeds ZBO modernization capacity 120.0 t within 2038-01 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2038 | 2 |  | 126.794 | 120.000 | 6.794 | stock after inflow 126.794 t exceeds ZBO modernization capacity 120.0 t within 2038-02 (before withdrawals) |
| INTRA_MONTH_PEAK | warning | 2038 | 3 |  | 133.326 | 120.000 | 13.326 | stock after inflow 133.326 t exceeds ZBO modernization capacity 120.0 t within 2038-03 (before withdrawals) |
| STORAGE_OVERFLOW | hard | 2038 | 4 |  | 123.192 | 120.000 | 3.192 | end-of-month stock 123.192 t exceeds ZBO modernization capacity 120.0 t in 2038-04 |
| STORAGE_OVERFLOW | hard | 2038 | 5 |  | 129.725 | 120.000 | 9.725 | end-of-month stock 129.725 t exceeds ZBO modernization capacity 120.0 t in 2038-05 |
| STORAGE_OVERFLOW | hard | 2038 | 6 |  | 136.257 | 120.000 | 16.257 | end-of-month stock 136.257 t exceeds ZBO modernization capacity 120.0 t in 2038-06 |
| STORAGE_OVERFLOW | hard | 2038 | 7 |  | 142.790 | 120.000 | 22.790 | end-of-month stock 142.790 t exceeds ZBO modernization capacity 120.0 t in 2038-07 |
| STORAGE_OVERFLOW | hard | 2038 | 8 |  | 149.322 | 120.000 | 29.322 | end-of-month stock 149.322 t exceeds ZBO modernization capacity 120.0 t in 2038-08 |
| STORAGE_OVERFLOW | hard | 2038 | 9 |  | 155.855 | 120.000 | 35.855 | end-of-month stock 155.855 t exceeds ZBO modernization capacity 120.0 t in 2038-09 |
| STORAGE_OVERFLOW | hard | 2038 | 10 |  | 162.387 | 120.000 | 42.387 | end-of-month stock 162.387 t exceeds ZBO modernization capacity 120.0 t in 2038-10 |
| STORAGE_OVERFLOW | hard | 2038 | 11 |  | 168.920 | 120.000 | 48.920 | end-of-month stock 168.920 t exceeds ZBO modernization capacity 120.0 t in 2038-11 |
| STORAGE_OVERFLOW | hard | 2038 | 12 |  | 175.452 | 120.000 | 55.452 | end-of-month stock 175.452 t exceeds ZBO modernization capacity 120.0 t in 2038-12 |
| STORAGE_OVERFLOW | hard | 2039 | 1 |  | 181.505 | 120.000 | 61.505 | end-of-month stock 181.505 t exceeds ZBO modernization capacity 120.0 t in 2039-01 |
| STORAGE_OVERFLOW | hard | 2039 | 2 |  | 187.557 | 120.000 | 67.557 | end-of-month stock 187.557 t exceeds ZBO modernization capacity 120.0 t in 2039-02 |
| STORAGE_OVERFLOW | hard | 2039 | 3 |  | 193.610 | 120.000 | 73.610 | end-of-month stock 193.610 t exceeds ZBO modernization capacity 120.0 t in 2039-03 |
| STORAGE_OVERFLOW | hard | 2039 | 4 |  | 199.662 | 120.000 | 79.662 | end-of-month stock 199.662 t exceeds ZBO modernization capacity 120.0 t in 2039-04 |
| STORAGE_OVERFLOW | hard | 2039 | 5 |  | 205.715 | 120.000 | 85.715 | end-of-month stock 205.715 t exceeds ZBO modernization capacity 120.0 t in 2039-05 |
| STORAGE_OVERFLOW | hard | 2039 | 6 |  | 211.767 | 120.000 | 91.767 | end-of-month stock 211.767 t exceeds ZBO modernization capacity 120.0 t in 2039-06 |
| STORAGE_OVERFLOW | hard | 2039 | 7 |  | 217.820 | 120.000 | 97.820 | end-of-month stock 217.820 t exceeds ZBO modernization capacity 120.0 t in 2039-07 |
| STORAGE_OVERFLOW | hard | 2039 | 8 |  | 223.872 | 120.000 | 103.872 | end-of-month stock 223.872 t exceeds ZBO modernization capacity 120.0 t in 2039-08 |
| STORAGE_OVERFLOW | hard | 2039 | 9 |  | 229.925 | 120.000 | 109.925 | end-of-month stock 229.925 t exceeds ZBO modernization capacity 120.0 t in 2039-09 |
| STORAGE_OVERFLOW | hard | 2039 | 10 |  | 235.978 | 120.000 | 115.978 | end-of-month stock 235.978 t exceeds ZBO modernization capacity 120.0 t in 2039-10 |
| STORAGE_OVERFLOW | hard | 2039 | 11 |  | 242.030 | 120.000 | 122.030 | end-of-month stock 242.030 t exceeds ZBO modernization capacity 120.0 t in 2039-11 |
| STORAGE_OVERFLOW | hard | 2039 | 12 |  | 248.083 | 120.000 | 128.083 | end-of-month stock 248.083 t exceeds ZBO modernization capacity 120.0 t in 2039-12 |
| STORAGE_OVERFLOW | hard | 2040 | 1 |  | 254.583 | 120.000 | 134.583 | end-of-month stock 254.583 t exceeds ZBO modernization capacity 120.0 t in 2040-01 |
| STORAGE_OVERFLOW | hard | 2040 | 2 |  | 261.083 | 120.000 | 141.083 | end-of-month stock 261.083 t exceeds ZBO modernization capacity 120.0 t in 2040-02 |
| STORAGE_OVERFLOW | hard | 2040 | 3 |  | 267.583 | 120.000 | 147.583 | end-of-month stock 267.583 t exceeds ZBO modernization capacity 120.0 t in 2040-03 |
| STORAGE_OVERFLOW | hard | 2040 | 4 |  | 274.083 | 120.000 | 154.083 | end-of-month stock 274.083 t exceeds ZBO modernization capacity 120.0 t in 2040-04 |
| STORAGE_OVERFLOW | hard | 2040 | 5 |  | 280.583 | 120.000 | 160.583 | end-of-month stock 280.583 t exceeds ZBO modernization capacity 120.0 t in 2040-05 |
| STORAGE_OVERFLOW | hard | 2040 | 6 |  | 287.083 | 120.000 | 167.083 | end-of-month stock 287.083 t exceeds ZBO modernization capacity 120.0 t in 2040-06 |
| STORAGE_OVERFLOW | hard | 2040 | 7 |  | 293.583 | 120.000 | 173.583 | end-of-month stock 293.583 t exceeds ZBO modernization capacity 120.0 t in 2040-07 |
| STORAGE_OVERFLOW | hard | 2040 | 8 |  | 300.083 | 120.000 | 180.083 | end-of-month stock 300.083 t exceeds ZBO modernization capacity 120.0 t in 2040-08 |
| STORAGE_OVERFLOW | hard | 2040 | 9 |  | 306.583 | 120.000 | 186.583 | end-of-month stock 306.583 t exceeds ZBO modernization capacity 120.0 t in 2040-09 |
| STORAGE_OVERFLOW | hard | 2040 | 10 |  | 313.083 | 120.000 | 193.083 | end-of-month stock 313.083 t exceeds ZBO modernization capacity 120.0 t in 2040-10 |
| STORAGE_OVERFLOW | hard | 2040 | 11 |  | 319.583 | 120.000 | 199.583 | end-of-month stock 319.583 t exceeds ZBO modernization capacity 120.0 t in 2040-11 |
| STORAGE_OVERFLOW | hard | 2040 | 12 |  | 326.083 | 120.000 | 206.083 | end-of-month stock 326.083 t exceeds ZBO modernization capacity 120.0 t in 2040-12 |

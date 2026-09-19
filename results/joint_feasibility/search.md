# EXP-15 Перебор единых графиков между планом BASE и стресс-адаптированным планом

| variant | base_feasible | stress_feasible | base_hard | stress_hard | base_rules | stress_rules | base_pv_mln | stress_pv_mln |
|---|---|---|---|---|---|---|---|---|
| lambda=0.0 | True | False | 0 | 3 | — | RESERVE_45D | 8,729.774 | 9,143.268 |
| lambda=0.1 | True | False | 0 | 3 | — | RESERVE_45D | 8,821.281 | 9,234.207 |
| lambda=0.2 | True | False | 0 | 3 | — | RESERVE_45D | 8,912.789 | 9,325.588 |
| lambda=0.3 | True | False | 0 | 3 | — | RESERVE_45D | 9,004.295 | 9,417.653 |
| lambda=0.4 | False | False | 10 | 3 | INTRA_MONTH_PEAK | RESERVE_45D | 9,095.802 | 9,510.928 |
| lambda=0.5 | False | False | 13 | 3 | INTRA_MONTH_PEAK | RESERVE_45D | 9,187.310 | 9,605.684 |
| lambda=0.6 | False | False | 19 | 3 | INTRA_MONTH_PEAK; STORAGE_OVERFLOW | RESERVE_45D | 9,278.817 | 9,701.633 |
| lambda=0.7 | False | False | 27 | 3 | INTRA_MONTH_PEAK; STORAGE_OVERFLOW | RESERVE_45D | 9,370.324 | 9,799.170 |
| lambda=0.8 | False | False | 33 | 3 | INTRA_MONTH_PEAK; STORAGE_OVERFLOW | RESERVE_45D | 9,461.831 | 9,898.507 |
| lambda=0.9 | False | False | 36 | 3 | INTRA_MONTH_PEAK; STORAGE_OVERFLOW | RESERVE_45D | 9,553.339 | 9,998.175 |
| lambda=1.0 | False | True | 39 | 0 | INTRA_MONTH_PEAK; STORAGE_OVERFLOW | — | 9,644.846 | 10,097.842 |

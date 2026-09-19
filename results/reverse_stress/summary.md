# EXP-07 Reverse stress: fixed P3_isru_zbo_adapted

Reference: MANDATORY_STRESS. Additional shocks in 2038-2040: demand *= 1+d; ISRU share *= 1-s.
Failure: any hard violation or annual service below the 97%/99% guidelines (engine tolerances apply).
Metric: max(d,s); domain [0, 0.5]^2; absolute radius tolerance 1.0e-12.
All table shocks are fractions, NOT percent. Each row brackets one point on the boundary.

| Direction d:s | Passing radius | Failing radius | d at failure | s at failure | First violation |
|---|---:|---:|---:|---:|---|
| 1:0 | 6.62500497128e-07 | 6.62501406623e-07 | 6.62501406623e-07 | 0 | RESERVE_45D @ 2040-01 |
| 1:0.25 | 6.30720023764e-07 | 6.30720933259e-07 | 6.30720933259e-07 | 1.57680233315e-07 | RESERVE_45D @ 2040-01 |
| 1:0.5 | 6.01849023951e-07 | 6.01849933446e-07 | 6.01849933446e-07 | 3.00924966723e-07 | RESERVE_45D @ 2040-01 |
| 1:0.75 | 5.75505509914e-07 | 5.75506419409e-07 | 5.75506419409e-07 | 4.31629814557e-07 | RESERVE_45D @ 2040-01 |
| 1:1 | 5.51372068003e-07 | 5.51372977498e-07 | 5.51372977498e-07 | 5.51372977498e-07 | RESERVE_45D @ 2040-01 |
| 0.75:1 | 6.96233655617e-07 | 6.96234565112e-07 | 5.22175923834e-07 | 6.96234565112e-07 | RESERVE_45D @ 2040-01 |
| 0.5:1 | 9.44339262787e-07 | 9.44340172282e-07 | 4.72170086141e-07 | 9.44340172282e-07 | RESERVE_45D @ 2040-01 |
| 0.25:1 | 1.46717320604e-06 | 1.46717411553e-06 | 3.66793528883e-07 | 1.46717411553e-06 | RESERVE_45D @ 2040-01 |
| 0:1 | 3.28704481944e-06 | 3.28704572894e-06 | 0 | 3.28704572894e-06 | RESERVE_45D @ 2040-01 |

## Minimum shock (diagonal certificate)

Failure infimum bracket: [5.51372068003e-07, 5.51372977498e-07].
First: RESERVE_45D @ 2040-01; severity=hard; actual=55.2945500353, limit=55.2945510358, excess=1.00052911023e-06.
A sub-rounding-sized threshold is numerical slack, not evidence of operational resilience.

The passing diagonal dominates every point in its L-inf square; the failing diagonal is a witness.
Monotonicity is specific to this fixed P3: demand rises, net inflow falls, ZBO loss rate is constant
in the shock years; contracts, capacities and investments stay fixed. Storage overflow cannot be introduced.
The strict failure boundary is reported as an interval, not an exact attained minimum.
report.json contains input/code hashes, snapshots, tolerances, endpoint scenarios/KPIs and all minimum-witness violations.

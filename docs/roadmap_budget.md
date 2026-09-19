# Budget and roadmap 2035–2040 (R2 selection: P2z; mln constant 2035 prices)

## Selection and scope

R2 selects **P2z (Earth-New + ZBO)** for the lowest PV cost of passing MANDATORY_STRESS
after advance adaptation among the tested P2z/P3/P4 plans: **10 097.472 mln PV**, versus
10 578.228 for P4 and 10 636.655 for P3 (EXP-02, `results/stress/summary.csv`).
All three adapted plans pass that scenario without shortage or violations. P3 remains cheaper
in BASE (EXP-01). This criterion-based selection is **not proof of universal robustness**.

BASE and stress-adapted budgets below represent different operating plans, not one online
response policy. The fixed BASE P2z has 95.9174 t shortage and reserve/service violations in
MANDATORY_STRESS; the stress-adapted P2z has 17 hard storage-overflow violations when run in BASE
(EXP-02). A switching policy that passes both environments has not been verified.

## Investment timeline (published P2z plans)

| Date | Decision | Amount | Gate / condition | Owner |
|---|---|---:|---|---|
| 2035-01 | Earth-New option fee + exercise | 90 + 270 = 360 | G1: recorded payment dates; planned commissioning 2037-01 | FIN/OP |
| 2037-01 | Earth-New commissioning | — | G2: check readiness against the published schedule; delay consequences are isolated in EXP-09 | OP |
| 2037-07 | ZBO modernization and commissioning | 180 | G3: zero commissioning lag assumed in the published plans; fixed OPEX 6 in 2037, then 12/yr | OP |
| 2038–2040 | operate the selected scenario-specific order/reservation schedule | see annual budgets | G4: check reserve as well as service; an advance-adapted schedule is not a tested reactive policy | OP |
| End of 2040 | review supply continuity beyond the study horizon | not calculated | G5: no validated 2041+ continuation budget in EXP-01/02/09 | OP/FIN |

Dates and investment amounts: `results/alternatives/P2z_earth_new_zbo_BASE/investments.csv`;
annual investment payments in EXP-02 are unchanged. Cumulative P2z CAPEX is **540** by 2037
and remains 540 through 2040; both published plans pass the CAPEX checks. Owners/gates above
are management checkpoints, not simulated contingency actions.

## Annual budget: P2z BASE (EXP-01)

Source: `results/alternatives/P2z_earth_new_zbo_BASE/financial_breakdown.csv`;
totals: `results/alternatives/summary.csv`. Values shown to one decimal; rounding may affect sums.

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV @ 8 % |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 360.0 | 1 218.2 | 1 218.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1 032.4 | 956.0 |
| 2037 | 1 271.6 | 89.5 | 18.9 | 6.0 | 180.0 | 1 566.0 | 1 342.6 |
| 2038 | 1 687.6 | 107.0 | 25.3 | 12.0 | 0.0 | 1 831.9 | 1 454.2 |
| 2039 | 2 213.3 | 126.4 | 31.5 | 12.0 | 0.0 | 2 383.2 | 1 751.8 |
| 2040 | 2 766.2 | 135.7 | 34.6 | 12.0 | 0.0 | 2 948.5 | 2 006.7 |
| **Σ** | 9 683.8 | 578.8 | 135.7 | 42.0 | 540.0 | 10 980.3 | 8 729.4 |

## Annual budget: P2z adapted to MANDATORY_STRESS (EXP-02)

Source: `results/stress/P2z_earth_new_zbo_adapted_MANDATORY_STRESS/financial_breakdown.csv`;
totals: `results/stress/summary.csv`. Same rounding convention as above.

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV @ 8 % |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 360.0 | 1 218.2 | 1 218.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 0.0 | 1 032.4 | 956.0 |
| 2037 | 1 305.4 | 90.9 | 20.6 | 6.0 | 180.0 | 1 602.9 | 1 374.2 |
| 2038 | 2 260.9 | 118.8 | 29.1 | 12.0 | 0.0 | 2 420.8 | 1 921.7 |
| 2039 | 3 091.0 | 133.9 | 36.2 | 12.0 | 0.0 | 3 273.1 | 2 405.8 |
| 2040 | 3 080.0 | 141.0 | 31.3 | 12.0 | 0.0 | 3 264.3 | 2 221.6 |
| **Σ** | 11 482.3 | 604.8 | 142.5 | 42.0 | 540.0 | 12 811.6 | 10 097.5 |

## Decision points

- **DP-1 (2035-01): Earth-New commitment.** The selected published P2z pays both the option fee
  and exercise cost at this date, with commissioning planned for 2037-01 (EXP-01).
- **DP-2 (2037-01): Earth-New readiness.** EXP-09 shifts commissioning by 3/6/12 months to
  2037-04 / 2037-07 / 2038-01. In fixed P2z under BASE, all three delays preserve 100% total
  and critical service but violate the reserve in 2038–2040; the first availability violation
  is at the missed delivery slot in 2037-01. Readiness is therefore a reserve-risk checkpoint,
  not merely a service check.
- **DP-3 (2037-07): ZBO investment.** Retain the published 180 payment and commissioning date;
  the budgets assume zero commissioning lag (EXP-01/02).
- **DP-4 (advance preparation for 2038–2040): orders and stock.** EXP-02's adapted P2z budget
  already differs from BASE in 2037. Adaptation must not be described as a response implemented
  only after stress observation. The experiments do not establish an information-at-order-date
  switching rule or its cost; using the adapted schedule unchanged in BASE causes overflow.

## Residual risk and budget limits

EXP-09 freezes original CAPEX dates, orders, reservations and monthly delivery slots. Missed
Earth-New slots are lost, with no automatic catch-up or substitution; ordered fuel remains payable.
The lower reported cost under delay is not a risk benefit: holding costs fall and reservation fees
are prorated. Delay damages, refunds and recovery orders are not priced. These BASE delay runs
are separate from EXP-02's mandatory stress and do not establish combined-shock protection.
Source: `results/earth_new_delay/summary.md` and `comparison.csv`.

R3 supplies the published cost, resilience and risk evidence; R2 selects P2z under the stated
cost criterion. The roadmap does not claim a universally robust plan, a validated reactive
policy or a funded continuation beyond 2040.

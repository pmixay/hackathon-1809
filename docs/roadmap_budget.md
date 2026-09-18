# Budget and roadmap 2035–2040 (draft, candidate plans P3 and P2z; mln constant 2035 prices)

## Investment timeline (as in the plans)

| Date | Decision | Amount | Gate / condition | Owner |
|---|---|---:|---|---|
| 2034-01 … 2034-12 | preparatory period: Earth-Core framework signed for 2035 (12-month lead), opening stock 12.9 t via Earth-Flex delivered 2034-12 | 116.9 (booked 2035) | channels available, lead times satisfied | R1/OP |
| 2035-01 | (P2z, P4) Earth-New option fee + exercise | 90 + 270 = 360 | Gate G1: base demand confirmed ≥ 100 t; commissioning 2037-01 | FIN/OP |
| 2036-01 | (P3, P4) Lunar-ISRU pilot CAPEX | 1 250 | Gate G2: financing deadline 2037-12; first-year reliability ≤ 0.78 accepted; first delivery 2038-03 | FIN/OP |
| 2037-07 | ZBO modernization | 180 | Gate G3: target commissioning by 2038-01 conservatively; the engine checks annual losses. EXP-04 lags 7–9 still pass the loss check, lag 10 fails; other stress constraints already fail at lag 0 | OP |
| 2038-01; observation 2038-03 | ISRU commissioning; fixed OPEX 70/yr; ZBO OPEX 12/yr | — | G4: first ISRU delivery in March; EXP-06 permits extra Emergency from May and Flex from July. Volumes use the full stress trajectory, not an online forecast policy | OP |
| 2039–2040 | full ramp; Earth-Core at 190 t/yr | — | G5: 2041 continuity decision (Earth-New if not yet exercised) | OP/FIN |

Cumulative CAPEX: P3 1 430 (2037) ≤ 1 800; P4 1 790 (2037) ≤ 1 800; all ≤ 2 800 by 2040.

## Annual budget (P3 BASE, from `results/alternatives/P3_isru_zbo_BASE/financial_breakdown.csv`)

| Year | Procurement | Reservation | Holding | Fixed OPEX | CAPEX | Total | PV @ 8 % |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2035 | 796.1 | 51.4 | 10.7 | 0.0 | 0.0 | 858.2 | 858.2 |
| 2036 | 948.9 | 68.9 | 14.6 | 0.0 | 1 250.0 | 2 282.4 | 2 113.4 |
| 2037 | 1 295.4 | 87.5 | 18.9 | 6.0 | 180.0 | 1 587.8 | 1 361.3 |
| 2038 | 1 303.0 | 72.8 | 19.4 | 82.0 | 0.0 | 1 477.2 | 1 172.6 |
| 2039 | 1 739.3 | 88.9 | 31.5 | 82.0 | 0.0 | 1 941.7 | 1 427.2 |
| 2040 | 2 292.2 | 98.2 | 34.6 | 82.0 | 0.0 | 2 507.0 | 1 706.2 |
| **Σ** | 8 374.9 | 467.6 | 129.7 | 252.0 | 1 430.0 | 10 654.3 | 8 638.9 |

Stress-adapted budgets: `results/stress/*_adapted_MANDATORY_STRESS/financial_breakdown.csv`.

## Decision points

- **DP-1 (2035-01)** Earth-New option: exercise now (P2z/P4) or keep the 90-mln right and exercise ≤ 2036-01 for 2038 capacity (research variant).
- **DP-2 (2036-01)** ISRU go/no-go: BASE saves 90 mln PV vs Earth-New+ZBO but costs 540 mln more under the mandatory stress; decision depends on the weight given to the stress case and to the 2041+ horizon.
- **DP-3 (2037-07)** ZBO: no-regret (needed for stress, cheaper in BASE).
- **DP-4 (2038-03)** first ISRU observation: Flex (4 months → July) and Emergency (6 weeks rounded to 2 months → May) call-offs in the conditional EXP-06 recovery benchmark. A later June observation has not been simulated and must not inherit EXP-06's service/cost results.

EXP-06 costs 498.506 mln PV more than EXP-02's adaptation, but closes 2040 with 55.295 t
instead of 21.755 t and adds 33.947 t Emergency in 2040. This is not an isolated value-of-information
estimate. The roadmap does not yet supply one adaptive policy that passes both BASE and stress.

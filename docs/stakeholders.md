# Stakeholders — interests, metrics, contract links (draft v0.1)

| Stakeholder | Interest | Metric in the model | Contract / rule that carries it | Bears which cost / risk |
|---|---|---|---|---|
| Depot operator | serve demand at minimum life-cycle cost, keep flexibility | total & PV cost, cost per served t, hard violations = 0, TOP idle t | all contracts; CAPEX limits; reserve rule | TOP idle payments, reservation fees, holding, CAPEX, ISRU under-delivery (no refund) |
| Critical consumers (state missions) | ≥ 99 % service every year, priority in shortage | SL critical, shortage_critical_t | allocation rule critical_first; 45-day reserve | none of the cost; consequence of a shortfall (mission slip, not monetised in the case) |
| Commercial consumers | ≥ 97 % total service, predictable price | SL total, shortage_total_t, cost per served t | allocation after critical demand | absorb the first tonnes of any shortage (critical_first) |
| Earth launch/fuel suppliers (A, B, C) | volume certainty, paid reservation, TOP minimum | reserved t/yr, payable volume, reservation payments | reservation rate, TOP 70 % / 50 %, lead times, revision windows | launch-failure replacement (to be contracted), price-shock exposure of the operator |
| Lunar ISRU supplier / pilot | CAPEX financed before 2038, ramp-up tolerance | actual_delivery_share, fixed OPEX 70/yr | pilot financing, first-year reliability ≤ 0.78 | technology risk shared: operator pays for ordered volume even if undelivered (mandatory stress) |
| Emergency supplier | standby fee, occasional high-price call-offs | Emergency reserved t/yr, ordered t, emergency_share_of_demand | reservation 0.35, 6-week lead time, ≤ 2 years as base | none; benefits from disruptions |
| Financier / investor | CAPEX within 1 800 / 2 800, investment gates, PV of commitments | cumulative CAPEX by year, PV cost, discount rate | CAPEX limits, option structure (90 + 270), gates in roadmap | capital at risk in ISRU (1 250) and Earth-New (360) |

## How risk changes shift the balance (from experiments)

- ISRU shortfall (R1): the operator absorbs +1 605 mln PV to protect critical and total service (adapted P3); without adaptation commercial consumers lose 170 t and critical service still holds (critical_first). Contract lever: no-pay-for-undelivered clause moves ~180 mln (3.0 × 60 t undelivered) back to the ISRU supplier — research scenario.
- Earth price shock (R4): cost lands on the operator (and through tariffs on consumers); Earth-New and ISRU shares are the hedge; suppliers A/B gain.
- Demand below base (R3): TOP on Earth-Core makes the operator pay for 70 % of reserved volume — the supplier keeps revenue, the operator pays for flexibility it does not use.

## MCDA (to do, R2)

Criteria: PV cost, min SL total, min SL critical, shortage in stress, CAPEX at risk, flexibility (share of
no-TOP capacity), losses. Normalisation min–max over the alternative set; weights per stakeholder profile
(operator-cost, critical-service, financier) disclosed in `configs/mcda_profiles.yaml`; results compared across
profiles; critical-service constraints are never traded away (weights cannot repair a hard violation).

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

- Joint mandatory stress (R1 ISRU + R2 demand + R4 prices): pre-committed P3 adaptation costs +1 605.030 mln PV against the fixed plan in the SAME stress; without adaptation commercial consumers lose 170.017 t and critical service still holds. These are not isolated R1 effects. A proposed no-pay-for-undelivered clause would cover (100−55)+(120−90)=75 t of ISRU in 2038–2039, or 225 mln nominal at 3 mln/t (`results/stress/P3_isru_zbo_adapted_MANDATORY_STRESS/source_schedule.csv`). This is conditional contract arithmetic, not a simulated refund/PV benefit or a negotiated term.
- Earth price shock (R4): cost lands on the operator (and through tariffs on consumers); Earth-New and ISRU shares are the hedge; suppliers A/B gain.
- Demand below base (R3): with unchanged orders, EXP-03 has overflow and higher holding cost, but zero TOP idle volume. Cutting orders while reservations stay fixed could create TOP idle payments (Core floor 70%); that operational contract scenario is not demonstrated by the advance re-planning of both orders and reservations in EXP-03.

## MCDA (to do, R2)

Criteria: PV cost, min SL total, min SL critical, shortage in stress, CAPEX at risk, flexibility (share of
no-TOP capacity), losses. Normalisation min–max over the alternative set; weights per stakeholder profile
(operator-cost, critical-service, financier) disclosed in `configs/mcda_profiles.yaml`; results compared across
profiles; critical-service constraints are never traded away (weights cannot repair a hard violation).

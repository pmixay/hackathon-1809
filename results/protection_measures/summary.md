# EXP-08 P3 protection measures: without -> with

Target: additional demand +1.00% and ISRU relative reduction 1.00%, 2038-2040.
Reference environment is MANDATORY_STRESS. Costs are deltas against the same adapted P3, mln constant-2035 units.
Practical minima within defined measure families: stock 0.1 net t, capacity 1 t/year, ZBO 1 month.

| Variant | Extra PV, mln | Extra nominal total, mln | Target passes | Failure radius, % | First failure |
|---|---:|---:|---|---:|---|
| without_measure | 0.000000 | 0.000000 | False | 0.000055137 | RESERVE_45D @ 2040 |
| physical_stock | 83.667825 | 100.208871 | True | 1.007056704 | RESERVE_45D @ 2040 |
| reservation_1t_per_year | 0.467533 | 0.650000 | False | 0.000055137 | RESERVE_45D @ 2040 |
| reservation_full | 69.115239 | 93.217050 | False | 0.000055137 | RESERVE_45D @ 2040 |
| zbo_1month_earlier | 1.958252 | 2.458229 | False | 0.067012751 | RESERVE_45D @ 2040 |
| early_zbo | 48.483510 | 43.628342 | False | 0.993181026 | RESERVE_45D @ 2040 |
| early_zbo_plus_stock | 49.458033 | 44.795530 | True | 1.004911331 | RESERVE_45D @ 2040 |

## Sizing

- physical_stock: minimum=8.6; reported level=8.6; target_met.
- early_zbo: minimum=None; reported level=18; target_unreachable_in_family.
- reservation_only: minimum=None; reported level=full_headroom; no_physical_effect_at_any_level.
- early_zbo_plus_stock: minimum=0.1; reported level=0.1; target_met.

## Interpretation

- Stock is actually purchased and delivered before 2038. Its price includes procurement, additional peak-capacity reservation and holding.
- Capacity-only has no finite protective minimum for this fixed-order test: even all available B/E headroom leaves deliveries and the boundary unchanged.
  The 1 t/year row is a cost diagnostic, not a recommended protection. Activation would require extra orders, lead times and a separate response policy.
- Early ZBO retains the fuel saved from lower pre-2038 losses. Orders are held fixed; reducing procurement by the same amount would remove this buffer.
  Additional costs include earlier CAPEX in PV, extra fixed OPEX and holding. Nominal CAPEX is unchanged; lag stays at the original 0-month assumption.
- Every smaller stock/ZBO level is recorded in sizing.csv. Both the no-additional-shock reference and the target must pass.
  For fixed plans, the diagonal is the worst point of the uncertainty square; boundary.csv includes all nine EXP-07 directions.
- report.json contains input/code hashes, assumptions, plans, yearly finance/reserves, target violations and delivery calendars.
  Units of shock coordinates in CSV/JSON are fractions, not percent. No probability model is used.

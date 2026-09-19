# EXP-09 Earth-New preparation delay: fixed P2z / BASE

Only Earth-New preparation is delayed; original CAPEX, orders, reservations and delivery slots are frozen.
Missed slots are lost, not redistributed. Other sources do not substitute. Prices and demand are BASE.

| Delay, mo | Commissioned | Missed C, t | Shortage, t | Min SL total / critical | Reserve failed years | Max reserve gap, t | PV cost, mln | Delta PV, mln | First violation |
|---:|---|---:|---:|---|---|---:|---:|---:|---|
| 0 | 2037-01 | 0.000000 | 0.000000 | 1.000000 / 1.000000 | none | 0.000000 | 8729.403762 | 0.000000 | none |
| 3 | 2037-04 | 3.297050 | 0.000000 | 1.000000 / 1.000000 | 2038;2039;2040 | 3.148356 | 8721.846100 | -7.557662 | SOURCE_NOT_AVAILABLE @ 2037-01 |
| 6 | 2037-07 | 6.594100 | 0.000000 | 1.000000 / 1.000000 | 2038;2039;2040 | 6.297039 | 8714.774346 | -14.629416 | SOURCE_NOT_AVAILABLE @ 2037-01 |
| 12 | 2038-01 | 13.188200 | 0.000000 | 1.000000 / 1.000000 | 2038;2039;2040 | 12.812010 | 8701.708813 | -27.694949 | SOURCE_NOT_AVAILABLE @ 2037-01 |

## Interpretation and reproduction

- First operational failure is reported separately from the first reserve failure in report.json; yearly.csv gives all annual service and reserve values.
  Year-only SOURCE_NOT_AVAILABLE checks are dated from the first missed frozen delivery in the experiment report; standard engine exports keep the original check.
- A 100% service level does not mean compliance: stock can cover demand while the required 45-day reserve is violated.
- Lower cash cost is not a risk benefit: missed fuel remains payable, but holding falls and reservation fees are prorated to availability.
  No delay damages, refunds or recovery orders are priced. Unchanged annual orders may exceed the delayed channel's prorated reservation.
- delay_XXm/ contains standard CSV/JSON exports and the actual case copy used for calculation.
  Replay with: python -m terraplan verify results/earth_new_delay/delay_03m --case results/earth_new_delay/delay_03m/case
- The scenario IDs are TEAM_*; service failures count in the experiment even when the engine labels them guidelines.

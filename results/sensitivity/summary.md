# EXP-04 Sensitivity — plan P3_isru_zbo (BASE plan, fixed unless stated)

Reference PV cost (BASE, r=8 %): 8,638.9 mln

## Thresholds

| Parameter | Range | Threshold (fixed plan) | Threshold (re-planned) | Note |
|---|---|---:|---:|---|
| demand_multiplier | 0.80..1.30 | 1.05 | 1.3 | fixed plan breaks when demand exceeds ordered volumes; re-planned plan breaks when reserved capacity (A+B+D) is exhausted |
| isru_delivery_share_2038 | 0.30..1.00 | 0.95 | — | largest share at which the fixed plan still breaks; below it the 2038 shortfall exceeds the reserve cushion |
| earth_price_multiplier | 0.80..1.50 | — | — | pure cost effect; no physical constraint depends on price |
| discount_rate_real | 0.00..0.12 | — | — | affects PV only; ranking of alternatives must be re-checked at each rate (see summary.md) |
| zbo_commissioning_lag_months | 0..12 | 10 | — | ZBO decided 2037-07; a lag beyond the threshold leaves base-storage months in 2038 and breaks the 2 % loss ceiling |

## Tornado (PV cost, mln)

| Parameter | Low | PV @ low | PV @ base | High | PV @ high | Swing |
|---|---:|---:|---:|---:|---:|---:|
| earth_price_multiplier | 0.8 | 7,457 | 8,639 | 1.5 | 11,594 | 4,137 |
| discount_rate_real | 0.0 | 10,654 | 8,639 | 0.12 | 7,870 | 2,784 |
| demand_multiplier | 0.8 | 8,980 | 8,639 | 1.3 | 8,539 | 441 |
| isru_delivery_share_2038 | 0.3 | 8,587 | 8,639 | 1.0 | 8,639 | 52 |

## Ranking of alternatives by PV cost at different discount rates (BASE)

| r | P1_earth_only | P2_earth_new | P2z_earth_new_zbo | P3_isru_zbo | P4_full |
|---|---:|---:|---:|---:|---:|
| 0.00 | 9,879 (infeasible) | 11,079 | 10,980 | 10,654 | 10,815 |
| 0.04 | 8,775 (infeasible) | 9,820 | 9,748 | 9,554 | 9,747 |
| 0.08 | 7,857 (infeasible) | 8,780 | 8,729 | 8,639 | 8,858 |
| 0.12 | 7,089 (infeasible) | 7,914 | 7,880 | 7,870 | 8,109 |

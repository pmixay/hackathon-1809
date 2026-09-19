# EXP-11: geopolitical price shock, fixed BASE P2z/P3/P4

TEAM_ASSUMPTION: Earth-Core and Earth-Flex variable prices +25% in 2038-2039 only.
Run on a case copy with an annual scenario overlay; no mandatory-stress demand or ISRU shock.
Costs: mln constant-2035 units, real discount rate 8%. Before/after use the same fixed plan.

| Plan | PV before | PV after | Delta PV | Shortage t before / after | Min reserve slack t before / after | Min total SL before / after | Min critical SL before / after | Reserve failed years before / after |
|---|---:|---:|---:|---|---|---|---|---|
| P2z_earth_new_zbo | 8729.403762 | 9200.295536 | 470.891774 | 0.000000 / 0.000000 | 0.000092 / 0.000092 | 1.000000 / 1.000000 | 1.000000 / 1.000000 | none / none |
| P3_isru_zbo | 8638.856936 | 9091.369527 | 452.512590 | 0.000000 / 0.000000 | 0.000092 / 0.000092 | 1.000000 / 1.000000 | 1.000000 / 1.000000 | none / none |
| P4_full | 8857.609145 | 9273.125433 | 415.516289 | 0.000000 / 0.000000 | 0.000092 / 0.000092 | 1.000000 / 1.000000 | 1.000000 / 1.000000 | none / none |

## Interpretation and limits

- The price shock changes procurement cost, not delivered fuel, stock or service under these fixed plans.
- price_overlay.csv shows every source/year; price_exposure.csv attributes the cost change to payable volumes (including TOP).
- yearly.csv exposes opening stock, reserve requirement/slack and total/critical service, not just aggregate feasibility.
- Failure includes hard and guideline violations: TEAM service checks may be labeled guideline by the existing scenario-scoped rules; the 97%/99% criteria are not relaxed.
- This is an illustrative surcharge on the organizer's aggregate variable price, not an inferred fuel/launch/insurance decomposition.
- No outage, delay, capacity restriction, contract renegotiation, cash-budget constraint or adaptive response is modeled.
- The background is BASE, not MANDATORY_STRESS. This is not a probability model or a universal resilience ranking.
- The P2z selection by lowest advance-adapted mandatory-stress cost remains unchanged.

## Reproduction

```bash
python experiments/run_geopolitical_price_shock.py
python experiments/run_geopolitical_price_shock.py --out results/geopolitical_price_shock_replay --compare results/geopolitical_price_shock
python experiments/provenance.py results/geopolitical_price_shock
python -m terraplan verify results/geopolitical_price_shock/P2z_earth_new_zbo/after --case results/geopolitical_price_shock/case
python tests/independent_recalc.py results/geopolitical_price_shock/P2z_earth_new_zbo/after results/geopolitical_price_shock/case
```

All six runs include standard CSV/JSON exports. The portable manifest hashes copied inputs, compact reports and stable per-run exports.
Standard result.json/run_manifest.json contain output paths and export_envelope.json contains a timestamp; those three files per run are excluded from byte replay comparison.
Their numerical results can be replayed with verify --case; same runtime versions are required for exact normalized-text replay.

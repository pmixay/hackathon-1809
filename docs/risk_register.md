# Risk register (draft v0.1, 2026-09-18) — consequences computed with the digital circuit where marked

Status: TEAM_ASSUMPTION for probabilities/ranges (no organizer statistics); consequences in tonnes / mln / service
come from engine runs listed in the "Evidence" column. Owner codes: OP operator, SUP supplier, FIN financier, CONS consumers.
Qualitative scale (L/M/H) is used only where no calculation exists yet and never replaces computed consequences.

| ID | Event | Cause | Affected parameter | Period | Probability basis / range | Consequence (t / mln / service) | Dependencies | Owner | Mitigation | Residual | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R1 | Lunar-ISRU under-delivery in first years | new technology, reliability 0.78 (2038) | actual_delivery_share D 2038–2039 | 2038–2039 | scenario: 55 % / 75 % (mandatory stress); range 0.3–1.0 explored | fixed P3 plan: shortage 170 t over 2038–2040, SL total 0.81 in 2039, RESERVE_45D broken 2038–2040; adapted plan: +1 605 mln PV (10 637 vs 9 032) to keep SL = 1.0 | R4 (Earth price shock) raises the cost of substitution | OP / SUP | pre-committed 2037 stock (35 t instead of 31 t), Earth-Flex top-ups within 4 months, Emergency standby; contract: no payment for undelivered ISRU volumes (research scenario) | shortfall covered but cost per served t rises 7.67 → 8.67 | `results/stress/compare_P3_isru_zbo.md`, `results/sensitivity/sweep_isru_share_2038.csv` |
| R2 | Demand above base | mission growth | demand multiplier | any year | organizer high case (+10…+25 %); sweep 0.8–1.3 | fixed P3: breaks at ×1.05 (RESERVE_45D); re-planned holds to ×1.25; at ×1.30 A+B+D capacity exhausted → shortage | R1 | OP / CONS | keep Earth-Flex reservation headroom; Earth-New option as capacity insurance (P4) | shortage above ×1.25 without Earth-New | `results/sensitivity/sweep_demand_multiplier.csv`, `results/demand/summary.md` |
| R3 | Demand below base | mission slippage | demand variant low | any year | organizer low case (−20 %) | fixed plan overfills depot (STORAGE_OVERFLOW) and pays TOP idle; re-planned P3 PV 6 873 vs 8 639 | — | OP / FIN | cut Earth-Flex (no TOP) first; keep Earth-Core reservation at TOP-neutral level | TOP on Earth-Core limits reduction to 70 % of reserved | `results/demand/summary.md` |
| R4 | Earth launch price shock | market / geopolitics | variable price A, B | 2038–2039 (+25 % mandatory) or any | scenario ×0.8–1.5 | PV cost swing 7 457 → 11 594 mln over the sweep (largest tornado bar); no physical constraint affected | amplifies R1 substitution cost | OP / FIN | share of ISRU / Earth-New (unshocked prices) as natural hedge; price-indexed contract caps (research scenario) | residual exposure ≈ share of A+B in supply | `results/sensitivity/sweep_earth_price_multiplier.csv` |
| R5 | ZBO commissioning delay | build/launch schedule | zbo_commissioning_lag_months | 2037–2038 | assumption range 0–12 months | in stress: loss ceiling 2 % broken from lag ≥ 10 months (ZBO decided 2037-07) | — | OP / SUP | decide ZBO earlier (2036) to keep ≥ 12 months slack; contract delay penalties | none if decided 2036 | `results/sensitivity/sweep_zbo_lag_stress.csv` |
| R6 | Earth-New preparation slips beyond 24 months | supplier readiness | Earth-New preparation lead time / commissioning | commissioning in 2037–2038; reserve consequences 2038–2040 | TEAM_ASSUMPTION: +0/3/6/12 months on a case copy; no probabilities | fixed P2z / BASE: +3/6/12 months miss 3.297/6.594/13.188 t of C deliveries; no shortage, total/critical SL = 1; RESERVE_45D fails 2038–2040 with maximum gaps 3.148/6.297/12.812 t; PV deltas −7.558/−14.629/−27.695 mln reflect lower holding and prorated reservation fees, not reduced risk | R2 demand growth could compound the event; not combined in this experiment | SUP / OP | pre-commit physical buffer or timely substitute orders; activation and cost need a separate recovery test | all positive tested delays still violate reserve; original 2035-01 option exercise alone does not protect frozen delivery slots | `results/earth_new_delay/summary.md`, `results/earth_new_delay/yearly.csv`, EXP-09 |
| R7 | Emergency lead time / capacity insufficient during a shortfall | 6-week lead time, 80 t/yr cap | Emergency availability | any | deterministic case parameters | 45-day reserve cannot be proven by contract alone; physical stock must cover 6 weeks | R1, R2 | OP | keep physical reserve (reserve_mode physical) | — | engine rule RESERVE_45D (contracted-equivalence test) |
| R8 | Storage overflow in delivery months | lumpy deliveries vs 70 t base capacity | monthly inflow profile | 2035–2037 (before ZBO) | deterministic | STORAGE_OVERFLOW if a monthly delivery exceeds free capacity (~40–55 t) | — | OP | uniform monthly profile; ZBO earlier | — | `tests/test_boundary.py::test_storage_overflow_is_detected` |
| R9 | CAPEX budget breach | option stacking | cumulative CAPEX | through 2037 | deterministic | P4 uses 1 790 of 1 800 mln by 2037 — 10 mln headroom; any overrun breaks CAPEX_2037 | — | FIN | phase Earth-New exercise or ZBO into 2038 only if stress loss ceiling allows (it does not for ZBO) | tight | `results/alternatives/P4_full_BASE/financial_breakdown.csv` |

## EXP-10 update: joint R1 + R2 + R4, conditional on mandatory stress

Evidence: `results/monte_carlo/summary.md`, `report.json`, `run_manifest.json`.
TEAM_ASSUMPTION: persistent additional demand U(0,2%) and relative ISRU delivery reduction
U(0,2%) in 2038–2040; independent Core/Flex price deviation U(-10%,10%) in 2038–2039.
N=10,000 per dependence model, seed=203510, common samples across fixed plans.
This supersedes the earlier proposed R1+R4-only / Core-availability Monte Carlo descriptions.
Core capacity outages remain unmodeled here; price and actual delivery share are distinct factors.

| Fixed adapted P3 protection | Conditional failure frequency (95% Wilson) | Mean extra PV, mln | Shortage frequency | Residual |
|---|---|---:|---:|---|
| None | 100.00% (99.96–100.00%) | 0 | 13.33% | almost all first reserve failures at 2038-01; max shortage 5.464 t |
| Physical stock +8.6 t | 49.43% (48.45–50.41%) | 83.662 | 0% observed | first reserve failure at 2040-01; maximum reserve gap 8.426 t |
| ZBO 2036-01 + stock 0.1 t | 49.59% (48.61–50.57%) | 49.453 | 0% observed | first reserve failure at 2040-01; maximum reserve gap 8.444 t; zero-lag ZBO assumption matters |

No realization violates the annual 97%/99% service thresholds, but reserve failures count as
failures. Mean cost deltas are paired on the same realization; no damage valuation is included.
With fully positively dependent demand/ISRU shocks (separate diagnostic), failure frequencies
are 99.99% / 49.87% / 50.03%; unprotected shortage frequency rises to 19.93%.
These are conditional model frequencies, not empirical real-world probabilities. Wilson intervals
exclude distribution/model uncertainty; neither protection guarantees compliance over the 2% square.

Next (R3 role): reactive reserve activation, Monte Carlo/reverse stress for alternative strategies,
event-based Core availability; geopolitics module (bonus) as a separate TEAM_* scenario with before/after export.

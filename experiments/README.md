# Experiments and test protocols

Every experiment is a script; re-running it regenerates `results/<experiment>/` deterministically.
EXP-10 uses a recorded random seed and common samples; EXP-01–09 and EXP-11 have no random sampling.
Determinism here refers to calculations; standard core export envelopes include timestamps.
Format of each protocol follows the case: goal, varied parameters and their origin, kept conditions, plan under test,
metrics, violation criterion, reproduction.

Common: case data `data/case/` (CASE_INPUT, unchanged), assumptions `configs/assumptions.yaml` (r = 8 % real,
lead-time policy max, ZBO lag 0), engine `src/terraplan`, time step month.

| ID | Script | Goal | Varied | Kept | Plans | Metrics | Violation criterion | Output |
|---|---|---|---|---|---|---|---|---|
| EXP-01 | `run_alternatives.py` | compare content-different strategies on one basis | strategy (sources, investments) | all CASE_INPUT, BASE and MANDATORY_STRESS as given | P1 Earth-only, P2 Earth-New, P2z Earth-New+ZBO, P3 ISRU+ZBO, P4 full | total & PV cost, cost per served t, SL total/critical, shortage, losses, CAPEX, TOP idle | any hard violation; SL < 0.97 / 0.99 | `results/alternatives/` |
| EXP-02 | `run_stress_adaptation.py` | quantify stress consequences and the effect of changing decisions | plan orders/reservations/opening stock re-planned for the stress environment; investments unchanged | mandatory stress multipliers exactly as given; budgets & capacities unchanged | P2z, P3, P4: fixed vs adapted; adapted also run in BASE (cost of hedging) | same + deltas | same | `results/stress/` |
| EXP-03 | `run_demand_sensitivity.py` | low / high demand checks | demand variant (organizer columns), critical share preserved | prices, capacities, stress not applied | fixed BASE plan and re-planned | same | same (guideline) | `results/demand/` |
| EXP-04 | `run_sensitivity.py` | one-at-a-time sensitivity with thresholds | demand ×0.8–1.3; ISRU share 2038 0.3–1.0; Core/Flex price ×0.8–1.5; r 0–12 %; ZBO lag 0–12 mo (in stress) | everything else as BASE | P3 fixed (and re-planned for demand) | PV, shortage, min SL, hard violations | first grid value with a hard violation or SL below threshold | `results/sensitivity/` (sweep_*.csv, thresholds.csv, tornado.csv, summary.md) |
| EXP-06 | `run_reaction.py` | conditional recovery benchmark with delayed activation; full future stress trajectory used to size orders | only Earth-Flex (from 2038-07) and Emergency (from 2038-05) deliveries after observation at 2038-03; monthly profiles | Core orders for ALL years, ISRU, investments and pre-2038 orders/stock fixed as in BASE | P3 fixed vs recovery vs pre-committed adapted; terminal stocks differ | same + shortage by month, Emergency share, terminal stock | same | `results/reaction/` |
| EXP-05 | `run_extensibility.py` | dataset extension on a copy | +Source-X (60 t/yr, 5.5 mln/t, from 2039), +2041 demand 450/290 t | original constraints, engine unchanged | P3 extended | run completes, Source-X used, 2041 computed | — | `results/extensibility/` |

## Reading the outputs

- `results/<exp>/summary.csv|md` — one row per (plan, scenario, variant).
- `results/<exp>/<plan>_<scenario>/` — full export: `summary.md`, `yearly_balance.csv`, `inventory_trace.csv` (monthly), `source_schedule.csv`, `financial_breakdown.csv`, `constraint_checks.csv`, `kpi.csv`, `investments.csv`, `assumptions.csv`, `plan.json`, `scenario.json`, `export_envelope.json`, `results.xlsx`, `run_manifest.json`.
- Comparison BASE vs STRESS: `results/stress/compare_<plan>.md` (metrics, decisions that differ, violations).

## Findings so far (2026-09-18)

1. Earth-only (P1) cannot serve 2040 (capacity 300 t/yr vs ~408 t gross need) — infeasible in BASE.
2. ZBO is needed to meet the annual stress loss ceiling with continued inflows; commissioning before 2038 is a conservative planning target, not an exact engine deadline. For the tested BASE P3 in stress, lags 7–9 still pass the annual loss check, lag 10 first fails it; reserve/service already fail at lag 0. P2z is cheaper than P2 in BASE by 50 mln PV.
3. Cheapest BASE plan: P3 ISRU+ZBO (8 639 mln PV) vs P2z Earth-New+ZBO (8 729) — difference 90 mln.
4. Same plans adapted to stress: P2z 10 097 < P4 10 578 < P3 10 637 mln PV. ISRU's 1250 CAPEX + 70/yr OPEX is not recovered within 2035–2040 when it delivers 55 %/75 % in 2038–2039 and Earth prices are shocked.
5. EXP-04 first sampled adverse failures for fixed BASE P3: demand ×1.05 or ISRU 2038 share 0.95. These are grid observations, not exact boundaries. Re-planned P3 passes constraints at ×1.25 with 12.437 t shortage (min annual service 97.45%); ×1.30 fails. Passing constraints does not imply zero shortage.
6. In stress 2040 Earth A+B+C (430 t/yr) or A+B+D (420) reach capacity; the adapted P3 closes with 21.755 t. Continuation at comparable demand would require added supply/stock; a 2041 recovery choice among the original sources is not calculated. EXP-05 demonstrates extensibility with synthetic Source-X on a different, non-mandatory-stress background.
7. Under low demand a fixed plan overfills the depot. EXP-03 has zero TOP idle volume with unchanged orders; advance re-planning reduces orders AND reservations. An operational order-cut policy under frozen contracts remains untested.
8. EXP-06 is a conditional recovery benchmark: observe in March 2038, permit Emergency from May and Flex from July, size orders using the entire known future stress trajectory. It yields min annual service 0.996987 and 0.866 t shortage, but cannot repair the January 2038 reserve. PV 11 135.161 vs 10 636.655 gives a 498.506 mln difference, not pure value of foresight: terminal stocks are 55.295 vs 21.755 t, including 33.947 t extra Emergency in 2040. Equal terminal conditions and an information-at-order-date policy are needed for a value-of-information claim. No cheapest-hedge claim follows from this comparison.
9. EXP-02 adapted plans are not universal hedges: in BASE P2z has 17 and P3/P4 each 25 hard overflow violations (`results/stress/summary.csv`). EXP-07's stress-adapted P3 boundary is about 0.0000551373% per physical shock, reflecting only 0.47 kg reserve slack at 2040-01.

## Portable provenance (EXP-07–10)

```bash
python experiments/provenance.py
```

- Report/manifest schema version **2**, hash format **`sha256-utf8-lf-v1`**: decode UTF-8,
  convert CRLF and CR to LF, encode UTF-8, SHA-256. No whitespace trimming, rounding,
  JSON reordering or removal of the final newline. Real content changes still fail verification.
- New experimental CSV/JSON/text outputs use LF. Git checkout may change EOL; verification
  compares exact normalized text. Input hashes include the shared `experiments/provenance.py`.
- The command validates saved input/code hashes for all four experiments, EXP-09 case-copy
  hashes and EXP-10's eight output hashes. Tests validate the delivered reports, not only fresh
  reports, and emulate both LF and CRLF checkouts including input/code files.
- The audit refresh re-ran EXP-07–10 with the current assumption registry. EXP-07–09 now include
  the three EXP-10 registry entries in their snapshots; these keys have no effect on their calculations.
  Numerical results are unchanged. This replaces stale historical input hashes with hashes of
  inputs actually used in the refreshed runs; it is not a blind re-signing of old results.
- EXP-09's per-run standard manifests get portable `case_file_sha256` with a separate
  `case_file_hash_format` marker. Core semantic plan/scenario/assumption/KPI hashes and the
  `terraplan verify` calculation check retain their own formats. Core code is unchanged.
- `--compare` for EXP-10 checks normalized artifacts and manifests with the same recorded
  runtime/package versions. Different versions remain visible and may require numerical
  comparison; portability of EOL hashes is not a promise of cross-version byte identity.

## EXP-07: reverse stress of the adapted P3

```bash
python experiments/run_reverse_stress.py --max-shock 0.5 --tolerance 1e-12 --out results/reverse_stress
python -m pytest -q tests/test_reverse_stress.py
```

- **Goal / plan:** find the failure boundary of the saved `configs/plans/P3_isru_zbo_adapted.json`.
  Read the plan as-is; all orders, reservations, opening stock and investments remain frozen.
- **Reference:** `MANDATORY_STRESS`, which the adapted plan passes. In **2038–2040** multiply both
  total and critical demand by `1+d`, and ISRU's actual delivery shares by `1-s`.
  Thus demand multipliers are `1.15*(1+d)` and ISRU shares are `[0.55, 0.75, 1.0]*(1-s)`.
  The reduction is relative, not percentage points. Earlier years, prices, loss ceiling and other
  sources are unchanged; reliability is never multiplied in again.
- **Minimal shock:** infimum of `max(d,s)` over failing points, in the exploratory square
  `0 <= d,s <= 0.5`. Equal weights on relative changes and the 50% search range are
  **TEAM_ASSUMPTION**, not empirical probabilities; saved in `report.json` with the other inputs.
- **Failure:** any engine hard violation **or** annual total/critical service guideline violation
  (97%/99%). Warnings alone do not count. Respect engine tolerances: physical reserve `1e-6 t`,
  service `1e-9`. First violation is chronological (annual checks dated December), ties by rule/source id.
- **Algorithm:** bisect nine normalized rays `(d,s)=t*(u,v)`, including both axes and the diagonal,
  to an absolute radius interval of at most `1e-12`. Save a passing and a failing endpoint.
  If the origin fails, abort; if the upper endpoint passes, report no failure within the domain.
  This fixed P3 has monotone adverse changes: net inflow/stock decrease, demand and reserve needs rise;
  ZBO losses stay at 1.2% in all shock years; unchanged contracts/investments introduce no new nonmonotone
  failure. A passing `(t,t)` dominates every point of `[0,t]^2`; a failing `(t,t)` is a witness.
  Hence the diagonal brackets the **global L-infinity failure infimum**, not just the best sampled ray.
  The other rays describe the boundary; no claim of enumerating its every point is made.
- **Outputs:** `boundary.csv` (full-precision coordinates, first rule/year/month, actual/limit/excess),
  `summary.md`, deterministic `report.json` (plan/scenario/assumption snapshots, input and code hashes,
  method, tolerances, baseline reserves/KPIs, minimum-witness scenarios/KPIs/violations).
  Repeat the command with another `--out` to compare outputs after UTF-8/LF normalization in the same environment.
  No random sampling or seed; `run_all.py` also includes EXP-07. This experiment uses compact CSV/JSON
  reports rather than the full per-run XLSX bundle. Tiny thresholds reflect rounding slack, not a
  meaningful operational safety margin; the passing/failing interval is retained instead of rounding to zero.

## EXP-08: compare protection measures for P3

```bash
python experiments/run_protection_measures.py --target 0.01 --out results/protection_measures
python -m pytest -q tests/test_protection_measures.py
```

The reference is the same saved stress-adapted P3 under MANDATORY_STRESS as in EXP-07.
"Minimum reasonable" means the smallest implementable level in a defined measure family
that passes both the reference and the square `0 <= d,s <= target`. The default **1%**
target is a disclosed TEAM_ASSUMPTION for comparison, not a probability or organizer requirement.
Each variant freezes its decisions during reverse stress; the EXP-07 criterion, nine rays,
50% search bound and `1e-12` radius tolerance are reused. This is a grid minimum within each
specified measure design, not global optimization over delivery schedules or reactive policies.

| Measure | Search / implementation | Cost accounting |
|---|---|---|
| Physical stock | net buffer at 2038-01, steps 0.1 t; extra Earth-Flex deliveries spread over July–December 2037, ordered March–August with 4-month lead; extra monthly deliveries rounded up to 0.0001 t; reserved annualized capacity covers monthly peak | extra procurement + reservation + holding; original investments unchanged |
| Reserved capacity only | 1 t/year diagnostic, cheapest unused B then E capacity in 2038–2040; full available B/E headroom as upper control; A/D already fully reserved | additional reservation payments; B/E have no take-or-pay; no fuel ordered or delivered |
| Early ZBO | move from 2037-07 backwards by whole months, no earlier than 2036-01 (CASE_INPUT availability); keep original orders and retain saved losses as extra stock | same nominal CAPEX, earlier discounted payment + extra OPEX + holding |
| Early ZBO + residual stock | selected early ZBO plus a separate 0.1 t-step search for the remaining buffer | combined costs; shown separately from standalone measures |

The lower storage-loss rate applies once to throughput; saved fuel persists under this model.
ZBO commissioning lag stays at the existing 0-month assumption. Reservation alone cannot improve
the physical boundary with fixed orders; if it cannot meet the target, the report states that no
protective minimum exists instead of labeling 1 t/year as sufficient. A reserve activation policy
would additionally need order decisions, reaction dates and lead-time verification.

Outputs in `results/protection_measures/`: `comparison.csv`, `boundary.csv`, `sizing.csv`
(every smaller stock/ZBO grid point), `summary.md`, standalone `*.plan.json`, and deterministic
`report.json` with input/code hashes, assumption snapshots, nominal cost decomposition,
yearly finance/reserves, delivery calendars, target violations and passing/failing boundary pairs.
Costs are always **with measure minus without measure in the same reference environment**.
Both present value (real 8%, existing annual timing convention) and nominal total differences
are reported. No purchase savings are credited while retaining the same purchased quantities.
The full experiment runner includes EXP-08.

## EXP-09: Earth-New preparation delay (risk R6)

```bash
python experiments/run_earth_new_delay.py --out results/earth_new_delay
python -m pytest -q tests/test_earth_new_delay.py
python -m terraplan verify results/earth_new_delay/delay_03m --case results/earth_new_delay/delay_03m/case
python tests/independent_recalc.py results/earth_new_delay/delay_03m results/earth_new_delay/delay_03m/case
```

- **Plan/environment:** saved P2z Earth-New + ZBO, BASE demand/prices. P3 has no Earth-New investment.
  Keep all investment/payment dates, reservations, annual orders and the original monthly delivery slots.
  This isolates the delay from mandatory stress and from any recovery policy.
- **Risk:** extend only Earth-New's preparation lead-time range on a copy of the case by
  **0/3/6/12 months**. With the existing max-lead policy, commissioning moves from 2037-01
  to 2037-04 / 2037-07 / 2038-01. ISRU, ZBO and other sources keep their original lead times.
  Both endpoints of C's 18–24 month range move by the same amount, marked TEAM_ASSUMPTION.
  CAPEX is paid on the original date; delay is not modeled as a later investment decision.
- **Delivery/contract convention (TEAM_ASSUMPTION):** C orders are frozen as explicit monthly profiles
  from the zero-delay schedule, preventing the engine's uniform profile from compressing the full
  annual order into fewer available months. Slots before commissioning are missed, with no automatic
  catch-up or substitution. Original ordered volumes remain payable; no refund/penalty is invented.
  The engine prorates reservation fees/capacity by availability and reports any resulting contract
  violation. This is a lost-delivery-slot scenario, not a shipment-backlog model.
- **Metrics:** total/critical shortage and service, every year's opening stock/45-day requirement/gap,
  total and PV cost with deltas, missed Earth-New deliveries, all violations, the first chronological
  violation and the first reserve violation. Hard violations and service guidelines count; warnings
  do not. A service level of 100% must not conceal a failed reserve or contract check.
  For an entirely unavailable year the engine's source check has no month; the experiment dates it
  from the first missed frozen delivery slot, explicitly annotating the report copy of the violation.
  Standard engine exports preserve the original annual check.
- **Reproducibility:** `comparison.csv`, `yearly.csv`, `summary.md`, deterministic `report.json`
  with plan/assumption snapshots and input/code hashes. Each `delay_XXm/` has its case copy, standard
  CSV/JSON exports, scenario and run manifest for the existing `verify` command and CSV-only checker.
  Numerical results repeat; standard export envelopes retain their generation timestamps.
  The original case/config files and core engine are unchanged. EXP-09 is included in `run_all.py`.

## EXP-10: conditional Monte Carlo of P3 protections

```bash
python experiments/run_monte_carlo.py --n 10000 --seed 203510 --out results/monte_carlo
python experiments/run_monte_carlo.py --n 10000 --seed 203510 --replay-samples results/monte_carlo/samples.csv --out results/monte_carlo_replay --compare results/monte_carlo
python -m pytest -q tests/test_monte_carlo.py
```

- **Goal / plans:** compare the fixed stress-adapted P3, EXP-08 physical stock +8.6 t,
  and ZBO moved 18 months earlier to 2036-01 plus stock +0.1 t. Reuse EXP-08's builders:
  Flex deliveries July–December 2037, four-month order lead, peak-capacity reservation,
  throughput losses and storage costs. No orders or investments respond to the sample.
- **Background:** MANDATORY_STRESS. A deterministic no-additional-shock control must pass
  for each plan before sampling. This is conditional stress analysis, not a mixture with BASE.
- **Distributions (TEAM_ASSUMPTION):** `d ~ U(0,0.02)` multiplies total AND critical demand
  by `1+d` in 2038–2040; `s ~ U(0,0.02)` multiplies stress ISRU actual delivery shares by
  `1-s` in 2038–2040. `p ~ U(-0.10,0.10)` multiplies stress Core/Flex variable prices by
  `1+p` in 2038–2039 (on top of 1.25). Every factor persists throughout its stated period.
  Reliability is not reapplied. Demand, ISRU and price are independent in the primary model;
  A/B share the same price draw. Parameters and rationale are registered in `configs/assumptions.yaml`.
- **Rationale / scope:** physical ranges straddle the EXP-08 1% protection target; uniforms
  avoid asserting a preferred mode without data. The +/-10% price range is illustrative.
  Older drafts disagreed between Core availability and prices: **EXP-10 selects demand +
  ISRU actual delivery + price**. Random Core capacity outages are excluded, not represented
  by price or conflated with ISRU delivery shares. Price affects cash cost, not the physical
  feasibility of these fixed plans. There are no empirical organizer probabilities.
- **Dependence diagnostic:** separately evaluate `d=0.02*u_demand`, `s=0.02*u_demand`,
  price still independent. Marginal distributions stay the same. Report separately, never
  pool with the independent model or claim this is a worst-case probability bound.
- **Sampling:** N=10,000 **per model**, seed=203510, `random.Random` (MT19937), exactly
  three `random()` calls per sample in order demand/ISRU/price. The diagnostic reuses the
  first uniform for ISRU and consumes no extra random numbers. All plans share the sample;
  60,000 stochastic simulations plus three reference controls. CLI supports smaller N for checks.
- **Failure:** reuse `failure_violations()` from EXP-07: any hard violation OR annual
  97%/99% service guideline violation. Warnings alone do not count. Preserve the engine's
  physical tolerance 1e-6 t and service tolerance 1e-9. First failure = earliest year/month,
  annual checks dated December, undated checks first; retain ALL simultaneous causes.
- **Metrics:** failure count/frequency and two-sided 95% Wilson score interval (valid also
  at zero/all observed failures); reserve/service violation and shortage frequencies separately;
  first-cause/date counts; total and critical shortage, minimum annual services, maximum
  physical reserve gap, PV and paired PV deltas. Every continuous metric includes mean,
  min/max and P5/P50/P95 (linear interpolation at `(N-1)*q`, quantile type 7).
  Shortage frequency uses >1e-6 t. Pairing also records eliminated and introduced failures,
  and net failure reduction in percentage points; no independent-samples comparison is used.
- **Costs:** real mln constant-2035 units, engine's 8% discounting/start-year convention.
  Compare with minus without protection in the SAME realization. No monetized damages,
  mission losses, recovery orders or penalties; no cost-benefit optimum is claimed.
- **Artifacts:** `samples.csv` saves uniforms and transforms at full precision; `runs.csv`
  saves every plan/sample result and simultaneous first violations; `comparison.csv`,
  `report.json`, `summary.md`, three standalone plans. `run_manifest.json` contains N/seed,
  generator/draw order, Python/package/model versions, normalized input/code/output SHA-256, method,
  plan/scenario/assumption snapshots and replay commands. It has no timestamp or output path.
  `--replay-samples` validates the saved sample against the declared N/seed/assumptions;
  `--compare` validates saved inputs and checks every artifact and manifest after LF normalization
  with the same recorded runtime versions; see the portable-provenance section above.
  The manifest does not hash itself. Standard core exporter manifests are not used for EXP-10.
- **Limits:** frequencies describe the chosen conditional model, not real-world risk
  probabilities. Wilson intervals measure sampling error only (~0.98 pp maximum half-width
  at N=10,000), not distribution/dependence uncertainty. Protection against the 1% square
  does not imply protection over the entire sampled 2% square. Early ZBO still assumes zero
  lag and retained throughput-loss savings. BASE overflow and adaptive policies remain separate.

## EXP-11: TEAM geopolitical price shock on a data copy

```bash
python experiments/run_geopolitical_price_shock.py
python experiments/run_geopolitical_price_shock.py --out results/geopolitical_price_shock_replay --compare results/geopolitical_price_shock
python experiments/provenance.py results/geopolitical_price_shock
python -m pytest -q tests/test_geopolitical_price_shock.py
python -m terraplan verify results/geopolitical_price_shock/P2z_earth_new_zbo/after --case results/geopolitical_price_shock/case
python tests/independent_recalc.py results/geopolitical_price_shock/P2z_earth_new_zbo/after results/geopolitical_price_shock/case
```

- **Goal / plans:** isolate procurement-price exposure of the saved BASE P2z/P3/P4 plans.
  Six runs: each fixed plan before (BASE) and after (`TEAM_GEOPOLITICAL_PRICE_SHOCK`).
  No re-planning, no use of stress-adapted orders, no change to the R2 decision.
- **Shock / origin:** variable prices of Earth-Core (A) and Earth-Flex (B) multiplied by
  **1.25 in 2038–2039 only**, returning to BASE in 2040. This is a disclosed illustrative
  `TEAM_ASSUMPTION`, not an empirical forecast or probability. Its magnitude/window matches
  only the price component of MANDATORY_STRESS for comparability; its demand, ISRU and
  loss-ceiling changes are not applied. A: 6.2 → 7.75; B: 8.9 → 11.125 mln/t.
- **Data-copy implementation:** `case/*.csv` is an isolated, unchanged copy of CASE_INPUT;
  `shock.yaml` is a copy of `configs/scenarios/team_geopolitical_price_shock.yaml`.
  The engine's existing annual scenario multiplier applies the surcharge once, on the copied
  dataset. A static source CSV price is not overwritten because it cannot encode the two-year
  window. `price_overlay.csv` records all source/year effective prices and the surcharge.
  The aggregate organizer price is not split into invented launch/fuel/insurance components.
  Original data, scenarios, plans, global assumptions and engine remain unchanged; hashes
  are checked before/after, so no restore operation on CASE_INPUT is needed.
- **Fixed conditions:** BASE demand and actual delivery shares; source capacities, lead times,
  investment/commissioning dates, opening stock, orders, reservations and allocation rules.
  Reservation rates, take-or-pay shares, CAPEX and OPEX remain unchanged. The multiplier
  applies to the price of payable procurement volume, including any take-or-pay floor.
- **Metrics / failure:** PV and total cost with paired deltas; total/critical shortage and
  minimum annual service; annual opening stock, 45-day reserve requirement, slack, maximum
  reserve gap and failed years. Hard **or guideline** violations count as failure, including
  total/critical service below 97%/99%; scenario-scoped TEAM guideline labels do not relax
  the experiment's criterion. `yearly.csv` retains all six years for each run.
- **Published result:** delta PV = **470.891774 / 452.512590 / 415.516289 mln** for
  P2z/P3/P4. After-shock PV = **9200.295536 / 9091.369527 / 9273.125433 mln**.
  All three retain zero shortage, 100% total/critical service and no reserve violations.
  Monthly physical balances are identical before/after. P4 has the smallest additional
  price cost, while P3 retains the lowest total PV on this BASE background; these are
  different criteria and do not replace R2's adapted mandatory-stress comparison.
- **Artifacts / replay:** `results/geopolitical_price_shock/` contains comparison, annual
  reserve/service data, per-source price exposure, method/input snapshots and six standard
  CSV/JSON exports. The top-level manifest uses schema 2 / `sha256-utf8-lf-v1` and hashes
  copied inputs, compact reports and stable per-run exports. Per-run `result.json` and
  `run_manifest.json` contain output paths; `export_envelope.json` contains timestamps.
  Those three files are excluded from byte replay comparison; standard `verify --case`
  replays their numerical results. `--compare` checks saved hashes and identical normalized
  outputs at the same runtime versions. The full runner includes EXP-11.
  Because EXP-10 hashes `run_all.py`, adding EXP-11 required a full EXP-10 replay with its
  saved N=10,000/seed=203510 samples. Its numerical output hashes are unchanged; only the
  input provenance manifest was regenerated (including the already integrated R4 source).
- **Tests / limits:** untouched-input and copy checks; exact source/period isolation and
  return to BASE price; independent surcharge/PV arithmetic; full physical invariance;
  six export replays and CSV-only recalculations; repeatability, tamper detection and
  published-artifact checks. The experiment does not model geopolitical supply outages,
  payment/budget limits, delay, response policies or combined shocks. Physical invariance
  in a price-only fixed-plan run is not evidence of universal geopolitical resilience.

## To do (R3)

- Reverse stress for alternative strategies (P3 baseline and protection measures: EXP-07/08 above).
- Event-based Core availability, response policies and alternative-strategy Monte Carlo beyond EXP-10.
- Geopolitical supply interruptions and combined price/availability shocks beyond the isolated EXP-11 price overlay.

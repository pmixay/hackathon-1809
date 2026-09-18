# Experiments and test protocols

Every experiment is a script; re-running it regenerates `results/<experiment>/` deterministically.
EXP-10 uses a recorded random seed and common samples; EXP-01–09 have no random sampling.
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
| EXP-06 | `run_reaction.py` | show reaction times and already-taken commitments under stress (no foresight) | only Earth-Flex (from 2038-07) and Emergency (from 2038-05) orders after the ISRU shortfall is observed at 2038-03; monthly profiles | everything decided before 2038-03 frozen as in the BASE plan (Core 2038–2039, ISRU, investments, 2037 stock) | P3 fixed vs reactive vs pre-committed adapted | same + shortage by month, Emergency share | same | `results/reaction/` |
| EXP-05 | `run_extensibility.py` | dataset extension on a copy | +Source-X (60 t/yr, 5.5 mln/t, from 2039), +2041 demand 450/290 t | original constraints, engine unchanged | P3 extended | run completes, Source-X used, 2041 computed | — | `results/extensibility/` |

## Reading the outputs

- `results/<exp>/summary.csv|md` — one row per (plan, scenario, variant).
- `results/<exp>/<plan>_<scenario>/` — full export: `summary.md`, `yearly_balance.csv`, `inventory_trace.csv` (monthly), `source_schedule.csv`, `financial_breakdown.csv`, `constraint_checks.csv`, `kpi.csv`, `investments.csv`, `assumptions.csv`, `plan.json`, `scenario.json`, `export_envelope.json`, `results.xlsx`, `run_manifest.json`.
- Comparison BASE vs STRESS: `results/stress/compare_<plan>.md` (metrics, decisions that differ, violations).

## Findings so far (2026-09-18)

1. Earth-only (P1) cannot serve 2040 (capacity 300 t/yr vs ~408 t gross need) — infeasible in BASE.
2. Every stress-feasible plan needs ZBO before 2038 (loss ceiling 2 %). ZBO also pays for itself in BASE (P2z cheaper than P2 by 50 mln PV).
3. Cheapest BASE plan: P3 ISRU+ZBO (8 639 mln PV) vs P2z Earth-New+ZBO (8 729) — difference 90 mln.
4. Same plans adapted to stress: P2z 10 097 < P4 10 578 < P3 10 637 mln PV. ISRU's 1250 CAPEX + 70/yr OPEX is not recovered within 2035–2040 when it delivers 55 %/75 % in 2038–2039 and Earth prices are shocked.
5. Fixed plans have zero slack: P3 breaks at demand ×1.05 or ISRU 2038 share 0.95 (RESERVE_45D). Re-planned P3 holds up to ×1.25 demand; at ×1.30 reserved capacity A+B+D is exhausted.
6. In stress 2040 all Earth channels (A 190 + B 110 + C 130 = 430) or A+B+D (420) are at capacity; closing stock falls below the 45-day level at end-2040 — 2041 continuity requires Emergency (≤ 2 years) or both Earth-New and ISRU.
7. Under low demand a fixed plan overfills the depot (STORAGE_OVERFLOW) — Earth-Flex orders must be cut; TOP on Earth-Core limits how far.
8. EXP-06: reacting only after the ISRU shortfall is observed (2038-03) keeps service at 0.997 (0.9 t short in 2038-04 before Flex/Emergency arrive) but costs 11 135 mln PV vs 10 637 for the pre-committed adaptation (+500 mln: Emergency 39 t in 2038 at 13.8, extra Flex) and cannot repair the 2038-01 reserve (30.8 t < 35.4 t) decided in 2037. Foresight of the stress is worth ≈ 500 mln PV; the cheapest hedge is the 2037 stock top-up (4.6 t).

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
  Repeat the command with another `--out` to compare outputs byte-for-byte in the same environment.
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
  generator/draw order, Python/package/model versions, input/code/output SHA-256, method,
  plan/scenario/assumption snapshots and replay commands. It has no timestamp or output path.
  `--replay-samples` validates the saved sample against the declared N/seed/assumptions;
  `--compare` checks every artifact and manifest byte-for-byte in the same environment.
  The manifest does not hash itself. Standard core exporter manifests are not used for EXP-10.
- **Limits:** frequencies describe the chosen conditional model, not real-world risk
  probabilities. Wilson intervals measure sampling error only (~0.98 pp maximum half-width
  at N=10,000), not distribution/dependence uncertainty. Protection against the 1% square
  does not imply protection over the entire sampled 2% square. Early ZBO still assumes zero
  lag and retained throughput-loss savings. BASE overflow and adaptive policies remain separate.

## To do (R3)

- Reverse stress for alternative strategies (P3 baseline and protection measures: EXP-07/08 above).
- Event-based Core availability, response policies and alternative-strategy Monte Carlo beyond EXP-10.
- Geopolitics module: event → price component multiplier on a data copy, before/after, restore.

# Stress-test methodology and protocols

The current authoritative protocols, including EXP-07–10, are in [experiments/README.md](../experiments/README.md).
The EXP-01–06 overview below is maintained against those protocols; the detailed protocols are not duplicated here.
EXP-10 uses a fixed seed and saved common samples; EXP-01–09 have no random sampling.
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
| EXP-06 | `run_reaction.py` | conditional recovery benchmark using the full future stress trajectory | Flex deliveries from 2038-07, Emergency from 2038-05 after observation at 2038-03 | Core orders ALL years, ISRU, investments and pre-2038 orders/stock fixed | fixed vs recovery vs pre-committed adaptation; different terminal stocks | same + shortage by month, Emergency share, terminal stock | same | `results/reaction/` |
| EXP-05 | `run_extensibility.py` | dataset extension on a copy | +Source-X (60 t/yr, 5.5 mln/t, from 2039), +2041 demand 450/290 t | original constraints, engine unchanged | P3 extended | run completes, Source-X used, 2041 computed | — | `results/extensibility/` |

## Reading the outputs

- `results/<exp>/summary.csv|md` — one row per (plan, scenario, variant).
- `results/<exp>/<plan>_<scenario>/` — full export: `summary.md`, `yearly_balance.csv`, `inventory_trace.csv` (monthly), `source_schedule.csv`, `financial_breakdown.csv`, `constraint_checks.csv`, `kpi.csv`, `investments.csv`, `assumptions.csv`, `plan.json`, `scenario.json`, `export_envelope.json`, `results.xlsx`, `run_manifest.json`.
- Comparison BASE vs STRESS: `results/stress/compare_<plan>.md` (metrics, decisions that differ, violations).

## Findings so far (2026-09-18)

1. Earth-only (P1) cannot serve 2040 (capacity 300 t/yr vs ~408 t gross need) — infeasible in BASE.
2. ZBO is needed for the annual stress loss ceiling with ongoing supply. A pre-2038 startup is a conservative target, not the exact annual-check boundary; EXP-04 first fails the loss check at lag 10, while reserve/service already fail at lag 0. P2z is cheaper than P2 in BASE by 50 mln PV.
3. Cheapest BASE plan: P3 ISRU+ZBO (8 639 mln PV) vs P2z Earth-New+ZBO (8 729) — difference 90 mln.
4. Same plans adapted to stress: P2z 10 097 < P4 10 578 < P3 10 637 mln PV. ISRU's 1250 CAPEX + 70/yr OPEX is not recovered within 2035–2040 when it delivers 55 %/75 % in 2038–2039 and Earth prices are shocked.
5. EXP-04's ×1.05 demand / 0.95 ISRU share are first failed adverse grid points for fixed BASE P3, not exact boundaries. Re-planned ×1.25 passes constraints but has 12.437 t shortage and min annual service 97.45%; ×1.30 fails.
6. Adapted P3 closes stress 2040 at 21.755 t with A+B+D at capacity. A 2041 recovery choice requires another calculation; EXP-05 is a non-mandatory-stress extensibility demonstration with synthetic Source-X.
7. Fixed low-demand plans overflow, but EXP-03 reports zero TOP idle volume. Its advance re-planning changes orders and reservations; it is not an operational policy under frozen commitments.
8. EXP-06 uses known future stress to size orders activated after a March 2038 observation (Emergency May, Flex July). Shortage is 0.866 t, min annual service 0.996987; January 2038 reserve still fails. The 498.506 mln PV difference from EXP-02 is not pure value of foresight: closing stock is 55.295 vs 21.755 t and recovery adds 33.947 t Emergency in 2040. Neither a cheapest hedge nor an information-limited policy is demonstrated.
9. Adapted P2z/P3/P4 fail BASE with 17/25/25 hard overflow violations. EXP-07 shows a near-zero extra-shock boundary for adapted P3 (~0.0000551373% per shock); the 0.47 kg reserve slack is rounding-sized.

## Reproducibility after the audit

EXP-07–10 use schema 2 and `sha256-utf8-lf-v1`: only CRLF/CR→LF normalization before
SHA-256, with all other text bytes significant. Run `python experiments/provenance.py` to
check saved input/code hashes, EXP-09 case copies and EXP-10 outputs. Refreshed runs use current
assumption snapshots without changing numerical results. EXP-10 `--compare` checks normalized
outputs/manifests at the same recorded runtime versions; core export timestamps and semantic
KPI hashes retain their own conventions. Full method: `experiments/README.md`.

## To do (R3)

- EXP-07 reverse stress, EXP-08 protection measures, EXP-09 Earth-New delay and EXP-10 Monte Carlo
  are implemented; see the authoritative protocols and `results/` summaries.
- EXP-10 resolves the old factor-set ambiguity: demand + ISRU actual delivery + Core/Flex prices
  on MANDATORY_STRESS, not stochastic Core capacity availability. N=10,000 per dependence
  model, seed=203510, 95% Wilson intervals, conditional TEAM_ASSUMPTION frequencies only.
- Open: event-based Core availability and reactive policies; reverse stress for alternative strategies.
- Geopolitics module: event → price component multiplier on a data copy, before/after, restore.

# Stress-test methodology and protocols (copy of experiments/README.md)

Every experiment is a script; re-running it regenerates `results/<experiment>/` deterministically (no random seeds).
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

## To do (R3)

- Reverse stress: smallest combination (ISRU share, demand) that breaks the adapted plan.
- Monte Carlo on ISRU delivery share and Earth-Core availability with disclosed distributions, N, seed, CI.
- Geopolitics module: event → price component multiplier on a data copy, before/after, restore.

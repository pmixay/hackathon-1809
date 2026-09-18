# TerraPlan — Case Summary (CosmoHackathon 2026, Case 2 "Fuel Space Circuit 2035")

English working summary of the organizer's case statement, evaluation criteria and reference
repository. Source of truth: `docs/organizer/case_statement_ru.pdf`, `docs/organizer/evaluation_criteria_ru.pdf`,
and the organizer reference repo snapshot in `docs/organizer/reference_repo/`
(github.com/SpaceEconomyPolicy/test_oil, commit in `SOURCE_COMMIT.txt`).

## 1. What we must build

A **working prototype** that lets the operator of a notional orbital propellant depot plan supply for
**2035–2040**: choose sources, order volumes, reserve capacity, hold physical stock, decide investments,
model contract terms, see costs and demand service, see constraint violations, switch between the
**BASE** and **MANDATORY_STRESS** scenarios, compare them, save/reopen a plan and export results (CSV/XLSX).

Deliverables (all mandatory):

| # | Deliverable | Where in this repo |
|---|---|---|
| 1 | Management note, 8–12 pages + 1-page scenario comparison | `docs/management_note.md`, `docs/one_pager_scenarios.md` |
| 2 | Working digital circuit with source code, data, configs, saved plans for both scenarios, test protocols, run instructions | `src/terraplan`, `data/`, `configs/`, `results/`, `README.md` |
| 3 | Presentation ≤ 12 slides | `docs/presentation/` (to do) |
| 4 | Reproducible calculations: BASE, stress, low/high demand, own risks, extended horizon (on a data copy) | `experiments/`, `results/` |
| 5 | Supply chain diagram, contract/financial architecture, budget & roadmap 2035–2040 | `docs/architecture.md`, `docs/management_note.md` |
| 6 | Risk register with computed consequences; stakeholder map; KPIs with formulas | `docs/risk_register.md`, `docs/stakeholders.md` |
| 7 | CSV/XLSX exports of plans, results, scenario comparison; proof of plan reopen and dataset extension | `results/`, `tests/` |

Form is free (dashboard, simulator, chat-bot over a real engine...). A calculation core with explicit
formulas is mandatory. Excel may support but not replace the core. No optimizer required.

Repo handover is on **GitVerse** with README (purpose, run command, dependencies, verification order:
install → BASE → mandatory stress → extra tests → comparison & export). No secrets in the repo.

## 2. Case data (CASE_INPUT — must not be changed in control runs)

All money in **million conventional units, constant 2035 prices**. Fuel in tonnes (aggregated propellant).

### Demand (t/year). Critical demand is **included in** total demand.

| Year | Base total | Base critical | Low total | High total |
|---:|---:|---:|---:|---:|
| 2035 | 100 | 80 | 80 | 110 |
| 2036 | 140 | 105 | 112 | 154 |
| 2037 | 190 | 135 | 152 | 209 |
| 2038 | 250 | 170 | 200 | 312.5 |
| 2039 | 320 | 210 | 256 | 400 |
| 2040 | 390 | 250 | 312 | 487.5 |

Low/high variants keep the critical **share** of the corresponding base year.

### Supply channels

| ID | Channel | Capacity t/yr | Variable cost mln/t | Reservation rate mln per (t/yr) | Take-or-pay | Lead time | Reliability (risk metadata only) |
|---|---|---:|---:|---:|---:|---|---|
| A | Earth-Core | 190 | 6.2 | 0.45 | 70 % of reserved | 12 months | 0.96 |
| B | Earth-Flex | 110 | 8.9 | 0.15 | 0 % | 4 months | 0.985 |
| C | Earth-New | 130 | 7.1 | 0.30 | 50 % after commissioning | 18–24 months | 0.88 first year, 0.94 after |
| D | Lunar-ISRU | 120 | 3.0 | 0 | none | 1–2 months after commissioning; available from 2038 after CAPEX | 0.78 / 0.90 / 0.93 (2038–2040) |
| E | Emergency | 80 | 13.8 | 0.35 | none (contract reserves capacity) | 6 weeks | 0.995 |

Variable price includes delivery to the depot. Emergency may not be the **base** channel for more than
two consecutive years. ISRU first-year reliability may not be assumed above 0.78 without own proof.

### Storage and investment options

| Option | Capacity | Loss rate on throughput | Holding cost | CAPEX | Extra fixed OPEX | Availability |
|---|---:|---:|---:|---:|---:|---|
| Base storage (exists) | 70 t | 4.5 % | 0.72 mln/t-year (avg physical stock) | 0 | 0 | 2035 |
| ZBO modernization | 120 t | 1.2 % (model coefficient, not a real ZBO claim) | 0.72 | 180 | 12/yr | option from 2036 |
| Lunar-ISRU pilot | +120 t/yr channel D | — | — | 1250, financed before 2038 | 70/yr | from 2038 |
| Earth-New option | +130 t/yr channel C | — | — | 90 option fee + 270 on exercise = **360 total** | 0 | 18–24 months after exercise |

### Hard constraints

| ID | Rule | Scope |
|---|---|---|
| BASE_CRITICAL_SERVICE | critical service level ≥ 0.99 each year | BASE (guideline in stress) |
| BASE_TOTAL_SERVICE | total service level ≥ 0.97 each year | BASE (guideline in stress) |
| CAPEX_2037 | cumulative CAPEX through end-2037 ≤ 1800 | all |
| CAPEX_2040 | cumulative CAPEX through 2040 ≤ 2800 | all |
| RESERVE_45D | physical stock ≥ 45 days of demand at start of each year: `R_y = D_y·45/365`, or a *demonstrated* equivalent contracted emergency reserve covering the waiting period | all |
| EMERGENCY_BASE_STREAK | Emergency as base channel ≤ 2 consecutive years | all |
| STRESS_LOSS_LIMIT | losses / throughput ≤ 0.02 from 2038 | MANDATORY_STRESS only |
| capacity / storage / lead time / availability | reserved ≤ capacity; ordered ≤ contractually available; inventory ≤ active storage capacity checked on the chosen time step; orders respect lead time; sources used only after commissioning | all |

## 3. Control calculation rules (organizer semantics)

```
I_end        = I_start + Q_delivered − Losses − Q_served          (per period, tonnes)
Shortage     = max(0, Demand − Q_served)                          (never negative inventory)
Losses       = Throughput × loss_rate      (throughput = gross inflow; applied ONCE)
R_y          = D_y × 45 / 365                                      (checked at start of year)
Q_pay        = max(Q_order, TOP_share × Q_reserved_period);  VariablePayment = price × Q_pay
ReservationPayment = rate × annual_reserved_capacity × period_fraction
SL_total     = served_total / demand_total;   SL_critical = served_critical / demand_critical
TotalCost    = Procurement + Reservation + Holding + FixedOPEX + CAPEX   (each once)
PV_t         = CF_t / (1+r)^(t−t0)        (r, t0 = TEAM_ASSUMPTION, same for all alternatives)
```

- BASE is **deterministic**: timely ordered, available volumes arrive as planned. Reliability is *not* a multiplier.
- Holding cost is charged on time-weighted **average physical stock**, method disclosed.
- Initial stock is a decision with source, volume, delivery date and cost (booked in 2035). No double counting of opening stock and inflow.
- Pre-2035 orders form a preparatory period (lead times checked). Its costs go into the first financial year.
- ISRU under-delivery in stress does **not** refund payments automatically.
- Time step is free but must reveal intra-year shortage and storage overflow, and distinguish 6 weeks / 4 / 12 / 18–24 / 1–2 months lead times.

## 4. Scenarios

| Parameter | 2035–2037 | 2038 | 2039 | 2040 |
|---|---:|---:|---:|---:|
| BASE | all inputs as given | | | |
| STRESS: total & critical demand | ×1.00 | ×1.15 | ×1.15 | ×1.15 |
| STRESS: Earth-Core, Earth-Flex variable price | ×1.00 | ×1.25 | ×1.25 | ×1.00 |
| STRESS: Lunar-ISRU actual delivery | plan | 55 % of plan | 75 % of plan | plan |
| STRESS: losses/throughput ceiling | — | ≤ 2 % | ≤ 2 % | ≤ 2 % |

Reservation tariffs, CAPEX and other prices are unchanged in stress. 55 %/75 % are actual shares —
**never multiply by reliability again**. Stress is not auto-combined with high demand or geopolitics;
combinations are separate `TEAM_*` research scenarios. Low/high demand = sensitivity checks.

Note: a full year of throughput at the base storage loss rate (4.5 %) violates the stress ceiling.
The engine checks annual losses / throughput, so commissioning before 2038 is a conservative
planning target rather than a mandatory exact date. A mixed-storage year must be calculated
explicitly (EXP-04 first breaches the annual loss check at a 10-month lag from 2037-07).

## 5. Required analyses

1. BASE plan satisfying all hard constraints.
2. MANDATORY_STRESS: same or justified different decisions; show violations numerically, do not enlarge budget/capacity.
3. Low / high demand sensitivity.
4. Sensitivity analysis of key parameters with thresholds where the plan breaks; joint variations if interactions studied.
5. One additional team-chosen method: reverse stress test, robust analysis on an explicit uncertainty set, or Monte Carlo (with distributions, dependencies, N, seed, accuracy).
6. Team-defined supply disruption risks; risk register with event, cause, parameters, period, probability basis/range, consequence in t / time / money / service, dependencies, owner, mitigation, residual risk.
7. Stakeholder interests (operator, critical & commercial consumers, launch/fuel suppliers, financier) linked to metrics, contracts and decision rules; MCDA optional with disclosed weights.
8. Extended horizon (e.g., 2041) and an added source on a **copy** of the dataset with explicit assumptions.
9. Optional bonus (+5): geopolitical price-change module (event → price component → costs & decisions), on a data copy, with before/after comparison and restore.

## 6. Evaluation criteria (100 + 5 bonus)

| Block | Points | Criteria |
|---|---:|---|
| Model reliability & correctness | 25 | 1 material balance · 2 capacities & lead times · 3 economics · 4 constraint checks per year · 5 verification & reproducibility |
| Architecture & strategy justification | 20 | 6 calculation architecture · 7 methods & scientific sources · 8 comparison of alternatives · 9 investments & contracts |
| Stress testing | 20 | 10 mandatory stress · 11 sensitivity · 12 methods & protocols · 13 plan behaviour under stress |
| Risk assessment | 15 | 14 risk register · 15 quantified consequences · 16 mitigations & residual risk |
| Stakeholders | 10 | 17 interests & metrics · 18 adaptation when risks change |
| Digital circuit functionality | 10 | 19 operator functions & access · 20 save/export/extensibility |

Scale per criterion 0–5: 5 = fully demonstrated, correct, verifiable. Numbers in UI, exports and note must match.

## 7. Parameter status vocabulary

- `CASE_INPUT` — organizer data, fixed in control runs (`data/case/*.csv`, `configs/scenarios/base.yaml`, `mandatory_stress.yaml`).
- `TEAM_DECISION` — plan choices: reservations, orders, stock policy, investments (`configs/plans/*.json`).
- `TEAM_ASSUMPTION` — everything else we need: discount rate, lead-time conversions, allocation rule, 2041 data, risk ranges (`configs/assumptions.yaml`), each with meaning, unit, range and justification.

## 8. Missing organizer files

- `Анкета_постановщика_КосмоХакатон_ЕТ.xlsx` (sheet "Данные кейса 2") is referenced by the case statement but is **not** in the organizer kit; the reference repo's `data/*.csv` is the machine-readable substitute (organizer states this in `data_README.md`).
- `Источники_Кейс_2_КЭП.docx` is referenced but not provided; the reference repo's `SCIENTIFIC_BASIS.md` and the Yandex literature folder cover it.
- `ERRATA_AND_PROVENANCE.md` is linked from the reference repo but absent from it at the snapshot commit.

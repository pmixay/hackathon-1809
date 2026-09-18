# TerraPlan — планирование топливного снабжения орбитального узла 2035–2040

**CosmoHackathon 2026 · кейс 2 «Топливный космоконтур 2035»** · команда TerraPlan (4 участника, см. `docs/TEAM.md`)

TerraPlan — рабочий цифровой контур для оператора условного орбитального топливного узла: помесячный
материальный баланс, контракты (резервирование мощности, take-or-pay), инвестиционные опции (Earth-New,
Lunar-ISRU, ZBO), потери хранения, экономика (CAPEX/OPEX, закупка, резерв, хранение, приведённая стоимость),
проверка ограничений с указанием года, величины и причины, сравнение стандартного и обязательного стрессового
сценариев, сохранение/повторное открытие плана и выгрузка CSV/XLSX/JSON.

*English:* TerraPlan is a Python calculation core + CLI + local browser UI that turns operator decisions
(reservations, orders, stock policy, investments) into a monthly material balance, costs, service levels and
constraint checks for the 2035–2040 orbital-depot supply case. Everything is deterministic and reproducible.

## Быстрый старт / Quick start

```bash
python -m pip install -e ".[dev]"                # Python ≥ 3.10; pyyaml, openpyxl, pytest
python -m terraplan ui                          # open http://127.0.0.1:8765; Ctrl+C to stop
python -m pytest -q                             # engine + UI tests, organizer vectors V01–V10
python -m terraplan control-cases               # prints V01–V10 PASS/FAIL
python -m terraplan run --plan configs/plans/P3_isru_zbo.json --scenario BASE             --out results/demo_BASE
python -m terraplan run --plan configs/plans/P3_isru_zbo.json --scenario MANDATORY_STRESS --out results/demo_STRESS
python -m terraplan compare results/demo_BASE results/demo_STRESS --out results/demo_compare
python -m terraplan verify results/demo_BASE           # reproducibility proof: re-run and compare with the export
python tests/independent_recalc.py results/demo_BASE    # CSV-only recalculation, no engine import
python experiments/run_all.py                   # EXP-01 … EXP-06, regenerates results/
```

Exit code of `run` is 0 when the plan is feasible, 2 when hard constraints are violated (violations are printed
with rule id, year, actual value, limit and reason), 3 on invalid input (message names the missing/conflicting field).

The browser UI runs offline after installation. Edit orders, reservations, investments, opening stock and
contract parameters on a data copy; calculate, inspect violations, pin A and compare with B. Save/reopen a
workspace JSON or download CSV/XLSX/JSON results. Operator walkthrough: [docs/operator_guide.md](docs/operator_guide.md).
Presentation: [12-slide PowerPoint](docs/presentation/TerraPlan.pptx). Delivery and remaining publication step:
[docs/HANDOVER.md](docs/HANDOVER.md).

## Порядок проверки (для жюри) / Verification order

1. **Install and run** — commands above; `results/<dir>/summary.md` shows KPIs, yearly balance, finance, source schedule, the full check matrix (every rule × year, passed or violated) and violations; `results.xlsx` / `*.csv` / `export_envelope.json` contain the same numbers; `delivery_schedule.csv` lists every delivery with its order date and lead time.
2. **Standard scenario** — `configs/plans/P3_isru_zbo.json` under `BASE` (feasible, all checks pass): `results/alternatives/P3_isru_zbo_BASE/`.
3. **Mandatory stress** — same plan under `MANDATORY_STRESS` (`results/alternatives/P3_isru_zbo_MANDATORY_STRESS/`: RESERVE_45D violated 2038–2040, shortage 170 t) and the adapted plan `configs/plans/P3_isru_zbo_adapted.json` (`results/stress/P3_isru_zbo_adapted_MANDATORY_STRESS/`: feasible). Comparison: `results/stress/compare_P3_isru_zbo.md`.
4. **Additional tests** — low/high demand (`results/demand/`), sensitivity sweeps and thresholds (`results/sensitivity/summary.md`), observe-then-react under stress (`results/reaction/`), extensibility on a data copy with Source-X and 2041 (`results/extensibility/`), invalid-input and boundary tests (`tests/`).
5. **Comparison and export** — `results/*/summary.csv`, `results/stress/compare_*.csv`, each run directory has CSV + XLSX + JSON envelope; plans reopen via `python -m terraplan run --plan results/<dir>/plan.json ...`.

Protocols of every experiment: `experiments/README.md`. Methods and formulas: `docs/architecture.md`. Rule catalogue: `docs/constraints_catalogue.md`. Hand check: `docs/manual_check.md`.

## Структура репозитория / Repository layout

| Path | Content |
|---|---|
| `src/terraplan/` | calculation core: `case.py` (CASE_INPUT loader), `scenario.py`, `plan.py` (TEAM_DECISION), `assumptions.py` (TEAM_ASSUMPTION registry), `rules.py` (organizer formulas), `engine.py` (monthly simulation + checks), `planner.py` (greedy merit-order plan builder), `export.py`, `compare.py`, `cli.py` |
| `data/case/` | organizer CASE_INPUT (csv, read-only copy of the reference repo `data/`) |
| `configs/scenarios/` | `base.yaml`, `mandatory_stress.yaml` (CASE_INPUT), `team_low_demand.yaml`, `team_high_demand.yaml` (sensitivity) |
| `configs/plans/` | saved plans (JSON, plan schema of the organizer) — P1…P4 and stress-adapted variants |
| `configs/assumptions.yaml` | every team assumption with meaning, unit, status, range, justification |
| `experiments/` | EXP-01…06 scripts and protocols (`README.md`) |
| `results/` | exports of every experiment (CSV, XLSX, JSON, summary.md, run_manifest.json with hashes) |
| `tests/` | pytest (33): control vectors V01–V10, engine integration, invalid input, boundary plans, extensibility, export parity, golden values, manual hand check, independent CSV recalculation, verify command |
| `schemas/` | organizer JSON schemas (plan, export, scenario, data) |
| `docs/` | `CASE_SUMMARY.md`, `TEAM.md`, `architecture.md`, `management_note.md`, `one_pager_scenarios.md`, `stress_test_protocol.md`, `risk_register.md`, `stakeholders.md`, `roadmap_budget.md`, `sources.md`, `ui_mockups/`, `organizer/` (case PDFs + reference repo snapshot), `literature/` (8 papers + digests), `presentation/` |

## Модель в двух словах / Model in brief

- Time step: calendar month, 2035-01 … 2040-12 (+ preparatory period from 2034-01 for pre-start orders). Demand uniform within a year.
- `I_end = I_start + delivered − losses − served`; `losses = throughput × loss_rate` (once); shortage is reported, stock is never negative.
- Contracts: `Q_pay = max(ordered, TOP × reserved × period_fraction)`, `reservation = rate × reserved × period_fraction`; ISRU under-delivery in stress is not refunded.
- Investments: CAPEX at decision date; Earth-New commissioned 24 months after exercise (conservative end of 18–24), ISRU from 2038-01 if paid by 2037-12 with 2-month order lead, ZBO active from its CAPEX month (assumption, sensitivity 0–12 months).
- Costs: procurement + reservation + holding (0.72 × average stock) + fixed OPEX + CAPEX; PV at a real 8 % (assumption, same for all alternatives, sensitivity 0–12 %).
- Checks per year: service ≥ 97 % / 99 % (hard in BASE, guideline in stress), CAPEX ≤ 1800 through 2037 / ≤ 2800 through 2040, 45-day reserve at year start, storage capacity monthly, capacity/reservation/availability/lead time per source, Emergency ≤ 2 consecutive years as base channel, losses/throughput ≤ 2 % from 2038 in stress.

## Ключевые результаты первого дня / First findings (see `results/`)

| Plan | BASE PV cost, mln | BASE feasible | STRESS (plan unchanged) | STRESS adapted PV, mln |
|---|---:|:---:|---|---:|
| P1 Earth-Core + Earth-Flex only | 7 857 | no (capacity 300 t/yr < 2040 demand) | infeasible | — |
| P2z Earth-New + ZBO | 8 729 | yes | 3 hard violations, shortage 96 t | **10 097** |
| P3 ISRU + ZBO | **8 639** | yes | 3 hard violations, shortage 170 t | 10 637 |
| P4 Earth-New + ISRU + ZBO | 8 858 | yes | 3 hard violations, shortage 170 t | 10 578 |

ZBO is required by every stress-feasible plan (base storage loses 4.5 % > 2 % ceiling from 2038). A plan
built for BASE carries no slack: it breaks at +5 % demand or a 5 % ISRU shortfall (`results/sensitivity/`).
Choosing between P2z and P3 is a robustness question, not a price question — see `docs/management_note.md`.

## Ограничения прототипа / Prototype limits

Web UI is available via `python -m terraplan ui`; `docs/ui_mockups/` contains the historical design reference.
It serves one local operator, retains the last 12 calculations until server shutdown, and saves work via downloaded files.
GitVerse publication remains pending a team repository URL; the configured origin is GitHub.
No optimizer (greedy merit-order builder only). Monte Carlo / reverse stress and the geopolitics bonus module
are planned (see `docs/TEAM.md`). No secrets, no external services; runs offline.

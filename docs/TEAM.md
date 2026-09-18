# TerraPlan — Team roles (4 members)

Roles are mapped to the organizer's 20 evaluation criteria (`docs/CASE_SUMMARY.md` §6) so every point
has an owner. Everybody reviews everybody's numbers: the jury checks that UI, exports and the note agree.

| Role | Owner | Criteria owned | Main deliverables |
|---|---|---|---|
| **R1 — Model lead (calculation core)** | member 1 | 1, 2, 3, 4, 5, 6 | `src/terraplan` engine, monthly material balance, contracts/take-or-pay, storage & losses, costs & discounting, constraint checks, control vectors V01–V10, boundary & invalid-input tests, reproducibility protocol |
| **R2 — Strategy & economics analyst** | member 2 | 7, 8, 9, 17, 18 | Alternative plans (Earth-only, Earth+New, Earth+ISRU+ZBO, full portfolio), contract & financial architecture, investment roadmap & gates, stakeholder map, MCDA with disclosed weights, scientific sources traceability (`docs/sources.md`) |
| **R3 — Stress & risk engineer** | member 3 | 10, 11, 12, 13, 14, 15, 16 | Mandatory stress run and adapted plan, sensitivity sweeps & thresholds, reverse stress / Monte Carlo (seeded), team risk scenarios, quantified risk register with mitigations & residual risk, geopolitics bonus module |
| **R4 — Product & UI / delivery** | member 4 | 19, 20 + presentation | Operator UI (dashboard, plan editor, violations, scenario compare, export), save/reopen, CSV/XLSX export, extensibility demo (Source-X, 2041), README & run instructions, presentation ≤ 12 slides, GitVerse handover |

Management note (8–12 pages) is co-written: R2 leads structure and strategy sections, R1 writes model &
architecture, R3 writes stress/risk sections, R4 writes UI/functionality, budget & roadmap tables.

## Working agreement

- `data/case/` and `configs/scenarios/base.yaml`, `mandatory_stress.yaml` are **read-only** (CASE_INPUT). Own scenarios go to `configs/scenarios/team_*.yaml`.
- Every assumption gets a row in `configs/assumptions.yaml` with meaning, unit, range, status, justification.
- Every experiment is a script in `experiments/` writing to `results/<experiment_id>/` with the plan, scenario, assumptions snapshot and exports. No hand-edited numbers in docs.
- Branch naming `feat/<role>-<topic>`; PRs into `main`; `pytest` must pass.
- Numbers quoted in the note/presentation are copied from `results/` files (cite the file name).

## Timeline (hackathon)

| Phase | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| Day 1 AM | engine skeleton, V01–V10 green | draft 4 alternative plans | stress scenario loader, sensitivity harness | UI mockups → clickable prototype |
| Day 1 PM | monthly balance, costs, checks | run alternatives, pick candidate | stress + adapted plan, first thresholds | plan editor + violations panel |
| Day 2 AM | invalid-input tests, reproducibility, export parity | contracts & roadmap, stakeholders, MCDA | risk register, Monte Carlo / reverse stress, geopolitics | save/reopen, export, extensibility demo |
| Day 2 PM | freeze numbers | management note + one-pager | protocols & appendices | presentation, README, handover |

## Current status (2026-09-18)

- Repo bootstrapped, organizer materials and literature laid in, engine + tests + first experiments running (see `README.md`).
- **R1 done**: monthly engine, V01–V10, 33 tests (boundary, invalid input, extensibility, export parity, golden, manual check), full check matrix per year, delivery/order calendar, discount-timing option, `verify` command, CSV-only independent recalculation, constraints catalogue, architecture doc, CI with reproducibility check. **R1 waiting on others**: final plan choice (R2) to freeze numbers; UI (R4) to call `simulate()`; stress protocol additions (R3) for Monte Carlo seeds in the manifest.
- **R4 delivered (2026-09-19)**: local operator UI calling `simulate()`, plan and copied-data/contract editors, violations and check matrix, scenario comparison, workspace save/reopen, CSV/XLSX/JSON downloads, Source-X/2041 demo, operator guide, 12-slide presentation, budget/roadmap and local handover instructions. Acceptance: `tests/test_web.py`, `tests/ui_smoke.cjs`, `docs/HANDOVER.md`. **R4 pending external handover**: GitVerse destination and team publication/access check.
- **R3 integrated**: EXP-07 reverse stress, EXP-08 protection measures, EXP-09 Earth-New delay, EXP-10 seeded Monte Carlo with portable provenance and protocols are in `main`.
- Open with R2/R3: final strategy selection, self-found sources, geopolitics module, expansion of risk methods to alternative strategies, final management-note consolidation.

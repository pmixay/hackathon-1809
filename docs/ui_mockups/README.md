# TerraPlan UI mockup

Single self-contained HTML mockup of the TerraPlan operator interface for
CosmoHackathon 2026, case 2 ("Топливный космоконтур 2035"). Open
`index.html` directly in a browser — no build step, no server, no external
scripts (only a Google Fonts stylesheet; all data and logic are inline).

This is a **UI mockup**, not the calculation engine: the "Пересчитать" button
and the plan-grid inputs are cosmetic (they show a toast, they do not
recompute anything). All numbers shown are read from the real files under
`results/`, `configs/`, and `data/case/` in this repository — nothing is
invented. Where a value was not available in those files the UI prints
`—` instead of a fabricated number.

## Purpose

Give the jury (and the team) a concrete, clickable picture of the operator
workflow described in `docs/organizer/reference_repo/README.md` §1 and the
evaluation criteria in `docs/CASE_SUMMARY.md` §6, using the team's own BASE
and MANDATORY_STRESS results for plan `P3_isru_zbo` (Earth-Core + Earth-Flex
+ Lunar-ISRU pilot + ZBO) as the running example.

## Screens and how they map to the operator flow

The reference README (§1) defines the minimal user flow: *load/select data →
build a plan → check feasibility → calculate (balance, stock, shortage,
service level, cost) → switch BASE→MANDATORY_STRESS → compare → sensitivity
and own risks → save plan → reopen plan → export*. Each screen below covers
one or more steps of that flow.

| # | Screen (RU tab label) | Flow step(s) covered | Evaluation criteria touched |
|---|---|---|---|
| 1 | «Рабочее место оператора» — dashboard | *select data/plan* (scenario + plan selector) → *calculate* (KPI tiles, charts, yearly table) | 1 (material balance), 3 (economics), 4 (constraint checks — feasibility pill), 19 (operator can change scenario/plan and see numbers change) |
| 2 | «План и контракты» — plan editor | *build a plan* (editable reservation/order grid, contract terms, investment timeline, opening stock, reserve mode) | 2 (capacities & lead times), 6 (calculation architecture — status legend CASE_INPUT/TEAM_DECISION/TEAM_ASSUMPTION), 9 (investments & contracts), 19 (recalculate / save / open buttons) |
| 3 | «Проверка ограничений» — violations | *check feasibility* (constraint table with rule/severity/year/month/source/actual/limit/excess/reason) + a live bad-input demo | 4 (constraint checks per year, with severity shown by icon **and** text, never colour alone), 19 (clear error message on bad input, matching the reference README §26 format) |
| 4 | «Сравнение сценариев» — scenario comparison | *switch BASE→MANDATORY_STRESS* + *compare* (BASE vs fixed-under-stress vs adapted-under-stress, with deltas and which decisions changed and why) | 8 (comparison of alternatives), 10 (mandatory stress), 13 (plan behaviour under stress), 19/20 (compare + export button) |
| 5 | «Стресс-тесты и чувствительность» — sensitivity | *sensitivity and own risks* (thresholds table, tornado chart, alternative ranking by discount rate, two reproduction protocols with the actual CLI command) | 11 (sensitivity), 12 (methods & protocols, reproducible command), 13 (plan behaviour under stress) |
| 6 | «Риски и стейкхолдеры» — risks & stakeholders | *own risks* (risk register), stakeholder interests → metrics → contract clauses, geopolitical bonus module (apply-on-copy / restore / before-after) | 14–16 (risk register, quantified consequences, mitigation & residual risk), 17–18 (stakeholder interests & metrics, adaptation under risk) |
| 7 | «Сохранение, выгрузка, расширение» — save/export/extend | *save plan* → *reopen plan* → *export* (CSV/XLSX/JSON envelope) → dataset extension on a copy | 5 (verification & reproducibility — sha256/run manifest), 19 (save/reopen), 20 (export + extensibility on a copy, control runs stay on original data) |

## Interactivity (kept minimal, per the design brief)

- Left sidebar = tabs between the 7 screens (collapses to a horizontal
  scroll bar on phone widths); the last opened tab is remembered per-browser
  via `localStorage` (best-effort, wrapped in try/catch).
- Screen 1: a BASE/MANDATORY_STRESS segmented toggle and a plan `<select>`
  swap the KPI tiles, the yearly table and (for `P3_isru_zbo` only — see
  below) the three charts, reading from one embedded JSON blob
  (`<script id="tp-data" type="application/json">`). "Пересчитать" shows a
  toast; no recomputation happens.
- Screen 2: the reservation/order grid cells are real `<input>` elements
  (edits just show a toast — mock, per the design brief).
  "Сохранить план" / "Открыть план" / "Пересчитать" each show a toast; none
  of them recomputes anything.
- Screen 3: a small live form reproduces the reference README's error
  format (`INPUT_INCOMPLETE` / `CAPACITY_EXCEEDED` with
  rule/source/year/actual/limit/excess) versus a crossed-out "bad" example
  (`Error 400`), so the jury can trigger both a missing-field error and an
  over-capacity error themselves.
- Screen 6: the geopolitical module lets the jury pick the case's own stress
  price-shock preset (or a free-text custom event) and click
  "Применить на копии" / "Восстановить исходные цены" / "До/после"; the
  "after" preview is the real sensitivity number at the multiplier that
  number actually belongs to (not a fabricated value at the preset's own
  multiplier) and says so explicitly.
- All charts are inline SVG built by ~150 lines of vanilla JS (stacked bar,
  step/line, tornado) with a `<title>` tooltip per mark; no chart library.

## Which numbers come from which file

All figures are for plan **P3_isru_zbo** (BASE) and **P3_isru_zbo_adapted**
(MANDATORY_STRESS) unless noted otherwise; embedded verbatim (rounded to the
same precision as the source) in the JSON blob at the bottom of `index.html`.

| UI element | Source file(s) |
|---|---|
| Screen 1 KPI tiles, yearly table, cost/supply/inventory charts (plan P3, both scenarios) | `results/alternatives/P3_isru_zbo_BASE/summary.md`, `results/stress/P3_isru_zbo_adapted_MANDATORY_STRESS/summary.md` (KPI, yearly balance, finance, source schedule) |
| Screen 1 inventory line chart (monthly opening/closing stock) | `results/alternatives/P3_isru_zbo_BASE/inventory_trace.csv`, `results/stress/P3_isru_zbo_adapted_MANDATORY_STRESS/inventory_trace.csv` |
| Screen 1 KPI tiles for plans P1/P2/P2z/P4 (plan selector) | `results/alternatives/summary.md`, `results/stress/summary.md` (feasible adapted variant where one exists, otherwise the fixed/unchanged plan under stress) |
| Screen 2 reservation/order grid, investments, opening stock, reserve mode | `configs/plans/P3_isru_zbo.json` (decisions), `configs/plans/P3_isru_zbo_adapted.json` |
| Screen 2 contract cards (capacity, price, reservation rate, take-or-pay, lead time, reliability) | `data/case/supply_sources.csv` |
| Screen 2 investment CAPEX figures | `data/case/investment_options.csv` |
| Screen 3 violations table (BASE_TOTAL_SERVICE, RESERVE_45D, 2038–2040) | `results/stress/P3_isru_zbo_fixed_MANDATORY_STRESS/summary.md` (constraint checks table) |
| Screen 4 KPI/yearly comparison, deltas | `results/alternatives/P3_isru_zbo_BASE/summary.md`, `results/stress/P3_isru_zbo_fixed_MANDATORY_STRESS/summary.md`, `results/stress/P3_isru_zbo_adapted_MANDATORY_STRESS/summary.md` (cross-checked against `results/stress/compare_P3_isru_zbo.md`) |
| Screen 4 "what changed in decisions" table | computed in-browser from `configs/plans/P3_isru_zbo.json` vs `configs/plans/P3_isru_zbo_adapted.json` (reservations/orders) |
| Screen 5 thresholds table, tornado chart | `results/sensitivity/thresholds.csv`, `results/sensitivity/tornado.csv` |
| Screen 5 ranking by discount rate | `results/sensitivity/summary.md` |
| Screen 5 reproduction commands | `README.md` (repo root, "Quick start" section) and `experiments/run_sensitivity.py` |
| Screen 6 risk register | narrative + dependencies are the team's own (marked «оценка команды»); the numeric anchors quoted inside each row (isru share thresholds, price-shock swing, ZBO lag threshold, demand thresholds) are read from `results/sensitivity/thresholds.csv` and `results/sensitivity/tornado.csv` |
| Screen 6 stakeholder map contract clauses | `data/case/constraints.csv`, `data/case/supply_sources.csv` |
| Screen 6 geopolitical module preset ("price shock ×1.25, 2038–2039") | `docs/CASE_SUMMARY.md` §4 (MANDATORY_STRESS price multiplier); the "after" preview number is the sensitivity test at ×1.5 from `results/sensitivity/tornado.csv`, explicitly labelled as that different multiplier |
| Screen 7 saved-plans list (plan id / scenario / timestamp / sha256) | `run_manifest.json` + `export_envelope.json` (`generated_at`) of each `results/alternatives/*` and `results/stress/*` run directory listed |
| Screen 7 export file lists (CSV set / XLSX / JSON envelope) | the actual file names present in any `results/alternatives/P3_isru_zbo_BASE/` (or `results/stress/P3_isru_zbo_adapted_MANDATORY_STRESS/`) run directory |
| Screen 7 dataset-extension preview (Source-X, 2041) | `results/extensibility/case_copy/README_COPY.md` (assumption values) and `results/extensibility/run/export_envelope.json` (computed KPI on the copy) |

## Design notes

- Light/dark theme via `@media (prefers-color-scheme: dark)` on CSS tokens
  defined on `:root`; `body` has an explicit background in both modes.
- Layout is phone-width friendly (16px gutters, no horizontal scroll on the
  page itself); wide tables and the nav bar scroll inside their own
  container instead.
- Colour is never the only channel for severity/status: every hard /
  guideline / warning indicator and every feasible/infeasible pill pairs an
  icon and a text label with its colour.
- Verified with a headless Chromium pass (Playwright) over both colour
  schemes and a 375px-wide viewport: no page-level horizontal overflow, no
  console/page errors, all seven tabs and the interactive demos (validation
  form, geopolitical module, scenario/plan toggle) exercised.

Footer line on every screen: *"TerraPlan v0.1 — макет интерфейса; числа из
results/ (BASE: P3_isru_zbo; STRESS: P3_isru_zbo_adapted)"*.

## Published preview

Private artifact page (share from its menu to give teammates access): https://claude.ai/artifact/94xJiuJBULiYuiZf3BGrjp

Local: open `docs/ui_mockups/index.html` in any browser (no server needed).

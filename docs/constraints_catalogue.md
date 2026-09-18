# Constraints catalogue — every rule the engine checks

Each rule has a stable id (used in `constraint_checks.csv`, `constraint_matrix.csv`, the UI and the note), a
severity, a scope, the exact test and the message format. `constraint_matrix.csv` lists **every rule × year with
its actual value, limit and OK/VIOLATED**, so passed checks are visible, not only failures. Severities:
**hard** = plan infeasible; **guideline** = organizer service targets used as resilience benchmarks outside BASE;
**warning** = informational (does not affect feasibility).

| Rule id | Severity | Scope | Test (per year unless stated) | Source of rule | Message fields |
|---|---|---|---|---|---|
| BASE_TOTAL_SERVICE | hard in BASE, guideline elsewhere | every year | `served_total / demand_total ≥ 0.97` (1.0 if demand = 0) | constraints.csv, case §Requirements | year, actual SL, limit, shortage t |
| BASE_CRITICAL_SERVICE | hard in BASE, guideline elsewhere | every year | `served_critical / demand_critical ≥ 0.99`; critical served first (allocation rule) | same | year, actual SL, limit, shortage t |
| CAPEX_2037 | hard | cumulative through 2037 | `Σ CAPEX(y ≤ 2037) ≤ 1800` | constraints.csv | through-year, cumulative, limit, excess |
| CAPEX_2040 | hard | cumulative through 2040 | `Σ CAPEX(y ≤ 2040) ≤ 2800` | constraints.csv | same |
| RESERVE_45D | hard | start of every year | physical: `I_start(y) ≥ D_y × 45/365`; contracted mode: also requires `I_start ≥ D_y × 42/365` (6-week wait) and reserved Emergency ≥ R_y | case §Initial stock and reserve; equivalence rule = TEAM_ASSUMPTION | year, stock, R_y, shortfall, equivalence detail |
| STORAGE_OVERFLOW | hard | every month | `I_end(month) ≤ capacity(active storage mode)`; opening stock also checked at 2035-01 | case §Losses and storage (capacity on the chosen step) | year, month, stock, capacity, excess |
| INTRA_MONTH_PEAK | warning | every month | `I_start + inflow − losses > capacity` before withdrawals (conservative timing) | TEAM_ASSUMPTION `storage_capacity_check` | year, month, peak, capacity |
| CAPACITY_EXCEEDED | hard | source × year | `reserved_t_per_year ≤ capacity` | control vector V08 | source, year, reserved, capacity, excess |
| ORDER_EXCEEDS_RESERVATION | hard | source × year | `ordered ≤ reserved × period_fraction` (capacity right needed to order) | case §Contracts | source, year, ordered, contractually available, excess |
| SOURCE_NOT_AVAILABLE | hard | source × year / month | order or reservation before the source can deliver (Earth-New before commissioning, ISRU before 2038-03 or unfinanced, explicit month before availability) | case §Investments; lead-time policy | source, year/month, volume, first possible delivery |
| LEAD_TIME_VIOLATED | hard | source × delivery month | `delivery_month − lead_time ≥ preparatory start (2034-01)`; for investment-linked sources ≥ commissioning | case §Time step and lead time; `lead_time_policy` = max | source, delivery month, required order date, earliest allowed |
| INVESTMENT_TIMING | hard | investment | ZBO decision ≥ 2036; ISRU CAPEX ≤ 2037-12 (else source never available); option fee ≤ exercise date; CAPEX dated inside 2035–2040 | case §Storage and investment options | investment, date, limit |
| EMERGENCY_BASE_STREAK | hard | horizon | a year counts as "Emergency = base channel" when ordered Emergency > 20 % of demand (assumption); `consecutive base years ≤ 2` | case §Requirements; threshold = TEAM_ASSUMPTION | years, streak, limit |
| STRESS_LOSS_LIMIT | hard | years ≥ 2038, scenarios with `loss_ceiling.enabled` | `losses_y / throughput_y ≤ 0.02` | mandatory_stress.yaml | year, ratio, limit, losses, throughput |
| UNSUPPORTED_CONSTRAINT | warning | — | a `constraints.csv` metric the engine does not implement (visible instead of silently ignored) | extensibility rule | constraint id, metric |
| INPUT errors (PlanError / CaseError / ScenarioError) | fatal, before calculation | — | missing field, negative value, unknown id, duplicate line, year outside horizon, critical > total, malformed JSON/YAML, scenario without id | organizer §26 error format | file, field, offending value |

Order of application: input validation → investments & availability → schedule (availability, lead time) →
monthly balance (overflow) → contracts (capacity, reservation) → finance → constraints.csv rules → loss ceiling →
check matrix. A plan is **feasible** iff no hard violation exists; guideline and warning items are reported but do not
change feasibility. Nothing is auto-repaired: an infeasible plan is shown with year, value and reason.

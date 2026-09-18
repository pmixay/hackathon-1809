# Independent manual check — plan P3_isru_zbo, year 2035, BASE

Hand calculation (calculator, no code) versus engine output `results/alternatives/P3_isru_zbo_BASE/`. The same expected values are asserted automatically in `tests/test_verification.py::test_manual_hand_check_2035`; a CSV-only recalculation of any exported run is `python tests/independent_recalc.py <results_dir>`.

Inputs: demand 2035 = 100 t (critical 80); base storage loss 4.5 %, holding 0.72 mln/t-yr; Earth-Core 6.2 mln/t,
reservation 0.45; Earth-Flex 8.9, reservation 0.15; 45-day reserve R = D × 45/365.

| Step | Hand calculation | Expected | Engine | OK |
|---|---|---:|---:|:---:|
| R_2035 | 100 × 45 / 365 | 12.329 t | 12.329 | ✓ |
| Opening stock (net) must equal R_2035; gross via Earth-Flex in 2034-12 | 12.329 / (1 − 0.045) | 12.910 t gross | 12.910 (plan.json opening_stock) | ✓ |
| Opening stock cost (booked 2035) | 8.9 × 12.910 + 0.15 × 12.910 | 114.90 + 1.94 = 116.84 | procurement 796.1 − 681.2 = 114.9; reservation 51.4 − 49.4 = 1.9 | ✓ |
| Target closing 2035 = R_2036 | 140 × 45 / 365 | 17.260 t | closing 17.26 | ✓ |
| Net inflow needed | 100 + 17.260 − 12.329 | 104.931 t | — | |
| Gross Earth-Core order | 104.931 / 0.955 | 109.876 t | ordered 109.9 | ✓ |
| Losses 2035 | 109.876 × 0.045 | 4.944 t | 4.94 | ✓ |
| Procurement Earth-Core | 6.2 × max(109.876, 0.7 × 109.876) | 681.23 | 681.2 | ✓ |
| Reservation Earth-Core | 0.45 × 109.876 | 49.44 | 49.4 | ✓ |
| Holding (stock grows linearly 12.33 → 17.26) | 0.72 × (12.329 + 17.260)/2 | 10.65 | 10.7 | ✓ |
| Total 2035 | 681.23 + 114.90 + 49.44 + 1.94 + 10.65 | 858.16 | 858.2 | ✓ |
| Service 2035 | served 100 / demand 100 | 1.000 | 1.000 | ✓ |

Boundary checks (see `tests/test_boundary.py`): empty plan → shortage = total demand, stock 0, no negative
inventory; 100 t delivered into a 70 t depot → STORAGE_OVERFLOW 2035-01 excess 30+ t; Emergency > 20 % for
3 years → EMERGENCY_BASE_STREAK; CAPEX 1 850 by 2037 → CAPEX_2037 excess 50; ISRU paid 2038-03 →
INVESTMENT_TIMING and SOURCE_NOT_AVAILABLE.

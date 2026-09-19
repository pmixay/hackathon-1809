# EXP-10 Conditional Monte Carlo: fixed P3 protections

N=10000 per dependence model; seed=203510; random.Random / MT19937.
Background: MANDATORY_STRESS. Demand U(0, 2.00%), ISRU reduction U(0, 2.00%) in 2038-2040; Core/Flex prices +/-10.00% in 2038-2039.
TEAM_ASSUMPTION distributions, not calibrated probabilities. All three plans use the same sample.

## No-additional-shock control

| Variant | PV, mln | Extra PV, mln | Passes |
|---|---:|---:|---|
| without_measure | 10637.024754 | 0.000000 | True |
| physical_stock | 10720.692579 | 83.667825 | True |
| early_zbo_plus_stock | 10686.482788 | 49.458033 | True |

## independent

| Variant | Failures / N | Failure % (95% Wilson) | Reduction, pp | Mean extra PV, mln | Mean PV | PV P5 / P50 / P95 |
|---|---:|---:|---:|---:|---:|---|
| without_measure | 10000 / 10000 | 100.00% (99.96%, 100.00%) | 0.00 | 0.000000 | 10631.080761 | 10309.783 / 10630.892 / 10951.337 |
| physical_stock | 4943 / 10000 | 49.43% (48.45%, 50.41%) | 50.57 | 83.662413 | 10714.743174 | 10393.450 / 10714.560 / 11035.005 |
| early_zbo_plus_stock | 4959 / 10000 | 49.59% (48.61%, 50.57%) | 50.41 | 49.452621 | 10680.533382 | 10359.241 / 10680.350 / 11000.795 |

| Variant | Reserve failure % | Service failure % | Shortage % | Max shortage, t | Worst annual total / critical service | Max reserve gap, t |
|---|---:|---:|---:|---:|---|---:|
| without_measure | 100.00% | 0.00% | 13.33% | 5.464047 | 98.805580% / 100.000000% | 17.026029 |
| physical_stock | 49.43% | 0.00% | 0.00% | 0.000000 | 100.000000% / 100.000000% | 8.425687 |
| early_zbo_plus_stock | 49.59% | 0.00% | 0.00% | 0.000000 | 100.000000% / 100.000000% | 8.444009 |

First failure (simultaneous causes kept together):

- without_measure: RESERVE_45D @ 2038-01: 9996 realizations.
- without_measure: RESERVE_45D @ 2039-01: 4 realizations.
- physical_stock: RESERVE_45D @ 2040-01: 4943 realizations.
- early_zbo_plus_stock: RESERVE_45D @ 2040-01: 4959 realizations.

## comonotonic_demand_isru

| Variant | Failures / N | Failure % (95% Wilson) | Reduction, pp | Mean extra PV, mln | Mean PV | PV P5 / P50 / P95 |
|---|---:|---:|---:|---:|---:|---|
| without_measure | 9999 / 10000 | 99.99% (99.94%, 100.00%) | 0.00 | 0.000000 | 10631.087298 | 10309.627 / 10630.683 / 10951.397 |
| physical_stock | 4987 / 10000 | 49.87% (48.89%, 50.85%) | 50.12 | 83.653749 | 10714.741047 | 10393.295 / 10714.351 / 11035.065 |
| early_zbo_plus_stock | 5003 / 10000 | 50.03% (49.05%, 51.01%) | 49.96 | 49.443957 | 10680.531255 | 10359.085 / 10680.141 / 11000.855 |

| Variant | Reserve failure % | Service failure % | Shortage % | Max shortage, t | Worst annual total / critical service | Max reserve gap, t |
|---|---:|---:|---:|---:|---|---:|
| without_measure | 99.99% | 0.00% | 19.93% | 5.560995 | 98.784402% / 100.000000% | 17.080361 |
| physical_stock | 49.87% | 0.00% | 0.00% | 0.000000 | 100.000000% / 100.000000% | 8.480019 |
| early_zbo_plus_stock | 50.03% | 0.00% | 0.00% | 0.000000 | 100.000000% / 100.000000% | 8.498341 |

First failure (simultaneous causes kept together):

- without_measure: RESERVE_45D @ 2038-01: 9996 realizations.
- without_measure: RESERVE_45D @ 2039-01: 3 realizations.
- physical_stock: RESERVE_45D @ 2040-01: 4987 realizations.
- early_zbo_plus_stock: RESERVE_45D @ 2040-01: 5003 realizations.

## Interpretation and limits

- Failure includes reserve compliance, not just unserved demand. Service guidelines count even if Result.feasible is true.
- Physical shocks are persistent, not independent monthly noise. The comonotonic diagnostic is not pooled with the primary independent model.
- Zero/all observed failures do not establish a true probability of zero/one: use the Wilson interval. It excludes model/distribution uncertainty.
- The protections target a 1% uncertainty square, while this experiment samples up to 2%; residual failures are expected.
- Extra PV is computed with minus without protection on EACH common realization. No damages, penalties or avoided-mission-loss benefit is priced.
- The price factor changes PV, not physical feasibility of fixed plans. Extra Flex purchases precede the 2038-2039 price shock.
- Early ZBO retains saved fuel; its advantage depends on zero commissioning lag and the throughput-only loss convention.
- Frequencies are conditional on MANDATORY_STRESS and TEAM_ASSUMPTION ranges; they are not real-world risk probabilities or evidence of BASE feasibility.
- samples.csv retains latent uniforms and both dependence transforms; runs.csv contains every realization, all first causes and paired cost deltas.
- report.json contains reference controls, reason/date counts and mean/min/max/P5/P50/P95 for all severity and cost metrics.
- run_manifest.json records parameters, versions, input/code/output SHA-256, plan/scenario/assumption snapshots. No timestamps or output paths enter its hashes.
- Hash format sha256-utf8-lf-v1 normalizes CRLF/CR to LF only; all other bytes remain significant. Saved-input verification: python experiments/provenance.py.

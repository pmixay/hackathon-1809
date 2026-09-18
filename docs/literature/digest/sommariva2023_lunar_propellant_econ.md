# Sommariva et al. (2023) — Preliminary analyses on technical and economic viability of moon-mined propellant for on-orbit refueling

**Full citation:** Sommariva, A., Gaudenzi, P., Pianorsi, M., Pasquali, M., Vittori, E., Eugeni, M., Italiano, M., Telli, C., Di Nicola, M., Gori, L., Chizzolini, B. (2023). *Preliminary analyses on technical and economic viability of moon-mined propellant for on-orbit refueling*. Acta Astronautica, 204, pp. 425–433. DOI: `10.1016/j.actaastro.2023.01.004`. Received 17 Jul 2022; accepted 4 Jan 2023. Collaboration between Sapienza Università di Roma (DIMA) and SDA Bocconi School of Management.

## Problem
Given evidence of substantial water ice at the lunar poles, is it technically feasible and economically preferable to mine and process lunar water into propellant (LH2/LOX) for on-orbit refueling of spacecraft, compared to shipping propellant from Earth to the same orbital depot?

## Method
Two architectures are defined, both delivering to a depot at Earth-Moon Lagrange point L1: Case 1 ("Moon") — a lunar mining/production plant plus a reusable "Moon shuttle" delivering to the L1 depot; Case 2 ("Earth") — propellant launched from Earth to the same depot. Both are evaluated first for technical feasibility (ΔV, vehicle sizing, depot architecture) and then economically via discounted cash flow: a Net Present Value (NPV) model with a 5-year construction phase followed by a 10-year operating phase (formula given, PDF p. 6: NPV₀ = −Σ CAPEXₜ/(1+r)ᵗ + Σ CFₜ/(1+r)ᵗ). Each case gets its own WACC discount rate reflecting its perceived risk (the lunar case's beta is set 13% higher than the Earth case's, reflecting larger/riskier investment, mainly the Moon shuttle). Because CAPEX/OPEX/revenue estimates are highly uncertain, the authors run a Monte Carlo simulation — 5,000 draws per case, with CAPEX modeled as lognormal (standard deviation set to 10% of the median in the reported "safe/low-risk" scenario) — to characterize the resulting NPV distribution around a "minimum" (breakeven, NPV = 0) price.

## Key results / numbers
WACC: 13% (Moon, Case 1) vs. 11.5% (Earth, Case 2). Zero-NPV minimum price: 5.07 M$/Mt (Moon) vs. 10.55 M$/Mt (Earth) — i.e., roughly half. CAPEX simulation for Case 1 yields a standard deviation of 314 (units as in Table 9 of the source; PDF p. 8). 5,000 Monte Carlo NPV draws per case are plotted as histograms (Figs. 7–8); the "expected" NPV (computed from the point-estimate cash flows) coincides with the median of each simulated distribution. Conclusion: transporting propellant from the Moon is identified "as the most promising solution" (abstract), being both cheaper at breakeven and less exposed to volatility than the Earth case in this analysis; the authors argue the price gap leaves room for multiple ventures and public co-financing of early demonstration phases.

## Relevance to our case
Directly analogous in structure to comparing Lunar-ISRU against the Earth-supply channels (Earth-Core/Earth-Flex/Earth-New) in TerraPlan: same idea of comparing architectures on a risk-adjusted economic basis (not nominal price alone), and the same Monte Carlo-around-a-breakeven-price technique is a usable template if the team implements the optional Monte Carlo module.

## Quotable statements
- "[T]hese analyses identify transporting propellant from the Moon as the most promising solution." (abstract)
- "[T]he more expensive alternative from Earth is also more exposed to volatility implying higher levels of the underlying operational risks." (PDF p. 9 / journal p. 433)
- "[O]ur study lays the foundation for approaching the development of transportation and distribution infrastructures for lunar-based propellant..." (PDF p. 9 / journal p. 433, conclusion)

## Cautions
- The "Moon wins" conclusion is entirely a function of this paper's own CAPEX/OPEX/demand/WACC assumptions; it must not be imported as a ready-made answer for this case, where Lunar-ISRU is one alternative among five with its own case-fixed CAPEX, timing (available from 2038), and ramp-up reliability — not a pre-selected winner.
- "Preliminary" is in the title deliberately: the authors themselves flag high uncertainty in investment/OPEX/revenue assumptions.
- Assumes a single-operator/limited-competition market structure at this stage, which simplifies away competitive-market pricing effects.

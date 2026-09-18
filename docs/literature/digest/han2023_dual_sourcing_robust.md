# Han, Zhang, Wang & Park (2023) — The efficient and stable planning for interrupted supply chain with dual-sourcing strategy: a robust optimization approach considering decision maker's risk attitude

**Full citation:** Han, B., Zhang, Y., Wang, S., Park, Y. (2023). *The efficient and stable planning for interrupted supply chain with dual-sourcing strategy: a robust optimization approach considering decision maker's risk attitude*. Omega, 115, article 102775. DOI: `10.1016/j.omega.2022.102775`. Received 19 Jan 2022; accepted 26 Sep 2022. Affiliations: Dalian Maritime University; St. Edward's University (Austin, TX).

## Problem
How should a firm split orders between a primary and a backup ("dual-sourcing") supplier to remain both cost-efficient and resistant to shortages when supply can be interrupted, and how does the decision-maker's own risk attitude (averse / neutral / seeking) change the optimal split?

## Method
Builds a dual-objective (minimize cost; minimize shortage) robust optimization model for a dual-sourcing ordering decision under supply-disruption uncertainty. Disruption/uncertainty is represented with interval-based robust-optimization uncertainty sets (not fitted probability distributions), producing a "robust counterpart" of the nominal model. The two objectives are combined and solved via the augmented ε-constraint method, which converts the problem into a single-objective mixed-integer program solvable with standard MIP tools. The model is parameterized directly by the decision-maker's risk attitude, and the paper performs risk-attitude analysis, a cost-vs-shortage trade-off (Pareto-type) analysis, and a comparison of dual- vs. single-sourcing strategies, illustrated with an enterprise numerical example (Section 4 of the source).

## Key results / numbers
No universal numeric constants (the results are case-specific to the paper's own enterprise example, not general parameters). The qualitative finding: as decision-makers become more risk-averse, order allocation shifts away from cheaper/less-reliable sourcing toward the more reliable ("leading") supplier, trading cost for shortage protection (PDF p. 1, citing prior literature, and reproduced in the paper's own numerical study). The augmented ε-constraint method is shown capable of tracing the full efficient (Pareto) frontier between the two objectives, letting a decision-maker see the cost paid at each level of shortage protection.

## Relevance to our case
Provides a concrete, citable method for framing the Earth-Core vs. Earth-Flex trade-off (Earth-Core: lower price, higher reservation commitment, longer lead time; Earth-Flex: higher price, low reservation, short lead time) as a cost-vs-shortage-protection Pareto trade-off, and gives a named technique (augmented ε-constraint on a dual-objective robust model) that the team could reference if it wants to formalize the mandatory stress scenario or an optional robust-analysis module around a stated risk attitude.

## Quotable statements
- "Dual-sourcing is a practical and cost-effective approach to mitigate interruption risk in the supply chain by reducing shortages [at] minimal economic cost." (PDF p. 1)
- Example given of Nokia vs. Ericsson after a shared supplier's factory fire: Nokia's backup supplier let it recover in 5 days, while Ericsson (having eliminated backup suppliers to cut cost) "endured a huge loss and withdrew from the mobile phone production market." (PDF p. 1)
- "[W]e build a dual-objective robust optimization model for a dual-sourcing strategy under interruption risk... [and] employ the augmented ε-constraint method to solve the proposed model by transforming [it] into a single-objective mixed-integer programming model." (abstract)

## Cautions
- The enterprise numerical example is illustrative of the method only; none of its cost/shortage figures apply to this case's channels, prices, or capacities.
- Uses interval/robust uncertainty sets, not statistically fitted disruption probabilities — the case's channel reliability coefficients are not automatically compatible inputs for this exact method without the team stating its own interpretation (as the organizer's evidence map also notes generally for probability/robustness claims in this case).
- Two-supplier setting; the case has five channels, so any direct application would need generalization (the paper's own "future research" section notes this as an open extension).

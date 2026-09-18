# Ho (2024) — Space Logistics Modeling and Optimization: Review of the State of the Art

**Full citation:** Ho, K. (2024). *Space Logistics Modeling and Optimization: Review of the State of the Art*. Journal of Spacecraft and Rockets, Vol. 61, No. 5 (Sept–Oct 2024), pp. 1417–1427. DOI: `10.2514/1.A35982`. Presented as AIAA SciTech Forum Paper 2024-1275, Orlando FL, Jan 2024. Author: Koki Ho, Georgia Institute of Technology (Dutton-Ducoffe Professor, Director of the Space Systems Optimization Group).

## Problem
Space logistics — designing/operating in-space infrastructure, refueling, servicing, assembly, manufacturing (ISAM), and multi-mission exploration campaigns — has become a distinct emerging field at the intersection of astrodynamics and logistics-driven operations research. The paper's stated goal is to categorize the state of the art two ways: (1) by the *application questions* practitioners need answered, and (2) by the *logistics-driven methods* researchers use, so both audiences can navigate the literature.

## Method
This is a structured literature review, not an original model. It defines three application domains — (A1) ISAM for satellites, (A2) multi-mission space exploration campaigns, (A3) megascale satellite constellations — and maps published studies to specific sub-questions within each (performance analysis, tactical planning/scheduling, strategic infrastructure sizing, response to uncertainty, government/commercial coordination; see Table 1, p. 2 of the PDF / journal p. 1419). It then re-categorizes the same literature by method family: (1) network-flow modeling and optimization (drawing formal analogies to the traveling-salesman problem, vehicle-routing problem, and facility-location problem, with orbital staging points as nodes and trajectories as arcs); (2) probabilistic modeling and queueing theory for logistics performance analysis (e.g., M/M/1 and M/G/1-type models adapted to an "orbital queueing" setting); (3) inventory control for infrastructure/resource operations management (e.g., multi-echelon spare-parts and constellation-servicing inventory policies).

## Key results / numbers
No new numerical results — this is a review. Its main "finding" is structural: with in-space refueling depots, the fuel-optimal trajectory is not necessarily the cost-optimal path (a route via a depot may cost more fuel but less lifecycle cost), which is why logistics-driven modeling must be coupled with astrodynamics rather than treated as a downstream add-on (PDF p. 1, journal p. 1417). It also explicitly notes that terrestrial logistics techniques cannot be directly transplanted to space because orbital mechanics couples the trajectory design problem to the commodity-flow optimization problem (e.g., ΔV and time-of-flight can be flow-dependent for low-thrust propulsion) (PDF p. 3–4).

## Relevance to our case
Supports the TerraPlan architectural choice to model the fuel depot as one integrated system — 5 supply channels, storage/throughput losses, inventory, timing/lead time, and demand service — rather than optimizing procurement, storage, and delivery timing as separate, decoupled problems. Useful as a citation for *why* the material-balance block should be built as a joint network-flow/inventory system.

## Quotable statements
- "[W]ith fuel depots in space, the optimal path to the destination in terms of the lifecycle cost is not necessarily a fuel-optimal trajectory... a path stopping by a fuel depot and being refueled before heading to the destination may be preferred even when it requires additional fuel." (PDF p. 1 / journal p. 1417)
- Three method families for space logistics: "1) Network flow modeling and optimization for logistics planning and scheduling, 2) Probabilistic modeling and queueing theory for logistics performance analysis, and 3) Inventory control for resource infrastructure operations management." (PDF p. 2 / journal p. 1418)

## Cautions
- Explicitly method-neutral: does not recommend one algorithm class over another for a given case, and gives no cost/capacity numbers of any kind.
- Reviews *existing published studies*; it is not itself a validated model and cannot be used to justify any specific number in this case.
- Funding acknowledgment discloses U.S. Air Force Office of Scientific Research support for the paper's later revision — irrelevant to content validity but noted for completeness.

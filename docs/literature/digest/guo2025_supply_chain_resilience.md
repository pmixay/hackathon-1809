# Guo, Liu, Song & Wang (2025) — Supply chain resilience: A review from the inventory management perspective

**Full citation:** Guo, Y., Liu, F., Song, J.-S., Wang, S. (2025). *Supply chain resilience: A review from the inventory management perspective*. Fundamental Research, 5(2), pp. 450–463. DOI: `10.1016/j.fmre.2024.08.002`. Received 16 Jan 2023; revised 4 Jul 2024; accepted 6 Aug 2024. Affiliations: Shandong Normal University; Durham University Business School; Duke University (Fuqua); University of Chinese Academy of Sciences. Open access, CC BY-NC-ND.

## Problem
COVID-19, geopolitical conflict, and climate-driven disasters exposed global supply-chain vulnerabilities to both demand surges and supply disruptions. The paper reviews inventory-management strategies — stockpiling, multi-sourcing, capacity reservation, flexible supply contracts — used to build resilience, organized by whether they address supply-side or demand-side disruption risk.

## Method
A structured literature review (not new modeling). Section 2 covers demand-side strategies (inventory pre-positioning/stockpiling for surges). Section 3 covers supply-side strategies in three sub-groups: (a) inventory reserves/prepositioning — with real-world examples such as the U.S. Strategic National Stockpile and documented failure modes (e.g., masks stockpiled in Ontario, Canada after SARS expiring before COVID-19 hit, PDF p. ~4, illustrating obsolescence/rotation cost); (b) multi-sourcing — reviewing optimal dual-sourcing policy structure results from the inventory-theory literature (e.g., threshold-plus-switching-curve base-stock policies for stochastic lead times, and monotonicity/limited-sensitivity properties of optimal dual-sourcing policies), plus the effect of correlated vs. independent supplier default risk (noting a counter-intuitive finding that a retailer might sometimes prefer *positively correlated* supplier risk if it increases supplier competition, despite losing diversification benefit); (c) flexible sourcing contracts — incentive contracts (e.g., investment subsidies) and capacity-reservation contracts (a.k.a. option contracts) that guarantee supply and speed up emergency ordering after a disruption. Section 4 lists future research gaps (e.g., dynamic/AI-supported supply-side decision-making, political-risk-driven "ally sourcing").

## Key results / numbers
No new quantitative results (it is a review); its contribution is the *classification* itself plus curated tables (Table 1, Table 2 in the source) mapping specific papers to specific resilience mechanisms and gaps.

## Relevance to our case
Gives an explicit three-way taxonomy that maps almost one-to-one onto three separate levers the case requires the team to model distinctly: the 45-day physical reserve rule (= inventory prepositioning), the 5-channel diversification across Earth-Core/Earth-Flex/Earth-New/Lunar-ISRU/Emergency (= multi-sourcing), and the take-or-pay / capacity-reservation contract terms on several channels (= flexible sourcing contracts, specifically "capacity reservation contracts (also known as option contracts)"). Useful to justify treating these three as separate, individually-costed resilience instruments in the model and risk register rather than one blended "safety factor."

## Quotable statements
- "[S]upply chain resilience refers to the ability of a supply chain 'to return to its original state or move to a new, more desirable state after being disturbed.'" (PDF p. 1, quoting Ponomarov & Holcomb)
- "Sourcing contracts, such as incentive contracts (e.g., investment subsidies) and capacity reservation contracts (also known as option contracts), are designed to minimize supply disruption risks by enabling choices among multiple unreliable suppliers and facilitating the swift arrival of emergency sourcing orders following a disruption." (PDF p. 10)
- "[T]he quantity of inventory reserves decreases with disruption time, but only when the disruption duration is already sufficiently long." (PDF p. 10)

## Cautions
- A general (mostly terrestrial/industrial) supply-chain review; not specific to space logistics or cryogenic propellant.
- Gives no numeric value for reserve-days, reservation percentages, or take-or-pay terms — the case's 45-day rule and channel-specific reservation terms remain organizer-fixed `CASE_INPUT` values, not derived from this paper.
- Findings about correlated-risk preference and policy structure come from cited primary studies within the review, not from original analysis by these review authors — if a specific structural claim (e.g., the threshold/switching-curve policy) is to be relied on precisely, the underlying primary paper should be checked directly.

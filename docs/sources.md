# TerraPlan — Sources and Evidence Map

Case: CosmoHackathon 2026, Case 2, "Fuel Space Circuit 2035" (Топливный космоконтур 2035). Team: TerraPlan.

This document lists every source used or considered for the TerraPlan model and, for each one, states the chain required by the organizers:

**source -> proposition/method it supports -> where it is used in the TerraPlan model -> limitation of applicability.**

No source in this document is used to justify the case's synthetic numbers (prices, capacities, CAPEX limits, reliability coefficients, loss rates). Those are fixed `CASE_INPUT` values set by the organizers. Sources are cited only for the *methods, structures, and classes of trade-off* the model uses to turn those inputs into a plan.

Organizer-provided materials (Section A) are kept separate from the organizer's literature folder (Section B), from sources the organizers mention but did not put in the folder (Section C), and from sources the team finds on its own (Section D).

All PDFs referenced in Section B were downloaded by the organizers into the Yandex Disk folder "Топливо" and mirrored into this repository at `docs/literature/` on 2026-09-18. Text was extracted with `pymupdf` (first 2-3 pages read in full for bibliographic data and abstract; remaining pages skimmed for methods/results) rather than transcribed from memory.

---

## A. Organizer-provided materials

| # | Material | Description |
|---|---|---|
| A1 | `docs/organizer/case_statement_ru.pdf` — "Постановка кейса — Топливный космоконтур 2035" (КосмоХакатон 2026 organizing committee, 14 pp.) | The case statement: problem framing, 5 supply channels, storage/loss rules, take-or-pay and capacity-reservation terms, CAPEX options, 45-day reserve rule, mandatory stress scenario. Primary source of truth for all numeric inputs. |
| A2 | `docs/organizer/evaluation_criteria_ru.pdf` — "Критерии оценки кейса — Топливный космоконтур 2035" (organizing committee, 5 pp.) | Scoring rubric: model correctness/reliability (max 25 pts) plus other weighted criteria for the management note, working digital circuit, stress tests, risk register, and defense. |
| A3 | Reference repository `github.com/SpaceEconomyPolicy/test_oil` (mirrored under `docs/organizer/reference_repo/`, snapshot commit `cec6de1950276091689e71a67f9a875fb4ca6213`, 2026-09-18) | Organizer's starter technical repository: control rules, exchange formats, synthetic test vectors, `docs_SCIENTIFIC_BASIS.md` evidence map, calculation/stress-test protocol, FAQ. Explicitly does **not** define supply mix, prices, capacities, or the "right" solver. |
| A4 | Yandex Disk literature folder "Топливо" — `https://disk.360.yandex.ru/d/oMVoGQwhXvzzGg` (link given in `docs/organizer/additional_links_ru.pdf`) | The organizer's supplementary-literature folder for this case; its 8 PDFs are mirrored in `docs/literature/` and reviewed in Section B below. |

`docs/organizer/additional_links_ru.pdf` itself is a one-page pointer document (contains only the two links above, A3 and A4) and is not treated as a separate content source.

---

## B. Organizer literature folder (8 papers)

### B1. Koki Ho (2024) — Space Logistics Modeling and Optimization: Review of the State of the Art

**Entry.** Ho, K. (2024). *Space Logistics Modeling and Optimization: Review of the State of the Art*. Journal of Spacecraft and Rockets, Vol. 61, No. 5 (Sept–Oct 2024), pp. 1417–1427. DOI: `10.2514/1.A35982`. (Presented as AIAA SciTech Forum Paper 2024-1275.) File: `Ho — Space Logistics Modeling and Optimization.pdf` (local name `ho-2024-space-logistics-modeling-and-optimization-review-of-the-state-of-the-art.pdf`).

**Summary.** This is a review paper that organizes the space-logistics literature two ways: by application (in-space servicing/assembly/manufacturing, multi-mission exploration campaigns, megascale constellations) and by underlying method. It identifies three core logistics-driven method families relevant to space: (1) network-flow modeling and optimization for planning/scheduling (drawing analogies to TSP/VRP/facility-location problems), (2) probabilistic modeling and queueing theory for performance analysis, and (3) inventory control for infrastructure/resource operations. The paper argues that with in-space depots and refueling, the "optimal path" is no longer a pure trajectory problem but a joint logistics-and-astrodynamics problem, and that terrestrial logistics theory needs adaptation (not direct transplantation) to orbital-mechanics constraints. It remains explicitly method-neutral about which specific algorithm a practitioner should use.

**Traceability table**

| Field | Content |
|---|---|
| Supports (proposition/method) | Framing an orbital fuel/depot system as an integrated network-flow + inventory-control + probabilistic-performance problem, not a trajectory-only problem; taxonomy of logistics-driven methods. |
| Use in TerraPlan model | Architectural justification for treating the 5 supply channels, depot storage, timing/lead time, and demand service jointly as one material-balance/inventory system rather than as independent trajectory or procurement sub-problems; motivates the "network of flows and stocks" framing behind the material-balance block. |
| Limitation / what it does NOT support | Method-neutral by design — it does not prescribe a specific solver (LP/MILP, simulation, rule-based) and gives no numbers for this case; it does not validate any of TerraPlan's specific prices, capacities, or channel parameters. |

---

### B2. Simonini et al. (2024) — Cryogenic propellant management in space: open challenges and perspectives

**Entry.** Simonini, A., Dreyer, M., Urbano, A., Sanfedino, F., Himeno, T., Behruzi, P., Avila, M., Pinho, J., Peveroni, L., Gouriet, J.-B. (2024). *Cryogenic propellant management in space: open challenges and perspectives*. npj Microgravity, 10:34. DOI: `10.1038/s41526-024-00377-5`. File: `Cryogenic_propellant_management_in_space_open_chal.pdf`.

**Summary.** A perspective/review article (based on a White Paper for ESA's SciSpacE strategy) covering long-duration cryogenic (LH2/LCH4/LOX) storage and on-orbit transfer for a depot-based deep-space architecture. It reviews reference missions and depot architectures (LEO/GEO/EML1/EML2), compiles rough-order-of-magnitude engineering parameters (tank capacity ~50 t/tank, storage 6–12 months, operating pressure 100–350 kPa, heat flux 1–100 W/m² depending on insulation, boil-off rates on the order of 0.01–0.2 kg/h at various orbital locations), and walks through the operational phases (storage, conditioning, maneuvers, transfer) with the associated unresolved physical phenomena (boiling regimes, chill-down, sloshing, interface dynamics in microgravity). Its central conclusion is that many physical-knowledge gaps remain open across all these operations, which is why it is framed as "open challenges."

**Traceability table**

| Field | Content |
|---|---|
| Supports (proposition/method) | The engineering plausibility and structure of treating cryogenic storage/transfer losses as a distinct block: boil-off as a physically grounded loss mechanism, tied to storage duration, insulation, and depot location; typical order-of-magnitude ranges for storage duration (months) and depot tank sizing. |
| Use in TerraPlan model | Subject-matter motivation for the storage/throughput-loss block of the material balance (separating "loss during storage/transfer" from "loss during transport"); qualitative backing for why loss rates depend on storage duration and depot conditions, supporting a distinct loss treatment per channel/inventory stage. |
| Limitation / what it does NOT support | Gives no single "correct" loss-rate percentage; the case's fixed loss parameters (e.g., a specific storage loss rate) are `CASE_INPUT` values and are not derived from or validated by this paper's ranges. It is a physics/engineering perspective, not an economic or supply-chain source. |

---

### B3. Sommariva et al. (2023) — Preliminary analyses on technical and economic viability of moon-mined propellant for on-orbit refueling

**Entry.** Sommariva, A., Gaudenzi, P., Pianorsi, M., Pasquali, M., Vittori, E., Eugeni, M., Italiano, M., Telli, C., Di Nicola, M., Gori, L., Chizzolini, B. (2023). *Preliminary analyses on technical and economic viability of moon-mined propellant for on-orbit refueling*. Acta Astronautica, 204, pp. 425–433. DOI: `10.1016/j.actaastro.2023.01.004`. File: `Preliminary_analyses_on_technical_and_economic_viability_of_moon-mined_propellant_for_on-orbit_refueling.pdf`.

**Summary.** Compares two architectures supplying an orbital depot at Earth–Moon L1: propellant shipped from Earth ("Case 2") versus propellant mined and produced on the Moon and delivered by a "Moon shuttle" ("Case 1"). Both are evaluated with a discounted-cash-flow / NPV model over a 5-year construction + 10-year operating horizon, each with its own WACC discount rate reflecting perceived risk (13% for the lunar case, 11.5% for the Earth case, the lunar beta being calibrated 13% higher due to larger, riskier investment). Because CAPEX/OPEX/revenue inputs are highly uncertain, the authors run a Monte Carlo simulation (5,000 draws, lognormal CAPEX distributions with standard deviation set to 10% of the median) to obtain a distribution of NPVs around the break-even ("minimum") price for each case (the paper computes zero-NPV minimum prices of 5.07 M$/Mt for the lunar case vs 10.55 M$/Mt for the Earth case). The paper concludes the lunar option is economically more attractive and less volatile in this analysis, and argues there is room for multiple ventures/public co-financing.

**Traceability table**

| Field | Content |
|---|---|
| Supports (proposition/method) | Comparing an Earth-supplied vs. Moon/ISRU-supplied propellant architecture on a common technical-economic basis under high input uncertainty, using discounted cash flow plus Monte Carlo to express that uncertainty (5,000-run design, lognormal input distributions, distinct discount rates per architecture's risk). |
| Use in TerraPlan model | Template for the lunar-vs-Earth economic comparison logic (comparing Lunar-ISRU against the Earth channels on cost/CAPEX/risk, not just nominal price); optional template for a Monte Carlo procedure around uncertain CAPEX/OPEX if the team implements the optional Monte Carlo module; illustrates why a lunar/new option can look attractive only once risk-adjusted discounting and uncertainty are made explicit, not from nominal price alone. |
| Limitation / what it does NOT support | This paper's own conclusion (Moon wins) is for its own bespoke assumptions (its own CAPEX, WACC, and demand estimates) and must **not** be carried over as a ready-made answer for this case — in the case, Lunar-ISRU is one alternative among five, not a pre-selected winner. It does not calibrate any of TerraPlan's synthetic prices, capacities, or CAPEX figures, and its Monte Carlo distributions are illustrative of a method, not a fitted model of this case's channels. |

---

### B4. Linkov et al. (2006) — From comparative risk assessment to multi-criteria decision analysis and adaptive management: Recent developments and applications

**Entry.** Linkov, I., Satterstrom, F.K., Kiker, G., Batchelor, C., Bridges, T., Ferguson, E. (2006). *From comparative risk assessment to multi-criteria decision analysis and adaptive management: Recent developments and applications*. Environment International, 32, pp. 1072–1093. DOI: `10.1016/j.envint.2006.06.013`. File: `From_comparative_risk_assessment_to_multi-criteria_decision_analysis_and_adaptive_management_recent_developments_and_applications.pdf`.

**Summary.** A methodological review arguing that comparative risk assessment (CRA) lacks a structured way to pick an optimal alternative, and that multi-criteria decision analysis (MCDA) fills that gap by combining modeling/monitoring results, risk analysis, cost information, and explicit stakeholder preferences into a decision matrix. It surveys MCDA technique families — multi-attribute utility theory (MAUT, compensatory, assumes a rational decision-maker with consistent preferences), the Analytic Hierarchy Process (AHP, compensatory, pairwise criteria comparisons), and outranking methods (partially compensatory, used when criteria are hard to aggregate onto one scale) — and reviews real applications to contaminated-site/environmental remediation decisions. It then couples MCDA with adaptive management: because ecosystem/decision outcomes are uncertain, the paper argues decisions should be revisited as new information arrives (active vs. passive adaptive management), rather than treated as one-shot optimizations.

**Traceability table**

| Field | Content |
|---|---|
| Supports (proposition/method) | Structured MCDA as a decision framework requiring explicit criteria, a stated normalization/aggregation method, and disclosed weights; explicit stakeholder-value elicitation; adaptive management (revisit decisions under new information) as a companion to one-shot optimization. |
| Use in TerraPlan model | Methodological basis for the optional MCDA module: if used, criteria, normalization, and weight origin must be disclosed and sensitivity-tested (per the case rules), following the MAUT/AHP/outranking distinctions in this paper; also supports framing the stakeholder analysis and any plan revision logic as adaptive management rather than a single fixed answer. |
| Limitation / what it does NOT support | Gives no ready-made stakeholder weight vector for this case (or for space-fuel-supply stakeholders at all) — the paper's worked example is a New York/New Jersey Harbor contaminated-sediment case, unrelated in substance; MCDA is optional in this case, and this paper does not make it mandatory or supply its parameters. |

---

### B5. Han, Zhang, Wang & Park (2023) — The efficient and stable planning for interrupted supply chain with dual-sourcing strategy: a robust optimization approach considering decision maker's risk attitude

**Entry.** Han, B., Zhang, Y., Wang, S., Park, Y. (2023). *The efficient and stable planning for interrupted supply chain with dual-sourcing strategy: a robust optimization approach considering decision maker's risk attitude*. Omega, 115, article 102775. DOI: `10.1016/j.omega.2022.102775`. File: `The_efficient_and_stable_planning_for_interrupted_supply_chain.pdf`.

**Summary.** Builds a dual-objective (cost vs. shortage) robust-optimization model for ordering from two suppliers under supply-disruption uncertainty, explicitly parameterized by the decision-maker's risk attitude (risk-averse / risk-neutral / risk-seeking). Disruption uncertainty is modeled with interval/robust-optimization uncertainty sets rather than fitted probability distributions, and the dual-objective is solved via the augmented ε-constraint method (converting it into a single-objective mixed-integer program). Using a numerical/enterprise example, the paper shows that a more risk-averse decision-maker shifts more of the order allocation toward the reliable "leading" supplier even at higher cost, illustrating a quantifiable trade-off between cost efficiency and shortage protection under dual sourcing. The conclusion notes the model could extend to more than two sources and multiple echelons.

**Traceability table**

| Field | Content |
|---|---|
| Supports (proposition/method) | Dual-source order allocation as a robust (interval-based, not probability-fitted) optimization problem trading off cost against shortage risk; the idea that risk attitude systematically changes how much volume is allocated to a cheaper-but-less-reliable source vs. a costlier-but-more-reliable one. |
| Use in TerraPlan model | Conceptual/methodological support for the dual-sourcing comparison between Earth-Core (cheaper, longer lead time, high reservation) and Earth-Flex (pricier, flexible, low reservation), and for framing the mandatory stress scenario and any optional robust-analysis module as a cost-vs-shortage trade-off under an explicit risk stance. |
| Limitation / what it does NOT support | Does not calibrate the actual Earth-Core/Earth-Flex split, prices, or capacities used in TerraPlan; its "two suppliers" setting and enterprise numerical example are illustrative of the *method*, not a fitted model of a 5-channel cryogenic-propellant supply system. |

---

### B6. Guo, Liu, Song & Wang (2025) — Supply chain resilience: A review from the inventory management perspective

**Entry.** Guo, Y., Liu, F., Song, J.-S., Wang, S. (2025). *Supply chain resilience: A review from the inventory management perspective*. Fundamental Research, 5(2), pp. 450–463. DOI: `10.1016/j.fmre.2024.08.002`. File: `Supply_chain_resilience_A_review_from_the_inventory_management_perspective.pdf`.

**Summary.** A literature review classifying inventory-management strategies for supply chain resilience into supply-side (disruption) and demand-side (surge) categories. On the supply side it reviews three mechanisms in turn: inventory prepositioning/stockpiling (with real examples such as national strategic stockpiles and their perishability/rotation problems), multi-sourcing (including optimal dual-sourcing policy structure — e.g., threshold/switching-curve base-stock policies — and the effect of correlated vs. independent supplier disruption risk), and flexible sourcing contracts (incentive contracts such as investment subsidies, and capacity-reservation/option contracts that guarantee supply and enable fast emergency ordering after a disruption). It stresses that these are distinct levers with distinct costs (stockpiling carries holding/obsolescence cost; multi-sourcing requires managing correlated risk; contracts require choosing the right contract type) and identifies open research gaps (e.g., dynamic/AI-supported supply-side decisions).

**Traceability table**

| Field | Content |
|---|---|
| Supports (proposition/method) | Explicit three-way classification of resilience levers — inventory prepositioning, multi-sourcing/diversification, and flexible/capacity-reservation contracts — as distinct instruments with distinct costs and failure modes; capacity-reservation (option) contracts as a named mechanism for guaranteeing supply and enabling fast emergency response. |
| Use in TerraPlan model | Direct conceptual support for keeping the model's resilience instruments separate rather than conflated: the 45-day physical reserve rule (inventory prepositioning), the 5-channel diversification incl. Earth-Core/Earth-Flex/Earth-New/Lunar-ISRU (multi-sourcing), and take-or-pay / capacity-reservation contract terms (flexible sourcing contracts) — each modeled and reported as its own lever in the risk register and stress analysis. |
| Limitation / what it does NOT support | Does not specify the exact 45 reserve-days, the specific reservation percentages, or take-or-pay terms used in this case — those remain organizer-fixed `CASE_INPUT` values; it is a generic (mostly terrestrial/industrial) review, not a space-logistics or cryogenic-propellant-specific source. |

---

### B7. Federgruen, Liu & Lu — Dual Sourcing under Internal and External Volatilities

**Entry.** Federgruen, A. (Columbia Business School), Liu, Z. (Imperial College Business School), Lu, J. (School of Data Science, CUHK–Shenzhen). *Dual Sourcing under Internal and External Volatilities*. Unpublished working paper (PDF metadata: created 2025-01-28, last modified 2025-11-30; LaTeX/macOS-Quartz-generated PDF with no journal header, volume, or page range). **No DOI found** in the PDF text (checked title page and the reference list). File on disk: `Dual_sourcing_Creating_and_utilizing_flexible_capacities_with_a_second_supply_source.pdf` — note the **file name does not match the in-document title**; the PDF's actual title page reads "Dual Sourcing under Internal and External Volatilities," with no subtitle matching the file name. This discrepancy could not be resolved from the PDF alone (likely a retitled/revised version of a paper downloaded under an earlier working title) and should be treated as unverified until the team locates the paper's canonical published form, if any.

**Summary.** Studies a periodic-review, single-item dual-sourcing inventory model where cost parameters, capacity limits, supply mechanisms, and demand distributions all fluctuate with an underlying Markov-modulated "state-of-the-world" (external volatility), while actual delivered quantities are also subject to random yield/curtailment around the ordered amount (internal volatility). Under the assumption that the two suppliers' lead times are consecutive (differ by one period), the authors show the optimal joint ordering-plus-salvaging policy has a relatively simple structure (a modified base-stock-type policy) and can be computed efficiently. The paper's central managerial finding is counter-intuitive: increased *external* volatility, when a firm has access to dual sourcing, can be *exploited* to improve system performance rather than simply raising cost — benefits from flexibility grow as external volatility increases in specific ways — whereas internal (yield/supply) volatility behaves more conventionally as a pure cost driver. Numerical studies support and refine these structural claims.

**Traceability table**

| Field | Content |
|---|---|
| Supports (proposition/method) | Separating "external" volatility (macro/market/regime shifts affecting both cost and capacity) from "internal" volatility (random shortfall in what is actually delivered) in a dual-sourcing model; base-stock-type optimal ordering policies for two capacitated, imperfectly reliable sources; the finding that flexible dual sourcing can turn macro volatility into an advantage rather than only a cost. |
| Use in TerraPlan model | Conceptual support for distinguishing, in the risk register and sensitivity analysis, disruption/shortfall risk internal to a channel (e.g., Lunar-ISRU commissioning delay, reliability coefficients below 1) from external volatility affecting the whole supply environment (e.g., demand growth uncertainty, price/tariff shifts); supports treating the Earth-Core / Earth-Flex / Earth-New / Lunar-ISRU / Emergency mix as a portfolio whose value partly comes from flexibility under volatility, not only from nominal unit price. |
| Limitation / what it does NOT support | Unpublished/unreviewed working paper with unverified bibliographic status and no DOI — cite with caution and re-verify before submission if a peer-reviewed version is found; its exact-policy results require a Markov-chain state-of-the-world and consecutive lead times, which are modeling choices not adopted verbatim in this case; it gives no numbers usable for calibration here. |

---

### B8. Tanaka (2014) — Toward project and program management paradigm in the space of complexity: a case study of mega and complex oil and gas development and infrastructure projects

**Entry.** Tanaka, H. (2014). *Toward project and program management paradigm in the space of complexity: a case study of mega and complex oil and gas development and infrastructure projects*. Procedia - Social and Behavioral Sciences, 119, pp. 65–74 (27th IPMA World Congress). DOI: `10.1016/j.sbspro.2014.03.010`. File: `Toward_project_and_program_management_paradigm_space_oil.pdf`.

**Summary.** A qualitative, practitioner-authored paper (42 years in EPC industry experience) analyzing why mega-scale, complex oil-and-gas and infrastructure projects outrun conventional project-management theory. It tracks PESTLE (political, economic, social, technological, legal, environmental) "complexity events" affecting the project industry and derives four "new thoughts" toward a program-management paradigm: (1) meta program management to balance multiple, sometimes misaligned stakeholder objectives across a program rather than a single project; (2) knowledge- and stakeholder-integration platforms; (3) finance planning/structuring as a first-class ingredient of materializing large projects (given the very large capital requirements typical of these projects); and (4) contingent/adaptive risk management for "wicked," unstructured-problem-type risks, explicitly citing Linkov (2006) (see B4 above) as a source for the CRA-to-MCDA-to-adaptive-management transition applied to complex-project risk.

**Traceability table**

| Field | Content |
|---|---|
| Supports (proposition/method) | Treating a large capital-intensive infrastructure/resource-extraction project (used here by analogy to the orbital fuel depot buildout) as a "complex project/program" requiring multi-objective, multi-stakeholder governance, deliberate finance-structuring, and adaptive/contingent risk management rather than single-objective delivery optimization. |
| Use in TerraPlan model | Analogy-based support for the management-note framing of the depot buildout (CAPEX phasing for Earth-New commissioning and Lunar-ISRU pilot, multi-stakeholder trade-offs) as a complex-program problem, and for linking the risk register / stakeholder analysis to an adaptive, PESTLE-style risk lens rather than a single deterministic forecast. |
| Limitation / what it does NOT support | Qualitative and terrestrial (oil & gas / infrastructure megaprojects), not a quantitative or space-specific source; gives no cost, capacity, or schedule numbers transferable to this case; it is used only as a program-management framing analogy, not as evidence for any numeric assumption. |

---

## C. Organizer-listed sources not in the folder

These sources are named in `docs/organizer/reference_repo/docs_SCIENTIFIC_BASIS.md` (the organizer's own evidence map) but are not among the 8 PDFs in the literature folder. DOIs/IDs are taken directly from that document; PDFs were not separately fetched or re-verified against a full read for this table (see limitation column).

### C1. NASA-STD-7009B — Standard for Models and Simulations

| Field | Content |
|---|---|
| Entry | NASA. *NASA-STD-7009, Standard for Models and Simulations*, Version B (active document, dated 2024-03-05); companion implementation guide `NASA-HDBK-7009B`. Links: `https://standards.nasa.gov/standard/nasa/nasa-std-7009`, `https://standards.nasa.gov/standard/NASA/NASA-HDBK-7009`. |
| Supports | Credibility, verification & validation, uncertainty/sensitivity disclosure, and traceable modeling-and-simulation (M&S) practice. |
| Use in TerraPlan model | Discipline for reproducibility/provenance of the model: explicit assumptions, source traceability, control-case checks, and a stated validation route in the management note. |
| Limitation | Does not specify the supply mix, prices, capacities, or a "correct" solver; the case does not require formal NASA certification of the team's model. |

### C2. Bertsimas & Sim (2004) — The Price of Robustness

| Field | Content |
|---|---|
| Entry | Bertsimas, D., Sim, M. (2004). *The Price of Robustness*. Operations Research, 52(1), pp. 35–53. DOI: `10.1287/opre.1030.0065`. |
| Supports | The trade-off between nominal (expected-case) objective performance and protection against worst-case realizations of uncertain data in robust optimization; the "budget of uncertainty" concept controlling how conservative the robust solution is. |
| Use in TerraPlan model | Methodological basis if the team implements the optional robust-analysis module, and for articulating a "price of robustness" (extra cost paid for protection) alongside the mandatory stress scenario. |
| Limitation | Robust optimization is optional, not mandatory, for this case; the paper gives no method for constructing the uncertainty set's parameters from this case's data — that remains the team's own, disclosed assumption. |

### C3. JCGM 101:2008

| Field | Content |
|---|---|
| Entry | Joint Committee for Guides in Metrology (JCGM). *Evaluation of measurement data — Supplement 1 to the "Guide to the expression of uncertainty in measurement" — Propagation of distributions using a Monte Carlo method*, JCGM 101:2008. DOI: `10.59161/JCGM101-2008`. Official page: `https://www.bipm.org/en/doi/10.59161/jcgm101-2008`. |
| Supports | A reproducible procedure for propagating input probability distributions through a model via Monte Carlo simulation (measurement-uncertainty context). |
| Use in TerraPlan model | Reference procedure for the optional Monte Carlo module (specified input distributions, stated dependence assumptions, numerical convergence/reporting practice), if the team runs one. |
| Limitation | Written for measurement uncertainty, not for supply/economic risk; it does not create or justify probability distributions for channel reliability or demand in this case — the case's reliability coefficients are not full statistical failure models, and any distribution used must be separately justified by the team. |

### C4. Kenny, Eddleman, Keplinger, Stephens, Hartwig & Perrin (2025) — Guidelines for In-Space Cryogenic Propellant Transfer

| Field | Content |
|---|---|
| Entry | Kenny, R.J., Eddleman, D.E., Keplinger, J.D., Stephens, J.R., Hartwig, J.W., Perrin, T.M. (2025). *Guidelines for In-Space Cryogenic Propellant Transfer*. AIAA ASCEND 2025 conference paper. DOI: `10.2514/6.2025-4122`. |
| Supports | Engineering guidance and early concept-of-operations (CONOPS) considerations for in-space cryogenic propellant transfer, incl. interface/safety considerations. |
| Use in TerraPlan model | Subject-matter context reinforcing why cryogenic transfer between channels/depot needs distinct engineering/operational treatment (complements B2, the Simonini et al. cryogenic-management review). |
| Limitation | Not an economic source; does not supply prices, investment figures, or a substitute for detailed engineering design; per the organizer's evidence map, must not be conflated with the related NTRS presentation (C5) as if they were the same bibliographic object. |

### C5. Perrin (2025) — NASA NTRS presentation, 31st Space Cryogenic Workshop

| Field | Content |
|---|---|
| Entry | Perrin, T.M. NASA NTRS Document ID `20250003540`, presented at the 31st Space Cryogenic Workshop (2025). Link: `https://ntrs.nasa.gov/citations/20250003540`. A related organizer-cited NTRS record, `20250004625` (`https://ntrs.nasa.gov/citations/20250004625`), is also named in the evidence map as a distinct object. |
| Supports | Contextual/engineering confirmation of ISCPT (In-Space Cryogenic Propellant Transfer) guidelines and CFM (cryogenic fluid management) operations context. |
| Use in TerraPlan model | Same subject-matter-context role as C4; used only to corroborate the plausibility of the cryogenic loss/transfer framing, not for numbers. |
| Limitation | A conference/workshop presentation, not a peer-reviewed economic study; not an independent source for this case's financial or capacity parameters. |

---

## D. Самостоятельно найденные и проверенные источники

19.09.2026 команда открыла карточки издателей/авторов/NASA и доступные тексты по ссылкам. Эти источники
поддерживают только метод принятия решения и конструкцию договоров; ни один не используется для
перекалибровки синтетических цен, мощностей, коэффициентов надёжности или потерь организатора.

| Источник (полная запись и ссылка) | Поддерживаемый аргумент | Применение в TerraPlan | Ограничение | Проверено |
|---|---|---|---|---|
| Dixit, A.K. & Pindyck, R.S. (1994), *Investment under Uncertainty*, Princeton University Press, DOI [10.2307/j.ctt7sncv](https://www.jstor.org/stable/j.ctt7sncv) | У необратимой инвестиции при сохраняющейся неопределённости есть опционная ценность поэтапности или ожидания информации. | Обосновывает конструкцию «опцион → реализация» Earth-New и отказ автоматически финансировать ISRU в P2z; дорожная карта использует gate, а не одновременный CAPEX. | TerraPlan не считает real-options valuation и волатильность; книга не доказывает, что Earth-New стоит именно 360 млн в синтетическом кейсе. | Да, 19.09.2026 |
| Anderson, E., Chen, B. & Shao, L. (2017), “Supplier Competition with Option Contracts for Discrete Blocks of Capacity,” *Operations Research* 65(4):952–967, DOI [10.1287/opre.2017.1593](https://pubsonline.informs.org/doi/10.1287/opre.2017.1593) | Опцион мощности разделяет авансовую плату за резерв и цену исполнения и может сочетаться со spot/гибкой закупкой при неопределённости. | Поддерживает раздельный учёт резерва и переменной закупки и оценку портфеля A/B/C, а не выбор только по минимальной номинальной цене. | Равновесие и известные распределения статьи не реализованы; поставщики кейса не ведут стратегические торги. | Да, 19.09.2026 |
| Li, J., Luo, X., Wang, Q. & Zhou, W. (2021), “Supply chain coordination through capacity reservation contract and quantity flexibility contract,” *Omega* 99:102195, DOI [10.1016/j.omega.2020.102195](https://www.sciencedirect.com/science/article/pii/S0305048318314816) | Резерв мощности и гибкость количества по-разному распределяют цену мощности, риск спроса и санкции за неисполнение; при долгом lead time явное распределение риска ценно. | Поддерживает term sheet P2z: B как клапан без TOP, минимумы A/C и меры поставщику за срыв подтверждённой мощности. | Статья оптимизирует стилизованную игру с прибылью/выручкой, которых нет в кейсе; уровни санкций не импортируются. | Да, 19.09.2026 |
| Masten, S.E. & Crocker, K.J. (1985), “Efficient Adaptation in Long-term Contracts: Take-or-Pay Provisions for Natural Gas,” *American Economic Review* 75(5):1083–1093; [карточка автора](https://websites.umich.edu/~semasten/publications.html) | Take-or-pay может быть механизмом стимулов/возмещения за невыборку, а не просто закупочной ценой; уровень связан с потерянной альтернативной ценностью поставщика. | Поддерживает TOP при доступной мощности, но исключение недоступного по вине поставщика объёма; риск спроса остаётся у оператора. | Газовые институты отличаются от пусков/топлива; TerraPlan принимает заданные 70%/50% и не оценивает оптимальную долю TOP. | Да, 19.09.2026 |
| Notardonato, W.U. et al. (2017), “Zero Boil-Off Methods for Large Scale Liquid Hydrogen Tanks Using Integrated Refrigeration and Storage,” NASA KSC-E-DAA-TN44054, NTRS [20170006481](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20170006481.pdf) | Испытания NASA показывают, что активное охлаждение/управление способно удерживать крупный бак LH2 в режиме zero boil-off в испытанной наземной конфигурации. | Поддерживает представление ZBO как активной системы с приёмкой, доступностью и OPEX, а не пассивного ярлыка; обосновывает performance tests. | Наземная демонстрация LH2 не квалифицирует орбитальное депо и не подтверждает 1,2% потерь, 120 т, CAPEX или нулевой лаг ввода в кейсе. | Да, 19.09.2026 |

**Почему этого достаточно для защиты.** Пять источников закрывают всю цепочку роли 2: поэтапная инвестиция
(Dixit/Pindyck), цена опциона мощности (Anderson et al.), гибкий резерв и санкции (Li et al.), владелец риска
take-or-pay (Masten/Crocker) и инженерный объект приёмки ZBO (NASA). Ограничения стоят рядом с применением,
поэтому методическая поддержка не выдаётся за доказательство входных чисел кейса.

---

## E. Как цитировать в управленческой записке

1. Каждая ссылка должна замыкать цепочку: **источник → положение/метод → место реализации в TerraPlan (модуль/раздел/формула) → ограничение**. Одного имени без указания реализации и границы недостаточно.
2. Источник цитируется только для поддерживаемого *метода или структурного паттерна* (например, компромисс стоимость/дефицит при dual sourcing, раскрытие весов MCDA, процедура Монте-Карло), а не для конкретного числа кейса. Цены, мощности, CAPEX, надёжность и потери берутся только из постановки (`docs/organizer/case_statement_ru.pdf`) и файлов `CASE_INPUT`.
3. Провенанс должен быть виден: раздел A и литература организатора B не выдаются за собственный поиск. Только проверенные позиции раздела D называются «найденными командой».

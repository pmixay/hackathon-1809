# Simonini et al. (2024) — Cryogenic propellant management in space: open challenges and perspectives

**Full citation:** Simonini, A., Dreyer, M., Urbano, A., Sanfedino, F., Himeno, T., Behruzi, P., Avila, M., Pinho, J., Peveroni, L., Gouriet, J.-B. (2024). *Cryogenic propellant management in space: open challenges and perspectives*. npj Microgravity, 10:34. DOI: `10.1038/s41526-024-00377-5`. Based on a White Paper for ESA's SciSpacE strategy. Lead author affiliation: Von Karman Institute for Fluid Dynamics.

## Problem
Crewed deep-space exploration architectures increasingly rely on cryogenic propellants (liquid hydrogen, liquid methane, liquid oxygen as oxidizer) for high specific impulse, but these fluids are liquid only below ~120 K, so long-duration storage and on-orbit transfer via a depot are needed to enable (or extend) missions. The paper reviews what is and is not physically understood about managing these fluids in space.

## Method
Structured review/perspective in two parts: (1) application perspective — reference missions, ΔV requirements, and candidate depot architectures/locations (LEO, GEO, EML1, EML2), compiling rough-order-of-magnitude engineering parameters from prior mission-architecture studies; (2) technology/physics perspective — walking through depot operational phases (storage, conditioning, maneuvers, transfer) and, for each, identifying the dominant physical phenomena and the open gaps in physical understanding (e.g., two-phase flow chill-down regimes, pool/flow boiling at tank walls, liquid sloshing and free-surface dynamics under variable acceleration, autogeneous vs. heterogeneous pressurization).

## Key results / numbers
Rough-order-of-magnitude compiled parameters (Table 1, PDF p. 2): depot with 6–8 tanks, ~50 t capacity per tank, tank length 10–20 m, diameter 5 m; storage duration 6–12 months; operating pressure 100–350 kPa; heat flux 1 W/m² (with multi-layer insulation) up to 100 W/m² (without); transfer rate 0.15–4.4 kg/s. Location-specific boil-off comparison (Table 2, PDF p. 3, hydrogen only): LEO heat flux ~216 W/m², boil-off 0.02–0.20 kg/h; GEO heat flux ~138 W/m², boil-off 0.01–0.13 kg/h; EML1 heat flux ~136 W/m², boil-off 0.01–0.12 kg/h — i.e., boil-off is lowest and most stable at the EML1 location among those compared. A four-month zero-boil-off (ZBO) methane storage demonstration using a cryocooler is cited (PDF p. 5) as evidence ZBO is achievable but not yet routine at depot scale/duration.

## Relevance to our case
Provides the physical/engineering backdrop for treating storage and transfer losses in the material-balance model as a distinct, location- and duration-dependent phenomenon (boil-off), rather than a flat, arbitrary "shrinkage" number — supporting the case's separation of storage losses from transport losses, and the idea that loss rates plausibly differ by depot configuration and dwell time.

## Quotable statements
- "[M]any gaps in physical knowledge still need to be filled." (abstract, PDF p. 1)
- "The most important quantity is the boil-off loss. This is the mass of liquid propellant which is converted into a gas due to the incoming heat fluxes." (PDF p. 2)
- Typical heat fluxes "range from 1 W m⁻² with multi-layer insulations (MLI) to 100 W m⁻² without MLI." (PDF p. 3)

## Cautions
- Gives ranges compiled from multiple prior mission-architecture studies (different assumptions each), not a single validated loss-rate model — none of its numbers should be read as "the" real-world loss rate.
- Focused on liquid hydrogen (and to a lesser extent methane/oxygen) physics; does not address cost, contracts, or supply-chain structure at all.
- Per the organizer's own evidence map (`docs_SCIENTIFIC_BASIS.md`), this paper does not confirm that any specific case loss-rate parameter (e.g., a fixed storage-loss percentage) is a real-world universal ZBO figure — those remain case-fixed synthetic inputs.

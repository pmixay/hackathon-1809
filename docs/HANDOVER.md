# R4 delivery and GitVerse handover

## Delivered scope

| Responsibility | Evidence |
|---|---|
| Criterion 19: operator functions | `python -m terraplan ui`; `src/terraplan/web.py`, `src/terraplan/static/` |
| Input and contract editing, errors | CSV copy editor, explicit TEAM_ASSUMPTION notes, plan forms; `tests/test_web.py` |
| Scenario comparison | Pin A, calculate B, compare decisions, KPIs and yearly metrics, download CSV |
| Criterion 20: save/reopen and exports | Workspace JSON, CSV/XLSX/JSON archive with case data and verification manifest |
| Source-X and 2041 | UI demo, `experiments/run_extensibility.py`, `results/extensibility/`, unchanged control data |
| Run instructions | `README.md`, `docs/operator_guide.md` |
| Presentation, ≤12 slides | `docs/presentation/TerraPlan.pptx` (12 slides), source `build_deck.mjs` |
| UI / delivery contribution to note | `docs/management_note.md` §12, budget and roadmap in `docs/roadmap_budget.md` |

## Acceptance record (2026-09-19)

- `python -m pytest -q`: 41 passed at the first R4 acceptance run (including 8 new UI tests).
- Real Edge browser: BASE, fixed stress, comparison, adapted stress, save/reopen, extension,
  invalid input, archive download and mobile layout. Reproduce with `tests/ui_smoke.cjs`.
- UI-export KPIs equal a direct `simulate()` call. An extracted UI archive passes CLI `verify`.
- The working application uses local assets and the existing engine, with no extra web dependency.
- R3's EXP-07–10 analyses are integrated. R2 selected P2z, added the disclosed MCDA,
  contract/stakeholder allocation, verified self-found sources and completed the management note.
  Alternative-strategy Monte Carlo, geopolitics and post-2040 economics remain future research.

## GitVerse publication status

**Not published.** The configured origin is GitHub (`pmixay/hackathon-1809`); no GitVerse
repository URL or publication credentials were supplied. Local preparation does not prove
delivery to the organizer. Do not mark this final step complete until the team publishes and
checks access from another account.

The release owner should review the diff, use the team's `feat/r4-...` branch/PR convention,
run the checks below, and publish the approved branch to the team's GitVerse repository.
Keep the GitHub origin intact. Once a destination exists:

```bash
git remote add gitverse <team-GitVerse-repository-URL>
git push gitverse <approved-release-branch>:main
```

No push is performed by the local UI or delivery scripts. Credentials belong in the team's
credential manager, never the repository. Include code, `data/`, `configs/`, `results/`, `tests/`
and `docs/`; exclude `.venv/`, `build/`, local caches and credentials.

## Release verification order

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
python -m terraplan control-cases
python -m terraplan ui
python -m terraplan verify results/alternatives/P2z_earth_new_zbo_BASE
python -m terraplan verify results/stress/P2z_earth_new_zbo_adapted_MANDATORY_STRESS
python tests/independent_recalc.py results/alternatives/P2z_earth_new_zbo_BASE
python experiments/run_mcda.py
```

Follow the operator-guide demonstration in order: BASE, mandatory stress, additional tests,
comparison and export. Ensure the README command works from a clean checkout and the jury
can access the GitVerse repository and the presentation. Strategy changes require updating
the source experiments, then regenerating result-derived presentation figures.

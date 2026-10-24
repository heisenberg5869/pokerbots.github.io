# Pokerbots Curriculum Implementation TODO

This checklist translates `CURRICULUM_PLAN.md` into implementation work for the repository.

## Current baseline

- Modules 00–07 have partial or substantial material.
- Core Kuhn, Leduc, CFR, MCCFR, regret-matching, hand evaluation, abstraction, and push/fold code exists.
- Modules 08–14 are incomplete; several recently added files are still experimental.
- The repository currently needs editable-install setup before tests can run:

```powershell
pip install -e ".[dev]"
pytest
```

## Priority 1: Finish the shared foundation

- [ ] Build a reusable browser widget layer for the planned widgets W1–W18.
- [ ] Implement the first shared widgets: game-tree explorer, strategy/heatmap, exploitability plot, regret bars, quiz, glossary, and simplex plot.
- [ ] Standardize demo layout: prediction prompt, controls, canvas, live readout, “Show the math”, reset, share link, notebook link, and provenance.
- [ ] Add responsive desktop/mobile layouts, keyboard controls, focus states, reduced-motion support, dark/light themes, and WCAG AA contrast.
- [ ] Add “view as table” output for every chart.
- [ ] Build the demo-data pipeline with fixed seeds, compressed artifacts, checksums, and a manifest containing commit, seed, iterations, and runtime.
- [ ] Add CI jobs for unit tests, property tests, notebooks, docs/link checks, accessibility, and demo-data validation.
- [ ] Add the progress tracker, prerequisite map, recurring-spot links, verified-numbers page, and shared hover glossary.

## Priority 2: Complete Modules 03–07

### Module 03 – Leduc

- [ ] Finish configurable CFR/CFR+ variants and cross-checks.
- [ ] Add complete convergence, belief, reach, and play/review demos.
- [ ] Add ground-truth game value and exploitability tests.

### Module 04 – Expanded Leduc, river poker, MCCFR

- [ ] Implement expanded Leduc and river-poker game models.
- [ ] Finish chance-sampled, external-sampled, and outcome-sampled MCCFR.
- [ ] Add vectorized/range-based interfaces and consistency tests against exact small games.
- [ ] Finish seven-card evaluation integration and river P0 interactive.
- [ ] Add variance and unbiasedness benchmarks.

### Module 05 – Limit Hold’em

- [ ] Implement the complete multi-street Limit Hold’em game.
- [ ] Add five- and seven-card evaluator cross-checks.
- [ ] Implement range equity and bucketed solver data generation.
- [ ] Add bot interface and play/review table.
- [ ] Finish all P0 demos and ground-truth tests.

### Module 06 – Abstraction and endgame solving

- [ ] Implement card bucketing and bucket translation.
- [ ] Implement safe and nested subgame solving.
- [ ] Add abstraction-loss metrics and endgame-safety tests.
- [ ] Finish abstraction, translation, bucket, and safe-solve demos.

### Module 07 – Heads-Up No-Limit

- [ ] Complete multi-street no-limit Hold’em mechanics.
- [ ] Implement continual re-solving/reduced-game solving.
- [ ] Add local best response and variance-reduced match evaluation.
- [ ] Build flop strategy library and precomputed strategy data.
- [ ] Add bot arena v1 and finish remaining no-limit demos.

## Priority 3: Implement Modules 08–12

### Module 08 – Deep CFR

- [ ] Complete neural advantage/regret training.
- [ ] Integrate reservoir sampling and strategy networks.
- [ ] Add tabular-vs-neural exploitability tests on Leduc.
- [ ] Add training notebook and convergence demo.

### Module 09 – Value networks and search

- [ ] Implement public-belief-state representations.
- [ ] Implement depth-limited search and self-play.
- [ ] Add value-network error, zero-sum consistency, and solved-subgame tests.
- [ ] Add notebook and search/value-network demos.

### Module 10 – Pot-Limit Omaha

- [ ] Implement complete Omaha game rules and pot-limit betting.
- [ ] Validate Omaha hand evaluation against brute-force enumeration.
- [ ] Add exact and Monte Carlo equity estimation.
- [ ] Add range tables, combinatorics explanations, notebook, and demos.

### Module 11 – Multiplayer

- [ ] Implement N-player Kuhn/Leduc and multiplayer no-limit foundations.
- [ ] Support general payoff/player interfaces beyond two-player zero-sum games.
- [ ] Add self-play population evaluation, round-robin leagues, ratings, and ICM.
- [ ] Add multiplayer tests, notebook, and demos.

### Module 12 – Opponent modelling

- [ ] Implement frequency/Bayesian opponent models.
- [ ] Implement safe exploitation and restricted-response frontiers.
- [ ] Add conjugate-update tests and profit-vs-exploitability experiments.
- [ ] Add notebook, interactive lab, and bot-arena integration.

## Priority 4: Complete Modules 13–14

### Module 13 – Custom variants

- [ ] Finish the rules-as-configuration framework.
- [ ] Implement Sneak Peek Hold’em, peek mechanics, auctions, and altered information.
- [ ] Add automatic observation-history information sets.
- [ ] Add invariants over large random simulations.
- [ ] Add rules builder, information timeline, variant card, and transfer-test demos.
- [ ] Verify that standard Hold’em is reproduced when variant options are disabled.

### Module 14 – Case studies and open problems

- [ ] Add curated case-study data for Cepheus, DeepStack, Libratus, Pluribus, and ReBeL.
- [ ] Build the solved-status timeline and technique landscape.
- [ ] Add technique-selection quiz and paper-anatomy cards.
- [ ] Add open-problems board, compute comparison, reading guide, and capstone rubric.

## Repository and tooling gaps

- [ ] Add `arena/` for bot interfaces, matches, tournaments, ratings, and leaderboard support.
- [ ] Add `benchmarks/` for convergence, runtime, memory, and evaluator comparisons.
- [ ] Add `papers/` for reading lists and one-page paper summaries.
- [ ] Add `data/` or release-asset handling for large precomputed artifacts.
- [ ] Complete `pokerbot/viz/` plotting/widget helpers.
- [ ] Ensure all new modules are exported through package `__init__.py` files.
- [ ] Add tests for every ground-truth anchor in the curriculum plan.
- [ ] Make notebooks execute from a clean environment.
- [ ] Update `README.md` and `docs/roadmap.md` after each completed milestone.

## Definition of done for each module

- [ ] All P0 interactives work on desktop and mobile.
- [ ] Keyboard, accessibility, dark-theme, and reduced-motion behavior works.
- [ ] Notebook runs top-to-bottom in a clean environment.
- [ ] Quantitative claims are listed on the verified-numbers page.
- [ ] Library tests cover the module’s ground-truth anchors.
- [ ] The page follows the nine-section curriculum template.
- [ ] The page includes misconceptions, exercises, checkpoint, and “Break it” lab.
- [ ] Prerequisite, next-module, and glossary links are complete.
- [ ] Another person can complete the module without assistance.

## Recommended execution order

1. Install the package and make the existing test suite pass.
2. Finish shared widgets and the demo-data/CI pipeline.
3. Complete Modules 03–04 and their verification data.
4. Complete Modules 05–07 and bot arena v1.
5. Implement Deep CFR and value-network search.
6. Implement Omaha, multiplayer, and opponent modelling.
7. Finish custom variants and case studies.
8. Perform accessibility, documentation, notebook, and clean-environment QA.


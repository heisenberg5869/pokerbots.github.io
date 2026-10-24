# Post-Module-07 Website Development Plan

## Purpose

The curriculum plan is broad, but the website currently stops being interactive after Module 07. Modules 08–14 mostly render as text pages with TODO placeholders and no browser labs.

This plan is for the implementation agent. The goal is to make every module after Module 07 a real teaching experience with visible, working, testable browser interactives—not just a completed Python file or a written page.

## Audit findings

- Interactive demos currently exist mainly for Modules 00–07.
- `docs/demos/` has no Module 08, 09, 10, 11, 12, 13, or 14 demo pages.
- `docs/modules/08_deep_cfr.md` through `docs/modules/13_variants.md` still contain TODO placeholders for intuition, algorithm, interactive lab, verification, exercises, checkpoints, and further reading.
- Module 14 has prose structure but no interactive case-study or open-problem experience.
- `mkdocs.yml` links Modules 08–14 as ordinary documentation pages, without interactive lab entries.
- The generated `site/` directory is not the source of truth. Edit `docs/`, then run the documentation build and verify the generated site.
- Existing Module 07 demos should be treated as the visual and interaction baseline.
- Every new demo must work on a static GitHub Pages deployment: no server, database, API, or runtime Python dependency may be required.

## Non-negotiable implementation rules

- Each module must have at least one prominent interactive lab above the fold or directly after the first explanation.
- Each lab must have a clear learning objective and a one-line prediction question.
- Every control must update a visible result; placeholder buttons and fake charts are not acceptable.
- Use deterministic precomputed data for expensive algorithms and small live calculations for toy examples.
- Include a “Show the math” or “Explain this result” panel in every lab.
- Include a “Break it” experiment that intentionally demonstrates a limitation.
- Add reset, presets, shareable URL state, keyboard support, responsive layout, and accessible text summaries.
- Every chart must provide a table view or a readable numeric summary.
- Every displayed number must have a source, seed, iteration count, or explicit “illustrative” label.
- Do not hide an unfinished lab behind prose. Mark it as incomplete in the roadmap until the full acceptance checklist passes.
- Keep demo JavaScript self-contained or use a small shared library under `docs/javascripts/`.
- Do not duplicate large CSS and interaction logic in every demo. Extract shared components.

## Shared website infrastructure to build first

### A. Demo shell

- [ ] Create a shared demo shell with title, objective, difficulty, estimated time, module tag, and progress indicator.
- [ ] Create a standard three-panel layout: controls, visualization, explanation/readout.
- [ ] Add a prediction card that records the learner’s answer before revealing the result.
- [ ] Add “Show the math”, “Break it”, “Reset”, “Share”, and “View data” controls.
- [ ] Add a source/provenance footer with dataset version, seed, algorithm, and commit.
- [ ] Add a consistent empty/loading/error state.
- [ ] Add a “What should I notice?” prompt after every meaningful interaction.

### B. Shared visual components

- [ ] Strategy probability bars.
- [ ] Regret and advantage bars.
- [ ] Exploitability/convergence line chart.
- [ ] Loss/metric training chart.
- [ ] Range matrix and combo-count display.
- [ ] Card and board renderer.
- [ ] Action timeline and game-tree node renderer.
- [ ] Belief/range distribution display.
- [ ] Sankey-style range-flow display.
- [ ] Payoff matrix and simplex/triangle plot.
- [ ] Network architecture diagram.
- [ ] Slider with numeric input and preset buttons.
- [ ] Accessible data-table fallback for all charts.

### C. Shared behavior and accessibility

- [ ] Keyboard navigation for every control.
- [ ] Visible focus states.
- [ ] ARIA labels and live-region summaries.
- [ ] Light and dark themes.
- [ ] Reduced-motion mode.
- [ ] Mobile layout at narrow widths.
- [ ] No information conveyed by color alone.
- [ ] Consistent player colors and action labels across all modules.
- [ ] URL serialization for lab state.
- [ ] “Copy share link” behavior with graceful fallback.

### D. Data and build pipeline

- [ ] Create `docs/demos/data/` or an equivalent structured data location.
- [ ] Create a manifest format containing dataset name, version, commit, seed, iterations, runtime, and expected metrics.
- [ ] Add scripts that generate static JSON for training curves, strategies, ranges, and benchmark tables.
- [ ] Compress large datasets and lazy-load them only when their demo opens.
- [ ] Validate JSON schemas during CI.
- [ ] Add a size budget for each demo and dataset.
- [ ] Add a docs build step that verifies every demo link and data URL.
- [ ] Add a smoke test that loads each demo and confirms its main controls exist.

## Module 08 — Deep CFR website work

### Page rewrite

- [ ] Replace all TODO sections in `docs/modules/08_deep_cfr.md`.
- [ ] Explain the failure of tabular CFR using a visual memory/table-size example.
- [ ] Explain advantage networks, strategy networks, regret targets, and reservoir sampling in plain language.
- [ ] Add pseudocode and map each pseudocode step to repository code.
- [ ] Add a checkpoint list, misconception box, exercises, and further reading.

### Browser labs

- [ ] `deep-cfr-training-lab.html`: choose game, iterations, network width, reservoir size, and learning rate; show loss, exploitability proxy, average strategy, and training progress.
- [ ] `deep-cfr-input-explorer.html`: inspect the feature vector for a selected information state and highlight which features change after an action.
- [ ] `deep-cfr-reservoir-lab.html`: compare uniform reservoir sampling with a biased buffer; show sample-age and state-frequency histograms.
- [ ] `deep-cfr-strategy-compare.html`: compare tabular CFR, Deep CFR, and a deliberately under-trained network.
- [ ] `deep-cfr-failure-lab.html`: reduce network capacity or reservoir size and show generalization failure.

### Data and verification

- [ ] Generate fixed-seed Leduc training runs.
- [ ] Store loss, exploitability, strategy distance, and reservoir statistics.
- [ ] Add a table showing expected qualitative behavior rather than pretending neural results are exact.
- [ ] Link each displayed curve to its generated dataset.

## Module 09 — Value Networks and Search website work

### Page rewrite

- [ ] Replace TODO sections in `docs/modules/09_value_nets_search.md`.
- [ ] Explain public belief states with a hidden-card example.
- [ ] Explain depth-limited search and why a value network replaces the rest of the tree.
- [ ] Explain self-play and value-target generation.
- [ ] Add failure modes: biased beliefs, value error, shallow search, and distribution shift.

### Browser labs

- [ ] `belief-state-explorer.html`: select public board, action history, and player; display the remaining private-hand distribution.
- [ ] `search-tree-lab.html`: adjust search depth and branching factor; show expanded nodes, leaf states, and estimated value.
- [ ] `value-network-lab.html`: compare network value with exact value on a small game; show absolute error by state.
- [ ] `search-vs-network.html`: compare shallow search, value-only evaluation, and deeper search on the same position.
- [ ] `belief-update-lab.html`: apply actions and visualize how the public belief changes.
- [ ] `search-failure-lab.html`: inject value error and show the selected action changing.

### Data and verification

- [ ] Produce solved toy-game state/value data.
- [ ] Add zero-sum consistency checks.
- [ ] Add value error distributions and calibration plots.
- [ ] Add a clear distinction between exact values and learned estimates.

## Module 10 — Pot-Limit Omaha website work

### Page rewrite

- [ ] Replace TODO sections in `docs/modules/10_plo.md`.
- [ ] Explain the exactly-two-hole-cards rule visually.
- [ ] Explain why four hole cards create combinatorial growth.
- [ ] Explain pot-limit bet sizing and equity estimation.

### Browser labs

- [ ] `plo-hand-builder.html`: deal/select four hole cards and a board; enumerate legal two-hole/two-board combinations.
- [ ] `plo-combination-counter.html`: compare Hold’em and Omaha hand-combination counts as hole-card count changes.
- [ ] `plo-equity-lab.html`: run exact enumeration for small cases and Monte Carlo for larger cases.
- [ ] `plo-nut-potential.html`: show current made hand, draws, nut potential, and redraw risk.
- [ ] `plo-pot-limit-tree.html`: adjust pot, stack, and bet size; show legal pot-limit actions and tree size.
- [ ] `plo-range-equity.html`: compare a hand against a range and show equity distribution.
- [ ] `plo-failure-lab.html`: contrast Hold’em-style evaluation with correct Omaha evaluation.

### Data and verification

- [ ] Add known Omaha matchup fixtures.
- [ ] Add exact-vs-Monte-Carlo convergence curves.
- [ ] Add brute-force evaluator comparison tables.
- [ ] Make all four-hole-card and exactly-two-card constraints visible in the UI.

## Module 11 — Multiplayer website work

### Page rewrite

- [ ] Replace TODO sections in `docs/modules/11_multiplayer.md`.
- [ ] Explain why two-player zero-sum guarantees do not transfer directly.
- [ ] Explain multiple equilibria, coalition incentives, population evaluation, ratings, and ICM.

### Browser labs

- [ ] `multiplayer-table.html`: configure player count, stacks, positions, and action history.
- [ ] `multiplayer-payoffs.html`: compare chip EV, tournament equity, and ICM equity.
- [ ] `nplayer-game-tree.html`: inspect a small N-player tree with player-specific payoffs.
- [ ] `population-arena.html`: select bots and run a deterministic round-robin summary.
- [ ] `rating-lab.html`: simulate matches and show rating/uncertainty updates.
- [ ] `equilibrium-lab.html`: show multiple equilibria in a small multiplayer game.
- [ ] `multiplayer-failure-lab.html`: show why heads-up exploitability is insufficient for a multiplayer population.

### Data and verification

- [ ] Add known small multiplayer game outcomes.
- [ ] Add ICM hand calculations and table views.
- [ ] Add confidence intervals to match results.
- [ ] Ensure UI language does not call multiplayer results “exact exploitability” when it is only a proxy.

## Module 12 — Opponent Modelling website work

### Page rewrite

- [ ] Replace TODO sections in `docs/modules/12_opponent_modelling.md`.
- [ ] Explain the difference between equilibrium play, exploitation, and overfitting.
- [ ] Explain frequency models, Bayesian updates, uncertainty, and safe exploitation.

### Browser labs

- [ ] `opponent-profile-lab.html`: adjust observed fold/call/raise frequencies and infer an opponent profile.
- [ ] `bayesian-opponent-lab.html`: update a prior after observations and display posterior uncertainty.
- [ ] `exploitability-profit-frontier.html`: show the trade-off between exploitative profit and safety.
- [ ] `observation-budget-lab.html`: show how many observations are needed before adaptation becomes reliable.
- [ ] `model-mismatch-lab.html`: change the opponent’s behavior after training and show adaptation failure.
- [ ] `safe-exploitation-lab.html`: compare aggressive exploitation against a conservative restricted response.
- [ ] `opponent-review-table.html`: replay decisions and show model belief, chosen action, and EV impact.

### Data and verification

- [ ] Add synthetic opponent fixtures with known distributions.
- [ ] Add Bayesian closed-form checks.
- [ ] Add confidence intervals and calibration displays.
- [ ] Clearly label simulated observations and avoid implying live opponent tracking.

## Module 13 — Custom Variants website work

### Page rewrite

- [ ] Replace TODO sections in `docs/modules/13_variants.md`.
- [ ] Explain rules as configuration and observations as information structure.
- [ ] Explain why changing one rule can change the game tree and equilibrium.

### Browser labs

- [ ] `variant-rules-builder.html`: configure deck, hole cards, streets, betting, peek rules, auctions, and player count.
- [ ] `variant-card.html`: generate a readable rule card from the configuration.
- [ ] `variant-tree-estimator.html`: estimate states, information sets, actions, and memory.
- [ ] `variant-information-timeline.html`: show what each player knows after every event.
- [ ] `sneak-peek-lab.html`: play a small Sneak Peek Hold’em hand and expose information asymmetry.
- [ ] `variant-solver-lab.html`: solve a tiny configured variant live or load a precomputed solution.
- [ ] `variant-transfer-lab.html`: compare a bot trained on standard Hold’em with performance on a modified variant.
- [ ] `variant-break-lab.html`: toggle one rule and show invariant/test failures or strategy changes.

### Data and verification

- [ ] Add schema validation for every variant configuration.
- [ ] Add random-play invariant tests.
- [ ] Verify standard Hold’em reproduction with all optional rules disabled.
- [ ] Make the generated rule card shareable by URL.

## Module 14 — Case studies and open problems website work

### Page rewrite

- [ ] Turn `docs/modules/14_case_studies.md` into a complete capstone page.
- [ ] Add structured case-study cards: game, players, method, abstraction, guarantees, evaluation, limitations, and lesson.
- [ ] Distinguish “solved”, “strongly solved”, “approximately solved”, “superhuman”, and “open”.

### Browser labs

- [ ] `solved-ladder.html`: place systems/games on a solved-status ladder.
- [ ] `technique-selector.html`: answer questions about players, information, game size, and objective; recommend a method.
- [ ] `paper-anatomy.html`: inspect landmark papers by problem, method, data, evaluation, and limitation.
- [ ] `compute-comparison.html`: compare approximate compute budgets on a log scale with citations.
- [ ] `open-problems-board.html`: filter problems by difficulty, prerequisites, and suggested experiment.
- [ ] `capstone-planner.html`: select a custom variant and generate an implementation/evaluation checklist.
- [ ] `case-study-breakdown.html`: click through a full system from game definition to bot evaluation.

### Data and verification

- [ ] Add citations and verification dates for all quantitative claims.
- [ ] Add downloadable structured case-study data.
- [ ] Add a capstone rubric and example submissions.

## Navigation and publishing work

- [ ] Add an “Interactive labs” subsection under Modules 08–14 in `mkdocs.yml`.
- [ ] Add “Lab available”, “Lab in progress”, and “Text only” status badges to module pages.
- [ ] Add a website-wide interactive-lab index.
- [ ] Add next/previous module links and links from prose to each lab.
- [ ] Update the home page to show actual post-07 progress rather than implying all modules are equally developed.
- [ ] Update `docs/roadmap.md` only when a lab passes its acceptance criteria.
- [ ] Rebuild `site/` and verify the deployed paths after every module.
- [ ] Check direct URLs to every demo, including refresh and back-button behavior.

## Testing and QA checklist

### Automated

- [ ] Unit tests for every calculation used by a demo.
- [ ] JSON schema tests for every generated dataset.
- [ ] Demo smoke tests for page load and primary control interaction.
- [ ] Link checker for all module-to-demo links.
- [ ] Notebook execution tests for Modules 08–14.
- [ ] Accessibility checks for labels, contrast, keyboard navigation, and live regions.
- [ ] Mobile viewport smoke tests.
- [ ] Build-size and load-time checks.

### Manual

- [ ] A learner can answer the prediction question before touching controls.
- [ ] Changing each control changes the visualization or readout.
- [ ] Reset returns to a documented default preset.
- [ ] Share URL reproduces the same state.
- [ ] “Show the math” explains the currently selected result.
- [ ] “Break it” visibly demonstrates the documented limitation.
- [ ] A screen-reader user receives a meaningful result summary.
- [ ] No lab depends on console errors or network services.

## Recommended delivery sequence

1. Build the shared demo shell and component library.
2. Build one complete Module 08 lab as the reference implementation.
3. Build the remaining Module 08 labs and rewrite its page.
4. Build Module 09 labs and its static datasets.
5. Build Modules 10 and 11, reusing the card, range, table, chart, and arena components.
6. Build Module 12 using the belief/update/chart components.
7. Build Module 13 using the rules builder, tree estimator, and timeline components.
8. Build Module 14 using structured case-study data and the capstone planner.
9. Update navigation, roadmap, home page, and generated site.
10. Run the complete automated and manual QA checklist.

## Definition of done

The post-Module-07 website is complete only when:

- Modules 08–14 each have a non-placeholder lesson page.
- Every module has at least three working browser labs.
- Each lab has real state-changing interactions, explanations, and accessible data output.
- Every lab is linked from navigation and from the relevant lesson text.
- Expensive results are reproducible from checked-in scripts and manifest-backed data.
- The website builds cleanly and all demos work from their deployed static URLs.
- The roadmap accurately reflects what is genuinely implemented.


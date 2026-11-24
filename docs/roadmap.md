# Roadmap

Track the lessons and library work below or [browse the available labs](labs.md).

| # | Module | Status | Library code | Tests | Notebook | Web demo |
|---|---|---|---|---|---|---|
| 00 | Prerequisites | draft | ✅ probability, card removal, Bayes, matrix solver | ✅ | ✅ executed notebook | ✅ five foundations labs + quiz |
| 01 | Kuhn Poker | in progress | ✅ engine, CFR, exploitability | ✅ | ✅ | ✅ tree, play + EV review, equilibrium, exploitability, CFR |
| 02 | Regret Matching | in progress | ✅ `RegretMatcher`, ✅ `matrix_games` (RM, RM+, Hedge) | ✅ | ✅ | ✅ strategy chart, regret bars, simplex, switch test, CFR bridge |
| 03 | Leduc Hold'em | in progress | ✅ engine, configurable CFR variants | ✅ rules-level | ✅ notebook | ✅ tree, heatmap, beliefs, reach, race, play |
| 04 | Expanded Leduc + MCCFR | in progress | ✅ chance / external MCCFR, sampled estimators, 5-/7-card evaluator | ✅ | ✅ executed notebook | ✅ sampling, variance, scale, bluff labs; river P0 pending |
| 05 | Limit Hold'em | in progress | ✅ evaluator, range equity, betting-round mechanics | ✅ | ✅ notebook | ✅ six P0 lab concepts; solver data and full game pending |
| 06 | Abstraction & Endgame | in progress | ✅ histogram EMD, k-medoids, action translation | ✅ | ✅ notebook | ✅ synthetic abstraction, translation, safe-solve concept |
| 07 | Heads-Up No-Limit | in progress | No-limit betting, push/fold, match evaluation, local best response | ✅ | ✅ push/fold notebook | Push/fold explorer |
| 08 | Deep CFR | draft | Deep CFR and Single Deep CFR trainers, networks, reservoirs | ✅ | — | Training, reservoirs, strategy comparison |
| 09 | Value Nets & Search | in progress | Value networks and depth-limited search | ✅ | — | Belief states, search tree, value network |
| 10 | Pot-Limit Omaha | in progress | Omaha hand evaluation and equity | ✅ | — | Hand builder, combinations, equity, failure cases |
| 11 | Multiplayer | in progress | Multiplayer game and round-robin evaluation | ✅ | — | Payoffs, game trees, population arena |
| 12 | Opponent Modelling | in progress | Frequency models and safe exploitation | ✅ | — | Profiles, Bayesian updates, exploitability and profit |
| 13 | Custom Variants | in progress | Variant framework and Sneak Peek Hold’em | ✅ | — | Rules builder, variant card, tree estimator |
| 14 | Case Studies | in progress | — | — | ✅ | Solved ladder, technique selector, compute comparison |

## Phases

- **Phase 0: skeleton** ✅ repo layout, notation, CI, docs site, module template, exact exploitability
- **Phase 1: prove the template.** Module 00 is drafted with its P0 browser labs; Module 01 and 02 have P0 labs. Shared-widget extraction and independent learner review remain.
- **Phase 2: small solvable games.** Leduc's core labs are present; expanded Leduc, the river solver, and remaining MCCFR P0 work are in progress.
- **Phase 3 (Hold’em and abstraction).** See the [Module 07 implementation plan](modules/07_nolimit_plan.md) for remaining no-limit solver and browser work.
- **Phase 4 (Neural solvers and the research frontier).** Modules 08–12 have lessons, library code, and browser labs. The [Deep CFR implementation plan](modules/08_deep_cfr_plan.md) tracks the original milestones.
- **Phase 5 (Capstone).** The variant framework, Sneak Peek Hold’em, and case studies have lessons and labs.

## Library plan

| Package | Contents (done ✅ / planned) |
|---|---|
| `games/` | ✅ `base`, ✅ `kuhn`, ✅ `leduc`, ✅ limit betting-round mechanics, ✅ no-limit betting round + sizing; planned: full limit hand, expanded leduc, plo, variants |
| `solvers/` | ✅ `regret_matching`, ✅ `matrix_games`, ✅ `cfr`, ✅ chance/external `mccfr`, ✅ `push_fold`; planned: deep_cfr, resolve |
| `eval/` | ✅ `exploitability`, ✅ `hand_eval`, ✅ `equity`; planned: local best response, tournaments |
| `abstraction/` | ✅ histogram EMD, k-medoids, action translation; planned: card buckets, safe re-solving |
| `viz/` | planned: plotting and widget helpers |

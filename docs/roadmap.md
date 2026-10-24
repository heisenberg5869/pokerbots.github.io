# Roadmap

Status values: **planned → outline → in progress → draft → reviewed → done**

| # | Module | Status | Library code | Tests | Notebook | Web demo |
|---|---|---|---|---|---|---|
| 00 | Prerequisites | draft | ✅ probability, card removal, Bayes, matrix solver | ✅ | ✅ executed notebook | ✅ five foundations labs + quiz |
| 01 | Kuhn Poker | in progress | ✅ engine, CFR, exploitability | ✅ | ✅ | ✅ tree, play + EV review, equilibrium, exploitability, CFR |
| 02 | Regret Matching | in progress | ✅ `RegretMatcher`, ✅ `matrix_games` (RM, RM+, Hedge) | ✅ | ✅ | ✅ strategy chart, regret bars, simplex, switch test, CFR bridge |
| 03 | Leduc Hold'em | in progress | ✅ engine, configurable CFR variants | ✅ rules-level | ✅ notebook | ✅ tree, heatmap, beliefs, reach, race, play |
| 04 | Expanded Leduc + MCCFR | in progress | ✅ chance / external MCCFR, sampled estimators, 5-/7-card evaluator | ✅ | ✅ executed notebook | ✅ sampling, variance, scale, bluff labs; river P0 pending |
| 05 | Limit Hold'em | in progress | ✅ evaluator, range equity, betting-round mechanics | ✅ | ✅ notebook | ✅ six P0 lab concepts; solver data and full game pending |
| 06 | Abstraction & Endgame | in progress | ✅ histogram EMD, k-medoids, action translation | ✅ | ✅ notebook | ✅ synthetic abstraction, translation, safe-solve concept |
| 07 | Heads-Up No-Limit | planned | — | — | — | — |
| 08 | Deep CFR | planned | — | — | — | — |
| 09 | Value Nets & Search | planned | — | — | — | — |
| 10 | Pot-Limit Omaha | planned | — | — | — | — |
| 11 | Multiplayer | planned | — | — | — | — |
| 12 | Opponent Modelling | planned | — | — | — | — |
| 13 | Custom Variants | planned | — | — | — | — |
| 14 | Case Studies | planned | — | — | — | — |

## Phases

- **Phase 0: skeleton** ✅ repo layout, notation, CI, docs site, module template, exact exploitability
- **Phase 1: prove the template.** Module 00 is drafted with its P0 browser labs; Module 01 and 02 have P0 labs. Shared-widget extraction and independent learner review remain.
- **Phase 2: small solvable games.** Leduc's core labs are present; expanded Leduc, the river solver, and remaining MCCFR P0 work are in progress.
- **Phase 3: real poker.** Hand evaluation, range equity, a single-round Limit betting engine, and six P0 lab concepts are started; the four-street Limit game, trained abstracted strategy, abstraction, endgame solving, and heads-up No-Limit remain.
- **Phase 4: neural and frontier.** Deep CFR, value nets, PLO, multiplayer, opponent modelling
- **Phase 5: capstone.** variant framework, Sneak Peek Hold'em, case studies

## Library plan

| Package | Contents (done ✅ / planned) |
|---|---|
| `games/` | ✅ `base`, ✅ `kuhn`, ✅ `leduc`, ✅ limit betting-round mechanics; planned: full limit hand, expanded leduc, nolimit, plo, variants |
| `solvers/` | ✅ `regret_matching`, ✅ `matrix_games`, ✅ `cfr`, ✅ chance/external `mccfr`; planned: deep_cfr, resolve |
| `eval/` | ✅ `exploitability`, ✅ `hand_eval`, ✅ `equity`; planned: local best response, tournaments |
| `abstraction/` | ✅ histogram EMD, k-medoids, action translation; planned: card buckets, safe re-solving |
| `viz/` | planned: plotting and widget helpers |

# Roadmap

Status values: **planned → outline → in progress → draft → reviewed → done**

| # | Module | Status | Library code | Tests | Notebook | Web demo |
|---|---|---|---|---|---|---|
| 00 | Prerequisites | outline | — | — | — | — |
| 01 | Kuhn Poker | in progress | ✅ engine, CFR, exploitability | ✅ | ✅ | — |
| 02 | Regret Matching | draft | ✅ `RegretMatcher`, ✅ `matrix_games` (RM, RM+, Hedge) | ✅ | ✅ | ✅ RPS demo |
| 03 | Leduc Hold'em | in progress | ✅ engine, configurable CFR variants | ✅ rules-level | ✅ notebook | ✅ tree, heatmap, beliefs, reach, race, play |
| 04 | Expanded Leduc + MCCFR | planned | — | — | — | — |
| 05 | Limit Hold'em | planned | — | — | — | — |
| 06 | Abstraction & Endgame | planned | — | — | — | — |
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
- **Phase 1: prove the template.** Module 01 ✅ and 02 (draft) done; finish Module 00 (prerequisites), then revise the template before replicating it
- **Phase 2: small solvable games.** Leduc, CFR+, expanded Leduc, MCCFR
- **Phase 3: real poker.** hand evaluator, Limit, abstraction, endgame solving, heads-up No-Limit
- **Phase 4: neural and frontier.** Deep CFR, value nets, PLO, multiplayer, opponent modelling
- **Phase 5: capstone.** variant framework, Sneak Peek Hold'em, case studies

## Library plan

| Package | Contents (done ✅ / planned) |
|---|---|
| `games/` | ✅ `base`, ✅ `kuhn`; planned: leduc, limit, nolimit, plo, variants |
| `solvers/` | ✅ `regret_matching`, ✅ `matrix_games`, ✅ `cfr`; planned: cfr_plus, mccfr, deep_cfr, resolve |
| `eval/` | ✅ `exploitability` (exact best response); planned: hand_eval, local best response, tournaments |
| `abstraction/` | planned: card buckets, action grids |
| `viz/` | planned: plotting and widget helpers |

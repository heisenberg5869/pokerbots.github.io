# pokerbots

**Learn to solve poker, one concept at a time — from a 3-card toy game to games that are still open research problems.**

This repo is a hands-on curriculum *and* a working code library. Every module explains one idea from scratch
(intuition → math → code → interactive demo → verification → "where does this break?"), and each module's failure
motivates the next. By the end you will have built solvers for Kuhn, Leduc, Limit, No-Limit, Omaha, multiplayer
games and your own custom variants.

> **Status:** early. Modules 00–06 have solver material, lessons, notebooks and browser labs; Module 07 now has a push/fold solver, single-street no-limit betting mechanics, and a push/fold explorer lab. Its larger deliverables — continual re-solving, the match harness, and the flop library — are still in progress. Per-module detail is in [`docs/roadmap.md`](docs/roadmap.md).

## The path

| # | Module | Level | You will learn |
|---|--------|-------|----------------|
| 00 | [Prerequisites](docs/modules/00_prereqs.md) | Beginner | EV, normal-form games, Nash, minimax, extensive form, LP |
| 01 | [Kuhn Poker](docs/modules/01_kuhn.md) | Beginner | game trees, information sets, mixed strategies, vanilla CFR, exploitability |
| 02 | [Regret Matching & No-Regret Learning](docs/modules/02_regret_matching.md) | Beginner | regret, average strategy, convergence, why CFR works |
| 03 | [Leduc Hold'em](docs/modules/03_leduc.md) | Intermediate | chance nodes, public cards, beliefs, CFR vs CFR+ |
| 04 | [Expanded Leduc / River Poker + MCCFR](docs/modules/04_mccfr.md) | Intermediate | sampling, variance reduction, scaling |
| 05 | [Limit Texas Hold'em](docs/modules/05_limit_holdem.md) | Intermediate | hand evaluation, betting rounds, ranges, abstraction |
| 06 | [Abstraction & Endgame Solving](docs/modules/06_abstraction_endgame.md) | Advanced | bucketing, action abstraction, safe subgame solving |
| 07 | [Heads-Up No-Limit](docs/modules/07_nolimit.md) | Advanced | arbitrary bet sizes, continual re-solving, public belief reasoning |
| 08 | [Deep CFR](docs/modules/08_deep_cfr.md) | Advanced | neural function approximation for regrets |
| 09 | [Value Networks & Search](docs/modules/09_value_nets_search.md) | Advanced | public belief states, depth-limited solving (ReBeL-style) |
| 10 | [Pot-Limit Omaha](docs/modules/10_plo.md) | Advanced | combinatorial explosion, equity estimation, range evaluation |
| 11 | [Multiplayer No-Limit](docs/modules/11_multiplayer.md) | Research | non-zero-sum games, self-play, population evaluation |
| 12 | [Opponent Modelling & Exploitation](docs/modules/12_opponent_modelling.md) | Advanced | safe exploitation, adaptation, the exploitability/profit tradeoff |
| 13 | [Custom Variants (Sneak Peek Hold'em…)](docs/modules/13_variants.md) | Research | modelling new rules, auctions, altered information |
| 14 | [Case Studies & Open Problems](docs/modules/14_case_studies.md) | Research | Cepheus, DeepStack, Libratus, Pluribus, ReBeL; what "solved" really means |

## Quick start

```bash
git clone https://github.com/heisenberg5869/pokerbots.github.io.git
cd pokerbots.github.io
pip install -e ".[dev]"
pytest                          # verifies the Kuhn solver against the known Nash equilibrium
python -m pokerbot.solvers.cfr  # trains CFR on Kuhn and prints strategy + exploitability
```

Docs site (local): `pip install -e ".[docs]" && mkdocs serve`

## Layout

```
docs/          prose for every module, notation, glossary, roadmap, interactive demos (MkDocs site)
modules/       hands-on material per module: notebooks and exercises
pokerbot/      the shared library: games/, solvers/, eval/, abstraction/, viz/
tests/         correctness tests (known equilibria, cross-checks)
benchmarks/    convergence and speed experiments
papers/        reading list per module
```

## How every module is structured

1. Motivation — what the previous module could not do
2. Intuition first — pictures and tiny examples before formulas
3. Formal definition — notation from [`docs/notation.md`](docs/notation.md)
4. Algorithm — pseudocode, then a minimal implementation
5. Interactive lab
6. Verification — compare against a known answer
7. Exercises (recall / implement / extend)
8. Failure analysis — where it breaks, and how it scales
9. Further reading

## Principle: exploitability is the scoreboard

Every solver in this repo is judged by one number: **exploitability** — how much a perfect opponent can win
against your strategy. It is computed exactly (best response) on small games and estimated on large ones.

## License

Code: MIT. Written explanations: CC BY 4.0. See [`LICENSE`](LICENSE).

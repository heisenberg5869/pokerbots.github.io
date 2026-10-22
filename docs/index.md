# pokerbots

**Learn to solve poker, one concept at a time: from a 3-card toy game to games that are still open research problems.**

Every module explains one idea from scratch (intuition, math, code, interactive demo, verification, and "where does this break?"). The failure at the end of each module motivates the next.

## Start here

1. [00 Prerequisites](modules/00_prereqs.md): the game theory you need
2. [01 Kuhn Poker](modules/01_kuhn.md): your first solved game (working code + tests)
3. [02 Regret Matching](modules/02_regret_matching.md): why CFR works (with an interactive demo)

See the [Roadmap](roadmap.md) for status of every module, [Notation](notation.md) for symbols, and the [Glossary](glossary.md) for terms.

## The three levels of "solved"

| Level | Meaning | Example |
|---|---|---|
| Solved | exact equilibrium known or provably near-exact | Kuhn, Leduc, heads-up limit Hold'em (Cepheus) |
| Practically strong | beats top humans via abstraction + search, no equilibrium guarantee | heads-up no-limit (Libratus, DeepStack), 6-player (Pluribus) |
| Open | no guarantees, or exploitability cannot even be measured | multiplayer equilibrium, full-scale PLO, novel variants |

Each module says which level its game sits at and why.

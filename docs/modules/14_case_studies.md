# 14 — Case Studies & Open Problems

| Level | Prerequisites | Status |
|---|---|---|
| Research | all earlier | in progress |

## Motivation
The preceding modules build poker solvers from first principles. This module steps back and asks what the headline results (Cepheus, DeepStack, Libratus, Pluribus, ReBeL) actually achieved, how they relate, and what remains open.

## What you will learn
- The three senses of "solved" and which games fall where.
- How Cepheus, DeepStack, Libratus, Pluribus and ReBeL differ in method and scale.
- Open problems: multiplayer, evaluation at scale, abstraction quality, real-time search, variants.

## What you will build
A critical reading guide and a table classifying every game in this repo.

## Intuition first
A solver being "strong" is not the same as a game being "solved". Solving is a statement about the game value and strategy; strength is a statement about play against humans.

## Formal definition
- **Ultra-weakly solved**: game value known.
- **Weakly solved**: optimal strategy known for all states reachable under optimal play (e.g. Cepheus for heads-up limit hold'em).
- **Strongly solved**: optimal strategy for every state (rare, small games only).

## Case studies

| System | Game | Approach | Result |
|---|---|---|---|
| Cepheus | HU Limit Hold'em | CFR+ with abstraction? (exact-ish) | Weakly solved |
| DeepStack | HU No-Limit | Depth-limited search + value net | Beat pros |
| Libratus | HU No-Limit | Blueprint + subgame solving | Beat pros |
| Pluribus | 6-max No-Limit | Blueprint + real-time search | Beat pros |
| ReBeL | HU No-Limit / other | Self-play + search + value net (model-free-ish) | Strong play |

## Algorithm
No single algorithm; synthesis. Each system combines abstraction, search, and learning. See modules 06, 07, 08, 09.

## Interactive lab
Notebook stub in `modules/14_case_studies/`.

## Verification
Classify each game in repo (Kuhn, Leduc, push/fold) by solved-level.

## Exercises
- **Recall:** Distinguish weakly vs strongly solved.
- **Implement:** Add a row to the classification table for a new variant.
- **Extend:** Propose an open problem and a measurable experiment.

## Where this breaks
Human evaluation is noisy; "beat pros" is not a proof of optimality. Multiplayer equilibria are not unique and exploitability is ill-defined beyond 2 players.

## Checkpoint — you are done when…
- You can state the three solved levels and give an example.
- You can contrast DeepStack/Libratus/Pluribus/ReBeL.
- You can list three open problems with concrete experiments.

## Further reading
- Bowling et al. 2015 (Cepheus)
- Moravčík et al. 2017 (DeepStack)
- Brown & Sandholm 2018 (Libratus), 2019 (Pluribus)
- Brown et al. 2020 (ReBeL)
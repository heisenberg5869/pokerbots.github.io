# 11 · Multiplayer No-Limit Hold'em

| Level | Prerequisites | Status |
|---|---|---|
| Research | 07, 09 | in progress |

## Motivation
Everything so far assumed two players in a zero-sum game. Add a third player and the guarantees vanish: equilibria are not unique, not interchangeable, and computing one is hard even in small games. Module 11 shows exactly how the math breaks and what practitioners do instead.

## What you will learn
Why Nash equilibrium loses its meaning with 3+ players; non-zero-sum structure and collusion-like (kingmaking) effects; coarse correlated equilibria from self-play; the Pluribus blueprint-plus-search recipe; population-based evaluation, ratings with uncertainty, non-transitivity; ICM (chips ≠ money).

## What you will build
A 3-player toy game exposing equilibrium multiplicity; a self-play league and rating harness; an ICM calculator.

## Intuition first
In heads-up zero-sum, any two equilibrium strategies are interchangeable: if Alice plays her part of eq A and Bob plays his part of eq B, the result is still an equilibrium. With three players this fails. Run a solver 50 times on three-player Kuhn with different seeds and you get different strategy profiles with different payoffs; swapping seats across runs can lose money. Equilibria are not a single answer anymore.

## Formal definition
- **Nash equilibrium (NE):** no player can gain by deviating alone. In 2-player zero-sum, all NE have the same value and are interchangeable.
- **Coarse correlated equilibrium (CCE):** a joint distribution over action profiles such that no player gains by ignoring the recommendation and playing a fixed action. No-regret self-play converges to CCE, a weaker concept.
- **ICM:** convert chip stacks to prize equity via the recursive formula: a player's ICM equity = sum over opponents of (their stack / total) × (equity if that opponent is eliminated first), with base case one player = whole prize.

## Algorithm
1. Represent an n-player extensive-form game with a list of payoffs per terminal.
2. For evaluation: round-robin league, compute win rates, fit a rating (Elo/Bradley-Terry) with uncertainty.
3. ICM: recursive prize-equity over stack distributions.

## Interactive lab
- `demos/multiplayer-payoffs.html` — chip vs ICM equity, three players.
- `demos/nplayer-game-tree.html` — n-player tree and equilibrium swap test.
- `demos/population-arena.html` — league ratings, non-transitive cycles.

## Verification
- ICM values match hand calculations for small prize structures.
- Rating system recovers known strengths of synthetic bots.

## Exercises
- **Recall:** Why is exploitability not meaningful for 3+ players?
- **Implement:** Build an ICM calculator for 4 players.
- **Extend:** Construct a non-transitive trio of bots and visualize the cycle.

## Where this breaks
A fixed equilibrium is unexploitable but not maximally profitable against actual opponents (Module 12).

## Checkpoint — you are done when…
- You can explain why NE loses meaning with 3+ players.
- You can compute ICM equity for a stack distribution.
- You can detect non-transitivity in a rating matrix.

## Further reading
Brown & Sandholm (2019) Pluribus; Daskalakis, Goldberg & Papadimitriou (2009); Balduzzi et al. (2018) Re-evaluating Evaluation.
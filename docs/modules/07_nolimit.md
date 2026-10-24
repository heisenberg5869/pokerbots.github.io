# 07 · Heads-Up No-Limit Texas Hold'em

| Level | Prerequisites | Status |
|---|---|---|
| Advanced | [05 Limit Hold'em](05_limit_holdem.md), [06 Abstraction and Endgame Solving](06_abstraction_endgame.md) | in progress |

## Motivation

Limit hold'em fixes the size of every bet, so a solver only chooses *whether* to bet and *whether* to raise. No-limit adds a second decision to every node — *how much* — and that single change multiplies the tree by orders of magnitude. The full game is far too large to store or solve exactly, yet it is the game where modern poker AI produced its headline results. It is also where the ideas of the previous six modules finally have to work together: hand evaluation, ranges, abstraction, action translation, and evaluation without exact exploitability.

This module starts with the smallest no-limit game that can still be solved: **push/fold**.

## What you will learn

You will reason about bet sizing with stack-to-pot ratio, geometric growth, commitment, and polarized versus merged ranges. You will build bet menus and see what they cost in tree size. You will solve a push/fold game and read the resulting charts. And you will explain continual re-solving, depth-limited lookahead, and how to compare bots when exact exploitability is out of reach.

## What you will build

The library now contains:

- `pokerbot.games.NoLimitBettingRound`, a single-street heads-up no-limit betting engine with a configurable pot-fraction bet menu, auditable minimum raises and all-ins, and a chip-conservation invariant;
- the sizing helpers `stack_to_pot_ratio`, `pot_odds_call_fraction`, and `pot_fraction_for_geometric_growth`;
- `pokerbot.solvers.push_fold`, a complete push/fold game and a chance-sampled CFR solver over the 169 starting-hand classes.

Still planned: the four-street no-limit game, a depth-limited re-solver, local best response, a match harness with variance reduction, a precomputed flop library, and the browser lab. See the [roadmap](../roadmap.md).

## Intuition first: why stack depth changes everything

In push/fold the small blind may shove all-in or fold; after a shove the big blind may call or fold. Both players post a one-ante blind, so the pot starts at two antes and the only thing that varies is how deep the stacks are.

Solve it and a clear pattern appears: **short stacks shove almost anything, deep stacks shove only strong hands.** At 5 big blinds the small blind can profitably shove roughly three quarters of all starting hands, because the big blind cannot call often enough to punish it and the reward (the antes) is large compared with the risk. At 40 big blinds the same shove risks forty times as much to win the same two antes, so only hands with real showdown equity survive.

The big blind's calling range moves in the opposite direction. It widens when the shover is forced to shove wide, then tightens again as the shover's range becomes strong. That interaction — each range defined by the other — is what an equilibrium is.

Measured with this repository's solver (200,000 iterations, seed 7):

| Stack | SB shoves | BB calls |
|---|---|---|
| 5 bb | 126 / 169 | 104 / 169 |
| 10 bb | 108 / 169 | 77 / 169 |
| 15 bb | 91 / 169 | 66 / 169 |
| 20 bb | 87 / 169 | 54 / 169 |
| 30 bb | 76 / 169 | 45 / 169 |
| 40 bb | 66 / 169 | 42 / 169 |

These are counts of hand *classes*, not combos, and they come from the default equity model described below. Treat the trend as the lesson and the exact numbers as approximate.

## Formal definition

Two players post an ante \(a\) each and start with stack \(s > a\). A chance move deals the small blind a class \(i\) and the big blind a class \(j\), each drawn from the 169 classes with probability proportional to its number of card combinations: 6 for a pair, 4 for suited, 12 for offsuit, summing to 1326. Let \(e(i,j)\) be the small blind's showdown equity, meaning \(\Pr(i \text{ wins}) + \tfrac12 \Pr(\text{tie})\).

The tree has three terminal kinds, with small-blind payoffs:

\[
u_{\text{SB fold}} = -a, \qquad
u_{\text{BB fold}} = +a, \qquad
u_{\text{showdown}} = s\,(2e(i,j) - 1).
\]

The big blind receives the negative of each. Each player's information set is their own class plus the action history, so there are 169 information sets for the small blind and 169 for the big blind.

A strategy profile is a Nash equilibrium when neither player can gain by deviating. The game is two-player and zero-sum, so an equilibrium exists in behavior strategies, and regret-minimizing algorithms converge to one.

The betting-round engine uses three scalars worth knowing:

\[
\text{SPR} = \frac{\text{stack}}{\text{pot}}, \qquad
\text{required equity} = \frac{c}{P + c},
\]

where \(c\) is the call amount and \(P\) the pot measured before the call. With \(n\) betting streets left, one bet and one call per street, and a target final pot \(P'\), the equal pot fraction that gets there is

\[
f = \frac{(P'/P)^{1/n} - 1}{2},
\]

because each round multiplies the pot by \(1 + 2f\). A pot of 10 with three streets and a target of 100 needs \(f = (10^{1/3}-1)/2 \approx 0.58\), so about 58% of the pot on each street.

## Algorithm

The push/fold solver uses **chance-sampled Monte Carlo CFR**. Full-tree CFR would touch \(169 \times 169 = 28{,}561\) deals per iteration, which is correct but slow. Instead, each iteration samples one deal and updates the two information sets that deal reaches.

```text
for t = 1 … T:
    sample (i, j) from the combo-weighted class distribution
    for traverser in (small blind, big blind):
        read the current strategy at that player's information set
        compute the counterfactual value of each action for this deal
        add the regrets and the reach-weighted strategy to that information set
average every information set's strategy
```

The average strategy converges at the usual \(O(1/\sqrt{T})\) rate, and sampling deals instead of enumerating them leaves the regret estimates unbiased. Because a deal is drawn independently for each player, the model ignores card removal: `AA` versus `AA` can be dealt. That keeps the game symmetric and the sampling cheap, at the cost of exactness.

```python
from pokerbot.games import NoLimitBettingRound, stack_to_pot_ratio
from pokerbot.solvers.push_fold import class_index, solve_push_fold

round_ = NoLimitBettingRound([100, 100], pot=10, bet_menu=(0.33, 0.75, 1.5))
print(round_.legal_actions())          # check, min bet, 33% / 75% / 150%, all-in

result = solve_push_fold(stack=20, iterations=100_000, seed=0)  # 20 antes = 10 bb
print(result.shove_range_names()[:8])
print(result.shove_threshold[class_index("AA")])   # near 1.0
print(stack_to_pot_ratio(100, 10))                 # 10
```

The default equity function is a deterministic strength heuristic: a hand-strength score (pair premium, high cards, suitedness, connectedness) mapped through a Bradley–Terry comparison, clamped away from 0 and 1. It is symmetric and monotone, and it produces the correct qualitative charts, but it is **not** a real preflop equity table. Real equities compress the extremes, so the ranges above are wider than published charts. Generate a table offline and plug it in with `load_equity_table`; the solver does not change.

## Interactive lab

There is no browser lab for this module yet. The fastest way to explore is the solver's command line:

```bash
python -m pokerbot.solvers.push_fold 10 100000
```

It prints both ranges for a ten-big-blind game. Change the first argument to move the stack depth, and the second to trade accuracy for time. A ten-big-blind solve at 100,000 iterations takes well under a second.

## Verification

`python -m pytest tests/test_push_fold.py` runs 17 tests. They check:

- the 169 classes are unique, and their combo counts sum to 1326;
- class names and indices round-trip, and malformed names raise;
- the equity model is symmetric, bounded, and ranks `AA` above `72o`;
- every terminal payoff is zero-sum and matches the formulas above;
- the game exposes the expected chance, player, information-set, and action structure;
- the solver returns a probability for all 338 information sets, always shoves `AA`, folds `72o` at 40 bb, widens its shoving range as stacks shrink, and is reproducible under a seed;
- the no-limit round and the push/fold solver are exported from their packages.

The module plan's strongest check — matching published push/fold charts — is **not yet met**, because the default equity model is a heuristic. With a real equity table loaded, the same test becomes meaningful. Exact exploitability of a solved strategy is also not computed here; the deal tree is small enough for `pokerbot.eval.exploitability` to do it, and that is a natural next step.

## Exercises

- **Recall:** Why does the small blind's shoving range widen as stacks shrink, and why does the big blind's calling range shrink at the same time?
- **Implement:** Generate a real preflop equity table with a small Monte Carlo script, load it with `load_equity_table`, and compare the resulting ranges with the table above.
- **Extend:** Add a minimum raise as a third small-blind action, then measure how the equilibrium changes and how much the tree grows.
- **Extend:** Compute exact exploitability of the solved average strategy with a full best response over the 169 × 169 deal tree.
- **Project:** Build a river-only no-limit game with a small bet menu and a depth-limited re-solver, then compare its value against the full solve.

## Where this breaks

Push/fold is tiny enough for a table of regrets. A real no-limit hand has four betting rounds, a large set of private hands, and several bet sizes per node; the number of information sets is far beyond what a dictionary can hold, and the number of deals is beyond what any tree walk can enumerate. The next two modules attack that from two directions: learn the regrets with a network instead of a table (Module 08), and replace deep subtrees with a learned value estimate plus a shallow search (Module 09).

## Checkpoint — you are done when…

- you can explain why no-limit is harder than limit even when the cards and streets are the same,
- you can compute stack-to-pot ratio, required calling equity, and an equal geometric bet size,
- you can read a push/fold chart and predict how it moves with stack depth,
- you can explain chance sampling in MCCFR and why the average strategy converges,
- you can separate what this module's code already does from what is still planned.

## Further reading

- B. Chen and J. Ankenman, *The Mathematics of Poker*, ConJelCo (2006) — commitment, SPR, and the original push/fold analysis.
- D. Billings, N. Burch, A. Davidson, R. Holte, J. Schaeffer, T. Schauenberg, and D. Szafron, “Approximate and Exact Solutions of No-Limit Poker,” *AAAI* (2003).
- M. Moravčík, M. Schmid, N. Burch, V. Lisý, D. Morrill, N. Bard, T. Davis, K. Waugh, M. Johanson, and M. Bowling, “DeepStack: Expert-Level Artificial Intelligence in Heads-Up No-Limit Poker,” *Science* (2017).
- N. Brown and T. Sandholm, “Superhuman AI for Heads-Up No-Limit Poker: Libratus Beats Top Professionals,” *Science* (2018).
- N. Brown and T. Sandholm, “Superhuman AI for Multiplayer Poker,” *Science* (2019).

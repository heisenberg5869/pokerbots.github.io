# 05 · Limit Texas Hold'em

| Level | Prerequisites | Status |
|---|---|---|
| Intermediate | [03 Leduc](03_leduc.md), [04 Sampling](04_mccfr.md) | in progress |

## Motivation

Leduc introduced public cards, but its deck has only six cards and its hands are easy to rank. Hold'em uses a standard
52-card deck, seven available cards at showdown, four betting streets, blinds, and ranges over many possible private
hands. Before a solver can reason about strategy, it needs a fast and correct way to compare hands and estimate equity.

## What you will learn

Five- and seven-card evaluation · best five of seven · hand categories and kickers · card removal · equity against a
range · exact versus Monte Carlo runouts · fixed-limit betting structure · why the game needs abstraction.

## What you will build

The library now has a dependency-free five/seven-card evaluator and exact and Monte Carlo equity calculators. The
notebook checks hand rankings, blockers, river equity, and seeded runout estimates. The full four-street Limit engine,
preflop strategy explorer, and bucketed solver remain planned P0 work.

## Intuition first: one board, two ranges

At showdown both players make the best five-card hand from their two private cards and the five-card board. If you
hold two aces on a river board, the opponent can hold at most one of the remaining ace combinations. This is why a
range is a set of *specific card combinations*, not just a list of hand labels. Removing known cards changes both the
number and the strength of the opponent's possible hands.

## Formal definition

The evaluator returns a lexicographically comparable tuple: first a category index, then the rank values that break
ties within that category. For example, a pair tuple contains the pair rank followed by the three kickers in descending
order. A seven-card hand is the maximum evaluator tuple over all \(\binom{7}{5}=21\) five-card subsets.

Equity against a range is

\[
\mathrm{equity} = \frac{\#\mathrm{wins} + \tfrac12\#\mathrm{ties}}{\#\mathrm{legal\ outcomes}}.
\]

For an incomplete board, each outcome includes a legal opponent combo and a board runout. Exact enumeration averages
all such outcomes; Monte Carlo samples them and reports the standard error of the win/tie share estimate.

## Algorithm

```python
from pokerbot.eval.hand_eval import evaluate_seven
from pokerbot.eval.equity import enumerate_equity, estimate_equity

# Cards are integers 0..51; rank = card % 13 + 2, suit = card // 13.
hero = [12, 25]                  # two aces, different suits
board = [0, 14, 28, 45, 7]      # a completed river board
villain_range = [[37, 50]]      # one legal two-card combo

exact = enumerate_equity(hero, board, villain_range)
sampled = estimate_equity(hero, board, villain_range, samples=5000, seed=9)
print(exact.equity, sampled.equity, sampled.standard_error)
```

The exact evaluator checks every five-card subset. The equity estimator removes hero cards and board cards from each
villain combo before dealing a runout, so blocked hands receive no weight.

## Interactive lab

The current notebook is [`modules/05_limit_holdem/notebook.ipynb`](https://github.com/heisenberg5869/pokerbots.github.io/blob/main/modules/05_limit_holdem/notebook.ipynb).
The six P0 labs are available in the [interactive lab](../demos/limit-module-05.html): hand evaluator, sampled equity
versus a painted range, hand-strength distribution, fixed-limit betting round, preflop strategy explorer, and game-size
calculator. The browser equity lab uses real card comparisons and reports a Monte Carlo interval. Its range weights are
uniform over selected hand classes; the Python equity API remains the combo-weighted reference implementation. The
preflop chart and state-size plot are teaching approximations, not trained strategy or measured game-tree counts.

## Verification

`python -m pytest tests/test_hand_eval.py tests/test_equity.py tests/test_limit.py` checks:

- category order, the wheel straight, kicker comparisons, and best-five selection,
- exact split equity when the board itself plays,
- blocker removal from a range,
- seeded Monte Carlo reproducibility and its river result,
- rejection of invalid card sets and ranges with no legal combos.
- fixed-limit betting-round closure, legal actions, raise cap, short all-in, and chip conservation.

The evaluator uses hand-worked examples here; a full five-card category-count enumeration and a large independent
reference-library comparison remain additional verification work.

## Exercises

- **Recall:** Why can two hands with the same made-hand category have different showdown ranks?
- **Implement:** Add a parser for strings such as `As Kh` and convert them to the library's integer card format.
- **Implement:** On a flop, compare exact equity enumeration with a Monte Carlo estimate and report the standard error.
- **Extend:** Add weighted opponent combos and verify that zero-weight hands do not affect equity.
- **Extend:** Design a fixed-limit betting state machine with blinds, a raise cap, short stacks, and chip-conservation tests.

## Where this breaks

Exact equity is useful for one hand against one range, but a solver also needs compact strategy representations across
many streets and public histories. Bucketing hands shrinks the problem, but can merge situations whose future
potential differs. [Abstraction and endgame solving](06_abstraction_endgame.md) studies that loss and how to repair it.

## Checkpoint — you are done when…

- you can explain how category and kicker tuples compare hands,
- you can evaluate the best five cards available from seven,
- you can calculate equity against a range while accounting for blockers,
- you can distinguish exact enumeration from a sampled estimate and its uncertainty,
- you can explain why a full Hold'em solver needs abstractions.

## Further reading

- B. Chen and J. Ankenman, [*The Mathematics of Poker*](https://www.conjelco.com/mathofpoker.html) (2006).
- M. Bowling, N. Burch, M. Johanson, and O. Tammelin, [“Heads-up limit hold'em poker is solved”](https://doi.org/10.1126/science.1259433), *Science* 347 (2015).
- O. Tammelin et al., [“Solving Heads-up Limit Texas Hold'em”](https://poker.cs.ualberta.ca/publications/2015-ijcai-cfrplus.pdf), IJCAI (2015).

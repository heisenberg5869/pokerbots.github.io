# 04 · Sampling and Monte Carlo CFR

| Level | Prerequisites | Status |
|---|---|---|
| Intermediate | [03 Leduc Hold'em](03_leduc.md) | in progress |

## Motivation

Full-tree CFR visits every chance deal and every legal action on every iteration. That is manageable for six-card
Leduc, but its cost grows with the game tree. Sampling lets us update from a smaller traversal while keeping the
updates correct *in expectation*.

## What you will learn

Chance sampling · external sampling · outcome sampling · importance weights · estimator variance · reproducible
seeds · why sampled solvers trade per-iteration cost against noise.

## What you will build

The library contains chance-sampling and external-sampling MCCFR, chance- and outcome-sampled value estimators, and a
dependency-free five-/seven-card Hold'em evaluator for the river work.
The notebook trains both MCCFR variants on Kuhn Poker, measures exact exploitability of their average strategies,
and checks sampled value estimates against the exact value.

## Intuition first: keep the paths you sample honest

Imagine a chance node that deals either J or K with equal probability. If we sample 1,000 deals, the estimate for an
action value is the average over those deals. We do not need to visit both deals on every iteration. If instead we
sample only J with probability 1/4 and K with probability 3/4, a plain average over sampled outcomes over-represents K.
An importance weight corrects each sample by \(p/q\), the probability under the game divided by the probability under
the sampling rule.

## Sampling schemes

| Scheme | Chance nodes | Opponent nodes | Traversing player's nodes |
|---|---|---|---|
| Full CFR | enumerate all | enumerate all | enumerate all |
| Chance sampling | sample | enumerate all | enumerate all |
| External sampling | sample | sample from current strategy | enumerate all |
| Outcome sampling | sample | sample | sample |

`MCCFRTrainer` implements chance sampling and external sampling. Its sampled chance outcomes use the game's chance
distribution. External sampling also draws opponent actions from the current strategy. Because the sampling
probabilities match the chance and opponent reach probabilities, those factors are accounted for by sampling and must
not be multiplied into the update a second time. In chance sampling, opponent actions are enumerated, so their reach
probabilities remain explicit in the regret and average-strategy updates.

Outcome sampling takes one path through every decision. `estimate_value` provides a simple outcome-sampled estimate
for a fixed profile. A full outcome-sampling CFR implementation needs additional importance weights and exploration
to ensure every action continues to be observed; it is not included in this first implementation slice.

## Formal definition: an unbiased sample

Let \(x\) be a sampled trajectory, \(q(x)\) its probability under the sampler, and \(p(x)\) its probability under
the game and strategy profile. For a trajectory quantity \(g(x)\), the importance-weighted estimator is

\[
\hat G = \frac{p(x)}{q(x)}g(x), \qquad \mathbb E_{x\sim q}[\hat G] = \sum_x p(x)g(x).
\]

When the sampler follows the same chance and opponent distributions as the game, those probabilities cancel. When the
sampling rule differs, the ratio is required. This factor corrects bias; it does not make an individual sample less
noisy.

## Algorithm: external-sampling MCCFR

For each iteration, traverse once for each player. At chance nodes, sample one outcome. At nodes belonging to the
other player, sample one action from their current strategy. At nodes belonging to the traverser, visit each action,
compute its value, and update regrets. Accumulate the traverser's own reach for its average strategy.

```python
from pokerbot.games.kuhn import KuhnPoker
from pokerbot.solvers.mccfr import MCCFRTrainer
from pokerbot.eval.exploitability import exploitability

trainer = MCCFRTrainer(KuhnPoker(), sampling="external", seed=7)
trainer.train(10_000)
strategy = trainer.average_strategy()
print(exploitability(trainer.game, strategy))  # typically around 0.01 with this seed
```

The exact value and exploitability functions from earlier modules remain useful on small games: they let us compare
the sampled strategy against a deterministic ground-truth evaluator.

## Variance and reproducibility

Two runs of a sampled algorithm differ because they visit different paths. Always record a seed, iteration count,
sampling scheme, and elapsed time when comparing runs. A baseline (control variate) can reduce variance if it is
correlated with the outcome and its expectation is known; it cannot repair an incorrect importance weight.

The sampler exposes a `seed` argument, and the tests average many fixed-profile samples against the exact Kuhn value.
The notebook also reports the exact exploitability of each sampled solver's average strategy, so sampling noise is
visible as a curve rather than hidden by a single final number.

## Interactive lab

The [sampling browser lab](../demos/mccfr-module-04.html) includes a miniature traversal visualizer, a repeated-estimate
variance experiment, a card-count scaling dial, and an analytic bluff-frequency anchor. The notebook at
[`modules/04_mccfr/notebook.ipynb`](https://github.com/heisenberg5869/pokerbots.github.io/blob/main/modules/04_mccfr/notebook.ipynb)
compares chance and external sampling on the same small game and checks that fixed-profile value estimates center on
the exact answer. The expanded-Leduc traversal viewer, river range solver, and measured scaling dashboard remain
planned P0 work.

## Verification

`python -m pytest tests/test_mccfr.py tests/test_hand_eval.py` checks that:

- chance- and external-sampling trainers produce normalized average strategies,
- chance- and outcome-sampled fixed-profile values are statistically close to exact Kuhn value with a fixed seed,
- invalid sampling modes are rejected.
- hand categories, wheel straights, kickers, seven-card best-five selection, and hand comparison are correct on hand-worked examples.

At 10,000 iterations with seed 4, the current reference run gives Kuhn exploitability about 0.0099 for chance
sampling and 0.0145 for external sampling; sampled runs vary, so these are examples rather than guarantees.

## Exercises

- **Recall:** Why must chance probabilities be used either by the sampling distribution or by an importance weight?
- **Implement:** Run the notebook with five seeds. Plot or tabulate final exploitability against wall-clock time.
- **Implement:** Add a baseline to an outcome estimator and measure the variance over repeated seeds.
- **Extend:** Make Leduc's chance deck larger and find where sampling becomes faster than full traversal at a fixed error target.
- **Extend:** Implement outcome-sampling CFR with explicit exploration and derive the action and trajectory importance weights.

## Where this breaks

Sampling reduces the number of states visited, but the game still needs correct hand values and useful features for
each private hand. A real river spot has thousands of hands per player and millions of runouts. Next we add a hand
evaluator and range-based abstractions in [Limit Hold'em](05_limit_holdem.md).

## Checkpoint — you are done when…

- you can explain how chance sampling differs from external sampling,
- you can identify which probability is corrected by an importance weight,
- you can reproduce a sampled value estimate with a fixed seed,
- you can compare a sampled average strategy with an exact exploitability evaluator on a toy game.

## Further reading

- M. Lanctot et al., “Monte Carlo Sampling for Regret Minimization in Extensive Games” (2009).
- M. Schmid et al., “Variance Reduction in Monte Carlo Counterfactual Regret Minimization” (2019).

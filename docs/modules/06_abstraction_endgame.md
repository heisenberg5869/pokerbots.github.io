# 06 · Abstraction and Endgame Solving

| Level | Prerequisites | Status |
|---|---|---|
| Advanced | [05 Limit Hold'em](05_limit_holdem.md) | in progress |

## Motivation

The full game tree is too large to solve directly. Abstraction merges situations that look strategically similar and replaces an enormous set of possible bet sizes with a small menu. Both steps trade fidelity for a smaller blueprint. At play time, safe subgame solving can refine a local decision while preserving the blueprint's promised value.

## What you will learn

You will build hand buckets from future-strength histograms, compare them with one-dimensional earth mover's distance (EMD), translate off-menu bets, and explain the difference between unsafe re-solving and a gadget-based safe solve.

## What you will build

The library now includes histogram EMD, deterministic k-medoids, and nearest, linear-randomized, and harmonic-randomized bet translation. The notebook and browser lab exercise these tools. A full game abstraction evaluator, safe subgame solver, nested solving, and real-game exploitability sweep remain planned.

## Intuition first: made hand and draw

Imagine two hands whose chance of winning at showdown averages 55%. A made pair may stay near that value on most turn cards. A flush draw may be far behind on many cards and far ahead when a flush arrives. If we bucket using only the mean, these hands collapse together. A histogram of future outcomes retains some of that shape.

For equally spaced bins, EMD compares the cumulative mass moved across the histogram. Moving all mass one bin costs 1; moving it three bins costs 3. It distinguishes nearby distributions more gently than a bin-by-bin squared error.

## Formal definition

For normalized histograms (p) and (q) over ordered bins, the one-dimensional EMD is

\[
W_1(p,q)=\sum_{i=1}^{m-1}\left|\sum_{j=1}^{i}(p_j-q_j)\right|.
\]

The implementation normalizes nonnegative inputs and sums absolute cumulative-mass differences. K-medoids selects actual observed histograms as representatives, minimizing within-cluster distances. This is easier to inspect than a synthetic centroid and costs (O(n^2)) distance storage in this teaching implementation.

For an off-tree bet (x) bracketed by abstract sizes (a < x < b), linear randomized translation chooses (b) with probability \((x-a)/(b-a)\), and (a) otherwise. Its expected translated size is (x). Deterministic nearest-size mapping is simpler but creates sharp boundaries an opponent can target. Harmonic translation interpolates in reciprocal-size space; it changes probabilities asymmetrically and does not inherit the linear method's expected-size guarantee.

## Algorithm

```python
from pokerbot.abstraction import earth_movers_distance, k_medoids
from pokerbot.abstraction import translation_probabilities, translate_bet

distance = earth_movers_distance([1, 0, 0], [0, 1, 0])  # one bin
labels, representatives = k_medoids([
    [1, 0, 0], [0.9, 0.1, 0], [0, 0.1, 0.9], [0, 0, 1]
], 2)
print(labels, representatives)
print(translation_probabilities(3, [2, 4]))  # 50% at each size
print(translate_bet(3, [2, 4], method="linear"))
```

Lossless suit-isomorphism reduction keeps strategic value because globally relabeling suits preserves rank and flush structure. Lossy bucketing can alter values and may create imperfect recall if the bucket forgets details needed to distinguish earlier histories.

## Blueprint and re-solving

A blueprint is a strategy solved on the abstracted game. Unsafe re-solving conditions on an estimated opponent range; a wrong estimate can make the new local strategy exploitable. Safe subgame solving adds a gadget action that lets the opponent opt out and receive the counterfactual value promised by the blueprint. This constrains the local solve so the opponent cannot force a lower continuation value than the blueprint allowed. A tested implementation of that guarantee is not yet in this repository.

## Interactive lab

Use the [abstraction and action-translation lab](../demos/abstraction-module-06.html) to compare average-strength bucketing with distribution-aware buckets, adjust the bucket count, and inspect randomized bet translation. The plotted cluster and game-size curves are synthetic teaching examples, not measured solver runs.

The executable notebook is [`modules/06_abstraction_endgame/notebook.ipynb`](https://github.com/heisenberg5869/pokerbots.github.io/blob/main/modules/06_abstraction_endgame/notebook.ipynb).

## Verification

`python -m pytest tests/test_abstraction.py` checks hand-computed EMD distances, deterministic clustering, linear translation's expectation, bounded harmonic probabilities, and invalid-input handling. These tests cover the current helpers; they do not establish an endgame-solving safety guarantee.

## Exercises

- **Recall:** Why can equal mean equity conceal different future potential?
- **Implement:** Add a histogram distance with nonuniform bin widths and test it against a hand-worked example.
- **Extend:** Give a scripted opponent an off-menu bet and compare nearest with randomized translation over repeated trials.
- **Project:** Measure abstraction loss by comparing an abstract strategy's real-game best response with its in-abstraction value on a small game.

## Where this breaks

Action menus in no-limit poker leave many plausible bet sizes off-tree, and lossy abstraction can hide the distinctions that make those actions dangerous. Module 07 studies no-limit play and action translation in a richer setting.

## Checkpoint — you are done when…

- you can compute one-dimensional EMD by cumulative mass,
- you can explain why histograms carry more information than average strength,
- you can compare deterministic and randomized action translation,
- you can state the opponent opt-out idea behind safe subgame solving,
- you can separate a blueprint's abstract-game quality from its real-game quality.

## Further reading

- N. Brown and T. Sandholm, “Safe and Nested Subgame Solving for Imperfect-Information Games,” *NeurIPS* (2017).
- M. Johanson, “Measuring the Size of Large No-Limit Poker Games,” University of Alberta thesis (2013).
- M. Johanson, N. Bard, N. Lanctot, and M. Bowling, “Take it to the Limit: the Limitations of Absolute Abstraction,” AAAI (2012).

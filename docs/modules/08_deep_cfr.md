# 08 · Deep CFR

| Level | Prerequisites | Status |
|---|---|---|
| Advanced | 02, 04 | draft |

## Motivation
_What the previous module could not do, and why this one exists._

## What you will learn
Neural advantage networks; reservoir sampling; training on sampled regrets; Single Deep CFR; approximation error and how it shows up in exploitability.

## What you will build
Deep CFR on Leduc, then on a Limit endgame; comparison against tabular MCCFR.

## Intuition first
_TODO: a tiny worked example and a picture before any formulas._

## Formal definition
_TODO: use the notation in [Notation](../notation.md)._

## Algorithm
Implementation: `pokerbot/nn/` (AdvantageNet, StrategyNet, features, reservoir) and `pokerbot/solvers/deep_cfr.py` (DeepCFRTrainer), plus `single_deep_cfr.py`. Run `python -m pokerbot.solvers.deep_cfr`.

## Interactive lab
_TODO: notebook in `modules/08_deep_cfr/` and/or a browser demo._

## Verification
_TODO: compare against a known answer (exact equilibrium, LP, or a published number)._

## Exercises
- **Recall:** _TODO_
- **Implement:** _TODO_
- **Extend:** _TODO_

## Where this breaks
Network values are only as good as the information they take in. We need public belief states and value functions for search (Module 09).

## Checkpoint — you are done when…
_TODO: 3 to 5 concrete things you can do or explain._

## Further reading
_TODO_

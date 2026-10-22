# 03 · Leduc Hold'em

| Level | Prerequisites | Status |
|---|---|---|
| Intermediate | 01, 02 | planned |

## Motivation
_What the previous module could not do, and why this one exists._

## What you will learn
Chance nodes and public cards; two betting rounds; raises and raise caps; beliefs over the opponent's hidden card; CFR+, linear CFR and alternating updates; equilibrium convergence on a game with ~10^4 information-state nodes.

## What you will build
Leduc engine; CFR and CFR+; exploitability curves; cross-check against OpenSpiel's published numbers.

## Intuition first
_TODO: a tiny worked example and a picture before any formulas._

## Formal definition
_TODO: use the notation in [Notation](../notation.md)._

## Algorithm
_TODO: pseudocode, then a minimal implementation._

## Interactive lab
_TODO: notebook in `modules/03_leduc/` and/or a browser demo._

## Verification
_TODO: compare against a known answer (exact equilibrium, LP, or a published number)._

## Exercises
- **Recall:** _TODO_
- **Implement:** _TODO_
- **Extend:** _TODO_

## Where this breaks
Full-tree traversal scales with the game tree. A bigger deck makes each iteration too slow, so we sample (Module 04).

## Checkpoint — you are done when…
_TODO: 3 to 5 concrete things you can do or explain._

## Further reading
_TODO_

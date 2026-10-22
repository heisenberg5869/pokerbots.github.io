# 02 · Regret Matching & No-Regret Learning

| Level | Prerequisites | Status |
|---|---|---|
| Beginner | 00, 01 | outline |

## Motivation
_What the previous module could not do, and why this one exists._

## What you will learn
External regret; regret matching; Hedge/multiplicative weights; why the AVERAGE strategy converges while the current one cycles; the O(1/sqrt(T)) rate; how CFR decomposes regret across information sets.

## What you will build
Self-play regret matching on rock-paper-scissors; convergence plots; the interactive demo below; a proof sketch of CFR's regret bound.

## Intuition first
_TODO: a tiny worked example and a picture before any formulas._

## Formal definition
_TODO: use the notation in [Notation](../notation.md)._

## Algorithm
_TODO: pseudocode, then a minimal implementation._

## Interactive lab

Regret matching on rock-paper-scissors. Use **vs fixed opponent** to see the strategy lock onto the best response, then switch to **self-play** and watch the *average* strategy drift toward 1/3, 1/3, 1/3.

<iframe src="../../demos/regret_matching_rps.html" width="100%" height="470" style="border:1px solid #8884;border-radius:6px"></iframe>

Questions to answer with it:

- Why does the average strategy converge in self-play while the *current* strategy keeps cycling?
- How does the speed of convergence change over time?
- What happens if the opponent changes mid-run?

## Verification
_TODO: compare against a known answer (exact equilibrium, LP, or a published number)._

## Exercises
- **Recall:** _TODO_
- **Implement:** _TODO_
- **Extend:** _TODO_

## Where this breaks
CFR as written traverses the whole tree every iteration. Games with chance and several betting rounds need a richer test bed (Module 03).

## Checkpoint — you are done when…
_TODO: 3 to 5 concrete things you can do or explain._

## Further reading
_TODO_

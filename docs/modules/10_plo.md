# 10 · Pot-Limit Omaha

| Level | Prerequisites | Status |
|---|---|---|
| Advanced | 05, 09 | in progress |

## Motivation

PLO adds a fourth hole card and the exactly-two-from-hand rule, exploding hand combinations and equity complexity.

## What you will learn

Four hole cards; exactly-two-from-hand, three-from-board; combinatorial growth; equity estimation; pot-limit sizing.

## What you will build

Browser labs: hand builder, combination counter, equity lab, failure lab.

## Intuition first

A PLO hand is not "best five of nine"; you must use exactly two private cards.

## Formal definition

Legal 5-card hand = choose 2 of 4 hole × choose 3 of 5 board = 6×10 = 60 combinations.

## Algorithm

Enumerate all 60 combinations and take max rank tuple.

## Interactive lab

- [plo-hand-builder.html](../demos/plo-hand-builder.html)
- [plo-combination-counter.html](../demos/plo-combination-counter.html)
- [plo-equity-lab.html](../demos/plo-equity-lab.html)
- [plo-failure-lab.html](../demos/plo-failure-lab.html)

## Verification

Compare against brute-force enumeration.

## Exercises

- Recall: why does PLO have more draws?
- Implement: Omaha evaluator.
- Extend: pot-limit tree.

## Where this breaks

Hold'em intuition fails; more variance.

## Checkpoint — you are done when…

- you can enumerate legal PLO hands,
- you can explain combo count,
- you can estimate equity.

## Further reading

- PLO strategy references.
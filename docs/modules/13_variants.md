# 13 Custom Variants: Sneak Peek Hold'em and Beyond

| Level | Prerequisites | Status |
|---|---|---|
| Research | all earlier | in progress |

## Motivation
Rules are part of the game. Changing one rule changes the tree, information sets, and equilibrium. A bot must reason about mechanics, not memorise a Hold'em policy.

## What you will learn
Modelling new rules as extensive-form games: auctions, altered information access, new actions; mechanism design basics; re-deriving information sets; adapting solvers and abstractions to a changed game.

## What you will build
A variant framework (rules as config); Sneak Peek Hold'em; a bot that solves it rather than reusing a Hold'em policy.

## Intuition first
A variant is a configuration of deck, actions, information, and payoffs. Standard Hold'em is one point in a large space.

## Formal definition
A variant game is an extensive-form game parameterised by rules R. Information sets depend on R.

## Algorithm
1. Specify rules as config.
2. Generate game tree.
3. Derive information sets.
4. Solve with CFR/abstraction.
5. Verify with invariants.

## Interactive lab
- [Rules builder](../demos/variant-rules-builder.html)
- [Rule card](../demos/variant-card.html)
- [Tree estimator](../demos/variant-tree-estimator.html)

## Verification
Reproduce standard Hold'em with all optional rules disabled; counts should match known values.

## Exercises
- **Recall:** What changes when peek rules are added?
- **Implement:** Build a variant config and estimate tree size.
- **Extend:** Add a new rule and update invariants.

## Where this breaks
What is actually solved, what is merely good, and what is open? (Module 14)

## Checkpoint
- Can configure a variant.
- Can estimate tree size.
- Can explain info set changes.

## Further reading
Custom game research, mechanism design.
# 01 · Kuhn Poker

| Level | Prerequisites | Status |
|---|---|---|
| Beginner | [00 Prerequisites](00_prereqs.md) | in progress |

## Motivation

Rock-paper-scissors has no hidden information and no sequence of moves. Poker has both: you act without knowing
the opponent's cards, and what you do *reveals* information. We need the smallest possible game that still has
these features. **Kuhn Poker** is that game, and it is small enough to solve by hand, check by computer, and
compare against a known answer.

## What you will learn
game trees · information sets · pure, mixed and behavior strategies · bluffing as an equilibrium phenomenon ·
best response · exploitability · a first look at counterfactual regret minimization (CFR)

## The game

- Deck: three cards, J < Q < K. Each of the two players antes 1 and receives one card.
- Player 0 acts first: **pass** (check) or **bet** 1.
- After a pass, player 1 may pass (showdown) or bet; after that bet player 0 may fold or call.
- After a bet, the other player may **fold** or **call**.
- Highest card wins at showdown.

Writing `p` for pass/check/fold and `b` for bet/call, there are only five ways a hand can end:

| History | What happened | Payoff to player 0 |
|---|---|---|
| `pp` | both check, showdown | ±1 |
| `pbp` | check, bet, fold | −1 |
| `pbb` | check, bet, call, showdown | ±2 |
| `bp` | bet, fold | +1 |
| `bb` | bet, call, showdown | ±2 |

## Intuition first: why this isn't a "solve the tree" problem

If you saw the opponent's card, you would simply play optimally for that deal. But you don't. When you hold **Q**
and face a bet, your opponent might hold J (bluffing) or K (value-betting). Both situations look identical to you.

An **information set** is a group of game states that one player cannot tell apart. In Kuhn, player 0's
information sets are named by what they see: their card plus the history, e.g. `Q` (to open) or `Qpb` (checked,
then faced a bet). A strategy must assign the *same* behavior to every state inside one information set.

!!! note "Why strategies must be random"
    If you always call with Q, a bettor who never bluffs profits. If you never call, a bettor who always bluffs
    profits. The only unexploitable play is to call **some fraction** of the time. That fraction is a *mixed
    strategy*, and finding it is the whole game.

## Formal definition

An extensive-form game with imperfect information has players \(i\), histories \(h\), chance probabilities, and
information sets \(I\). A **behavior strategy** \(\sigma_i(I, a)\) gives the probability that player \(i\) plays
action \(a\) at information set \(I\). A **best response** to \(\sigma_{-i}\) maximizes \(u_i\) against it.

\[
\text{exploitability}(\sigma) \;=\; \tfrac12\sum_{i\in\{0,1\}} \Big( \max_{\sigma_i'}\, u_i(\sigma_i', \sigma_{-i}) \;-\; u_i(\sigma) \Big)
\]

In a two-player zero-sum game, exploitability is 0 exactly at a Nash equilibrium. It is the scoreboard used for
the rest of this repo.

## The known answer (your ground truth)

Kuhn Poker has a family of equilibria indexed by \(\alpha \in [0, 1/3]\):

| Player 0 | Strategy |
|---|---|
| holds J, opens | bet with probability \(\alpha\) |
| holds Q, opens | always check |
| holds K, opens | bet with probability \(3\alpha\) |
| J, after check-bet | fold |
| Q, after check-bet | call with probability \(\alpha + 1/3\) |
| K, after check-bet | call |

| Player 1 | Strategy |
|---|---|
| J facing a bet | fold |
| Q facing a bet | call with probability 1/3 |
| K facing a bet | call |
| J after a check | bet (bluff) with probability 1/3 |
| Q after a check | check |
| K after a check | bet |

The value of the game to player 0 is **−1/18** ≈ −0.0556 for every α: the player who acts first is at a small,
exact disadvantage.

## Algorithm: vanilla CFR (first look)

CFR plays the game against itself many times. At each information set it tracks **regret**: how much better an
action would have done than the strategy actually played, weighted by how likely the *other* parties were to
reach this situation. The next strategy plays actions in proportion to positive regret (regret matching).
The *average* strategy over all iterations converges to equilibrium.

```python
from pokerbot.games.kuhn import KuhnPoker
from pokerbot.solvers.cfr import CFRTrainer
from pokerbot.eval.exploitability import exploitability, expected_value

game = KuhnPoker()
trainer = CFRTrainer(game)
trainer.train(20000)
strategy = trainer.average_strategy()

print(exploitability(game, strategy))        # about 0.0016
print(expected_value(game, strategy, 0))     # about -0.0556  (= -1/18)
```

Why this works and what the regret bound is are the subject of [Module 02](02_regret_matching.md). Here, treat
the solver as a tool and focus on the game.

## Interactive lab

Open the [Kuhn Poker browser lab](../demos/kuhn-module-01.html) to explore the deal tree, play against scripted
opponents, move through the equilibrium family, probe exploitability, and step vanilla CFR. The notebook remains the
reproducible Python path.

Open [`modules/01_kuhn/notebook.ipynb`](https://github.com/heisenberg5869/pokerbots.github.io/blob/main/modules/01_kuhn/notebook.ipynb)
and try:

1. Print the learned strategy and compare it to the table above.
2. Plot exploitability against iterations (it should fall roughly as \(1/\sqrt{T}\)).
3. Pick α yourself, build the strategy by hand, and check its exploitability is 0.
4. Break the equilibrium: change one probability slightly and measure how much a best response gains.

## Verification

Run `pytest tests/test_kuhn_cfr.py`. The tests check that:

- terminal payoffs are correct,
- the uniform strategy is clearly exploitable,
- the hand-written α = 0 equilibrium has exploitability ≈ 0 and game value −1/18,
- CFR's output has exploitability below 0.005 and matches the equilibrium structure (K bets about 3× as often as J bluffs, Q calls about 1/3 of the time).

## Exercises

- **Recall:** Why can't player 1's strategy depend on player 0's card? Name the information sets of each player.
- **Implement:** Compute player 0's expected payoff for a fixed strategy pair by hand for one deal, then check it against `expected_value`.
- **Implement:** Write `best_response_value` from scratch for Kuhn without looking at `pokerbot/eval/exploitability.py`.
- **Extend:** Change the deck to 4 cards (J, Q, K, A). Does the first player's disadvantage grow or shrink? Why?
- **Extend:** Allow a second raise. What breaks in the hand-derived equilibrium?

## Where this breaks

Kuhn has one betting round, no public cards and 12 information sets. Hold'em has several rounds, shared cards
that change what both players believe, and raises. We now need chance nodes in the middle of the game,
conditional beliefs, and faster algorithms — [Leduc Hold'em](03_leduc.md) is the next step.

## Checkpoint — you are done when…

- you can explain what an information set is using a Kuhn example,
- you can say why bluffing with J is part of an equilibrium even though J always loses at showdown,
- you can compute (by hand or code) the exploitability of a given strategy,
- your CFR run reproduces the −1/18 game value.

## Further reading

- H. W. Kuhn, *A Simplified Two-Person Poker* (1950): the original analysis.
- Neller & Lanctot, *An Introduction to Counterfactual Regret Minimization* (2013): a gentle CFR walk-through on Kuhn.
- Zinkevich et al., *Regret Minimization in Games with Incomplete Information* (2007): the CFR paper.

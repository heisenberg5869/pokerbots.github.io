# 12 · Opponent Modelling & Exploitation

| Level | Prerequisites | Status |
|---|---|---|
| Advanced | 11 | complete |

## Motivation
Nash equilibrium guarantees not losing, but against a predictable opponent it leaves money on the table. Opponent modelling turns observed actions into a belief about the opponent's strategy, then exploits that belief—while staying safe against counter-exploitation.

## What you will learn
Inferring opponent behaviour from observed actions; Bayesian models; safe exploitation; the tradeoff between exploiting and being exploitable; online adaptation.

## What you will build
An opponent model plus a safe-exploitation agent; experiments against scripted opponents.

## Intuition first
If an opponent folds too often to bets, bet more. But if you over-commit to that belief and they adapt, you become exploitable. The art is measuring how much to exploit given uncertainty.

## Formal definition
Let $p$ be opponent action probabilities. Observed counts $n$ update a Dirichlet posterior $\alpha$. Exploitability of your strategy $x$ is the gain of the best response to $x$. Safe exploitation maximizes EV against the posterior while keeping exploitability $\le \epsilon$.

## Algorithm
1. Maintain counts per information set.
2. Posterior predictive: $\hat p(a) = (\alpha_a + n_a)/(\alpha_0 + n)$.
3. Best-respond to $\hat p$ with a mixed strategy.
4. Clip mixing to keep exploitability under budget.

## Interactive labs
- [Opponent Profile Lab](../demos/opponent-profile-lab.html)
- [Bayesian Opponent Lab](../demos/bayesian-opponent-lab.html)
- [Exploitability-Profit Frontier](../demos/exploitability-profit-frontier.html)

## Verification
Against a known scripted opponent, expected profit matches closed-form best response.

## Exercises
- **Recall:** Define exploitability.
- **Implement:** Bayesian updater for a 2-action node.
- **Extend:** Add non-stationary (decaying) priors.

## Where this breaks
Opponents adapt; non-stationarity invalidates static models. Use Module 13 for variant robustness.

## Checkpoint — you are done when…
- You can build a Bayesian opponent model.
- You can compute exploitability of an exploitative strategy.
- You can choose an exploitation level on the profit frontier.

## Further reading
- Billings et al., Opponent Modelling in Poker.
- Ganzfried & Sandholm, Safe and Nested Subgame Solving.
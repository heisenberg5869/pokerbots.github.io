# 09 — Value Networks & Search (ReBeL-style)

| Level | Prerequisites | Status |
|---|---|---|
| Advanced | 07, 08 | in progress |

## Motivation
Pure CFR on full NLHE is intractable: the game tree is too large and the state space too big. Module 08 scaled CFR with neural function approximation; Module 09 generalises the AlphaZero recipe — *depth-limited search with a learned value network* — to imperfect-information games.

## What you will learn
- Public belief states (PBS): the state of an imperfect-information game is a distribution over private hands conditioned on public actions.
- Value functions over beliefs: $V(\beta)$ estimates expected value of a belief state.
- Depth-limited search: solve a subtree of depth $d$ using a value network at the leaves.
- Self-play RL + search: improve the value network by playing against itself with search.
- Failure modes: belief leakage, off-tree actions, value-network bias, search exploitation.

## What you will build
Interactive labs: belief-state explorer, search-tree lab, value-network lab (plus search-vs-network, belief-update, search-failure).

## Intuition first
In perfect-information games (chess), the state is the board. In poker, the "state" is what both players *know publicly* plus a distribution over hidden cards — a belief state. Search evaluates a belief state by solving a small subtree and trusting a value network at the leaves.

## Formal definition
A public belief state $\beta = (S, \mu)$ where $S$ is public state and $\mu$ is a distribution over (private info, history). Value $V(\beta) = \mathbb{E}_{(h,\sigma)\sim\beta}[u(h)]$ under optimal play of the subtree.

## Algorithm
1. Observe public state + opponent actions → update belief.
2. Build depth-$d$ search tree over public actions.
3. At leaves, query value network $V_\theta(\beta)$.
4. Solve subtree (CFR on beliefs) → strategy + value.
5. Use value to train $V_\theta$ via self-play.

## Interactive lab
- `demos/belief-state-explorer.html`
- `demos/search-tree-lab.html`
- `demos/value-network-lab.html`

## Verification
Belief updates sum to 1; search values converge to tabular CFR on small games; value network reduces leaf error.

## Exercises
- **Recall:** Define a PBS.
- **Implement:** belief update on a toy game.
- **Extend:** vary depth and measure exploitability.

## Where this breaks
Four hole cards and exactly-two rule blow up combinatorics (Module 10). Belief leakage and off-tree actions.

## Checkpoint — you are done when…
- You can explain why belief state replaces hidden state.
- You can run depth-limited search and read leaf values.
- You can name 3 failure modes.

## Further reading
Brown & Sandholm ReBeL (2020); AlphaZero.
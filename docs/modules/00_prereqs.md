# 00 · Prerequisites

| Level | Prerequisites | Status |
|---|---|---|
| Beginner | none | in progress |

## Motivation

Poker combines uncertainty about outcomes with competition against someone who chooses actions strategically. Before
building a poker solver, we need a language for both. This lesson introduces expected value for uncertain outcomes,
then uses small matrix games to explain strategies and equilibrium. The next lesson adds sequences of actions and
hidden cards.

## What you will learn

Card combinations and card removal · expected value and variance · pot odds and bluff break-even · Bayesian range
updates · normal-form games · pure and mixed strategies · best responses · Nash equilibrium · zero-sum minimax ·
extensive-form games · perfect and imperfect information · exact solutions by indifference and linear programming.

## What you will build

Probability, card-combination, pot-odds, and Bayes helpers, plus two exact methods for small zero-sum matrices:
support enumeration by indifference and a primal/dual minimax linear program. The examples use only Python's standard
library; the LP helper enumerates vertices for teaching-sized games.

## Intuition first: a bet and a coin

### Counting unseen hands

If order does not matter, the number of ways to choose \(k\) objects from \(n\) is

\[
\binom{n}{k}=\frac{n!}{k!(n-k)!}.
\]

There are \(\binom{52}{2}=1{,}326\) possible two-card starting hands. If you hold two cards, only 50 remain, so an
opponent has \(\binom{50}{2}=1{,}225\) possible combinations before considering any action. There are six pocket-ace
combinations in a fresh deck, but only three if you hold one ace. This is **card removal**: known cards change the
possible opponent holdings and therefore their range.

Suppose a fair coin pays you $3 on heads and costs you $2 on tails. The average payoff over many repetitions is

\[
\mathbb{E}[X] = \tfrac12(3) + \tfrac12(-2) = 0.5.
\]

The bet has positive expected value, but a single toss can still lose. Expected value describes the long-run average,
not a promise about the next outcome. Variance measures how widely outcomes spread around that average:

\[
\mathrm{Var}(X) = \mathbb{E}[(X-\mathbb{E}[X])^2].
\]

In poker, a call can be profitable over many similar situations even though it loses this particular hand. To decide,
we need probabilities for the opponent's possible hands and the payoff for each result.

### Pot odds and bluff break-even

Let \(P\) be the pot before an opponent bets, \(B\) their bet, and \(C\) the amount you must call. If a call wins
with probability \(e\) and loses otherwise, its expected net payoff is

\[
\mathrm{EV}(\text{call})=e(P+B)-(1-e)C.
\]

The break-even equity is \(C/(P+B+C)\). If the bet and call are both \(B\), this becomes \(B/(P+2B)\). For
example, calling 100 into a pot of 100 after a 100-chip bet needs \(100/(100+100+100)=1/3\) equity.

A zero-equity bluff risking \(B\) to win a pot \(P\) breaks even when the opponent folds often enough:

\[
fB-(1-f)P=0 \quad\Longrightarrow\quad f=\frac{P}{P+B}.
\]

Here \(f\) is the fold frequency. A pot-sized bluff (\(B=P\)) needs folds half the time. The corresponding minimum
defense frequency is \(P/(P+B)\): if the defender continues more often than this, a zero-equity bluff loses money.

## Bayes' rule: update a range after an action

Suppose the opponent is strong, medium, or bluffing with prior probabilities \((0.2,0.5,0.3)\). If those types bet
with probabilities \((0.8,0.4,0.1)\), then after seeing a bet their unnormalized weights are
\((0.2\cdot0.8, 0.5\cdot0.4, 0.3\cdot0.1)=(0.16,0.20,0.03)\). Normalize by their sum, 0.39, to get posterior
probabilities \((16/39,20/39,3/39)\). The medium type is now most likely even though it was already the most common.

In general, for hidden type \(H\) and observed action \(A\),

\[
P(H\mid A)=\frac{P(A\mid H)P(H)}{\sum_{h}P(A\mid h)P(h)}.
\]

The posterior is a **range**: a probability distribution over the opponent's possible holdings or types. An action
changes the range according to how likely each type was to take that action.

## Normal-form games: choose without seeing the opponent's move

A finite two-player normal-form game is a payoff table. Player 1 chooses a row, player 2 chooses a column, and each
cell gives the players' payoffs. In a zero-sum game, one payoff is the negative of the other, so we can record only
player 1's payoff.

For matching pennies, matching earns player 1 `+1`; mismatching gives `−1`:

| Player 1 \\ Player 2 | Heads | Tails |
|---|---:|---:|
| Heads | +1 | −1 |
| Tails | −1 | +1 |

Neither player has a dominant pure action. If player 1 always chooses Heads, player 2 chooses Tails. If player 1
always chooses Tails, player 2 chooses Heads. A **mixed strategy** randomizes: player 1 chooses Heads with
probability \(p\), and player 2 chooses Heads with probability \(q\).

Player 1's expected payoff from choosing Heads is \(2q-1\), and from choosing Tails is \(1-2q\). Player 2 makes
player 1 indifferent by choosing \(q=1/2\). Symmetrically, player 1 chooses \(p=1/2\). This is a Nash equilibrium:
neither player can improve their expected payoff by changing strategy alone. Its value to player 1 is zero.

!!! note "Dominance and equilibrium"
    An action is **strictly dominated** if another action does better against every opponent action. A Nash equilibrium
    is a strategy profile where each player's strategy is a best response to the others. Equilibrium does not mean
    that every action is equally good, or that the outcome of each play is predictable.

## Worked example: rock-paper-scissors

Use payoff `+1` for a win, `0` for a tie, and `−1` for a loss. No pure strategy is safe: the opponent can choose the
action that beats it. If the opponent plays Rock, Paper, and Scissors each one-third of the time, every pure action
has expected payoff zero. The same uniform mix is therefore a best response, so the profile is a Nash equilibrium.

More generally, in a zero-sum game each player maximizes their own payoff, which is the same as minimizing the
opponent's. The **minimax theorem** says that for finite two-player zero-sum games, the best guaranteed value equals
the value obtained at equilibrium. This is why we can judge a poker strategy by how much a best-responding opponent
can gain.

## From simultaneous moves to poker

A normal-form table describes what each player chooses, but it hides the timing. An **extensive-form game** makes
the sequence explicit as a tree: nodes are decision or chance points, edges are actions or chance outcomes, and
leaves have payoffs.

When a player cannot distinguish two decision nodes, those nodes belong to the same **information set**. A legal
strategy must choose the same action distribution at every node in that set. Poker has imperfect information because
players do not see opponents' private cards; it has perfect recall because each player remembers their own cards and
past actions. Module 01 builds the smallest useful example, Kuhn Poker, as an extensive-form game.

One way to convert a tree to normal form is to list every complete contingent plan for each player. A plan specifies
an action at every decision the player might face, even if some decisions will never be reached. If a player has
\(d\) binary decisions, this can create \(2^d\) pure strategies. The tree stores shared prefixes once, so it can be
much smaller. Mixed strategies randomize over complete plans; behavior strategies randomize separately at each
information set. In games with perfect recall these representations can realize the same outcome distributions,
but behavior strategies are usually much more compact.

| Model | What it represents | Example |
|---|---|---|
| Expected value | Uncertain outcomes under fixed probabilities | Call payoff against a known range |
| Normal form | One strategic choice per player | Matching pennies, RPS |
| Extensive form | Ordered actions and chance | A poker hand |
| Information set | Decisions a player cannot distinguish | Holding Q after facing a bet |

## Exact solution by indifference

For a small zero-sum matrix game, an equilibrium can often be found by making the opponent indifferent between the
actions they randomize over. For matching pennies, set the opponent's mix so Heads and Tails have the same expected
payoff; solve the corresponding equation for each player. With more actions, the same idea becomes a system of linear
constraints. Linear programming provides a general exact method, though this first module keeps the examples small
enough to solve directly.

## Interactive lab

Open [`modules/00_prereqs/notebook.ipynb`](https://github.com/heisenberg5869/pokerbots.github.io/blob/main/modules/00_prereqs/notebook.ipynb).
It calculates expected values, verifies the matching-pennies equilibrium, and evaluates all three RPS actions against
the uniform mix. The [Foundations browser lab](../demos/foundations-module-00.html) also explores bet outcomes, pot odds,
card removal, Bayesian range updates, and editable payoff matrices. Change the probabilities and observe when a best
response appears.

## Self-check

1. A pot-sized zero-equity bluff needs the opponent to fold: **A)** 25% **B)** 50% **C)** 75%.
2. You hold one ace. How many pocket-ace combinations remain for the opponent: **A)** 1 **B)** 3 **C)** 6.
3. If you observe a bet, the posterior probability of a type depends on: **A)** its prior only **B)** its betting likelihood only **C)** both.
4. Against uniform rock-paper-scissors, which pure action has the highest expected payoff: **A)** Rock **B)** Paper **C)** all tie.

Answers: 1B, 2B, 3C, 4C. Show the arithmetic in the browser lab and notebook before checking.

## Verification

Check these results by hand and in the notebook:

- The coin bet has expected payoff `0.5` and variance `6.25`.
- Against a fair matching-pennies opponent, both pure actions have expected payoff `0`.
- Against any non-uniform matching-pennies mix, the opponent has a pure action with positive expected payoff.
- Against uniform RPS, Rock, Paper, and Scissors each have expected payoff `0`.
- A 2×2 matrix equilibrium has matching-pennies strategies `(1/2, 1/2)` and value `0`.
- `solve_zero_sum` and `solve_zero_sum_lp` agree on the matching-pennies, RPS, and rectangular examples.

## Exercises

- **Recall:** What is the difference between an outcome's payoff and its expected payoff?
- **Implement:** A call costs 4 chips and wins 10 chips total with probability 0.3; otherwise it loses the 4-chip call. Compute its expected net payoff. Should you call if you maximize chips alone?
- **Implement:** Write a function that returns the expected payoff of each row action against a probability distribution over columns. Check it on matching pennies.
- **Implement:** Write a function that solves a 2×2 zero-sum game by indifference, and compare its answer with `solve_zero_sum` in `pokerbot.foundations`.
- **Extend:** In matching pennies, let a match pay `+2` and a mismatch cost `−1`. Find the equilibrium probability that player 2 chooses Heads and the game's value.
- **Extend:** Give one poker decision tree node that belongs to an information set with another node. What facts are hidden from the acting player?

## Where this breaks

Normal form does not show how information changes as actions unfold. A poker player may check, observe a bet, and then
choose whether to call without seeing the opponent's cards. To model that correctly, we need histories, chance nodes,
and information sets. That is the subject of [Kuhn Poker](01_kuhn.md).

## Checkpoint — you are done when…

- you can compute an expected payoff from outcome probabilities,
- you can explain why a best response exploits a predictable pure strategy,
- you can verify the matching-pennies and RPS equilibrium mixes,
- you can update an opponent range with Bayes' rule and calculate pot odds,
- you can distinguish a normal-form game from an extensive-form game,
- you can explain why a poker strategy must act the same way throughout one information set.

## Further reading

- M. J. Osborne, *An Introduction to Game Theory* (2004), chapters 1–3.
- J. Nash, “Equilibrium Points in n-Person Games” (1950).
- J. von Neumann and O. Morgenstern, *Theory of Games and Economic Behavior* (1944).

# 02 · Regret Matching & No-Regret Learning

| Level | Prerequisites | Status |
|---|---|---|
| Beginner | [00 Prerequisites](00_prereqs.md), [01 Kuhn Poker](01_kuhn.md) | draft |

## Motivation

In Module 01 you ran CFR and it produced the right equilibrium. But *why*? Nothing in the code solved for an
equilibrium: it just played against itself and nudged probabilities toward actions it "regretted" not taking.

This module explains why that works, in the simplest setting where it can be seen completely: a **matrix game**
(rock-paper-scissors). The same idea, applied once at every information set, *is* CFR. By the end you will know:

- what **regret** means and why "no regret" is a meaningful goal,
- the **regret matching** rule and a short proof that its regret grows only like \(\sqrt{T}\),
- why two no-regret learners playing each other converge to Nash equilibrium (in the **average**, not the current strategy),
- exactly what the lines `regret_sum += cf_reach * (...)` in the CFR solver are computing.

## What you will learn
external regret · no-regret algorithms · regret matching · regret matching+ · Hedge (multiplicative weights) ·
average vs current strategy · the \(1/\sqrt{T}\) rate · from no-regret to equilibrium · from matrix games to CFR

## The setting: learning from hindsight

Forget equilibrium for a moment. You play the same game against an opponent over many rounds \(t = 1,\dots,T\).
Each round:

1. you choose a probability distribution \(\sigma^t\) over your actions,
2. the opponent's move is revealed, so you learn the utility \(u^t(a)\) *every* action \(a\) would have earned,
3. you receive \(\langle \sigma^t, u^t\rangle = \sum_a \sigma^t(a)\,u^t(a)\).

After \(T\) rounds, ask: **what if I had played one fixed action the whole time?** The best such action's total
minus what you actually got is your **external regret**:

\[
R^T \;=\; \max_{a}\sum_{t=1}^{T} u^t(a)\;-\;\sum_{t=1}^{T}\langle \sigma^t,u^t\rangle .
\]

An algorithm is **no-regret** if \(R^T/T \to 0\) against *every* opponent, even one that adapts to try to hurt you.
That is a strong promise, and it needs no model of the opponent at all.

!!! note "What regret is *not*"
    Regret compares you with the best **fixed** action in hindsight. It does not compare you with the best
    *sequence* of actions. Against an opponent who cycles Rock, Paper, Scissors, always-Rock has zero advantage,
    but a player who reacts one step ahead would win every round. No-regret does not promise that.

## The rule: regret matching

Define the **instantaneous regret** of action \(a\) at round \(t\): how much better \(a\) would have done than what you played.

\[
r^t(a) \;=\; u^t(a) \;-\; \langle \sigma^t,u^t\rangle, \qquad
R^t(a)=\sum_{s\le t} r^s(a).
\]

**Regret matching** plays each action in proportion to its *positive* cumulative regret:

\[
\sigma^{t+1}(a)\;=\;\frac{R^{t}(a)^{+}}{\sum_{b} R^{t}(b)^{+}}\quad\text{(uniform if all regrets are}\le 0\text{)},
\qquad x^+=\max(x,0).
\]

Actions you regret not having played get more weight; actions that did worse than your mix get none.

### Worked example (check it against the code)

You use regret matching on rock-paper-scissors; the opponent plays Rock, then Scissors, then Rock.
Utilities are listed in the order (Rock, Paper, Scissors).

| Round | Your \(\sigma^t\) | Opponent | \(u^t\) | Value | \(r^t\) | Cumulative \(R^t\) |
|---|---|---|---|---|---|---|
| 1 | (⅓, ⅓, ⅓) | Rock | (0, 1, −1) | 0 | (0, 1, −1) | (0, 1, −1) |
| 2 | (0, 1, 0) | Scissors | (1, −1, 0) | −1 | (2, 0, 1) | (2, 1, 0) |
| 3 | (⅔, ⅓, 0) | Rock | (0, 1, −1) | ⅓ | (−⅓, ⅔, −4⁄3) | (5⁄3, 5⁄3, −4⁄3) |
| 4 | (½, ½, 0) | | | | | |

After round 1 you regret not playing Paper, so you play Paper. It loses to Scissors, which makes you regret Rock
the most, and so on. Scissors (negative regret) is eliminated until it earns positive regret. This table is
reproduced exactly by `Learner` in `pokerbot/solvers/matrix_games.py`.

## Why it works: the regret bound

!!! success "Theorem (regret matching)"
    If every utility lies in a range of width \(\Delta\) and there are \(n\) actions, then against any opponent
    \[
    R^T \;\le\; \Delta\sqrt{nT}.
    \]
    So average regret \(R^T/T \le \Delta\sqrt{n}/\sqrt{T}\to 0\).

??? note "Proof sketch (about ten lines)"
    Let \(R^t_+\) be the vector of positive parts of \(R^t\). Track its squared length.

    1. Clipping only shrinks things: \(\|R^{t}_+\|^2 \le \|R^{t-1}_+ + r^t\|^2 = \|R^{t-1}_+\|^2 + 2\langle R^{t-1}_+, r^t\rangle + \|r^t\|^2.\)
    2. **The cross term is exactly zero.** Regret matching plays \(\sigma^t = R^{t-1}_+/Z\) with \(Z=\sum_a R^{t-1}_+(a)\), so
       \(\langle R^{t-1}_+, r^t\rangle = Z\big(\langle\sigma^t,u^t\rangle - \langle\sigma^t,u^t\rangle\big)=0.\)
       The rule is built so that, on average, you gain nothing from the direction regret is pointing.
    3. Each \(|r^t(a)|\le\Delta\), so \(\|r^t\|^2\le n\Delta^2\). Telescoping: \(\|R^T_+\|^2 \le nT\Delta^2\).
    4. And \(R^T=\max_a R^T(a) \le \|R^T_+\|\le\Delta\sqrt{nT}.\) ∎

The bound is **sublinear**: regret grows, but slower than \(T\). You can see it in the notebook: for RPS the
measured regret sits well below \(\Delta\sqrt{3T}\).

## From no-regret to Nash equilibrium

Now let two no-regret learners play a **zero-sum** game against each other, each treating the other as "the opponent".

!!! success "Theorem (no-regret ⇒ equilibrium)"
    Let \(\bar x, \bar y\) be the players' **average** strategies over \(T\) rounds, and suppose their average regrets
    are \(\varepsilon_1,\varepsilon_2\). Then the exploitability of \((\bar x,\bar y)\) is at most \((\varepsilon_1+\varepsilon_2)/2\).

??? note "Why (four lines)"
    - Utility is linear in the opponent's mix, so the best fixed action's average payoff against the sequence \(y^1,\dots,y^T\)
      equals its payoff against the average \(\bar y\). Hence \(\max_i u(i,\bar y)\) is the row player's best-response value to \(\bar y\), and
      \(R^T_{\text{row}}/T\le\varepsilon_1\) says: *best response to \(\bar y\)* \(\le\) *average realised payoff* \(+\,\varepsilon_1\).
    - The same holds for the column player.
    - In a zero-sum game the two players' realised payoffs cancel every round.
    - Adding the two inequalities: (BR gain against \(\bar y\)) + (BR gain against \(\bar x\)) \(\le \varepsilon_1+\varepsilon_2\). That sum is NashConv; exploitability is half of it. ∎

This is the whole engine. **You never solve for equilibrium; you just keep regret small, and equilibrium
falls out of the average.** The test `test_low_regret_implies_low_exploitability` checks this inequality numerically.

### Why the *average*, not the current strategy?

Try the interactive demo below in **self-play** mode. The thin lines (current strategy) keep swinging between
nearly pure strategies: when you play too much Rock, your opponent drifts toward Paper, which pushes you toward
Scissors, and so on. The thick lines (average strategy) settle at ⅓, ⅓, ⅓.

The guarantee is only about the average. This is why the CFR solver stores `strategy_sum` and why `average_strategy()`, not the
current strategy, is what we evaluate.

!!! warning "Pitfall: starting at the equilibrium"
    In a symmetric game like RPS, if both players start at uniform, all regrets are exactly zero and
    **nothing ever changes**: you sit on the equilibrium without learning anything. `self_play` therefore
    starts the row player slightly off-equilibrium (`skewed`). Test: `test_symmetric_game_stays_at_equilibrium_if_started_there`.

## How fast?

Regret is \(O(\sqrt{T})\), so *average* regret and therefore exploitability fall like \(1/\sqrt{T}\). Measured on rock-paper-scissors:

| \(T\) | exploitability | exploitability \(\times\sqrt{T}\) |
|---|---|---|
| 100 | 0.0993 | 0.99 |
| 1,000 | 0.0287 | 0.91 |
| 10,000 | 0.0094 | 0.94 |
| 100,000 | 0.0032 | 1.02 |

The last column is roughly constant, as the theory predicts. Practical meaning: **10× more accuracy costs 100× more iterations.**
This slow rate is what later modules fight (CFR+, sampling, neural approximation).

## Variants you should know

| Rule | Update | Notes |
|---|---|---|
| Regret matching (`"rm"`) | play ∝ \(R^+\) | the baseline; used in vanilla CFR |
| Regret matching+ (`"rm+"`) | after every step, \(R \leftarrow \max(R + r,\,0)\) | forgets old negative regret so a good action recovers faster. Basis of **CFR+**, which solved heads-up limit Hold'em |
| Hedge (`"hedge"`) | play ∝ \(\exp(\eta\sum_t u^t)\) | smoother, regret \(O(\Delta\sqrt{T\ln n})\): better when \(n\) is large; needs a learning rate \(\eta\) |

On RPS at \(T=20{,}000\) in this repo: RM ≈ 7×10⁻³, RM+ ≈ 2×10⁻³, Hedge ≈ 3×10⁻⁴ exploitability.
Do not read too much into one game, but the ordering is why RM+ is worth knowing.

## From matrix games to CFR

A poker game is not a matrix game: actions come in sequences, with hidden cards. The key idea of CFR
(Zinkevich et al., 2007) is a **decomposition**:

> The regret of the whole strategy is bounded by the sum, over information sets \(I\), of the regret you would have
> if you could choose your action at \(I\) alone, measured in **counterfactual value**.

So we run an independent regret matcher at *every information set*, each fed with a slightly different "utility":

\[
r^t(I,a) \;=\; \pi^{\sigma^t}_{-i}(I)\,\Big(v^{\sigma^t}(I,a) - v^{\sigma^t}(I)\Big),
\]

where \(v\) is the expected payoff given you reach \(I\) and then play \(a\) (or follow \(\sigma\)), and
\(\pi_{-i}(I)\) is the probability that **everyone except you** (opponent and chance) lets play reach \(I\).
"Counterfactual" means: weight the situation as if you had *tried* to get here, so it counts by how often others
cooperate in getting here, not by how often you did.

That is precisely this line of `pokerbot/solvers/cfr.py`:

```python
node.regret_sum[i] += cf_reach * (action_values[i][player] - node_value[player])
```

and the same file's `strategy_sum[i] += reach[player] * strategy[i]` is the averaging, weighted by *your own* reach.
Zinkevich et al. show total regret \(R^T \le \Delta\,|\mathcal I|\sqrt{|A|}\,\sqrt{T}\) (with \(|\mathcal I|\) information sets), so
average regret falls like \(1/\sqrt{T}\), and by the theorem above the average strategy's exploitability does too.
You measured that in Module 01's convergence curve.

## Interactive lab

**Browser demo** (no install). Pick **vs fixed opponent** to watch the strategy lock onto the best response, then
switch to **self-play** and watch the thick (average) lines converge while the thin (current) lines keep swinging.

<iframe src="../../demos/regret_matching_rps.html" width="100%" height="470" style="border:1px solid #8884;border-radius:6px"></iframe>

**Notebook:** [`modules/02_regret_matching/notebook.ipynb`](https://github.com/heisenberg5869/pokerbots.github.io/blob/main/modules/02_regret_matching/notebook.ipynb) lets you

1. see the worked example reproduced by `Learner`,
2. plot current vs average strategy in self-play,
3. plot regret against the \(\Delta\sqrt{nT}\) bound,
4. fit the \(1/\sqrt{T}\) rate on a log-log plot,
5. compare RM, RM+ and Hedge,
6. find the non-uniform equilibrium of a biased RPS.

Questions to answer with the demo:

- Why does the average strategy converge in self-play while the *current* strategy keeps cycling?
- What happens to the learner when the opponent changes strategy mid-run? (Hint: old regret takes time to unwind. RM+ fixes this.)
- Make the opponent's mix very close to uniform. How long does the learner take to commit to a best response?

## Verification

`pytest tests/test_regret_matching.py` checks that:

- hand-derived equilibria of RPS and a biased RPS have exploitability 0,
- all three rules learn a best response to a fixed opponent,
- self-play average strategies converge to ⅓, ⅓, ⅓ (and to \((¼, ½, ¼)\) in the biased game),
- the *current* strategy keeps swinging by more than 0.3 while the average converges,
- the symmetric-start pitfall is real,
- external regret stays under \(\Delta\sqrt{nT}\),
- exploitability \(\times \sqrt{T}\) stays roughly constant over three orders of magnitude of \(T\),
- average regret upper-bounds the exploitability of the average profile.

## Exercises

- **Recall:** Why is regret measured against the best *fixed* action rather than the best sequence of actions? What would be impossible otherwise?
- **Recall:** In the proof, which property of regret matching makes the cross term \(\langle R^+, r\rangle\) vanish?
- **Implement:** Without looking at `matrix_games.py`, write regret matching for RPS and reproduce the table in the worked example.
- **Implement:** Add *linear averaging* (weight round \(t\) by \(t\)) to `Learner.average_strategy`. Does exploitability improve for RM+ on RPS? (This is the "+" in CFR+ too.)
- **Extend:** Solve the biased game by hand (set \(A x = 0\)) and confirm \((¼,½,¼)\). Now make Rock-beats-Scissors worth 3 instead. Predict the new equilibrium, then check it.
- **Extend:** Implement Hedge with a *fixed* learning rate. Show that for large \(\eta\) the current strategy cycles wildly, and for small \(\eta\) learning is slow. What does this say about choosing \(\eta\)?
- **Extend:** Let the row player use regret matching and the column player play a fixed strategy that *switches* halfway through the run. Measure how long the row player takes to adapt, for RM and for RM+.

## Where this breaks

Matrix games list every strategy up front. Poker has far too many strategies for that, which is why CFR works
on information sets instead. But vanilla CFR walks the **entire** game tree every iteration, and its \(1/\sqrt{T}\) rate is slow.
[Leduc Hold'em](03_leduc.md) is the first game where chance nodes in the middle of the game, public cards and raises
make both costs visible, and where CFR+ and better averaging start to pay off.

Two caveats worth carrying forward:

- The guarantees above are for **two-player zero-sum** games. With three or more players, average strategies of no-regret learners need not be an equilibrium ([Module 11](11_multiplayer.md)).
- Convergence is of the **average** only. Anything that *plays* the current strategy (or needs a single policy for a neural net to imitate) must be handled with care ([Module 08](08_deep_cfr.md)).

## Checkpoint: you are done when…

- you can define external regret and explain what "no-regret" does and does not promise,
- you can run regret matching by hand for three rounds,
- you can state why the average strategy, not the current one, converges to equilibrium in self-play,
- you can explain what \(\pi_{-i}\) is doing in the counterfactual regret formula,
- you can predict how many more iterations you need for 10× lower exploitability.

## Further reading

- S. Hart & A. Mas-Colell, *A Simple Adaptive Procedure Leading to Correlated Equilibrium* (2000): where regret matching comes from.
- Y. Freund & R. Schapire, *Adaptive Game Playing Using Multiplicative Weights* (1999): Hedge and the zero-sum theorem.
- N. Cesa-Bianchi & G. Lugosi, *Prediction, Learning, and Games* (2006): the standard reference on regret.
- M. Zinkevich et al., *Regret Minimization in Games with Incomplete Information* (2007): the CFR paper; sections 2–3 are exactly this module plus the decomposition.
- O. Tammelin, *Solving Large Imperfect Information Games Using CFR+* (2014): regret matching+.
- T. Neller & M. Lanctot, *An Introduction to Counterfactual Regret Minimization* (2013): a gentle companion to this page.

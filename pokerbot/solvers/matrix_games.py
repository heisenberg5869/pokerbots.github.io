"""No-regret learning on two-player zero-sum MATRIX games (the setting of Module 02).

A matrix game is a payoff matrix A for the row player (the column player gets -A).
Three learning rules are provided:

  "rm"     regret matching      play actions in proportion to positive cumulative regret
  "rm+"    regret matching+     like rm, but cumulative regret is floored at 0 after every step
  "hedge"  multiplicative weights (exponential weights) on cumulative utility

Key facts demonstrated by the tests and the notebook:
  * the AVERAGE strategy converges to equilibrium in self-play; the CURRENT one cycles,
  * external regret grows like sqrt(T), so average regret shrinks like 1/sqrt(T),
  * average regret r for both players  =>  exploitability of the average profile <= r.
"""
from __future__ import annotations
import math

# rows/cols: Rock, Paper, Scissors. Entry = payoff to the ROW player.
RPS = [[0, -1, 1],
       [1, 0, -1],
       [-1, 1, 0]]

# Rock beats scissors for 2 instead of 1. The equilibrium is no longer uniform: (1/4, 1/2, 1/4).
BIASED_RPS = [[0, -1, 2],
              [1, 0, -1],
              [-2, 1, 0]]


def payoff_range(A) -> float:
    flat = [x for row in A for x in row]
    return max(flat) - min(flat)


def row_utils(A, y):
    """Expected payoff of each row action against column mix y."""
    return [sum(a * q for a, q in zip(row, y)) for row in A]


def col_utils(A, x):
    """Expected payoff of each column action (column player gets -A) against row mix x."""
    n_cols = len(A[0])
    return [-sum(x[i] * A[i][j] for i in range(len(A))) for j in range(n_cols)]


def matrix_exploitability(A, x, y) -> float:
    """Average gain of best-responding opponents; 0 exactly at a Nash equilibrium.

    Same definition as pokerbot.eval.exploitability: (NashConv) / 2, where
    NashConv = max_i (A y)_i  -  min_j (x^T A)_j  for zero-sum games.
    """
    return 0.5 * (max(row_utils(A, y)) - min(-u for u in col_utils(A, x)))


class Learner:
    """One player's online learner. Call strategy(), then update() with the realised action utilities."""

    def __init__(self, n_actions: int, algorithm: str = "rm", payoff_range: float = 2.0,
                 first_strategy=None):
        if algorithm not in ("rm", "rm+", "hedge"):
            raise ValueError("algorithm must be 'rm', 'rm+' or 'hedge'")
        self.n = n_actions
        self.algorithm = algorithm
        self.range = payoff_range
        self.regret = [0.0] * n_actions        # accumulator used by rm / rm+
        self.cum_util = [0.0] * n_actions      # true cumulative utility of each fixed action
        self.cum_value = 0.0                   # cumulative utility actually obtained
        self.strategy_sum = [0.0] * n_actions
        self.t = 0
        self.first_strategy = first_strategy   # optional strategy for the very first iteration

    def strategy(self) -> list[float]:
        if self.t == 0 and self.first_strategy is not None:
            return list(self.first_strategy)
        if self.algorithm == "hedge":
            eta = math.sqrt(8 * math.log(self.n) / max(self.t, 1)) / self.range
            top = max(self.cum_util)
            w = [math.exp(eta * (u - top)) for u in self.cum_util]
            s = sum(w)
            return [x / s for x in w]
        pos = [max(r, 0.0) for r in self.regret]
        s = sum(pos)
        return [p / s for p in pos] if s > 0 else [1.0 / self.n] * self.n

    def update(self, strategy, action_utils) -> None:
        value = sum(p * u for p, u in zip(strategy, action_utils))
        for i in range(self.n):
            self.strategy_sum[i] += strategy[i]
            self.cum_util[i] += action_utils[i]
            gain = action_utils[i] - value
            self.regret[i] = max(self.regret[i] + gain, 0.0) if self.algorithm == "rm+" else self.regret[i] + gain
        self.cum_value += value
        self.t += 1

    def external_regret(self) -> float:
        """Utility of the best FIXED action in hindsight minus utility actually obtained."""
        return max(self.cum_util) - self.cum_value

    def average_strategy(self) -> list[float]:
        s = sum(self.strategy_sum)
        return [x / s for x in self.strategy_sum] if s > 0 else [1.0 / self.n] * self.n


def _record(rec, t, row, col, x, y, A):
    ax, ay = row.average_strategy(), col.average_strategy()
    rec["t"].append(t)
    rec["avg_row"].append(ax)
    rec["avg_col"].append(ay)
    rec["cur_row"].append(list(x))
    rec["cur_col"].append(list(y))
    rec["exploitability"].append(matrix_exploitability(A, ax, ay))
    rec["regret_row"].append(row.external_regret())
    rec["regret_col"].append(col.external_regret())


def _new_record():
    keys = ["t", "avg_row", "avg_col", "cur_row", "cur_col", "exploitability", "regret_row", "regret_col"]
    return {k: [] for k in keys}


def skewed(n: int, weight: float = 0.6) -> list[float]:
    """A deliberately non-uniform starting strategy: `weight` on action 0, the rest split evenly."""
    return [weight] + [(1 - weight) / (n - 1)] * (n - 1)


def self_play(A, iterations: int, algorithm: str = "rm", record_every: int = 1,
              init_row=None, init_col=None):
    """Both players learn simultaneously. Returns a dict of histories (see _new_record).

    Pitfall: in a symmetric game like RPS, if both players start at the uniform equilibrium
    they stay there forever (all regrets are exactly 0). So by default the row player's FIRST
    strategy is skewed; the column player starts uniform.
    """
    rng = payoff_range(A)
    if init_row is None:
        init_row = skewed(len(A))
    row = Learner(len(A), algorithm, rng, first_strategy=init_row)
    col = Learner(len(A[0]), algorithm, rng, first_strategy=init_col)
    rec = _new_record()
    for t in range(1, iterations + 1):
        x, y = row.strategy(), col.strategy()
        ux, uy = row_utils(A, y), col_utils(A, x)
        row.update(x, ux)
        col.update(y, uy)
        if t % record_every == 0 or t == iterations:
            _record(rec, t, row, col, x, y, A)
    return rec


def vs_fixed(A, opponent, iterations: int, algorithm: str = "rm", record_every: int = 1):
    """The row player learns against a FIXED column strategy `opponent`."""
    row = Learner(len(A), algorithm, payoff_range(A))
    rec = {"t": [], "avg_row": [], "cur_row": [], "regret_row": []}
    for t in range(1, iterations + 1):
        x = row.strategy()
        row.update(x, row_utils(A, opponent))
        if t % record_every == 0 or t == iterations:
            rec["t"].append(t)
            rec["avg_row"].append(row.average_strategy())
            rec["cur_row"].append(list(x))
            rec["regret_row"].append(row.external_regret())
    return rec

"""Head-to-head match harness with duplicate play and variance reduction."""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

from pokerbot.games.base import Game
from pokerbot.games.kuhn import KuhnPoker as Kuhn  # default game


def _strategy_prob(strategy, state, player):
    if callable(strategy):
        return list(strategy(state, player))
    key = state.info_set_key(player)
    actions = state.legal_actions()
    probs = strategy.get(key) if isinstance(strategy, dict) else None
    if not probs:
        return [1.0 / len(actions)] * len(actions)
    return list(probs)


def play_hand(game: Game, strategy_a, strategy_b, rng: random.Random) -> float:
    """Play one hand; return payoff to player 0 (in chips)."""
    s = game.root()
    # sample chance
    while True:
        if s.is_terminal():
            return float(s.returns()[0])
        if s.is_chance():
            outcomes = s.chance_outcomes()
            r = rng.random()
            acc = 0.0
            chosen = outcomes[-1][0]
            for o, p in outcomes:
                acc += p
                if r <= acc:
                    chosen = o
                    break
            s = s.child(chosen)
            continue
        cp = s.current_player()
        strat = strategy_a if cp == 0 else strategy_b
        probs = _strategy_prob(strat, s, cp)
        actions = list(s.legal_actions())
        r = rng.random()
        acc = 0.0
        chosen = actions[-1]
        for a, p in zip(actions, probs):
            acc += p
            if r <= acc:
                chosen = a
                break
        s = s.child(chosen)


def duplicate_play(game, strategy_a, strategy_b, seed) -> float:
    """Play the hand twice with swapped positions; return average payoff to A."""
    rng1 = random.Random(seed)
    rng2 = random.Random(seed)
    # first: A is player 0
    v1 = play_hand(game, strategy_a, strategy_b, rng1)
    # second: A is player 1 -> swap roles, negate
    v2 = -play_hand(game, strategy_b, strategy_a, rng2)
    return (v1 + v2) / 2.0


@dataclass
class MatchResult:
    mean: float
    std: float
    ci_low: float
    ci_high: float
    n_hands: int
    outcomes: list = field(default_factory=list)
    reduced_mean: float = None
    reduced_std: float = None

    def hands_needed(self, edge: float) -> int:
        if edge <= 0:
            return float("inf")
        # variance of per-hand outcome in (bb)^2; mean in bb/hand -> bb/100 scale
        var = self.std ** 2 if self.std is not None else 1.0
        # convert std (bb/100 per hand? we store mean in bb/100) ; use raw outcome variance
        # use outcomes if available
        if self.outcomes:
            vals = [o * 100.0 for o in self.outcomes]
            m = sum(vals) / len(vals)
            var = sum((v - m) ** 2 for v in vals) / max(1, len(vals) - 1)
        z = 1.96 + 0.84
        n = (z * z * var) / (edge * edge)
        return max(1, int(math.ceil(n)))


class Match:
    def __init__(self, game=None):
        self.game = game if game is not None else Kuhn()

    @staticmethod
    def play(strategy_a, strategy_b, n_hands, seed=0, game=None, duplicate=True, covariate=None):
        g = game if game is not None else Kuhn()
        rng = random.Random(seed)
        outcomes = []
        for i in range(n_hands):
            if duplicate:
                v = duplicate_play(g, strategy_a, strategy_b, rng.randrange(1 << 30))
            else:
                v = play_hand(g, strategy_a, strategy_b, rng)
            outcomes.append(v)
        # bb/100
        vals = [o * 100.0 for o in outcomes]
        n = len(vals)
        mean = sum(vals) / n
        var = sum((v - mean) ** 2 for v in vals) / max(1, n - 1)
        std = math.sqrt(var)
        se = std / math.sqrt(n)
        ci_low = mean - 1.96 * se
        ci_high = mean + 1.96 * se
        res = MatchResult(mean=mean, std=std, ci_low=ci_low, ci_high=ci_high, n_hands=n, outcomes=outcomes)
        # control variate if covariate provided
        if covariate is not None:
            try:
                from pokerbot.eval.variance_reduction import control_variate
                adj = control_variate(vals, covariate)
                avals = adj if not isinstance(adj, tuple) else adj[0]
                amean = sum(avals) / len(avals)
                avar = sum((v - amean) ** 2 for v in avals) / max(1, len(avals) - 1)
                res.reduced_mean = amean
                res.reduced_std = math.sqrt(avar)
            except Exception:
                pass
        return res


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    r = Match.play({}, {}, args.n, seed=args.seed)
    print(r)


if __name__ == "__main__":
    main()

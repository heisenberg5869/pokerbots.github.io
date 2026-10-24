"""Minimal multiplayer (N-player) game helpers for population evaluation."""
from __future__ import annotations

import random
from typing import Callable, List


class MultiplayerGame:
    """A simple symmetric N-player zero-sum-ish game defined by a payoff function."""

    def __init__(self, n_players=3, seed=None):
        self.n = n_players
        self.rng = random.Random(seed)

    def payoff(self, actions):
        # Rock-paper-scissors-like: majority wins? Implement simple: winner gets +1, losers -1/(n-1)
        # actions: list of ints 0..2 (rock/paper/scissors)
        # count wins
        res = [0.0] * self.n
        for i in range(self.n):
            for j in range(self.n):
                if i == j:
                    continue
                a, b = actions[i], actions[j]
                if (a + 1) % 3 == b:
                    res[i] -= 1.0 / (self.n - 1)
                elif (b + 1) % 3 == a:
                    res[i] += 1.0 / (self.n - 1)
        return res


def population_round_robin(strategies: List[Callable], game: MultiplayerGame, n_rounds=1000, seed=None):
    """Evaluate list of strategy callables (each returns action given rng) via round-robin groups."""
    rng = random.Random(seed)
    scores = [0.0] * len(strategies)
    for _ in range(n_rounds):
        # pick a random group of n players from strategies (with replacement)
        idxs = [rng.randrange(len(strategies)) for _ in range(game.n)]
        actions = [strategies[i](rng) for i in idxs]
        pays = game.payoff(actions)
        for k, i in enumerate(idxs):
            scores[i] += pays[k]
    return [s / n_rounds for s in scores]

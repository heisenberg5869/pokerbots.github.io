import random

from pokerbot.games.multiplayer import MultiplayerGame, population_round_robin


def test_payoff_zero_sum():
    g = MultiplayerGame(n_players=3)
    pays = g.payoff([0, 1, 2])
    assert abs(sum(pays)) < 1e-9


def test_round_robin_runs():
    def strat(rng):
        return rng.randrange(3)
    scores = population_round_robin([strat, strat, strat], MultiplayerGame(), n_rounds=100, seed=1)
    assert len(scores) == 3
    assert all(isinstance(s, float) for s in scores)

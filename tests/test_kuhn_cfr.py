"""Verify the Kuhn engine, exploitability code and CFR against known theory."""
import pytest
from pokerbot.games.kuhn import KuhnPoker
from pokerbot.solvers.cfr import CFRTrainer
from pokerbot.eval.exploitability import exploitability, expected_value, best_response_value


@pytest.fixture(scope="module")
def solved():
    game = KuhnPoker()
    t = CFRTrainer(game)
    t.train(20000)
    return game, t.average_strategy()


def test_terminal_payoffs():
    from pokerbot.games.kuhn import KuhnState
    assert KuhnState((2, 0), "pp").returns() == (1, -1)
    assert KuhnState((0, 2), "pp").returns() == (-1, 1)
    assert KuhnState((0, 2), "pbp").returns() == (-1, 1)
    assert KuhnState((0, 2), "bp").returns() == (1, -1)
    assert KuhnState((1, 0), "bb").returns() == (2, -2)


def test_uniform_strategy_is_exploitable():
    game = KuhnPoker()
    assert exploitability(game, {}) > 0.1


def test_exploitability_of_known_nash():
    """Hand-written equilibrium: the alpha = 0 member of Kuhn's Nash family.

    Player 0 (acts first): never bluffs with J, always checks Q, checks K to trap.
      after check-bet: fold J, call Q with prob 1/3, call K.
    Player 1: after a check, bluff J with prob 1/3, check Q, bet K.
      facing a bet: fold J, call Q with prob 1/3, call K.
    Strategies are [P(pass), P(bet)].
    """
    game = KuhnPoker()
    nash = {
        "J": [1.0, 0.0], "Q": [1.0, 0.0], "K": [1.0, 0.0],
        "Jpb": [1.0, 0.0], "Qpb": [2 / 3, 1 / 3], "Kpb": [0.0, 1.0],
        "Jp": [2 / 3, 1 / 3], "Qp": [1.0, 0.0], "Kp": [0.0, 1.0],
        "Jb": [1.0, 0.0], "Qb": [2 / 3, 1 / 3], "Kb": [0.0, 1.0],
    }
    assert exploitability(game, nash) < 1e-9
    assert expected_value(game, nash, 0) == pytest.approx(-1 / 18, abs=1e-9)


def test_cfr_exploitability_small(solved):
    game, strat = solved
    assert exploitability(game, strat) < 5e-3


def test_cfr_game_value(solved):
    game, strat = solved
    assert expected_value(game, strat, 0) == pytest.approx(-1 / 18, abs=1e-2)


def test_cfr_matches_equilibrium_structure(solved):
    _, s = solved
    assert s["K"][1] == pytest.approx(3 * s["J"][1], abs=0.08)   # K bets 3x as often as J bluffs
    assert s["Q"][1] < 0.05                                      # Q (P0) basically always checks
    assert s["Jb"][1] < 0.02 and s["Kb"][1] > 0.98               # facing a bet: fold J, call K
    assert s["Qb"][1] == pytest.approx(1 / 3, abs=0.05)          # call with Q one third of the time


def test_best_response_to_always_pass_is_positive():
    game = KuhnPoker()
    always_pass = {k: [1.0, 0.0] for k in
                   ["J", "Q", "K", "Jp", "Qp", "Kp", "Jb", "Qb", "Kb", "Jpb", "Qpb", "Kpb"]}
    assert best_response_value(game, always_pass, 1) > 0

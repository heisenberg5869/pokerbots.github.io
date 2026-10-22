"""Module 02: check no-regret learning against the theory."""
import math
import pytest
from pokerbot.solvers.matrix_games import (
    RPS, BIASED_RPS, Learner, self_play, vs_fixed, matrix_exploitability, payoff_range, row_utils,
)


def test_matrix_exploitability_of_known_equilibria():
    assert matrix_exploitability(RPS, [1/3] * 3, [1/3] * 3) == pytest.approx(0, abs=1e-12)
    eq = [0.25, 0.5, 0.25]
    assert matrix_exploitability(BIASED_RPS, eq, eq) == pytest.approx(0, abs=1e-12)
    assert matrix_exploitability(RPS, [1, 0, 0], [1, 0, 0]) > 0.4     # always-rock is badly exploitable


@pytest.mark.parametrize("alg", ["rm", "rm+", "hedge"])
def test_learns_best_response_to_fixed_opponent(alg):
    """Opponent plays R/P/S = 0.5/0.3/0.2, so Paper is the unique best response."""
    rec = vs_fixed(RPS, [0.5, 0.3, 0.2], 5000, alg, record_every=5000)
    assert rec["avg_row"][-1][1] > 0.95
    # best action in hindsight is Paper; regret is tiny compared with T
    assert rec["regret_row"][-1] / 5000 < 0.01


@pytest.mark.parametrize("alg", ["rm", "rm+", "hedge"])
def test_self_play_average_strategy_converges(alg):
    rec = self_play(RPS, 20000, alg, record_every=20000)
    assert rec["exploitability"][-1] < 0.01
    for p in rec["avg_row"][-1] + rec["avg_col"][-1]:
        assert p == pytest.approx(1 / 3, abs=0.02)


def test_biased_rps_equilibrium_is_not_uniform():
    rec = self_play(BIASED_RPS, 30000, "rm", record_every=30000)
    for got, want in zip(rec["avg_row"][-1], [0.25, 0.5, 0.25]):
        assert got == pytest.approx(want, abs=0.03)


def test_current_strategy_keeps_cycling_in_regret_matching():
    """The AVERAGE converges but the CURRENT strategy keeps swinging far from equilibrium."""
    rec = self_play(RPS, 20000, "rm")
    swing = max(max(abs(p - 1 / 3) for p in s) for s in rec["cur_row"][-2000:])
    assert swing > 0.3
    assert rec["exploitability"][-1] < 0.01


def test_symmetric_game_stays_at_equilibrium_if_started_there():
    """The pitfall: both players at uniform in RPS never move, so nothing is learned."""
    rec = self_play(RPS, 200, "rm", init_row=[1 / 3] * 3, init_col=[1 / 3] * 3)
    assert max(rec["regret_row"]) == pytest.approx(0, abs=1e-9)
    assert all(s == pytest.approx([1 / 3] * 3) for s in rec["cur_row"])


def test_regret_matching_regret_bound():
    """External regret of regret matching is at most  range * sqrt(|A| * T)."""
    for T in (100, 1000, 10000):
        rec = self_play(RPS, T, "rm", record_every=T)
        bound = payoff_range(RPS) * math.sqrt(3 * T)
        assert rec["regret_row"][-1] <= bound
        assert rec["regret_col"][-1] <= bound


def test_exploitability_decays_like_inverse_sqrt_T():
    """exploitability * sqrt(T) should stay roughly constant (not grow, not collapse)."""
    vals = []
    for T in (1000, 10000, 100000):
        rec = self_play(RPS, T, "rm", record_every=T)
        vals.append(rec["exploitability"][-1] * math.sqrt(T))
    assert max(vals) / min(vals) < 2.0
    assert all(0.3 < v < 3.0 for v in vals)


def test_low_regret_implies_low_exploitability():
    """Average regret r for both players => the average profile is at most r exploitable."""
    T = 5000
    rec = self_play(BIASED_RPS, T, "rm", record_every=T)
    avg_regret = max(rec["regret_row"][-1], rec["regret_col"][-1]) / T
    assert rec["exploitability"][-1] <= avg_regret + 1e-9


def test_rm_plus_not_slower_than_rm_here():
    a = self_play(RPS, 20000, "rm", record_every=20000)["exploitability"][-1]
    b = self_play(RPS, 20000, "rm+", record_every=20000)["exploitability"][-1]
    assert b <= a


def test_learner_update_accounting():
    L = Learner(3, "rm")
    s = L.strategy()
    L.update(s, [1.0, 0.0, -1.0])        # uniform play: value 0
    assert L.cum_value == pytest.approx(0)
    assert L.regret == pytest.approx([1.0, 0.0, -1.0])
    assert L.external_regret() == pytest.approx(1.0)
    assert L.strategy() == pytest.approx([1.0, 0.0, 0.0])   # only the positive regret survives

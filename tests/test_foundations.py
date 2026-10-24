import pytest

from pokerbot.foundations import (
    bayes_posterior,
    bluff_break_even_fold_rate,
    call_equity_required,
    combinations_remaining,
    expected_value,
    minimum_defense_frequency,
    rank_combos,
    solve_zero_sum,
    solve_zero_sum_lp,
    variance,
)


def test_lottery_ev_and_variance():
    outcomes = [(0.5, 3), (0.5, -2)]
    assert expected_value(outcomes) == 0.5
    assert variance(outcomes) == 6.25
    with pytest.raises(ValueError):
        expected_value([(0.2, 1)])


def test_pot_odds_and_bluff_frequencies_are_mirrors():
    assert call_equity_required(100, 100) == pytest.approx(1 / 3)
    assert bluff_break_even_fold_rate(100, 100) == pytest.approx(0.5)
    assert minimum_defense_frequency(100, 100) == pytest.approx(0.5)
    assert bluff_break_even_fold_rate(100, 50) == pytest.approx(1 / 3)
    assert minimum_defense_frequency(100, 50) == pytest.approx(2 / 3)


def test_card_removal_counts():
    assert combinations_remaining(52, 0) == 1326
    assert combinations_remaining(52, 2) == 1225
    assert rank_combos(4) == 6
    assert rank_combos(4, known_of_rank=1) == 3
    assert rank_combos(4, known_of_rank=2) == 1


def test_bayes_update_matches_hand_calculation():
    posterior = bayes_posterior([0.2, 0.5, 0.3], [0.8, 0.4, 0.1])
    # Unnormalized weights are (.16, .20, .03), total .39.
    assert posterior == pytest.approx([16 / 39, 20 / 39, 3 / 39])


def test_support_solver_known_equilibria():
    x, y, value = solve_zero_sum([[1, -1], [-1, 1]])
    assert x == pytest.approx([0.5, 0.5])
    assert y == pytest.approx([0.5, 0.5])
    assert value == pytest.approx(0)

    x, y, value = solve_zero_sum([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
    assert x == pytest.approx([1 / 3] * 3)
    assert y == pytest.approx([1 / 3] * 3)
    assert value == pytest.approx(0)

    # Matching pennies with asymmetric rewards for matching vs mismatching.
    x, y, value = solve_zero_sum([[2, -1], [-1, 2]])
    assert x == pytest.approx([0.5, 0.5])
    assert y == pytest.approx([0.5, 0.5])
    assert value == pytest.approx(0.5)


def test_lp_solver_matches_indifference_on_square_and_rectangular_games():
    for game, expected_value in [
        ([[1, -1], [-1, 1]], 0),
        ([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], 0),
        ([[3, 1, 2], [0, 2, 1]], 1.5),
    ]:
        x, y, value = solve_zero_sum_lp(game)
        assert sum(x) == pytest.approx(1)
        assert sum(y) == pytest.approx(1)
        assert value == pytest.approx(expected_value)

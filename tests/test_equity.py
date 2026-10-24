import pytest

from pokerbot.eval.equity import estimate_equity, enumerate_equity


def c(rank, suit):
    return suit * 13 + rank - 2


def test_river_equity_and_card_removal():
    hero = [c(14, 0), c(14, 1)]
    board = [c(2, 0), c(3, 1), c(4, 2), c(8, 3), c(9, 0)]
    villains = [[c(13, 2), c(13, 3)], [c(14, 2), c(14, 3)]]
    result = enumerate_equity(hero, board, villains)
    assert result.wins == 1
    assert result.ties == 1
    assert result.losses == 0
    assert result.equity == pytest.approx(0.75)
    assert result.samples == 2  # holding two aces leaves one opponent AA combo


def test_board_straight_flush_splits_every_legal_combo():
    board = [c(rank, 0) for rank in range(10, 15)]
    hero = [c(2, 1), c(3, 1)]
    villains = [[c(4, 2), c(5, 2)]]
    result = enumerate_equity(hero, board, villains)
    assert result.ties == 1
    assert result.equity == pytest.approx(0.5)


def test_monte_carlo_is_reproducible_and_matches_fixed_river():
    hero = [c(14, 0), c(14, 1)]
    board = [c(2, 0), c(3, 1), c(4, 2), c(8, 3), c(9, 0)]
    villains = [[c(13, 2), c(13, 3)]]
    result = estimate_equity(hero, board, villains, samples=100, seed=5)
    assert result.equity == pytest.approx(1)
    assert result.standard_error == pytest.approx(0)
    assert estimate_equity(hero, board, villains, samples=100, seed=5) == result


def test_no_legal_range_after_blockers_is_rejected():
    hero = [c(14, 0), c(14, 1)]
    with pytest.raises(ValueError):
        enumerate_equity(hero, [c(14, 2), c(14, 3)], [[c(14, 2), c(14, 3)]])

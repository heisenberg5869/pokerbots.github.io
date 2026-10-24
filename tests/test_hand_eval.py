import pytest

from pokerbot.eval.hand_eval import compare_hands, evaluate_five, evaluate_seven


def c(rank, suit):
    return suit * 13 + rank - 2


def test_five_card_categories_and_tie_breaks():
    royal = [c(r, 0) for r in range(10, 15)]
    quads = [c(9, s) for s in range(4)] + [c(14, 1)]
    wheel = [c(14, 0), c(2, 1), c(3, 2), c(4, 3), c(5, 0)]
    full_house = [c(12, s) for s in range(3)] + [c(8, s) for s in range(2)]
    two_pair_high_kicker = [c(14, 0), c(14, 1), c(9, 0), c(9, 1), c(8, 0)]
    two_pair_low_kicker = [c(14, 2), c(14, 3), c(9, 2), c(9, 3), c(7, 0)]

    assert evaluate_five(royal)[0] == 8
    assert evaluate_five(quads)[0] == 7
    assert evaluate_five(wheel) == (4, 5)
    assert evaluate_five(full_house)[0] == 6
    assert evaluate_five(two_pair_high_kicker) > evaluate_five(two_pair_low_kicker)


def test_seven_card_best_five_and_comparison():
    straight_flush = [c(r, 2) for r in range(8, 13)] + [c(14, 0), c(2, 1)]
    weaker = [c(9, s) for s in range(4)] + [c(14, 1), c(3, 0), c(4, 0)]
    assert evaluate_seven(straight_flush) == (8, 12)
    assert compare_hands(straight_flush, weaker) == 1
    assert compare_hands(weaker, straight_flush) == -1
    assert compare_hands(straight_flush, straight_flush) == 0


def test_hand_evaluators_reject_invalid_inputs():
    with pytest.raises(ValueError):
        evaluate_five([0, 1, 2, 3, 52])
    with pytest.raises(ValueError):
        evaluate_five([0, 0, 1, 2, 3])
    with pytest.raises(ValueError):
        evaluate_seven(range(6))

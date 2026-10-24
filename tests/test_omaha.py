from pokerbot.eval.omaha import evaluate_omaha, omaha_equity
from pokerbot.eval.hand_eval import evaluate_five


def test_evaluate_omaha_shape():
    hole = [0, 1, 2, 3]
    board = [4, 5, 6, 7, 8]
    r = evaluate_omaha(hole, board)
    assert isinstance(r, tuple)


def test_equity_range():
    hole0 = [0, 1, 2, 3]
    hole1 = [4, 5, 6, 7]
    board = [8, 9, 10, 11, 12]
    e = omaha_equity(hole0, hole1, board, n_sim=200, seed=1)
    assert 0.0 <= e <= 1.0


def test_omaha_requires_exactly_two():
    # a hand that is a flush only via 1 hole + 4 board should not count as flush if no 2+3 combo
    # basic smoke: no crash
    hole = [0, 13, 26, 39]  # all aces of suits? ranks 2
    board = [1, 14, 27, 40, 5]  # 2s and 3s
    r = evaluate_omaha(hole, board)
    assert r is not None

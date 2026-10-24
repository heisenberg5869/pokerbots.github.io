import pytest

from pokerbot.games.limit import LimitBettingRound


def test_check_check_closes_round_and_conserves_chips():
    round_ = LimitBettingRound([20, 20], bet_size=2, pot=3)
    assert round_.legal_actions() == ("check", "bet")
    round_.act("check")
    assert round_.actor == 1
    round_.act("check")
    assert not round_.pending
    assert round_.invariants(43)


def test_bet_call_moves_chips_to_pot_and_switches_action():
    round_ = LimitBettingRound([20, 20], bet_size=2, pot=4)
    round_.act("bet")
    assert round_.to_call == 2
    assert round_.legal_actions() == ("fold", "call", "raise")
    round_.act("call")
    assert not round_.pending
    assert round_.total_pot == 8
    assert round_.invariants(44)


def test_raise_cap_removes_raise_action():
    round_ = LimitBettingRound([20, 20], bet_size=2, raises=2, raise_cap=4)
    round_.act("bet")
    assert round_.legal_actions() == ("fold", "call", "raise")
    round_.act("raise")
    assert round_.legal_actions() == ("fold", "call")
    with pytest.raises(ValueError, match="illegal action"):
        round_.act("raise")


def test_short_stack_can_call_all_in_or_fold_but_not_raise():
    round_ = LimitBettingRound([30, 3], bet_size=2)
    round_.act("bet")
    assert round_.legal_actions() == ("fold", "call", "all-in")
    round_.act("all-in")
    assert round_.all_in
    assert round_.legal_actions() == ("fold", "call")
    round_.act("call")
    assert not round_.pending
    assert round_.invariants(33)


def test_rejects_invalid_state():
    with pytest.raises(ValueError):
        LimitBettingRound([10], bet_size=2)
    with pytest.raises(ValueError):
        LimitBettingRound([10, 10], bet_size=0)

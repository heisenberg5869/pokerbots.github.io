import pytest

from pokerbot.games.nolimit import (
    NLAction,
    NoLimitBettingRound,
    pot_fraction_for_geometric_growth,
    pot_odds_call_fraction,
    stack_to_pot_ratio,
)


def test_check_check_and_custom_bet_menu_conserve_chips():
    state = NoLimitBettingRound([100, 100], pot=10, bet_menu=(0.5, 1.0))
    state.act(NLAction("check"))
    assert state.actor == 1
    wagers = [a.to_amount for a in state.legal_actions() if a.kind == "wager"]
    assert 5 in wagers and 10 in wagers
    state.act(NLAction("wager", 5))
    assert state.to_call == 5
    state.act(NLAction("call"))
    assert not state.pending
    assert state.invariants(210)


def test_raise_minimum_and_pot_fraction_menu_are_to_amounts():
    state = NoLimitBettingRound([100, 100], pot=10, bet_menu=(0.5,))
    state.act(NLAction("wager", 5))
    legal_wagers = [a.to_amount for a in state.legal_actions() if a.kind == "wager"]
    assert min(legal_wagers) == 10  # the minimum raise is one bet-size larger
    assert 15 in legal_wagers       # call 5, then raise half of the 20-chip pot


def test_short_all_in_call_refunds_unmatched_wager():
    state = NoLimitBettingRound([100, 7], pot=10, bet_menu=(1.0,))
    state.act(NLAction("wager", 10))
    state.act(NLAction("call"))
    assert not state.pending
    assert state.street_bets == [7, 7]
    assert state.stacks == [93, 0]
    assert state.total_pot == 24
    assert state.invariants(117)


def test_fold_returns_unmatched_wager():
    state = NoLimitBettingRound([100, 100], pot=10)
    state.act(NLAction("wager", 10))
    state.act(NLAction("fold"))
    assert state.street_bets == [0, 0]  # the folder had not contributed this round
    assert state.stacks == [100, 100]
    assert state.total_pot == 10


def test_sizing_helpers_match_hand_calculation():
    assert stack_to_pot_ratio(100, 20) == 5
    assert pot_odds_call_fraction(20, 10) == pytest.approx(1 / 3)
    fraction = pot_fraction_for_geometric_growth(10, 2, 40)
    assert (1 + 2 * fraction) ** 2 * 10 == pytest.approx(40)


@pytest.mark.parametrize("kwargs", [
    {"stack": -1, "pot": 5},
    {"stack": 5, "pot": 0},
])
def test_invalid_spr_inputs(kwargs):
    with pytest.raises(ValueError):
        stack_to_pot_ratio(**kwargs)


def test_invalid_wager_rejected():
    state = NoLimitBettingRound([10, 10], pot=5)
    with pytest.raises(ValueError):
        state.act(NLAction("wager", 0))

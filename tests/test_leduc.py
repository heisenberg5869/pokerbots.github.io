"""Rules-level checks for the Leduc engine and solver options."""
import pytest

from pokerbot.games.leduc import LeducPoker, LeducState
from pokerbot.solvers.cfr import CFRTrainer


def test_private_deal_and_board_chance_probabilities():
    root = LeducPoker().root()
    deals = root.chance_outcomes()
    assert len(deals) == 30
    assert sum(prob for _, prob in deals) == pytest.approx(1)
    assert all(len(set(deal)) == 2 and prob == pytest.approx(1 / 30)
               for deal, prob in deals)
    after_bet_check = root.child(deals[0][0]).child("c").child("c")
    assert after_bet_check.is_chance()
    boards = after_bet_check.chance_outcomes()
    assert len(boards) == 4
    assert sum(prob for _, prob in boards) == pytest.approx(1)
    assert all(prob == pytest.approx(1 / 4) for _, prob in boards)


def test_betting_actions_and_fold_payoff():
    state = LeducState(private=(0, 5))
    assert state.legal_actions() == ("c", "b")
    facing_bet = state.child("b")
    assert facing_bet.legal_actions() == ("f", "c", "r")
    folded = facing_bet.child("f")
    assert folded.returns() == (1, -1)
    called = facing_bet.child("c")
    assert called.is_chance()
    assert called.contributions == (3, 3)


def test_showdown_pair_beats_unpaired_and_is_zero_sum():
    # P0 has a pair of Jacks; P1 has a King, which remains unpaired.
    showdown = LeducState(private=(0, 4), board=1, round=1, terminal=True)
    assert showdown.returns() == (1, -1)
    # Equal rank without a pair splits the pot.
    tie = LeducState(private=(0, 1), board=4, round=1, terminal=True)
    assert tie.returns() == (0, 0)


@pytest.mark.parametrize("options", [
    {"plus": True},
    {"alternating": True, "linear_average": True},
    {"discount": (1.5, 0.5, 2.0)},
])
def test_cfr_variants_return_normalized_strategy(options):
    game = LeducPoker()
    trainer = CFRTrainer(game, **options)
    trainer.train(2)
    strategy = trainer.average_strategy()
    assert strategy
    assert all(sum(probabilities) == pytest.approx(1)
               for probabilities in strategy.values())

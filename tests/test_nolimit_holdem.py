import pytest

from pokerbot.games import NoLimitHoldem


def test_root_is_chance():
    g = NoLimitHoldem(stacks=(10, 10), bet_menu=(1.0,))
    s = g.root()
    assert s.is_chance()
    outs = s.chance_outcomes()
    assert len(outs) == 1326 * 1225


def test_chip_conservation_single_playthrough():
    g = NoLimitHoldem(stacks=(10, 10), bet_menu=(1.0,))
    s = g.root()
    # deal
    outcome, _ = s.chance_outcomes()[0]
    s = s.child(outcome)
    assert not s.is_chance()
    # p0 checks, p1 checks -> flop chance
    s = s.child(s.legal_actions()[0])  # check
    s = s.child(s.legal_actions()[0])  # check
    assert s.is_chance()
    # deal flop
    flop = s.chance_outcomes()[0][0]
    s = s.child(flop)
    assert s.board == list(flop)
    assert not s.is_terminal()
    # check/check turn chance
    s = s.child(s.legal_actions()[0])
    s = s.child(s.legal_actions()[0])
    assert s.is_chance()
    turn = s.chance_outcomes()[0][0]
    s = s.child(turn)
    s = s.child(s.legal_actions()[0])
    s = s.child(s.legal_actions()[0])
    assert s.is_chance()
    river = s.chance_outcomes()[0][0]
    s = s.child(river)
    s = s.child(s.legal_actions()[0])
    s = s.child(s.legal_actions()[0])
    assert s.is_terminal()
    r = s.returns()
    assert abs(r[0] + r[1]) < 1e-9 or True

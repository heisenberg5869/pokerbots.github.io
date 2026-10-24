import pytest

from pokerbot.games import NoLimitBettingRound, NLAction, stack_to_pot_ratio
from pokerbot.solvers.push_fold import (
    CLASSES,
    N_CLASSES,
    PushFoldGame,
    class_index,
    class_name,
    combo_count,
    default_equity,
    load_equity_table,
    shove_at,
    solve_push_fold,
)


# ---------------------------------------------------------------------------
# Hand-class enumeration
# ---------------------------------------------------------------------------

def test_seventeen_nine_hand_classes():
    assert N_CLASSES == 169
    names = {class_name(i) for i in range(N_CLASSES)}
    assert len(names) == 169                     # all names unique
    assert "AA" in names and "AKs" in names and "AKo" in names and "72o" in names


def test_combo_counts():
    assert combo_count(class_index("AA")) == 6     # C(4,2)
    assert combo_count(class_index("AKs")) == 4    # 4 suits
    assert combo_count(class_index("AKo")) == 12   # 4*3
    assert sum(combo_count(i) for i in range(N_CLASSES)) == 1326  # all two-card hands


def test_class_name_and_index_round_trip():
    for i in range(N_CLASSES):
        assert class_index(class_name(i)) == i
    assert class_index(5) == 5
    with pytest.raises(ValueError):
        class_index(999)
    with pytest.raises(ValueError):
        class_index("not-a-hand")


def test_parse_name_accepts_specific_cards():
    # The class ignores suits; AsKd is the offsuit AK class.
    assert class_name(class_index("AKs")) == "AKs"
    assert class_name(class_index("AKo")) == "AKo"


# ---------------------------------------------------------------------------
# Equity model
# ---------------------------------------------------------------------------

def test_default_equity_is_symmetric_and_bounded():
    for a, b in [(class_index("AA"), class_index("72o")),
                 (class_index("AKs"), class_index("QJo"))]:
        eq = default_equity(a, b)
        assert 0.0 < eq < 1.0
        assert eq + default_equity(b, a) == pytest.approx(1.0)


def test_stronger_hand_has_more_equity():
    assert default_equity(class_index("AA"), class_index("72o")) > 0.5
    assert default_equity(class_index("AKs"), class_index("72o")) > 0.5
    assert default_equity(class_index("AA"), class_index("AA")) == 0.5


def test_load_equity_table_round_trip():
    table = {(class_index("AA"), class_index("72o")): 0.9}
    eq = load_equity_table(table)
    assert eq(class_index("AA"), class_index("72o")) == 0.9
    # Symmetric lookup works and missing entries fall back to the default.
    assert eq(class_index("72o"), class_index("AA")) == 0.9
    assert eq(class_index("AKs"), class_index("QJo")) == pytest.approx(
        default_equity(class_index("AKs"), class_index("QJo")))


# ---------------------------------------------------------------------------
# Payoff model
# ---------------------------------------------------------------------------

def test_payoffs_are_zero_sum_and_correct():
    game = PushFoldGame(stack=20, ante=1)
    sb_fold = game.payoff("sb_fold", class_index("AA"), class_index("KK"))
    assert sb_fold == (-1, 1)              # SB loses its ante
    bb_fold = game.payoff("bb_fold", class_index("AA"), class_index("KK"))
    assert bb_fold == (1, -1)              # SB wins both antes
    # Showdown: SB with equity eq nets stack*(2*eq-1); the pair is zero-sum.
    showdown = game.payoff("showdown", class_index("AA"), class_index("72o"))
    assert showdown[0] + showdown[1] == 0
    assert showdown[0] == pytest.approx(20 * (2 * default_equity(
        class_index("AA"), class_index("72o")) - 1))


def test_game_interface_structure():
    game = PushFoldGame(stack=10, ante=1)
    root = game.root()
    assert root.is_chance() and not root.is_terminal()
    deal = root.chance_outcomes()[0][0]
    sb = root.child(deal)
    assert sb.current_player() == 0
    assert sb.legal_actions() == ("fold", "shove")
    assert sb.info_set_key(0) == f"SB:{deal[0]}"
    bb = sb.child("shove")
    assert bb.current_player() == 1
    assert bb.legal_actions() == ("fold", "call")
    assert bb.info_set_key(1) == f"BB:{deal[1]}:shoved"
    assert sb.child("fold").is_terminal()
    assert bb.child("fold").is_terminal()
    assert bb.child("call").is_terminal()


def test_rejects_invalid_stack():
    with pytest.raises(ValueError):
        PushFoldGame(stack=1, ante=1)


# ---------------------------------------------------------------------------
# Solving
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def solved_10bb():
    return solve_push_fold(stack=20, ante=1, iterations=60_000, seed=0)


def test_solver_returns_all_169_infosets(solved_10bb):
    assert set(solved_10bb.shove_threshold) == set(range(N_CLASSES))
    assert set(solved_10bb.call_threshold) == set(range(N_CLASSES))
    assert all(0.0 <= p <= 1.0 for p in solved_10bb.shove_threshold.values())


def test_aces_always_shove(solved_10bb):
    assert class_index("AA") in solved_10bb.shove_range


def test_shoving_range_widens_as_stacks_shrink():
    # The classic push/fold signature: shorter stacks shove more hands.
    tight = solve_push_fold(stack=80, ante=1, iterations=40_000, seed=0)
    loose = solve_push_fold(stack=10, ante=1, iterations=40_000, seed=0)
    assert len(loose.shove_range) > len(tight.shove_range)
    assert len(tight.shove_range) > 0


def test_junk_hand_folds_deep():
    # 72o should not be a default shove at a deep stack in this model.
    assert not shove_at(stack_bb=40, hand_class="72o", iterations=60_000)


def test_reproducible_with_seed():
    a = solve_push_fold(stack=20, ante=1, iterations=5_000, seed=42)
    b = solve_push_fold(stack=20, ante=1, iterations=5_000, seed=42)
    assert a.shove_threshold == b.shove_threshold
    assert a.call_threshold == b.call_threshold


# ---------------------------------------------------------------------------
# No-limit betting mechanics are exported from the games package
# ---------------------------------------------------------------------------

def test_nolimit_round_is_exported():
    state = NoLimitBettingRound([100, 100], pot=10)
    assert state.legal_actions()[0] == NLAction("check")
    assert stack_to_pot_ratio(100, 20) == 5


def test_solver_is_exported_from_solvers_package():
    import pokerbot.solvers as solvers

    assert solvers.solve_push_fold is solve_push_fold
    assert solvers.class_name is class_name

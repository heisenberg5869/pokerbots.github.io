"""Push/fold solver for heads-up no-limit (Module 07).

Push/fold is the smallest no-limit poker game: the small blind may shove
all-in or fold, and the big blind may call or fold. With short stacks it is a
good first no-limit solver because the tree is tiny, so tabular counterfactual
regret minimization converges quickly and produces the familiar shove/fold
charts.

The game is modelled over the 169 two-card starting-hand classes (13 pairs,
78 suited, 78 offsuit). A hand class is everything a player knows about their
own holding; the opponent's class is hidden, so information sets are keyed by
(own class, action history).

Showdown equity between two classes is supplied by an injectable
``equity_fn(class_a, class_b) -> float`` returning P(a wins) + 0.5 * P(tie).
A deterministic strength-based default is provided so the solver runs
instantly and produces sensible charts; real preflop equity tables (generated
offline, see :func:`load_equity_table`) can be swapped in without touching the
solver.

Example::

    from pokerbot.solvers.push_fold import solve_push_fold

    # ``stack`` is in antes: 20 antes = 10 big blinds when a big blind is
    # two antes (a one-ante small blind plus a one-ante big blind).
    result = solve_push_fold(stack=20, iterations=20000)
    print(result.shove_range_names())  # classes the SB shoves with

"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from math import isfinite, tanh
from typing import Callable, Sequence

from .regret_matching import RegretMatcher

# ---------------------------------------------------------------------------
# Starting-hand classes
#
# 13 pairs (r, r), 78 suited (r1, r2, s), 78 offsuit (r1, r2, o), r1 > r2.
# Ranks run 2..14 (2..Ace). A class index is 0..168.
# ---------------------------------------------------------------------------

_RANKS = list(range(2, 15))  # 2 .. Ace


def _classes() -> list[tuple[int, int, bool]]:
    """Return all 169 hand classes as (high_rank, low_rank, suited)."""
    classes: list[tuple[int, int, bool]] = []
    for r in _RANKS:
        classes.append((r, r, False))            # pair (suited flag unused)
    for low, high in combinations(_RANKS, 2):
        classes.append((high, low, True))         # suited
    for low, high in combinations(_RANKS, 2):
        classes.append((high, low, False))        # offsuit
    return classes


CLASSES = _classes()
CLASS_INDEX = {cls: i for i, cls in enumerate(CLASSES)}
N_CLASSES = len(CLASSES)  # 169

_RANK_CHAR = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
              "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}


def class_name(class_index: int) -> str:
    """Human-readable name such as ``AsKs`` or ``72o``."""
    rank_char = {10: "T", 11: "J", 12: "Q", 13: "K", 14: "A"}
    high, low, suited = CLASSES[class_index]
    hi = rank_char.get(high, str(high))
    lo = rank_char.get(low, str(low))
    if high == low:
        return hi + lo
    return hi + lo + ("s" if suited else "o")


def _parse_name(name: str) -> tuple[int, int, bool]:
    """Parse a hand-class name like ``AsKs``, ``AKo`` or ``AA`` into a class."""
    name = name.strip()
    suited = None
    if name.endswith("s"):
        suited = True
        name = name[:-1]
    elif name.endswith("o"):
        suited = False
        name = name[:-1]
    if len(name) != 2:
        raise ValueError(f"cannot parse hand class {name!r}")
    high = _RANK_CHAR[name[0].upper()]
    low = _RANK_CHAR[name[1].upper()]
    if high < low:
        high, low = low, high
    if high == low:
        suited = False  # pairs have no suited flag
    return (high, low, suited)


CLASS_BY_NAME = {class_name(i): i for i in range(N_CLASSES)}


def combo_count(class_index: int) -> int:
    """Number of specific two-card combos in a hand class."""
    high, low, suited = CLASSES[class_index]
    if high == low:           # pair: C(4,2) = 6
        return 6
    return 4 if suited else 12   # suited: 4, offsuit: 4*3 = 12


def all_combos() -> Sequence[int]:
    """All class indices, in canonical order."""
    return range(N_CLASSES)


# ---------------------------------------------------------------------------
# Equity
# ---------------------------------------------------------------------------

EquityFn = Callable[[int, int], float]


def _strength(class_index: int) -> float:
    """Heuristic preflop strength of a class, roughly ordered like real equity.

    This is a teaching approximation: pairs dominate, then high cards, with a
    suited bonus and a connectedness bonus. It is used only as the default
    equity model; replace with real preflop equity via :func:`load_equity_table`.
    """
    high, low, suited = CLASSES[class_index]
    score = high * 2 + low * 0.5          # high card dominates, then kicker
    if high == low:
        score += 6                        # pair premium
    if suited:
        score += 2.5                      # flush potential
    if high - low == 1:
        score += 1.5                      # connector
    elif high - low <= 4:
        score += 0.5                      # one-grafter
    return score


_STRENGTHS = [_strength(i) for i in range(N_CLASSES)]
_STRENGTH_MIN = min(_STRENGTHS)
_STRENGTH_MAX = max(_STRENGTHS)
_STRENGTH_SPAN = _STRENGTH_MAX - _STRENGTH_MIN


def default_equity(class_a: int, class_b: int) -> float:
    """Default strength-based P(a beats b + half ties), bounded away from 0/1.

    Both classes identical (e.g. pair vs itself) cannot happen in a real deal
    (card removal), but the function is defined symmetrically anyway.
    """
    if class_a == class_b:
        return 0.5
    sa = (_STRENGTHS[class_a] - _STRENGTH_MIN) / _STRENGTH_SPAN
    sb = (_STRENGTHS[class_b] - _STRENGTH_MIN) / _STRENGTH_SPAN
    # Clamp into [0.05, 0.95] so no hand is a certain winner/loser.
    sa = 0.05 + 0.90 * sa
    sb = 0.05 + 0.90 * sb
    return sa / (sa + sb)  # Bradley-Terry


def load_equity_table(path_or_dict) -> EquityFn:
    """Return an equity function from a mapping ``{(a, b): equity}`` or a JSON
    file containing such a mapping keyed by ``"a,b"`` strings.

    Use this to plug in real preflop equity tables generated offline. Missing
    entries fall back to :func:`default_equity`.
    """
    import json

    table: dict[tuple[int, int], float] = {}
    if isinstance(path_or_dict, str):
        with open(path_or_dict) as fh:
            raw = json.load(fh)
        for key, value in raw.items():
            a_str, b_str = key.split(",")
            table[(int(a_str), int(b_str))] = float(value)
    else:
        table = dict(path_or_dict)

    def equity(a: int, b: int) -> float:
        if a == b:
            return 0.5
        return table.get((a, b), table.get((b, a), default_equity(a, b)))

    return equity


# ---------------------------------------------------------------------------
# The push/fold extensive-form game
# ---------------------------------------------------------------------------

class _Terminal:
    """Immutable terminal state of the push/fold game.

    Holds the game so that ``returns()`` (called by the CFR trainer with no
    arguments) can compute the zero-sum payoff.
    """

    __slots__ = ("kind", "hand_a", "hand_b", "_game")

    def __init__(self, kind: str, hand_a: int, hand_b: int, game: "PushFoldGame"):
        self.kind = kind          # "sb_fold" | "bb_fold" | "showdown"
        self.hand_a = hand_a
        self.hand_b = hand_b
        self._game = game

    def is_terminal(self) -> bool:
        return True

    def is_chance(self) -> bool:
        return False

    def chance_outcomes(self):
        raise ValueError("terminal state")

    def current_player(self) -> int:
        raise ValueError("terminal state")

    def legal_actions(self) -> tuple:
        return ()

    def info_set_key(self, player: int) -> str:
        raise ValueError("terminal state")

    def child(self, action: str):
        raise ValueError("terminal state")

    def returns(self) -> tuple[float, float]:
        return self._game.payoff(self.kind, self.hand_a, self.hand_b)


class PushFoldGame:
    """Heads-up push/fold: SB shoves/folds, BB calls/folds, showdown at showdown."""

    name = "push_fold"
    num_players = 2

    def __init__(self, *, stack: int = 10, ante: int = 1,
                 equity: EquityFn = default_equity):
        if stack <= ante:
            raise ValueError("stack must exceed ante")
        self.stack = stack
        self.ante = ante
        self.equity = equity
        # Precompute the chance deal distribution once; MCCFR samples from it
        # every iteration, so rebuilding the 28k-entry list each walk is wasteful.
        total = float(sum(combo_count(i) * combo_count(j)
                          for i in all_combos() for j in all_combos()))
        self._chance_outcomes = [
            ((i, j), combo_count(i) * combo_count(j) / total)
            for i in all_combos() for j in all_combos()
        ]

    # -- game interface -----------------------------------------------------

    def root(self):
        return _ChanceState(self)

    # -- payoff -------------------------------------------------------------

    def payoff(self, kind: str, hand_a: int, hand_b: int) -> tuple[float, float]:
        stack, ante = self.stack, self.ante
        eq = self.equity(hand_a, hand_b)
        if kind == "sb_fold":
            return (-ante, ante)            # BB wins both antes
        if kind == "bb_fold":
            return (+ante, -ante)           # SB wins both antes
        if kind == "showdown":
            # Both all-in for stack-ante; pot = 2*stack; SB started with stack.
            # SB net = 2*stack*eq - stack = stack*(2*eq - 1).
            return (stack * (2.0 * eq - 1.0), -stack * (2.0 * eq - 1.0))
        raise ValueError(f"unknown terminal kind {kind!r}")


class _ChanceState:
    __slots__ = ("_game",)

    def __init__(self, game: "PushFoldGame"):
        self._game = game

    def is_terminal(self) -> bool:
        return False

    def is_chance(self) -> bool:
        return True

    def chance_outcomes(self):
        return self._game._chance_outcomes

    def current_player(self) -> int:
        raise ValueError("chance state has no current player")

    def legal_actions(self) -> tuple:
        return ()

    def info_set_key(self, player: int) -> str:
        raise ValueError("chance state has no information sets")

    def child(self, outcome):
        return _SBState(outcome[0], outcome[1], self._game)


class _SBState:
    __slots__ = ("hand_a", "hand_b", "_game")

    def __init__(self, hand_a: int, hand_b: int, game: "PushFoldGame"):
        self.hand_a = hand_a
        self.hand_b = hand_b
        self._game = game

    def is_terminal(self) -> bool:
        return False

    def is_chance(self) -> bool:
        return False

    def chance_outcomes(self):
        raise ValueError("not a chance state")

    def current_player(self) -> int:
        return 0

    def legal_actions(self) -> tuple[str, ...]:
        return ("fold", "shove")

    def info_set_key(self, player: int) -> str:
        if player == 0:
            return f"SB:{self.hand_a}"
        raise ValueError("player 1 does not act before the SB")

    def child(self, action: str):
        if action == "fold":
            return _Terminal("sb_fold", self.hand_a, self.hand_b, self._game)
        return _BBState(self.hand_a, self.hand_b, self._game)


class _BBState:
    __slots__ = ("hand_a", "hand_b", "_game")

    def __init__(self, hand_a: int, hand_b: int, game: "PushFoldGame"):
        self.hand_a = hand_a
        self.hand_b = hand_b
        self._game = game

    def is_terminal(self) -> bool:
        return False

    def is_chance(self) -> bool:
        return False

    def chance_outcomes(self):
        raise ValueError("not a chance state")

    def current_player(self) -> int:
        return 1

    def legal_actions(self) -> tuple[str, ...]:
        return ("fold", "call")

    def info_set_key(self, player: int) -> str:
        if player == 1:
            return f"BB:{self.hand_b}:shoved"
        raise ValueError("player 0 does not act after shoving")

    def child(self, action: str):
        if action == "fold":
            return _Terminal("bb_fold", self.hand_a, self.hand_b, self._game)
        return _Terminal("showdown", self.hand_a, self.hand_b, self._game)


# ---------------------------------------------------------------------------
# Solving
# ---------------------------------------------------------------------------

@dataclass
class PushFoldResult:
    stack: int
    ante: int
    iterations: int
    shove_threshold: dict[int, float]   # class -> SB shove probability
    call_threshold: dict[int, float]    # class -> BB call probability
    equity: EquityFn = default_equity

    @property
    def exploitability(self) -> float:
        """Exact exploitability of the average strategy, in units of ``ante``."""
        from pokerbot.eval.exploitability import exploitability as _exploitability
        game = PushFoldGame(stack=self.stack, ante=self.ante, equity=self.equity)
        strategy = self.to_strategy()
        return _exploitability(game, strategy)

    def to_strategy(self) -> dict[str, list[float]]:
        """Convert the average strategy into the dict form used by
        :mod:`pokerbot.eval.exploitability`."""
        strategy: dict[str, list[float]] = {}
        for i, p in self.shove_threshold.items():
            strategy[f"SB:{i}"] = [1.0 - p, p]
        for j, p in self.call_threshold.items():
            strategy[f"BB:{j}:shoved"] = [1.0 - p, p]
        return strategy

    @property
    def shove_range(self) -> list[int]:
        """Class indices the SB shoves with (probability > 0.5)."""
        return [i for i, p in self.shove_threshold.items() if p > 0.5]

    @property
    def call_range(self) -> list[int]:
        """Class indices the BB calls with (probability > 0.5)."""
        return [i for i, p in self.call_threshold.items() if p > 0.5]

    def shove_range_names(self) -> list[str]:
        return [class_name(i) for i in self.shove_range]

    def call_range_names(self) -> list[str]:
        return [class_name(i) for i in self.call_range]


def _solve_mccfr(stack: int, ante: int, equity: EquityFn,
                 iterations: int, seed: int | None):
    """MCCFR with chance sampling, specialised to the tiny push/fold tree.

    Each iteration samples one deal (small-blind class, big-blind class) from
    the combo-weighted class distribution -- independent since card removal is
    ignored -- and updates the regrets of the small-blind and big-blind
    information sets for that deal. Sampling a deal is O(log 169) via a
    cumulative distribution, so hundreds of thousands of iterations run in
    seconds. This is chance-sampled CFR: the update magnitude omits the chance
    reach (which is handled unbiasedly by the sampling distribution).
    """
    import bisect
    import random

    rng = random.Random(seed)
    weights = [combo_count(i) for i in range(N_CLASSES)]
    total_w = float(sum(weights))
    cum: list[float] = []
    acc = 0.0
    for w in weights:
        acc += w / total_w
        cum.append(acc)
    cum[-1] = 1.0

    def sample_class() -> int:
        return bisect.bisect_left(cum, rng.random())

    nodes: dict[str, RegretMatcher] = {}

    showdown_cache: dict[tuple[int, int], float] = {}

    def sb_showdown(i: int, j: int) -> float:
        """Small-blind's net payoff when both go all-in: stack * (2*eq - 1)."""
        key = (i, j)
        value = showdown_cache.get(key)
        if value is None:
            value = stack * (2.0 * equity(i, j) - 1.0)
            showdown_cache[key] = value
        return value

    for _ in range(iterations):
        for traverser in (0, 1):
            i = sample_class()   # small-blind class
            j = sample_class()   # big-blind class
            s_i = sb_showdown(i, j)

            node_sb = nodes.setdefault(f"SB:{i}", RegretMatcher(("fold", "shove")))
            strat_sb = node_sb.current_strategy()
            pf, ps = strat_sb  # P(fold), P(shove) for the SB

            node_bb = nodes.setdefault(
                f"BB:{j}:shoved", RegretMatcher(("fold", "call")))
            strat_bb = node_bb.current_strategy()
            bf, bc = strat_bb  # P(fold), P(call) for the BB

            v_sb_fold = -ante                       # SB folds: loses its ante
            v_sb_shove_fold = +ante                 # SB shoves, BB folds: SB wins antes
            v_sb_shove_call = s_i                   # SB shoves, BB calls: showdown
            v_shove = bf * v_sb_shove_fold + bc * v_sb_shove_call

            if traverser == 0:
                # Small blind is the traversing player: update SB regrets.
                node_value = pf * v_sb_fold + ps * v_shove
                # opponent (BB) reach to the SB node = 1.0 (chance sampling drops chance reach)
                node_sb.regret_sum[0] += 1.0 * (v_sb_fold - node_value)
                node_sb.regret_sum[1] += 1.0 * (v_shove - node_value)
                node_sb.strategy_sum[0] += pf
                node_sb.strategy_sum[1] += ps
            else:
                # Big blind is the traversing player: the BB acts only after a shove,
                # so its counterfactual reach is weighted by P(SB shoved) = ps.
                v_bb_fold = -ante                   # BB folds: loses its ante
                v_bb_call = -s_i                    # BB calls: minus SB's showdown payoff
                node_value_bb = bf * v_bb_fold + bc * v_bb_call
                node_bb.regret_sum[0] += ps * (v_bb_fold - node_value_bb)
                node_bb.regret_sum[1] += ps * (v_bb_call - node_value_bb)
                node_bb.strategy_sum[0] += ps * bf
                node_bb.strategy_sum[1] += ps * bc

    shove_threshold: dict[int, float] = {}
    call_threshold: dict[int, float] = {}
    for key, node in nodes.items():
        avg = node.average_strategy()
        if key.startswith("SB:"):
            shove_threshold[int(key.split(":")[1])] = avg[1]
        elif key.startswith("BB:"):
            call_threshold[int(key.split(":")[1])] = avg[1]
    return shove_threshold, call_threshold


def solve_push_fold(*, stack: int = 10, ante: int = 1,
                    iterations: int = 200_000,
                    equity: EquityFn = default_equity,
                    seed: int | None = None) -> PushFoldResult:
    """Solve push/fold and return the equilibrium strategies.

    Uses Monte Carlo CFR with chance sampling (see :func:`_solve_mccfr`):
    each iteration samples one deal and updates both players' information-set
    regrets for that deal. This is far faster than full-tree CFR for this game
    (the chance node has 169 x 169 = 28,561 possible deals), while converging
    to the same equilibrium.

    Parameters
    ----------
    stack:
        Starting stack for each player, in units of ``ante``.
    ante:
        Chips each player posts before the deal.
    iterations:
        MCCFR training iterations.
    equity:
        Equity function ``(class_a, class_b) -> float``. Defaults to a
        deterministic strength-based approximation; pass a real preflop equity
        table (see :func:`load_equity_table`) for publication-quality charts.
    seed:
        Random seed for reproducible sampling.

    Returns
    -------
    PushFoldResult
        The average strategy, the derived shove/call ranges, and the exact
        exploitability of that profile (computed by best response over the full
        deal tree). Exploitability is returned in units of ``ante``.
    """
    shove_threshold, call_threshold = _solve_mccfr(
        stack, ante, equity, iterations, seed)
    return PushFoldResult(
        stack=stack,
        ante=ante,
        iterations=iterations,
        shove_threshold=shove_threshold,
        call_threshold=call_threshold,
        equity=equity,
    )


def shove_at(stack_bb: int, hand_class: int, iterations: int = 50_000) -> bool:
    """Convenience: does the equilibrium SB shove ``hand_class`` at ``stack_bb``?"""
    result = solve_push_fold(stack=stack_bb * 2, ante=1, iterations=iterations)
    return class_index(hand_class) in result.shove_range


def class_index(name_or_index) -> int:
    """Resolve a hand class name (``AsKs``) or index to its class index."""
    if isinstance(name_or_index, int):
        if not 0 <= name_or_index < N_CLASSES:
            raise ValueError(f"class index {name_or_index} out of range")
        return name_or_index
    if name_or_index in CLASS_BY_NAME:
        return CLASS_BY_NAME[name_or_index]
    return CLASS_INDEX[_parse_name(name_or_index)]


if __name__ == "__main__":
    import sys
    stack_bb = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 200_000
    result = solve_push_fold(stack=stack_bb * 2, ante=1, iterations=iterations)
    print(f"Push/fold equilibrium, {stack_bb} bb, {iterations:,} iterations")
    print(f"SB shoves {len(result.shove_range)}/169: {' '.join(result.shove_range_names())}")
    print(f"BB calls  {len(result.call_range)}/169: {' '.join(result.call_range_names())}")

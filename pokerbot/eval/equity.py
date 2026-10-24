"""Exact and Monte Carlo Hold'em equity against two-card ranges."""
from __future__ import annotations

import random
from dataclasses import dataclass
from itertools import combinations

from .hand_eval import compare_hands


@dataclass(frozen=True)
class EquityEstimate:
    wins: int
    ties: int
    losses: int
    equity: float
    standard_error: float
    samples: int


def _validate(hero, board, villain_range):
    hero, board = tuple(hero), tuple(board)
    if len(hero) != 2 or len(board) > 5 or len(set(hero + board)) != len(hero) + len(board):
        raise ValueError("hero must have two cards and board 0-5 cards, all distinct")
    if any(not isinstance(c, int) or not 0 <= c < 52 for c in hero + board):
        raise ValueError("cards must be integers from 0 to 51")
    combos = []
    for combo in villain_range:
        combo = tuple(combo)
        if len(combo) != 2 or combo[0] == combo[1]:
            raise ValueError("each villain combo must contain two distinct cards")
        if any(not isinstance(c, int) or not 0 <= c < 52 for c in combo):
            raise ValueError("cards must be integers from 0 to 51")
        if set(combo).isdisjoint(hero + board):
            combos.append(combo)
    if not combos:
        raise ValueError("villain range has no combos after card removal")
    return hero, board, combos


def enumerate_equity(hero, board, villain_range) -> EquityEstimate:
    """Enumerate all legal villain combos and runouts exactly.

    Each combo in ``villain_range`` has equal weight. This is intended for
    small river/flop examples; preflop enumeration can be very large.
    """
    hero, board, combos = _validate(hero, board, villain_range)
    missing = 5 - len(board)
    wins = ties = losses = 0
    for villain in combos:
        dead = set(hero + board + villain)
        deck = [card for card in range(52) if card not in dead]
        runouts = combinations(deck, missing) if missing else [()]
        for runout in runouts:
            final_board = board + tuple(runout)
            result = compare_hands(hero + final_board, villain + final_board)
            if result > 0:
                wins += 1
            elif result < 0:
                losses += 1
            else:
                ties += 1
    total = wins + ties + losses
    equity = (wins + ties / 2) / total
    return EquityEstimate(wins, ties, losses, equity, 0.0, total)


def estimate_equity(hero, board, villain_range, *, samples: int = 10_000, seed: int | None = None) -> EquityEstimate:
    """Estimate equity by uniformly sampling a legal villain combo and runout."""
    if samples <= 0:
        raise ValueError("samples must be positive")
    hero, board, combos = _validate(hero, board, villain_range)
    rng = random.Random(seed)
    missing = 5 - len(board)
    wins = ties = losses = 0
    payoff_sum = payoff_sq_sum = 0.0
    for _ in range(samples):
        villain = rng.choice(combos)
        dead = set(hero + board + villain)
        deck = [card for card in range(52) if card not in dead]
        runout = tuple(rng.sample(deck, missing)) if missing else ()
        result = compare_hands(hero + board + runout, villain + board + runout)
        payoff = 1.0 if result > 0 else 0.5 if result == 0 else 0.0
        payoff_sum += payoff
        payoff_sq_sum += payoff * payoff
        if result > 0:
            wins += 1
        elif result < 0:
            losses += 1
        else:
            ties += 1
    equity = payoff_sum / samples
    variance = max(0.0, payoff_sq_sum / samples - equity * equity)
    return EquityEstimate(wins, ties, losses, equity, (variance / samples) ** 0.5, samples)

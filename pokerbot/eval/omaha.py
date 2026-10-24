"""Pot-Limit Omaha hand evaluation and equity estimation.

Omaha: each player holds 4 hole cards and must use exactly 2 of them
together with exactly 3 of the 5 board cards.
"""
from __future__ import annotations

import random
from itertools import combinations

from .hand_eval import evaluate_five


def evaluate_omaha(hole, board) -> tuple:
    """Best 5-card rank using exactly 2 hole + 3 board cards."""
    if len(hole) != 4 or len(board) != 5:
        raise ValueError("Omaha needs 4 hole and 5 board cards")
    best = None
    for hc in combinations(hole, 2):
        for bc in combinations(board, 3):
            r = evaluate_five(hc + bc)
            if best is None or r > best:
                best = r
    return best


def omaha_equity(hole0, hole1, board, n_sim=2000, seed=None):
    """Monte Carlo equity for two Omaha hands given partial board."""
    rng = random.Random(seed)
    used = set(hole0) | set(hole1) | set(board)
    deck = [c for c in range(52) if c not in used]
    wins = 0.0
    ties = 0.0
    total = 0
    for _ in range(n_sim):
        rng.shuffle(deck)
        # complete board to 5
        b = list(board) + [c for c in deck[: 5 - len(board)]]
        # opponent? only two players already given holes; if more cards needed for deck, fine
        r0 = evaluate_omaha(hole0, b)
        r1 = evaluate_omaha(hole1, b)
        total += 1
        if r0 > r1:
            wins += 1
        elif r0 == r1:
            ties += 0.5
    return (wins + ties) / total if total else 0.5


def random_omaha_hand(rng=None):
    rng = rng or random
    deck = list(range(52))
    rng.shuffle(deck)
    return deck[:4], deck[4:8], deck[8:13]

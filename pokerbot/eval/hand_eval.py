"""Dependency-free five- and seven-card Texas Hold'em hand evaluation.

Cards are integers 0..51: ``rank = card % 13 + 2`` (2 through Ace) and
``suit = card // 13``. Larger returned tuples represent stronger hands.
"""
from __future__ import annotations

from itertools import combinations


def _straight_high(ranks: list[int]) -> int | None:
    unique = set(ranks)
    if 14 in unique:
        unique.add(1)  # Ace can also be low in A-2-3-4-5.
    for high in range(14, 4, -1):
        if all(rank in unique for rank in range(high - 4, high + 1)):
            return high
    return None


def evaluate_five(cards) -> tuple[int, ...]:
    """Rank exactly five distinct cards, returning category then kickers.

    Categories from weakest to strongest: high card, pair, two pair, trips,
    straight, flush, full house, quads, straight flush.
    """
    cards = tuple(cards)
    if len(cards) != 5 or len(set(cards)) != 5 or any(not isinstance(c, int) or not 0 <= c < 52 for c in cards):
        raise ValueError("evaluate_five expects five distinct card integers from 0 to 51")
    ranks = sorted((c % 13 + 2 for c in cards), reverse=True)
    suits = [c // 13 for c in cards]
    counts: dict[int, int] = {}
    for rank in ranks:
        counts[rank] = counts.get(rank, 0) + 1
    groups = sorted(((count, rank) for rank, count in counts.items()), reverse=True)
    flush = len(set(suits)) == 1
    straight = _straight_high(ranks)

    if flush and straight:
        return (8, straight)
    if groups[0][0] == 4:
        quad = groups[0][1]
        return (7, quad, max(rank for rank in ranks if rank != quad))
    if groups[0][0] == 3 and groups[1][0] == 2:
        return (6, groups[0][1], groups[1][1])
    if flush:
        return (5, *ranks)
    if straight:
        return (4, straight)
    if groups[0][0] == 3:
        trip = groups[0][1]
        kickers = sorted((rank for rank in ranks if rank != trip), reverse=True)
        return (3, trip, *kickers)
    pairs = sorted((rank for rank, count in counts.items() if count == 2), reverse=True)
    if len(pairs) == 2:
        kicker = next(rank for rank, count in counts.items() if count == 1)
        return (2, pairs[0], pairs[1], kicker)
    if len(pairs) == 1:
        pair = pairs[0]
        kickers = sorted((rank for rank in ranks if rank != pair), reverse=True)
        return (1, pair, *kickers)
    return (0, *ranks)


def evaluate_seven(cards) -> tuple[int, ...]:
    """Return the best five-card rank available from exactly seven cards."""
    cards = tuple(cards)
    if len(cards) != 7 or len(set(cards)) != 7 or any(not isinstance(c, int) or not 0 <= c < 52 for c in cards):
        raise ValueError("evaluate_seven expects seven distinct card integers from 0 to 51")
    return max(evaluate_five(hand) for hand in combinations(cards, 5))


def compare_hands(cards_a, cards_b) -> int:
    """Compare two seven-card Hold'em holdings: +1 for A, -1 for B, 0 for tie."""
    rank_a, rank_b = evaluate_seven(cards_a), evaluate_seven(cards_b)
    return (rank_a > rank_b) - (rank_a < rank_b)

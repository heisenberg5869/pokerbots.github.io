"""Kuhn Poker: 3 cards (J < Q < K), 2 players, 1 ante each, one bet of size 1.

Actions: 'p' = pass (check/fold), 'b' = bet (bet/call).
Histories and outcomes (payoffs for player 0, zero-sum):
    pp   -> showdown, winner takes 1
    pbp  -> player 0 folds: player 1 wins 1
    pbb  -> showdown, winner takes 2
    bp   -> player 1 folds: player 0 wins 1
    bb   -> showdown, winner takes 2
"""
from __future__ import annotations
from itertools import permutations
from .base import Game, State

CARDS = "JQK"
TERMINAL = {"pp", "pbp", "pbb", "bp", "bb"}


class KuhnState(State):
    __slots__ = ("cards", "history")

    def __init__(self, cards=None, history=""):
        self.cards = cards          # (card_p0, card_p1) as ints 0..2, or None before the deal
        self.history = history

    def is_terminal(self):
        return self.history in TERMINAL

    def is_chance(self):
        return self.cards is None

    def chance_outcomes(self):
        deals = list(permutations(range(3), 2))      # 6 equally likely deals
        return [(d, 1 / len(deals)) for d in deals]

    def current_player(self):
        return len(self.history) % 2

    def legal_actions(self):
        return ("p", "b")

    def info_set_key(self, player):
        return f"{CARDS[self.cards[player]]}{self.history}"

    def child(self, action):
        if self.is_chance():
            return KuhnState(action, "")
        return KuhnState(self.cards, self.history + action)

    def returns(self):
        h, (c0, c1) = self.history, self.cards
        if h == "bp":
            u0 = 1
        elif h == "pbp":
            u0 = -1
        else:
            stake = 2 if "b" in h else 1
            u0 = stake if c0 > c1 else -stake
        return (u0, -u0)


class KuhnPoker(Game):
    name = "kuhn"

    def root(self):
        return KuhnState()

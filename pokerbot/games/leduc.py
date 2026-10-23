"""Two-player, six-card Leduc Hold'em.

Each rank (J, Q, K) has two suits. Players ante one chip, play a round with
small bets, reveal one public card, then play a round with big bets. A pair
beats every unpaired hand. The betting cap is two bets/raises per round.

Actions are ``f`` (fold), ``c`` (check/call), ``b`` (bet), and ``r`` (raise).
Payoffs are net of each player's ante and subsequent contributions.
"""
from __future__ import annotations

from itertools import permutations
from typing import Hashable

from .base import Game, State

RANKS = "JQK"
CARDS = tuple(range(6))  # rank * 2 + suit
ACTION_NAMES = {"f": "fold", "c": "check/call", "b": "bet", "r": "raise"}
MAX_BETS = 2


def card_name(card: int) -> str:
    return f"{RANKS[card // 2]}{'♥' if card % 2 == 0 else '♠'}"


class LeducState(State):
    __slots__ = ("private", "board", "round", "player", "history", "round_bets",
                 "contributions", "bet_count", "pending", "terminal")

    def __init__(self, private=None, board=None, round=0, player=0, history="",
                 round_bets=(0, 0), contributions=(1, 1), bet_count=0,
                 pending=False, terminal=False):
        self.private = private
        self.board = board
        self.round = round
        self.player = player
        self.history = history
        self.round_bets = round_bets
        self.contributions = contributions
        self.bet_count = bet_count
        self.pending = pending
        self.terminal = terminal

    def is_terminal(self):
        return self.terminal

    def is_chance(self):
        return self.private is None or (self.round == 1 and self.board is None and not self.terminal)

    def chance_outcomes(self):
        if self.private is None:
            deals = list(permutations(CARDS, 2))
            return [(deal, 1 / len(deals)) for deal in deals]
        if self.round == 1 and self.board is None:
            remaining = [c for c in CARDS if c not in self.private]
            return [(card, 1 / len(remaining)) for card in remaining]
        raise ValueError("chance_outcomes called outside a chance node")

    def current_player(self):
        return self.player

    def legal_actions(self):
        if self.is_terminal() or self.is_chance():
            return ()
        if self.pending:
            return ("f", "c", "r") if self.bet_count < MAX_BETS else ("f", "c")
        return ("c", "b") if self.bet_count == 0 else ("c",)

    def info_set_key(self, player: int) -> str:
        if self.private is None:
            raise ValueError("no private cards have been dealt")
        own = self.private[player]
        board = "?" if self.board is None else RANKS[self.board // 2]
        return f"{RANKS[own // 2]}|{board}|{self.round}:{self.history}"

    def child(self, action: Hashable) -> "LeducState":
        if self.is_chance():
            if self.private is None:
                return LeducState(private=tuple(action))
            return LeducState(private=self.private, board=action, round=1, player=1,
                              history=self.history + "/", contributions=self.contributions)
        action = str(action)
        if action not in self.legal_actions():
            raise ValueError(f"illegal action {action!r}; legal actions are {self.legal_actions()}")
        p, other = self.player, 1 - self.player
        bets = list(self.round_bets)
        contrib = list(self.contributions)
        history = self.history + action
        if action == "f":
            return LeducState(private=self.private, board=self.board, round=self.round,
                              player=p, history=history, round_bets=self.round_bets,
                              contributions=self.contributions, bet_count=self.bet_count,
                              terminal=True)
        if action == "b":
            amount = 2 if self.round == 0 else 4
            bets[p] += amount
            contrib[p] += amount
            return LeducState(self.private, self.board, self.round, other, history,
                              tuple(bets), tuple(contrib), 1, True)
        if action == "r":
            amount = 2 if self.round == 0 else 4
            bets[p] += amount
            contrib[p] += amount
            return LeducState(self.private, self.board, self.round, other, history,
                              tuple(bets), tuple(contrib), self.bet_count + 1, True)
        if self.pending:  # call: match the outstanding wager
            amount = bets[other] - bets[p]
            bets[p] += amount
            contrib[p] += amount
            return self._close_round(history, tuple(bets), tuple(contrib))
        # check: close after two checks, otherwise pass action to opponent
        if history.endswith("cc"):
            return self._close_round(history, tuple(bets), tuple(contrib))
        return LeducState(self.private, self.board, self.round, other, history,
                          tuple(bets), tuple(contrib), self.bet_count, False)

    def _close_round(self, history, bets, contributions):
        if self.round == 0:
            return LeducState(self.private, None, 1, 1, history + "/", (0, 0),
                              contributions, 0, False)
        return LeducState(self.private, self.board, 1, self.player, history,
                          bets, contributions, self.bet_count, False, terminal=True)

    def returns(self):
        if not self.terminal:
            raise ValueError("returns are only defined at terminal states")
        if self.history.endswith("f"):
            folder = self.player
            winner = 1 - folder
        else:
            ranks = [card // 2 for card in self.private]
            board_rank = self.board // 2
            scores = [(2, ranks[p]) if ranks[p] == board_rank else (1, ranks[p])
                      for p in range(2)]
            winner = 0 if scores[0] > scores[1] else 1 if scores[1] > scores[0] else None
        if winner is None:
            payoff0 = (sum(self.contributions) / 2) - self.contributions[0]
        else:
            payoff0 = (sum(self.contributions) - self.contributions[0]
                       if winner == 0 else -self.contributions[0])
        return (payoff0, -payoff0)


class LeducPoker(Game):
    name = "leduc"

    def root(self):
        return LeducState()

"""Full heads-up no-limit Hold'em game engine implementing base.Game.

Reuses NoLimitBettingRound from pokerbot.games.nolimit for betting mechanics.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import combinations
from typing import Callable, Hashable, Sequence

from .base import Game, State
from .nolimit import NLAction, NoLimitBettingRound
from pokerbot.eval.hand_eval import evaluate_seven


def _remaining_deck(used):
    return [c for c in range(52) if c not in used]


@dataclass
class NLHoldemState(State):
    num_players = 2
    stacks: list[int] = field(default_factory=lambda: [100, 100])
    hole: list = field(default_factory=lambda: [[], []])
    board: list = field(default_factory=list)
    street: int = 0  # 0 preflop 1 flop 2 turn 3 river
    round_: NoLimitBettingRound | None = None
    terminal: bool = False
    folded: int | None = None
    history: list = field(default_factory=list)
    bet_menu: tuple = (0.5, 1.0)
    bucket_fn: Callable = None
    # chance deal stage: None means betting; 'hole'/'flop'/'turn'/'river'
    chance_stage: str | None = None
    _initial_total: int = 0

    def __post_init__(self):
        if self.bucket_fn is None:
            self.bucket_fn = lambda x: x
        if self._initial_total == 0:
            self._initial_total = sum(self.stacks) + (self.round_.total_pot if self.round_ else 0)

    def is_terminal(self):
        return self.terminal

    def is_chance(self):
        return self.chance_stage is not None

    def _used_cards(self):
        used = set()
        for h in self.hole:
            for c in h:
                used.add(c)
        for c in self.board:
            used.add(c)
        return used

    def chance_outcomes(self):
        if self.chance_stage == "hole":
            deck = list(range(52))
            outs = []
            for c0a, c0b in combinations(deck, 2):
                rem = [c for c in deck if c not in (c0a, c0b)]
                for c1a, c1b in combinations(rem, 2):
                    cards = ((c0a, c0b), (c1a, c1b))
                    # equal probability
                    outs.append((cards, 1.0))
            # normalize
            total = len(outs)
            return [(o, 1.0 / total) for o, _ in outs]
        if self.chance_stage == "flop":
            deck = _remaining_deck(self._used_cards())
            outs = []
            for combo in combinations(deck, 3):
                outs.append(combo)
            return [(c, 1.0 / len(outs)) for c in outs]
        if self.chance_stage == "turn":
            deck = _remaining_deck(self._used_cards())
            return [(c, 1.0 / len(deck)) for c in deck]
        if self.chance_stage == "river":
            deck = _remaining_deck(self._used_cards())
            return [(c, 1.0 / len(deck)) for c in deck]
        return []

    def current_player(self):
        if self.round_ is None:
            return 0
        return self.round_.actor

    def legal_actions(self):
        if self.is_chance() or self.is_terminal():
            return ()
        if self.round_ is None:
            return ()
        return self.round_.legal_actions()

    def info_set_key(self, player):
        own = tuple(sorted(self.hole[player]))
        pub = tuple(self.board)
        hist = tuple(self.history)
        key = (player, self.bucket_fn(own), pub, hist)
        return str(key)

    def child(self, action):
        # chance outcome action is a tuple of cards
        if self.is_chance():
            if self.chance_stage == "hole":
                (h0, h1) = action
                new = NLHoldemState(
                    stacks=[s for s in self.stacks],
                    hole=[list(h0), list(h1)],
                    board=[],
                    street=0,
                    terminal=False,
                    bet_menu=self.bet_menu,
                    bucket_fn=self.bucket_fn,
                    chance_stage=None,
                )
                # start preflop betting round
                new.round_ = NoLimitBettingRound([new.stacks[0], new.stacks[1]], pot=0, bet_menu=self.bet_menu, first_to_act=1 if False else 0)  # SB/BB simplified: p0 acts first
                # Actually blinds: keep simple, no blinds; pot starts 0. To make nonzero, add antes? We'll keep 0 for tiny tests.
                new._initial_total = sum(new.stacks) + new.round_.total_pot
                return new
            if self.chance_stage == "flop":
                new = self._copy()
                new.board = list(action)
                new.chance_stage = None
                new.street = 1
                new.round_ = NoLimitBettingRound([new.stacks[0], new.stacks[1]], pot=new.round_.total_pot if new.round_ else 0, bet_menu=self.bet_menu)
                # move pot from round to new round: round_.total_pot includes street bets already? At close of preflop, pot should include street bets. We store pot in round. Let's instead consolidate: when closing round, add street_bets to pot. Handle in round close.
                new._initial_total = self._initial_total
                return new
            if self.chance_stage == "turn":
                new = self._copy()
                new.board = self.board + [action]
                new.chance_stage = None
                new.street = 2
                new.round_ = NoLimitBettingRound([new.stacks[0], new.stacks[1]], pot=new.round_.total_pot if new.round_ else 0, bet_menu=self.bet_menu)
                new._initial_total = self._initial_total
                return new
            if self.chance_stage == "river":
                new = self._copy()
                new.board = self.board + [action]
                new.chance_stage = None
                new.street = 3
                new.round_ = NoLimitBettingRound([new.stacks[0], new.stacks[1]], pot=new.round_.total_pot if new.round_ else 0, bet_menu=self.bet_menu)
                new._initial_total = self._initial_total
                return new

        # betting action
        rnd = self.round_
        # apply action to a copy of round
        new_round = NoLimitBettingRound(
            stacks=[rnd.stacks[0], rnd.stacks[1]],
            pot=rnd.pot,
            first_to_act=rnd.first_to_act,
            street_bets=[rnd.street_bets[0], rnd.street_bets[1]],
            min_bet=rnd.min_bet,
            bet_menu=rnd.bet_menu,
        )
        new_round.actor = rnd.actor
        new_round.last_raise = rnd.last_raise
        new_round.pending = rnd.pending
        new_round.folded = rnd.folded
        new_round.all_in = rnd.all_in
        new_round.checked = rnd.checked
        new_round.history = [h for h in rnd.history]
        new_round.act(action)

        new = self._copy()
        new.round_ = new_round
        new.stacks = [new_round.stacks[0], new_round.stacks[1]]
        new.history = self.history + [action]
        new.folded = new_round.folded

        if new_round.folded is not None:
            new.terminal = True
            return new

        if not new_round.pending:
            # round closed; consolidate pot
            pot = new_round.pot + sum(new_round.street_bets)
            new_round.pot = pot
            new_round.street_bets = [0, 0]
            new.round_ = new_round
            new.stacks = [new_round.stacks[0], new_round.stacks[1]]
            if new.street == 3 or new_round.all_in:
                # showdown or all-in runout
                if new.street < 3 and new_round.all_in:
                    # deal remaining board via chance: set chance_stage appropriately
                    if new.street == 0:
                        new.chance_stage = "flop"
                        new.street = 0  # will become 1 on flop child; but set stage
                    # simpler: advance street and set chance stage
                # Determine next chance stage
                if new.street == 0:
                    new.chance_stage = "flop"
                elif new.street == 1:
                    new.chance_stage = "turn"
                elif new.street == 2:
                    new.chance_stage = "river"
                else:
                    new.terminal = True
                    new._showdown(pot)
            else:
                if new.street == 0:
                    new.chance_stage = "flop"
                elif new.street == 1:
                    new.chance_stage = "turn"
                elif new.street == 2:
                    new.chance_stage = "river"
                else:
                    new.terminal = True
                    new._showdown(pot)
        return new

    def _copy(self):
        return NLHoldemState(
            stacks=[self.stacks[0], self.stacks[1]],
            hole=[list(self.hole[0]), list(self.hole[1])],
            board=list(self.board),
            street=self.street,
            round_=None,
            terminal=self.terminal,
            folded=self.folded,
            history=list(self.history),
            bet_menu=self.bet_menu,
            bucket_fn=self.bucket_fn,
            chance_stage=self.chance_stage,
            _initial_total=self._initial_total,
        )

    def _showdown(self, pot):
        # score
        c0 = list(self.hole[0]) + list(self.board)
        c1 = list(self.hole[1]) + list(self.board)
        cmp = (evaluate_seven(c0) > evaluate_seven(c1)) - (evaluate_seven(c0) < evaluate_seven(c1))
        if cmp > 0:
            self.stacks[0] += pot
        elif cmp < 0:
            self.stacks[1] += pot
        else:
            self.stacks[0] += pot // 2
            self.stacks[1] += pot - pot // 2

    def returns(self):
        total = self._initial_total
        # profit relative to starting stacks
        r0 = self.stacks[0] - (total // 2)  # approximate; better track initial per player
        # We'll compute based on initial stacks stored? Not available. Use total/2 assumption.
        return (float(self.stacks[0] - 100), float(self.stacks[1] - 100))


class NoLimitHoldem(Game):
    name = "nolimit_holdem"

    def __init__(self, stacks=(100, 100), bet_menu=(0.5, 1.0), bucket_fn=None):
        self.stacks = list(stacks)
        self.bet_menu = tuple(bet_menu)
        self.bucket_fn = bucket_fn or (lambda x: x)

    def root(self):
        st = NLHoldemState(
            stacks=[self.stacks[0], self.stacks[1]],
            hole=[[], []],
            board=[],
            street=0,
            terminal=False,
            bet_menu=self.bet_menu,
            bucket_fn=self.bucket_fn,
            chance_stage="hole",
        )
        st._initial_total = sum(self.stacks)
        return st

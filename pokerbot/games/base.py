"""The extensive-form game interface every game in this repo implements.

A game is described by its root state. A state is one of:
  * terminal   -> returns()  gives the payoff of every player
  * chance     -> chance_outcomes() gives [(outcome, probability), ...]
  * decision   -> current_player(), legal_actions(), info_set_key(player)

States are immutable: child(action) returns a NEW state. This keeps the
solvers simple (no undo logic) at the cost of speed; later modules swap in
faster representations behind the same interface.
"""
from __future__ import annotations
from typing import Hashable, Sequence


class State:
    num_players = 2

    def is_terminal(self) -> bool:
        raise NotImplementedError

    def is_chance(self) -> bool:
        raise NotImplementedError

    def returns(self) -> Sequence[float]:
        """Payoffs for each player. Only valid at terminal states."""
        raise NotImplementedError

    def chance_outcomes(self) -> list[tuple[Hashable, float]]:
        raise NotImplementedError

    def current_player(self) -> int:
        raise NotImplementedError

    def legal_actions(self) -> Sequence[Hashable]:
        raise NotImplementedError

    def info_set_key(self, player: int) -> str:
        """Everything `player` knows. States sharing a key are indistinguishable to them."""
        raise NotImplementedError

    def child(self, action: Hashable) -> "State":
        raise NotImplementedError


class Game:
    name = "game"
    num_players = 2

    def root(self) -> State:
        raise NotImplementedError

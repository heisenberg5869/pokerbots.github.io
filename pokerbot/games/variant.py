"""Module 13: a flexible framework for custom poker variants.

Rules are described declaratively through :class:`VariantConfig`; a
``VariantGame`` interprets that config to produce an extensive-form game
following the shared ``Game``/``State`` interface. New variants can be added
by subclassing :class:`VariantGame` or by composing a new config.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Hashable, Sequence

from .base import Game, State


@dataclass
class VariantConfig:
    name: str = "custom"
    num_players: int = 2
    antes: float = 0.0
    wild_cards: list[str] = field(default_factory=list)
    auction: bool = False
    hole_cards: int = 2
    community_cards: int = 5
    peek_allowed: bool = False
    extra: dict[str, Any] = field(default_factory=dict)


class VariantState(State):
    """Minimal state wrapper carrying a config and a phase marker."""

    def __init__(self, config: VariantConfig, phase: str = "start"):
        self.config = config
        self.phase = phase
        self._num_players = config.num_players

    @property
    def num_players(self) -> int:
        return self._num_players

    def is_terminal(self) -> bool:
        return self.phase == "terminal"

    def is_chance(self) -> bool:
        return self.phase == "chance"

    def returns(self) -> Sequence[float]:
        if not self.is_terminal():
            raise RuntimeError("returns() only valid at terminal states")
        return [0.0] * self.num_players

    def chance_outcomes(self) -> list[tuple[Hashable, float]]:
        return []

    def current_player(self) -> int:
        return 0

    def legal_actions(self) -> Sequence[Hashable]:
        return []

    def info_set_key(self, player: int) -> str:
        return f"{self.config.name}:{self.phase}:p{player}"

    def child(self, action: Hashable) -> "VariantState":
        return VariantState(self.config, "terminal")


class VariantGame(Game):
    """Base for custom variants driven by a :class:`VariantConfig`."""

    def __init__(self, config: VariantConfig | None = None):
        self.config = config or VariantConfig()
        self.name = self.config.name
        self.num_players = self.config.num_players

    def root(self) -> State:
        return VariantState(self.config, "start")

    def describe(self) -> dict[str, Any]:
        return {
            "name": self.config.name,
            "num_players": self.config.num_players,
            "antes": self.config.antes,
            "wild_cards": list(self.config.wild_cards),
            "auction": self.config.auction,
            "hole_cards": self.config.hole_cards,
            "community_cards": self.config.community_cards,
            "peek_allowed": self.config.peek_allowed,
        }


class SneakPeekHoldem(VariantGame):
    """Stub variant: Hold'em where a player may peek at one opponent card."""

    def __init__(self):
        super().__init__(VariantConfig(
            name="Sneak Peek Hold'em",
            num_players=2,
            antes=0.0,
            hole_cards=2,
            community_cards=5,
            peek_allowed=True,
        ))

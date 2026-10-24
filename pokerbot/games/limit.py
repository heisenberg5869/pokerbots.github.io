"""Heads-up fixed-limit Hold'em betting-round mechanics.

Amounts are integer chip units. This module models one betting round; dealing,
showdown, and hand-level transitions are intentionally kept by the caller.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LimitBettingRound:
    """A small, auditable betting state for one heads-up limit round.

    ``street_bets`` are the players' contributions to this street and
    ``pot`` is the amount already committed before this round. A round starts
    with the first player to act and closes after a check/check or call.
    ``raise_cap`` counts the opening bet as bet 1 (the common four-bet cap).
    """

    stacks: list[int]
    bet_size: int
    first_to_act: int = 0
    pot: int = 0
    street_bets: list[int] = field(default_factory=lambda: [0, 0])
    raise_cap: int = 4
    raises: int = 0
    actor: int = field(init=False)
    pending: bool = field(default=True, init=False)
    folded: int | None = field(default=None, init=False)
    all_in: bool = field(default=False, init=False)
    checked: bool = field(default=False, init=False)
    history: list[tuple[int, str, int]] = field(default_factory=list, init=False)

    def __post_init__(self):
        if len(self.stacks) != 2 or len(self.street_bets) != 2:
            raise ValueError("heads-up rounds require two stacks and two street bets")
        if any(not isinstance(x, int) or x < 0 for x in (*self.stacks, *self.street_bets, self.pot)):
            raise ValueError("stacks, bets, and pot must be nonnegative integer chips")
        if self.bet_size <= 0 or self.raise_cap < 1 or self.raises < 0:
            raise ValueError("bet_size and raise_cap must be positive; raises cannot be negative")
        if self.first_to_act not in (0, 1):
            raise ValueError("first_to_act must be player 0 or 1")
        if self.raises > self.raise_cap:
            raise ValueError("raises cannot exceed the raise cap")
        self.stacks = list(self.stacks)
        self.street_bets = list(self.street_bets)
        self.actor = self.first_to_act
        if min(self.stacks) == 0:
            self.pending = False
            self.all_in = True

    @property
    def total_pot(self) -> int:
        return self.pot + sum(self.street_bets)

    @property
    def to_call(self) -> int:
        return max(0, self.street_bets[1 - self.actor] - self.street_bets[self.actor])

    def legal_actions(self) -> tuple[str, ...]:
        if not self.pending:
            return ()
        owed = self.to_call
        actions = ["fold"] if owed else []
        if owed:
            actions.append("call")
        else:
            actions.append("check")
        can_raise = self.raises < self.raise_cap
        full_raise_cost = owed + self.bet_size
        if can_raise and self.stacks[self.actor] >= full_raise_cost:
            actions.append("raise" if owed else "bet")
        elif can_raise and self.stacks[self.actor] > owed:
            # A short all-in raise is legal when it exceeds the call amount.
            actions.append("all-in")
        return tuple(actions)

    def act(self, action: str) -> None:
        """Apply a legal action, raising ValueError for an illegal choice."""
        legal = self.legal_actions()
        if action not in legal:
            raise ValueError(f"illegal action {action!r}; legal actions are {legal}")
        player = self.actor
        owed = self.to_call
        paid = 0
        if action == "fold":
            self.folded = player
            self.pending = False
        elif action in ("check", "call"):
            paid = min(owed, self.stacks[player])
            self._pay(player, paid)
            if self.stacks[player] == 0:
                self.pending = False
                self.all_in = True
            elif action == "check" and self.checked:
                self.pending = False
            elif action == "check":
                self.checked = True
                self.actor = 1 - player
            elif self.street_bets[0] == self.street_bets[1]:
                self.pending = False
            else:
                self.actor = 1 - player
        elif action in ("bet", "raise"):
            paid = owed + self.bet_size
            self._pay(player, paid)
            self.checked = False
            self.raises += 1
            if self.stacks[player] == 0:
                self.all_in = True
            self.actor = 1 - player
        elif action == "all-in":
            paid = self.stacks[player]
            self._pay(player, paid)
            self.raises += 1
            self.all_in = True
            # Opponent may call the unmatched part or fold; no further raise.
            self.raise_cap = self.raises
            self.actor = 1 - player
        self.history.append((player, action, paid))

    def _pay(self, player: int, amount: int) -> None:
        if amount < 0 or amount > self.stacks[player]:
            raise ValueError("payment exceeds remaining stack")
        self.stacks[player] -= amount
        self.street_bets[player] += amount

    def invariants(self, initial_total_chips: int) -> bool:
        """Return whether chips are conserved across stacks and committed pot."""
        return sum(self.stacks) + self.total_pot == initial_total_chips

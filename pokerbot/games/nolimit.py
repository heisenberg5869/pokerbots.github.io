"""Heads-up no-limit betting-round mechanics and sizing utilities.

Actions specify the player's target street contribution, which makes minimum
raises, pot-sized raises, and all-ins auditable. This is a single betting
round, not a complete dealt Hold'em hand.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import Literal


@dataclass(frozen=True)
class NLAction:
    kind: Literal["fold", "check", "call", "wager"]
    to_amount: int | None = None

    def __str__(self):
        return self.kind if self.to_amount is None else f"{self.kind} to {self.to_amount}"


def stack_to_pot_ratio(stack: float, pot: float) -> float:
    """Return SPR, rejecting a zero/negative pot or negative stack."""
    if stack < 0 or pot <= 0:
        raise ValueError("stack must be nonnegative and pot must be positive")
    return stack / pot


def pot_odds_call_fraction(pot_before_call: float, call_amount: float) -> float:
    """Minimum equity required to call when the pot is measured before calling."""
    if pot_before_call < 0 or call_amount < 0:
        raise ValueError("pot and call amount must be nonnegative")
    if pot_before_call + call_amount == 0:
        return 0.0
    return call_amount / (pot_before_call + call_amount)


def pot_fraction_for_geometric_growth(pot: float, remaining_streets: int,
                                       final_pot: float) -> float:
    """Equal pot-fraction wager that reaches ``final_pot`` after each street.

    Assumes one player bets and is called on every remaining street. If each
    bet is ``f`` times the current pot, the pot multiplies by ``1 + 2f``.
    """
    if pot <= 0 or final_pot < pot or remaining_streets <= 0:
        raise ValueError("require pot > 0, final_pot >= pot, and at least one street")
    return ((final_pot / pot) ** (1 / remaining_streets) - 1) / 2


@dataclass
class NoLimitBettingRound:
    """Stateful two-player no-limit round with an optional bet-size menu.

    Menu entries are pot fractions. The engine always includes the minimum
    legal wager and the all-in size when distinct from menu actions. Check/call
    completes a round after both players have acted or matched the wager.
    """

    stacks: list[int]
    pot: int
    first_to_act: int = 0
    street_bets: list[int] = field(default_factory=lambda: [0, 0])
    min_bet: int = 1
    bet_menu: tuple[float, ...] = (0.5, 1.0)
    actor: int = field(init=False)
    last_raise: int = field(init=False)
    pending: bool = field(default=True, init=False)
    folded: int | None = field(default=None, init=False)
    all_in: bool = field(default=False, init=False)
    checked: bool = field(default=False, init=False)
    history: list[tuple[int, NLAction, int]] = field(default_factory=list, init=False)

    def __post_init__(self):
        if len(self.stacks) != 2 or len(self.street_bets) != 2:
            raise ValueError("heads-up betting requires two stacks and two street bets")
        if any(not isinstance(x, int) or x < 0 for x in (*self.stacks, *self.street_bets, self.pot)):
            raise ValueError("chips must be nonnegative integers")
        if self.min_bet <= 0 or self.first_to_act not in (0, 1):
            raise ValueError("min_bet must be positive and first_to_act must be 0 or 1")
        if any(not isfinite(x) or x <= 0 for x in self.bet_menu):
            raise ValueError("bet menu fractions must be finite and positive")
        self.stacks = list(self.stacks)
        self.street_bets = list(self.street_bets)
        self.bet_menu = tuple(sorted(set(float(x) for x in self.bet_menu)))
        self.actor = self.first_to_act
        self.last_raise = max(self.min_bet, abs(self.street_bets[0] - self.street_bets[1]))
        if min(self.stacks) == 0:
            self.pending = False
            self.all_in = True

    @property
    def total_pot(self) -> int:
        return self.pot + sum(self.street_bets)

    @property
    def to_call(self) -> int:
        return max(0, self.street_bets[1 - self.actor] - self.street_bets[self.actor])

    def legal_actions(self) -> tuple[NLAction, ...]:
        if not self.pending:
            return ()
        player = self.actor
        owed = self.to_call
        actions: list[NLAction] = []
        if owed:
            actions.extend((NLAction("fold"), NLAction("call")))
        else:
            actions.append(NLAction("check"))

        max_to = self.street_bets[player] + self.stacks[player]
        min_to = (self.street_bets[1 - player] + self.last_raise) if owed else max(self.min_bet, self.street_bets[player] + self.min_bet)
        if max_to <= self.street_bets[1 - player]:
            return tuple(actions)
        if max_to < min_to:  # short all-in wager/raise is legal
            actions.append(NLAction("wager", max_to))
            return tuple(actions)
        pot_now = self.total_pot
        targets = {min_to, max_to}
        for fraction in self.bet_menu:
            if owed:
                # Raise-to = call amount plus fraction of the pot after the call.
                target = self.street_bets[1 - player] + round(fraction * (pot_now + owed))
            else:
                target = self.street_bets[player] + round(fraction * pot_now)
            targets.add(max(min_to, min(max_to, target)))
        actions.extend(NLAction("wager", target) for target in sorted(targets)
                       if min_to <= target <= max_to)
        return tuple(dict.fromkeys(actions))

    def act(self, action: NLAction) -> None:
        """Apply a legal action; wagering amount is total street contribution."""
        legal = self.legal_actions()
        if action not in legal:
            raise ValueError(f"illegal action {action}; legal actions are {legal}")
        player = self.actor
        owed = self.to_call
        paid = 0
        if action.kind == "fold":
            self.folded = player
            self._refund_uncalled()
            self.pending = False
        elif action.kind == "check":
            if self.checked:
                self.pending = False
            else:
                self.checked = True
                self.actor = 1 - player
        elif action.kind == "call":
            paid = min(owed, self.stacks[player])
            self._pay(player, paid)
            self.pending = self.street_bets[0] != self.street_bets[1] and self.stacks[player] > 0
            self.all_in = self.stacks[player] == 0
            if not self.pending:
                self._refund_uncalled()
            if self.pending:
                self.actor = 1 - player
        else:
            assert action.to_amount is not None
            paid = action.to_amount - self.street_bets[player]
            previous_bet = max(self.street_bets)
            self._pay(player, paid)
            new_raise = self.street_bets[player] - previous_bet
            if new_raise > 0:
                self.last_raise = max(new_raise, self.min_bet)
            self.checked = False
            self.all_in = self.stacks[player] == 0
            self.actor = 1 - player
        self.history.append((player, action, paid))

    def _pay(self, player: int, amount: int) -> None:
        if amount < 0 or amount > self.stacks[player]:
            raise ValueError("wager exceeds remaining stack")
        self.stacks[player] -= amount
        self.street_bets[player] += amount

    def _refund_uncalled(self) -> None:
        """Return any unmatched contribution to the player who made it."""
        if self.street_bets[0] != self.street_bets[1]:
            leader = 0 if self.street_bets[0] > self.street_bets[1] else 1
            other = 1 - leader
            refund = self.street_bets[leader] - self.street_bets[other]
            self.street_bets[leader] -= refund
            self.stacks[leader] += refund

    def invariants(self, initial_total_chips: int) -> bool:
        return sum(self.stacks) + self.total_pot == initial_total_chips

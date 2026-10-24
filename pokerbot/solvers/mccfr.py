"""Chance-sampling and external-sampling Monte Carlo CFR for small games."""
from __future__ import annotations

import random

from .regret_matching import RegretMatcher


class MCCFRTrainer:
    """Train tabular CFR while sampling chance and/or opponent actions.

    ``sampling="chance"`` samples chance outcomes and enumerates both players'
    actions. ``sampling="external"`` also samples the non-traversing player's
    actions while fully expanding the traverser's choices. The sampling
    distribution is the game's chance distribution and the opponent's current
    strategy, so the resulting counterfactual-regret estimates are unbiased.
    This reference implementation favors clarity over speed.
    """

    def __init__(self, game, *, sampling: str = "external", seed: int | None = None):
        if sampling not in ("chance", "external"):
            raise ValueError("sampling must be 'chance' or 'external'")
        self.game = game
        self.sampling = sampling
        self.rng = random.Random(seed)
        self.nodes: dict[str, RegretMatcher] = {}
        self.iterations = 0

    def train(self, iterations: int, callback=None, callback_every: int = 0):
        if iterations < 0:
            raise ValueError("iterations must be non-negative")
        for _ in range(iterations):
            for traverser in range(self.game.num_players):
                self._walk(self.game.root(), [1.0] * self.game.num_players + [1.0], traverser)
            self.iterations += 1
            if callback and callback_every and self.iterations % callback_every == 0:
                callback(self)
        return self

    def _walk(self, state, reach, traverser: int):
        if state.is_terminal():
            return list(state.returns())

        if state.is_chance():
            outcomes = state.chance_outcomes()
            outcome, probability = self.rng.choices(outcomes, weights=[p for _, p in outcomes], k=1)[0]
            child_reach = list(reach)
            child_reach[-1] *= probability
            return self._walk(state.child(outcome), child_reach, traverser)

        player = state.current_player()
        key = state.info_set_key(player)
        actions = list(state.legal_actions())
        node = self.nodes.setdefault(key, RegretMatcher(actions))
        strategy = node.current_strategy()

        if player != traverser and self.sampling == "external":
            index = self.rng.choices(range(len(actions)), weights=strategy, k=1)[0]
            child_reach = list(reach)
            child_reach[player] *= strategy[index]
            return self._walk(state.child(actions[index]), child_reach, traverser)

        action_values = []
        for action, probability in zip(actions, strategy):
            child_reach = list(reach)
            child_reach[player] *= probability
            action_values.append(self._walk(state.child(action), child_reach, traverser))
        node_value = [sum(strategy[i] * action_values[i][p] for i in range(len(actions)))
                      for p in range(self.game.num_players)]

        if player == traverser:
            # External sampling draws both chance and opponent actions, so the
            # sampling distribution already accounts for counterfactual reach.
            # Chance sampling expands opponent actions, so retain their reach
            # explicitly; chance reach is sampled and must not be squared.
            opponent_reach = reach[1 - player] if self.sampling == "chance" else 1.0
            for i in range(len(actions)):
                node.regret_sum[i] += opponent_reach * (action_values[i][player] - node_value[player])
                node.strategy_sum[i] += opponent_reach * reach[player] * strategy[i]
        return node_value

    def average_strategy(self) -> dict[str, list[float]]:
        return {key: node.average_strategy() for key, node in self.nodes.items()}


def estimate_value(game, strategy, *, samples: int = 1000, sampling: str = "external", seed: int | None = None,
                   player: int = 0) -> float:
    """Estimate a fixed strategy's value by chance or outcome sampling.

    Chance sampling draws chance outcomes and integrates over every action.
    Outcome sampling draws chance and decision actions from ``strategy``.
    Both are unbiased estimates of the exact expected value.
    """
    if samples <= 0:
        raise ValueError("samples must be positive")
    if sampling not in ("chance", "outcome"):
        raise ValueError("sampling must be 'chance' or 'outcome'")
    if not 0 <= player < game.num_players:
        raise ValueError("player index is out of range")
    rng = random.Random(seed)

    def probabilities(state):
        p = state.current_player()
        actions = state.legal_actions()
        probs = strategy.get(state.info_set_key(p))
        if probs is None:
            return [1 / len(actions)] * len(actions)
        if len(probs) != len(actions) or any(x < 0 for x in probs) or abs(sum(probs) - 1) > 1e-8:
            raise ValueError(f"invalid strategy probabilities at {state.info_set_key(p)!r}")
        return probs

    def sampled(s, outcome_only: bool):
        if s.is_terminal():
            return s.returns()[player]
        if s.is_chance():
            outcomes = s.chance_outcomes()
            outcome, _ = rng.choices(outcomes, weights=[p for _, p in outcomes], k=1)[0]
            return sampled(s.child(outcome), outcome_only)
        actions = list(s.legal_actions())
        probs = probabilities(s)
        if outcome_only:
            index = rng.choices(range(len(actions)), weights=probs, k=1)[0]
            return sampled(s.child(actions[index]), True)
        return sum(p * sampled(s.child(a), False) for a, p in zip(actions, probs))

    outcome_only = sampling == "outcome"
    return sum(sampled(game.root(), outcome_only) for _ in range(samples)) / samples

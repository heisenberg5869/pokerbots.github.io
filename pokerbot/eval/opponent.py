"""Opponent modelling and safe exploitation (Module 12)."""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional


class FrequencyOpponentModel:
    """Simple frequency-based opponent model.

    Tracks observed actions per context (info set / state key) and produces
    a (smoothed) distribution over actions.
    """

    def __init__(self, actions: Optional[List[Any]] = None, smoothing: float = 1.0):
        self.actions: List[Any] = list(actions) if actions else []
        self.smoothing = float(smoothing)
        self._counts: Dict[Any, Dict[Any, float]] = defaultdict(lambda: defaultdict(float))

    def observe(self, context: Any, action: Any) -> None:
        self._counts[context][action] += 1.0
        if action not in self.actions:
            self.actions.append(action)

    def counts(self, context: Any) -> Dict[Any, float]:
        return dict(self._counts.get(context, {}))

    def total(self, context: Any) -> float:
        return float(sum(self._counts.get(context, {}).values()))

    def _action_list(self, context: Any, actions: Optional[List[Any]] = None) -> List[Any]:
        if actions is not None:
            return list(actions)
        if self.actions:
            return list(self.actions)
        return sorted(self._counts.get(context, {}).keys())

    def frequencies(self, context: Any, actions: Optional[List[Any]] = None) -> Dict[Any, float]:
        acts = self._action_list(context, actions)
        cnt = self._counts.get(context, {})
        out = {}
        for a in acts:
            out[a] = float(cnt.get(a, 0.0)) + self.smoothing
        total = sum(out.values())
        if total <= 0:
            n = len(acts) if acts else 1
            return {a: 1.0 / n for a in acts}
        return {a: v / total for a, v in out.items()}

    def predict(self, context: Any, actions: Optional[List[Any]] = None) -> List[float]:
        f = self.frequencies(context, actions)
        return [f[a] for a in f]


class SafeExploiter:
    """Best-response mixed with a Nash strategy (epsilon-safe exploitation)."""

    def __init__(
        self,
        nash_strategy: Dict[Any, List[float]],
        epsilon: float = 0.1,
        opponent_model: Optional[FrequencyOpponentModel] = None,
        actions: Optional[List[Any]] = None,
    ):
        self.nash_strategy = nash_strategy
        self.epsilon = float(epsilon)
        self.opponent_model = opponent_model
        self.actions = list(actions) if actions else None

    def _nash(self, context: Any, n: int) -> List[float]:
        strat = self.nash_strategy.get(context)
        if strat is None:
            return [1.0 / n] * n
        return list(strat)

    def mix(self, br_probs: List[float], nash_probs: List[float]) -> List[float]:
        return [
            (1.0 - self.epsilon) * b + self.epsilon * n
            for b, n in zip(br_probs, nash_probs)
        ]

    def best_response_action(
        self,
        context: Any,
        legal_actions: List[Any],
        payoff: Callable[[Any, Any], float],
        opponent_actions: Optional[List[Any]] = None,
        opponent_probs: Optional[List[float]] = None,
    ) -> int:
        if opponent_probs is None:
            if self.opponent_model is not None:
                opp_acts = opponent_actions if opponent_actions is not None else (self.opponent_model.actions or legal_actions)
                freq = self.opponent_model.frequencies(context, opp_acts)
                opponent_actions = list(freq.keys())
                opponent_probs = [freq[a] for a in opponent_actions]
            else:
                opponent_actions = opponent_actions or legal_actions
                opponent_probs = [1.0 / len(opponent_actions)] * len(opponent_actions)
        if opponent_actions is None:
            opponent_actions = legal_actions
        best_i = 0
        best_val = float("-inf")
        for i, a in enumerate(legal_actions):
            val = 0.0
            for oa, p in zip(opponent_actions, opponent_probs):
                val += p * payoff(a, oa)
            if val > best_val:
                best_val = val
                best_i = i
        return best_i

    def safe_strategy(
        self,
        context: Any,
        legal_actions: List[Any],
        payoff: Callable[[Any, Any], float],
        opponent_actions: Optional[List[Any]] = None,
        opponent_probs: Optional[List[float]] = None,
    ) -> List[float]:
        br_idx = self.best_response_action(
            context, legal_actions, payoff, opponent_actions, opponent_probs
        )
        br_probs = [1.0 if i == br_idx else 0.0 for i in range(len(legal_actions))]
        nash_probs = self._nash(context, len(legal_actions))
        if len(nash_probs) != len(legal_actions):
            nash_probs = [1.0 / len(legal_actions)] * len(legal_actions)
        return self.mix(br_probs, nash_probs)

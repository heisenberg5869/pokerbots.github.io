"""Regret matching: play each action in proportion to its positive cumulative regret."""
from __future__ import annotations


class RegretMatcher:
    def __init__(self, actions):
        self.actions = list(actions)
        n = len(self.actions)
        self.regret_sum = [0.0] * n
        self.strategy_sum = [0.0] * n

    def current_strategy(self) -> list[float]:
        pos = [max(r, 0.0) for r in self.regret_sum]
        total = sum(pos)
        n = len(pos)
        return [p / total for p in pos] if total > 0 else [1.0 / n] * n

    def average_strategy(self) -> list[float]:
        total = sum(self.strategy_sum)
        n = len(self.strategy_sum)
        return [s / total for s in self.strategy_sum] if total > 0 else [1.0 / n] * n

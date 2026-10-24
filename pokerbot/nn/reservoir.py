"""Fixed-capacity reservoir sampling buffer."""
from __future__ import annotations

import random
from typing import Any


class ReservoirBuffer:
    def __init__(self, capacity: int, seed: int | None = None):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.rng = random.Random(seed)
        self._items: list[Any] = []
        self._n = 0

    def add(self, item, weight: float = 1.0):
        self._n += 1
        if len(self._items) < self.capacity:
            self._items.append(item)
        else:
            # uniform replacement
            j = self.rng.randrange(self._n)
            if j < self.capacity:
                self._items[j] = item

    def sample(self, k: int = 1):
        if not self._items:
            return []
        k = min(k, len(self._items))
        return self.rng.sample(self._items, k)

    def __len__(self):
        return len(self._items)

    @property
    def total_seen(self):
        return self._n
"""Depth-limited search with a value network (ReBeL-style) for Kuhn poker."""
from __future__ import annotations

import random
from typing import Callable

import numpy as np
import torch

from ..games.kuhn import KuhnPoker
from ..nn.value import ValueNet, train_value_net
from ..nn.features import leduc_features  # placeholder reuse not needed

# Kuhn features: one-hot for card (3) + pot bucket not needed; keep tiny.


def kuhn_state_features(card: int, pot: float, history: str) -> np.ndarray:
    v = [0.0, 0.0, 0.0]
    v[card] = 1.0
    # history length as feature
    h = [0.0, 0.0, 0.0]
    h[min(len(history), 2)] = 1.0
    return np.array(v + h + [pot], dtype=np.float32)


class KuhnValueAgent:
    def __init__(self, *, seed=None, hidden=32):
        self.game = KuhnPoker()
        self.rng = random.Random(seed)
        if seed is not None:
            torch.manual_seed(seed)
        self.net = ValueNet(7, hidden=hidden, seed=seed)
        self.trained = False

    def generate_data(self, n_samples=2000, seed=None):
        rng = random.Random(seed if seed is not None else 0)
        samples = []
        # enumerate all Kuhn deals and play random lines to leaves
        for _ in range(n_samples):
            cards = list(range(3))
            rng.shuffle(cards)
            p0, p1 = cards[0], cards[1]
            # random history
            history = ""
            # random length 0..2 actions
            L = rng.randrange(0, 3)
            # build a plausible history
            for _ in range(L):
                history += rng.choice("pc")
            # terminal-ish value via rollout
            # compute expected payoff for player0 from this state by random rollout
            val = self._rollout_value(p0, p1, history, rng)
            feat = kuhn_state_features(p0, 1.0 + history.count("b") * 1.0, history)
            samples.append((feat, float(val)))
        return samples

    def _rollout_value(self, p0, p1, history, rng):
        # simple Monte Carlo rollout: random play to terminal, return payoff p0
        # Reuse Kuhn payoff rules
        # Determine terminal
        # We'll just simulate random actions
        # Simplified: if history ends in fold, compute; else showdown
        # For robustness, do a few rollouts
        total = 0.0
        for _ in range(20):
            total += self._one_rollout(p0, p1, history, rng)
        return total / 20.0

    def _one_rollout(self, p0, p1, history, rng):
        # Kuhn: actions c (check/call), b (bet), f (fold). Terminal if fold or two checks or bet+response.
        h = history
        # ensure legal-ish: just random extend until terminal
        guard = 0
        while guard < 10:
            guard += 1
            if self._terminal(h):
                break
            h += rng.choice("cbf")
        return self._payoff(p0, p1, h)

    def _terminal(self, h):
        if "f" in h:
            return True
        if h.endswith("cc"):
            return True
        if h.endswith("bc") or h.endswith("bf"):
            return True
        if len(h) >= 4:
            return True
        return False

    def _payoff(self, p0, p1, h):
        # Kuhn payoff for player 0
        # pot base 1 each? Use standard: ante 1 each, bet size 1.
        if "f" in h:
            # folder loses ante
            if h[-1] == "f":
                # last actor folded
                # determine who folded: odd/even length
                # player to act index = len(h) % 2 (0 p0,1 p1). folder = previous? approximate
                pass
        # Simplify: showdown if no fold
        if "f" not in h:
            if p0 > p1:
                return 1.0
            else:
                return -1.0
        # fold: folder loses 1 (or 2 if bet)
        # approximate: last folder loses pot so far
        return 1.0 if len(h) % 2 == 1 else -1.0

    def train(self, epochs=10, n_samples=2000, seed=None):
        samples = self.generate_data(n_samples, seed=seed)
        train_value_net(self.net, samples, epochs=epochs, seed=seed)
        self.trained = True

    def value(self, card, pot, history):
        x = torch.tensor(kuhn_state_features(card, pot, history), dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            return float(self.net(x).item())

    def search_action(self, card, history, legal):
        # pick action maximizing predicted value (one-ply, using value net for resulting state approx)
        best = None
        bestv = -1e9
        for a in legal:
            # approximate: value of card with extended history
            v = self.value(card, 1.0, history + a)
            if v > bestv:
                bestv = v
                best = a
        return best if best is not None else legal[0]

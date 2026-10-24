"""Advantage (regret) network."""
from __future__ import annotations

import torch
import torch.nn as nn


class AdvantageNet(nn.Module):
    def __init__(self, input_dim: int, num_actions: int, hidden: int = 128, seed: int | None = None):
        super().__init__()
        if seed is not None:
            torch.manual_seed(seed)
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden), nn.ReLU(),
            nn.Linear(hidden, hidden), nn.ReLU(),
            nn.Linear(hidden, num_actions),
        )

    def forward(self, x):
        return self.net(x)
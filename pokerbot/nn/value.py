"""Value network: predicts expected payoff (player 0) for an imperfect-info state."""
from __future__ import annotations

import random

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class ValueNet(nn.Module):
    def __init__(self, in_dim: int, hidden: int = 64, seed: int | None = None):
        super().__init__()
        if seed is not None:
            torch.manual_seed(seed)
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden),
            nn.ReLU(),
            nn.Linear(hidden, hidden),
            nn.ReLU(),
            nn.Linear(hidden, 1),
        )

    def forward(self, x):
        return self.net(x).squeeze(-1)


def train_value_net(net, samples, *, epochs=5, lr=1e-3, batch_size=64, seed=None):
    """samples: list of (features np array, target float)."""
    if seed is not None:
        torch.manual_seed(seed)
    opt = torch.optim.Adam(net.parameters(), lr=lr)
    X = torch.tensor(np.array([s[0] for s in samples]), dtype=torch.float32)
    y = torch.tensor([s[1] for s in samples], dtype=torch.float32)
    n = len(samples)
    for _ in range(epochs):
        perm = torch.randperm(n)
        for i in range(0, n, batch_size):
            idx = perm[i:i + batch_size]
            pred = net(X[idx])
            loss = F.mse_loss(pred, y[idx])
            opt.zero_grad()
            loss.backward()
            opt.step()
    return net

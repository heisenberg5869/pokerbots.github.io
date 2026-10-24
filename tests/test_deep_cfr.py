import numpy as np
import torch

from pokerbot.nn.features import leduc_features, FEATURE_DIM
from pokerbot.nn.reservoir import ReservoirBuffer
from pokerbot.nn.advantage import AdvantageNet
from pokerbot.nn.strategy import StrategyNet
from pokerbot.solvers.deep_cfr import DeepCFRTrainer
from pokerbot.solvers.single_deep_cfr import SingleDeepCFRTrainer


def test_features_shape():
    v = leduc_features("J|?|0:")
    assert v.shape == (FEATURE_DIM,)


def test_reservoir_capacity():
    b = ReservoirBuffer(5, seed=0)
    for i in range(100):
        b.add(i)
    assert len(b) == 5
    assert b.total_seen == 100


def test_nets_forward():
    a = AdvantageNet(FEATURE_DIM, 4, seed=0)
    s = StrategyNet(FEATURE_DIM, 4, seed=0)
    x = torch.tensor(leduc_features("J|?|0:"), dtype=torch.float32).unsqueeze(0)
    assert a(x).shape == (1, 4)
    assert s(x).shape == (1, 4)


def test_deep_cfr_runs():
    t = DeepCFRTrainer(seed=1)
    t.train(3)
    assert t.iterations == 3
    strat = t.average_strategy()
    assert len(strat) > 0
    for v in strat.values():
        assert abs(sum(v) - 1.0) < 1e-6


def test_single_deep_cfr_runs():
    t = SingleDeepCFRTrainer(seed=1)
    t.train(3)
    assert t.iterations == 3
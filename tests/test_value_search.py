import numpy as np

from pokerbot.solvers.value_search import KuhnValueAgent, kuhn_state_features


def test_features_shape():
    f = kuhn_state_features(0, 1.0, "")
    assert f.shape == (7,)


def test_train_runs():
    agent = KuhnValueAgent(seed=0)
    agent.train(epochs=2, n_samples=200, seed=0)
    assert agent.trained
    v = agent.value(0, 1.0, "")
    assert isinstance(v, float)


def test_search_action_legal():
    agent = KuhnValueAgent(seed=1)
    agent.train(epochs=2, n_samples=200, seed=1)
    a = agent.search_action(0, "", ["c", "b"])
    assert a in ["c", "b"]

import pytest

from pokerbot.eval.exploitability import expected_value
from pokerbot.games.kuhn import KuhnPoker
from pokerbot.solvers.mccfr import MCCFRTrainer, estimate_value


NASH = {
    "J": [1, 0], "Q": [1, 0], "K": [1, 0],
    "Jpb": [1, 0], "Qpb": [2 / 3, 1 / 3], "Kpb": [0, 1],
    "Jp": [2 / 3, 1 / 3], "Qp": [1, 0], "Kp": [0, 1],
    "Jb": [1, 0], "Qb": [2 / 3, 1 / 3], "Kb": [0, 1],
}


@pytest.mark.parametrize("sampling", ["chance", "external"])
def test_mccfr_training_produces_normalized_average_strategies(sampling):
    trainer = MCCFRTrainer(KuhnPoker(), sampling=sampling, seed=12).train(100)
    assert trainer.iterations == 100
    assert trainer.average_strategy()
    for probs in trainer.average_strategy().values():
        assert sum(probs) == pytest.approx(1)
        assert all(p >= 0 for p in probs)


@pytest.mark.parametrize("sampling", ["chance", "outcome"])
def test_sampled_value_estimates_match_exact_value(sampling):
    game = KuhnPoker()
    exact = expected_value(game, NASH, 0)
    estimate = estimate_value(game, NASH, samples=4000, sampling=sampling, seed=7)
    assert estimate == pytest.approx(exact, abs=0.06)


def test_invalid_sampling_scheme_is_rejected():
    with pytest.raises(ValueError):
        MCCFRTrainer(KuhnPoker(), sampling="unknown")

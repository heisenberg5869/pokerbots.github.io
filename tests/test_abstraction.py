import random

import pytest

from pokerbot.abstraction import earth_movers_distance, k_medoids, translate_bet, translation_probabilities


def test_earth_movers_distance_hand_calculations_and_mass_normalization():
    assert earth_movers_distance([1, 0, 0], [0, 1, 0]) == pytest.approx(1)
    assert earth_movers_distance([1, 0, 0], [0, 0, 1]) == pytest.approx(2)
    assert earth_movers_distance([2, 0], [0, 5]) == pytest.approx(1)
    assert earth_movers_distance([0, 1], [0, 3]) == pytest.approx(0)


def test_k_medoids_groups_nearby_distributions_and_is_deterministic():
    data = [[1, 0, 0], [0.9, 0.1, 0], [0, 0.1, 0.9], [0, 0, 1]]
    labels, medoids = k_medoids(data, 2)
    assert labels[0] == labels[1]
    assert labels[2] == labels[3]
    assert len(set(labels)) == 2
    assert medoids == k_medoids(data, 2)[1]


def test_linear_translation_preserves_expected_size():
    dist = translation_probabilities(3, [2, 4])
    assert dist == pytest.approx({2: 0.5, 4: 0.5})
    draws = [translate_bet(3, [2, 4], method="linear", rng=random.Random(i)) for i in range(1000)]
    assert sum(draws) / len(draws) == pytest.approx(3, abs=0.1)


def test_harmonic_translation_is_randomized_and_bounded():
    dist = translation_probabilities(3, [2, 4], method="harmonic")
    assert sum(dist.values()) == pytest.approx(1)
    assert all(0 <= p <= 1 for p in dist.values())
    assert translate_bet(3, [2, 4], method="harmonic", rng=random.Random(4)) in (2, 4)


@pytest.mark.parametrize("args", [([], 1), ([[1], [0]], 1), ([[1], [1]], 0), ([[1], [1]], 3)])
def test_invalid_clustering_inputs_are_rejected(args):
    points, k = args
    with pytest.raises(ValueError):
        k_medoids(points, k)


def test_invalid_histograms_and_menus_are_rejected():
    with pytest.raises(ValueError):
        earth_movers_distance([1, -1], [1, 0])
    with pytest.raises(ValueError):
        translate_bet(3, [], method="nearest")
    with pytest.raises(ValueError):
        translate_bet(3, [1, 4], method="unknown")

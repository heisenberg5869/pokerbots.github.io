"""Small, dependency-free tools for distribution-aware card abstraction."""
from __future__ import annotations

from typing import Sequence


def earth_movers_distance(histogram_a: Sequence[float], histogram_b: Sequence[float]) -> float:
    """1-D earth mover's distance for equally spaced, equally weighted bins.

    Histograms may have different total mass; each is normalized first. The
    distance is the sum of absolute cumulative-mass differences, in bin units.
    """
    if len(histogram_a) != len(histogram_b) or not histogram_a:
        raise ValueError("histograms must have the same nonzero number of bins")
    a, b = [float(x) for x in histogram_a], [float(x) for x in histogram_b]
    if any(x < 0 for x in (*a, *b)):
        raise ValueError("histogram mass cannot be negative")
    total_a, total_b = sum(a), sum(b)
    if total_a <= 0 or total_b <= 0:
        raise ValueError("histograms must have positive total mass")
    ca = cb = distance = 0.0
    for x, y in zip(a, b):
        ca += x / total_a
        cb += y / total_b
        distance += abs(ca - cb)
    return distance


def k_medoids(points: Sequence[Sequence[float]], k: int, *, max_iterations: int = 100) -> tuple[list[int], list[int]]:
    """Cluster short histograms with deterministic PAM-style medoid updates.

    Returns ``(labels, medoid_indices)``. This simple O(n^2) implementation is
    intended for curriculum-sized examples, not million-hand production runs.
    """
    data = [tuple(float(v) for v in p) for p in points]
    if not data or not data[0] or any(len(p) != len(data[0]) for p in data):
        raise ValueError("points must be a nonempty rectangular set of vectors")
    if any(any(v < 0 for v in p) or sum(p) <= 0 for p in data):
        raise ValueError("each point must be a nonnegative histogram with positive mass")
    if not 1 <= k <= len(data):
        raise ValueError("k must be between one and the number of points")
    n = len(data)
    distances = [[earth_movers_distance(data[i], data[j]) for j in range(n)] for i in range(n)]
    medoids = [0]
    while len(medoids) < k:
        candidate = max((i for i in range(n) if i not in medoids),
                        key=lambda i: (min(distances[i][m] for m in medoids), -i))
        medoids.append(candidate)
    labels = [0] * n
    for _ in range(max_iterations):
        labels = [min(range(k), key=lambda c: (distances[i][medoids[c]], c)) for i in range(n)]
        updated = medoids.copy()
        for c in range(k):
            members = [i for i, label in enumerate(labels) if label == c]
            if members:
                updated[c] = min(members, key=lambda i: (sum(distances[i][j] for j in members), i))
        if updated == medoids:
            break
        medoids = updated
    labels = [min(range(k), key=lambda c: (distances[i][medoids[c]], c)) for i in range(n)]
    return labels, medoids


def assign_nearest(point: Sequence[float], representatives: Sequence[Sequence[float]]) -> int:
    """Return the nearest representative index under 1-D EMD."""
    if not representatives:
        raise ValueError("at least one representative is required")
    return min(range(len(representatives)), key=lambda i: earth_movers_distance(point, representatives[i]))

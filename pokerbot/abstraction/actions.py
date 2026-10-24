"""Action abstraction and off-tree bet translation helpers."""
from __future__ import annotations

import random
from collections.abc import Sequence


def translate_bet(amount: float, abstract_sizes: Sequence[float], *, method: str = "nearest",
                  rng: random.Random | None = None) -> float:
    """Map an off-tree bet to an abstract size.

    ``nearest`` picks the closest size (ties go smaller). ``linear`` randomly
    chooses the adjacent sizes with probabilities preserving the input amount
    in expectation. ``harmonic`` uses inverse-size interpolation weights. These are
    pedagogical translation rules, not safe solving.
    """
    sizes = sorted(set(float(x) for x in abstract_sizes))
    if not sizes or any(x < 0 for x in sizes) or amount < 0:
        raise ValueError("bet and abstract sizes must be nonnegative; menu cannot be empty")
    if amount <= sizes[0]:
        return sizes[0]
    if amount >= sizes[-1]:
        return sizes[-1]
    upper_i = next(i for i, size in enumerate(sizes) if size >= amount)
    lo, hi = sizes[upper_i - 1], sizes[upper_i]
    if method == "nearest":
        return lo if amount - lo <= hi - amount else hi
    if method == "linear":
        p_hi = (amount - lo) / (hi - lo)
    elif method == "harmonic":
        # Interpolate in reciprocal size, then convert to a probability over
        # the two sizes. The formula reduces to linear at the interval edges.
        inv_lo, inv_hi, inv_x = 1 / max(lo, 1e-12), 1 / hi, 1 / amount
        p_hi = (inv_lo - inv_x) / (inv_lo - inv_hi)
    else:
        raise ValueError("method must be 'nearest', 'linear', or 'harmonic'")
    p_hi = min(1.0, max(0.0, p_hi))
    return hi if (rng or random).random() < p_hi else lo


def translation_probabilities(amount: float, abstract_sizes: Sequence[float], *, method: str = "linear") -> dict[float, float]:
    """Return the exact discrete distribution used by randomized translation."""
    sizes = sorted(set(float(x) for x in abstract_sizes))
    if not sizes or any(x < 0 for x in sizes) or amount < 0:
        raise ValueError("bet and abstract sizes must be nonnegative; menu cannot be empty")
    if amount <= sizes[0]:
        return {sizes[0]: 1.0}
    if amount >= sizes[-1]:
        return {sizes[-1]: 1.0}
    i = next(i for i, x in enumerate(sizes) if x >= amount)
    lo, hi = sizes[i - 1], sizes[i]
    if method == "linear":
        p_hi = (amount - lo) / (hi - lo)
    elif method == "harmonic":
        p_hi = ((1 / max(lo, 1e-12)) - (1 / amount)) / ((1 / max(lo, 1e-12)) - (1 / hi))
    else:
        raise ValueError("method must be 'linear' or 'harmonic'")
    return {lo: 1 - p_hi, hi: p_hi}

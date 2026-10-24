"""Control-variate variance reduction for match estimates."""
from __future__ import annotations

import math
from typing import Sequence


def _mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def control_variate(y: Sequence[float], x: Sequence[float]) -> list:
    """Return control-variate adjusted values with same mean as y but smaller variance.

    Uses linear regression of y on x and adjusts by the covariate's deviation
    from its own mean. The adjustment preserves the sample mean of y (unbiased).
    """
    n = len(y)
    if n == 0:
        return []
    mx = _mean(x)
    my = _mean(y)
    # beta = cov(y,x)/var(x)
    cov = sum((yi - my) * (xi - mx) for yi, xi in zip(y, x)) / n
    varx = sum((xi - mx) ** 2 for xi in x) / n
    beta = cov / varx if varx > 0 else 0.0
    adjusted = [yi - beta * (xi - mx) for yi, xi in zip(y, x)]
    return adjusted


def cv_estimate(y, x):
    adj = control_variate(y, x)
    return _mean(adj), adj


class ControlVariateEstimator:
    def estimate(self, y, x):
        adj = control_variate(y, x)
        m = _mean(adj)
        var = sum((v - m) ** 2 for v in adj) / max(1, len(adj) - 1)
        return m, math.sqrt(var), adj


# aliases
control_variate_estimate = cv_estimate
variance_reduction = control_variate

"""Featurization for information sets (Leduc-focused)."""
from __future__ import annotations

import numpy as np


def leduc_features(info_key: str) -> np.ndarray:
    # info_key like "J|?|0:cb" or "J|K|1:cc/b"
    parts = info_key.split("|")
    rank = parts[0]
    board = parts[1]
    rest = parts[2]  # round:history
    rnd, hist = (rest.split(":", 1) + [""])[:2] if ":" in rest else (rest, "")

    ranks = "JQK"
    vec = []
    # private rank one-hot (3)
    for r in ranks:
        vec.append(1.0 if rank == r else 0.0)
    # board one-hot (3 ranks + unknown)
    for r in ranks:
        vec.append(1.0 if board == r else 0.0)
    vec.append(1.0 if board == "?" else 0.0)
    # round one-hot (2)
    for r in ("0", "1"):
        vec.append(1.0 if rnd == r else 0.0)
    # history: counts of actions
    for a in "fcbr/":
        vec.append(float(hist.count(a)))
    # history length
    vec.append(float(len(hist)))
    return np.asarray(vec, dtype=np.float32)


FEATURE_DIM = len(leduc_features("J|?|0:"))
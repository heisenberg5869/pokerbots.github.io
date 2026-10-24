"""Rebuild the deterministic push/fold chart data for the Module 07 browser lab.

The lab needs a strategy table per stack depth. Solving in the browser would
duplicate the Python solver and drift from it, so this script solves each depth
here, rounds the probabilities, and writes a static JSON file. The seed and
iteration budget are recorded in the manifest so the output is reproducible and
``tests/test_pushfold_demo_data.py`` can re-solve one depth and compare exactly.

Run from the repository root::

    python tools/build_pushfold_lab_data.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pokerbot.solvers.push_fold import (  # noqa: E402
    N_CLASSES,
    class_name,
    combo_count,
    default_equity,
    solve_push_fold,
)

OUTPUT = ROOT / "docs" / "demos" / "pushfold-module-07-data.json"
DEPTHS = tuple(range(1, 21))      # big blinds
ITERATIONS = 200_000
SEED = 7
ANTE = 1                          # one ante = half a big blind in this model


def profile_value(result, stack: int) -> float:
    """Small blind's EV in antes for the solved profile, no card removal."""
    total = float(sum(combo_count(i) for i in range(N_CLASSES)))
    value = 0.0
    for i in range(N_CLASSES):
        shove = result.shove_threshold[i]
        fold = 1.0 - shove
        row = 0.0
        for j in range(N_CLASSES):
            call = result.call_threshold[j]
            showdown = stack * (2.0 * default_equity(i, j) - 1.0)
            row += combo_count(j) * (shove * ((1.0 - call) * ANTE + call * showdown)
                                     + fold * -ANTE)
        value += combo_count(i) * row
    return value / (total * total)


def main() -> None:
    depths: dict[str, dict] = {}
    for bb in DEPTHS:
        stack = bb * 2  # two antes per big blind
        result = solve_push_fold(stack=stack, ante=ANTE,
                                 iterations=ITERATIONS, seed=SEED)
        depths[str(bb)] = {
            "shove": [round(result.shove_threshold[i], 3) for i in range(N_CLASSES)],
            "call": [round(result.call_threshold[i], 3) for i in range(N_CLASSES)],
            "ev_bb": round(profile_value(result, stack) / 2.0, 4),
        }

    data = {
        "manifest": {
            "game": "Heads-up push/fold",
            "rules": "Both players post a one-ante blind (half a big blind); "
                     "the small blind shoves all-in or folds, then the big blind "
                     "calls or folds. Stack depth is measured in big blinds.",
            "equity": "Deterministic Bradley-Terry strength heuristic over 169 "
                      "starting-hand classes; not a measured preflop equity table, "
                      "so ranges are wider than published charts.",
            "model_note": "Chance sampling draws the two hand classes independently, "
                          "so card removal between the players is ignored.",
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "iterations": ITERATIONS,
            "seed": SEED,
            "depths_bb": list(DEPTHS),
            "class_order": [class_name(i) for i in range(N_CLASSES)],
            "combos": [combo_count(i) for i in range(N_CLASSES)],
        },
        "depths": depths,
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size:,} bytes)")
    for bb in DEPTHS:
        row = depths[str(bb)]
        shoves = sum(1 for p in row["shove"] if p > 0.5)
        calls = sum(1 for p in row["call"] if p > 0.5)
        print(f"{bb:>2} bb: shove {shoves:>3}/169  call {calls:>3}/169  "
              f"EV {row['ev_bb']:+.3f} bb")


if __name__ == "__main__":
    main()

"""Keep the static Module 07 push/fold lab aligned with the Python solver."""
import json
from pathlib import Path

import pytest

from pokerbot.solvers.push_fold import (
    N_CLASSES,
    class_index,
    class_name,
    combo_count,
    solve_push_fold,
)

DATA_PATH = (Path(__file__).parents[1] / "docs" / "demos"
             / "pushfold-module-07-data.json")


@pytest.fixture(scope="module")
def data():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def weighted(values, combos):
    return sum(v * c for v, c in zip(values, combos)) / sum(combos)


def test_manifest_describes_a_reproducible_game(data):
    manifest = data["manifest"]
    assert manifest["game"] == "Heads-up push/fold"
    assert manifest["depths_bb"] == list(range(1, 21))
    assert manifest["iterations"] == 200_000
    assert isinstance(manifest["seed"], int)
    assert "heuristic" in manifest["equity"]
    assert "card removal" in manifest["model_note"]
    assert len(manifest["class_order"]) == N_CLASSES
    assert len(set(manifest["class_order"])) == N_CLASSES
    assert manifest["class_order"] == [class_name(i) for i in range(N_CLASSES)]
    assert sum(manifest["combos"]) == 1326


def test_every_depth_has_a_complete_strategy(data):
    for depth in data["manifest"]["depths_bb"]:
        row = data["depths"][str(depth)]
        assert len(row["shove"]) == N_CLASSES
        assert len(row["call"]) == N_CLASSES
        assert all(0.0 <= p <= 1.0 for p in row["shove"] + row["call"])
        assert row["ev_bb"] <= 0.0      # the small blind posts first


def test_value_falls_monotonically_with_depth(data):
    values = [data["depths"][str(d)]["ev_bb"] for d in data["manifest"]["depths_bb"]]
    assert all(a > b for a, b in zip(values, values[1:]))


def test_ranges_narrow_with_depth(data):
    combos = data["manifest"]["combos"]
    shallow = data["depths"]["1"]
    deep = data["depths"]["20"]
    assert weighted(shallow["shove"], combos) > 0.90
    assert weighted(deep["shove"], combos) < 0.55
    assert weighted(deep["call"], combos) < 0.40
    assert weighted(deep["call"], combos) < weighted(shallow["call"], combos)


def test_known_hands_behave_as_expected(data):
    aces = class_index("AA")
    junk = class_index("72o")
    for depth in data["manifest"]["depths_bb"]:
        assert data["depths"][str(depth)]["shove"][aces] > 0.95
    assert data["depths"]["20"]["shove"][junk] < 0.5
    assert data["depths"]["20"]["call"][junk] < 0.5


def test_stored_strategy_reproduces_from_the_manifest(data):
    """Re-solve one depth with the recorded seed and iterations."""
    manifest = data["manifest"]
    result = solve_push_fold(stack=10 * 2, ante=1,
                             iterations=manifest["iterations"],
                             seed=manifest["seed"])
    stored = data["depths"]["10"]
    assert [round(result.shove_threshold[i], 3) for i in range(N_CLASSES)] == stored["shove"]
    assert [round(result.call_threshold[i], 3) for i in range(N_CLASSES)] == stored["call"]


def test_combo_counts_match_the_solver(data):
    assert data["manifest"]["combos"] == [combo_count(i) for i in range(N_CLASSES)]

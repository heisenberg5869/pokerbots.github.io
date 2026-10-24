"""Keep the static Module 03 browser lab aligned with the Python solver."""
import json
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def data():
    path = Path(__file__).parents[1] / "docs" / "demos" / "leduc-module-03-data.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_has_reproducible_game_and_iteration_budgets(data):
    manifest = data["manifest"]
    assert manifest["game"] == "Six-card Leduc Hold'em"
    assert manifest["iterations"] == [1, 5, 20, 50]
    assert manifest["node_count"] == 9451
    assert manifest["infoset_count_rank_symmetric"] == 288
    assert "two wagers total" in manifest["rules"]
    assert "deterministic" in manifest["seed"]
    counts = manifest["example_path_counts"]
    assert counts["after_deal"] < manifest["node_count"]
    assert counts["after_p0_bet"] < counts["after_p0_check"]
    assert counts["after_king_board"] < counts["after_checks"]


def test_snapshot_strategies_match_game_action_catalog(data):
    for variant in data["variants"].values():
        frames = variant["frames"]
        assert [frame["iteration"] for frame in frames] == data["manifest"]["iterations"]
        for frame in frames:
            assert set(frame["strategy"]) <= set(data["actions"])
            for key, probabilities in frame["strategy"].items():
                assert len(probabilities) == len(data["actions"][key])
                assert sum(probabilities) == pytest.approx(1)
                assert all(0 <= probability <= 1 for probability in probabilities)
            assert frame["exploitability"] >= 0


def test_round_two_keys_have_one_round_separator(data):
    keys = [key for key in data["actions"] if "|1:" in key]
    assert keys
    assert all("//" not in key for key in keys)

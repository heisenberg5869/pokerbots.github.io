import json
from pathlib import Path
DATA_PATH = Path(__file__).parents[1] / "docs" / "demos" / "flop-module-07-data.json"
def test_manifest():
    d=json.loads(DATA_PATH.read_text(encoding="utf-8"))
    assert d["manifest"]["board_count"] == 30
    assert len(d["boards"]) == 30
def test_probs_sum():
    d=json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for b in d["boards"].values():
        for pos in ("oop","ip"):
            n=len(b[pos]["bet"])
            for i in range(n):
                assert abs(b[pos]["bet"][i]+b[pos]["check"][i]-1.0) < 1e-9
def test_ranges():
    d=json.loads(DATA_PATH.read_text(encoding="utf-8"))
    for b in d["boards"].values():
        for pos in ("oop","ip"):
            for p in b[pos]["bet"]+b[pos]["check"]:
                assert 0.0 <= p <= 1.0
import json

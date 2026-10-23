"""Rebuild deterministic strategy snapshots and CFR comparison data for Module 03."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pokerbot.eval.exploitability import expected_value, exploitability
from pokerbot.games.leduc import LeducPoker
from pokerbot.solvers.cfr import CFRTrainer

OUTPUT = ROOT / "docs" / "demos" / "leduc_data.json"
CHECKPOINTS = (1, 5, 20, 50)
VARIANTS = {
    "vanilla": {},
    "cfr_plus": {"plus": True},
    "alternating_plus_linear": {"plus": True, "alternating": True, "linear_average": True},
    "discounted": {"discount": (1.5, 0.5, 2.0)},
}


def action_catalog(game):
    catalog = {}

    def walk(state):
        if state.is_terminal():
            return
        if state.is_chance():
            for outcome, _ in state.chance_outcomes():
                walk(state.child(outcome))
            return
        player = state.current_player()
        key = state.info_set_key(player)
        catalog[key] = list(state.legal_actions())
        for action in state.legal_actions():
            walk(state.child(action))

    walk(game.root())
    return catalog


def count_tree(state):
    if state.is_terminal():
        return 1
    if state.is_chance():
        return 1 + sum(count_tree(state.child(outcome)) for outcome, _ in state.chance_outcomes())
    return 1 + sum(count_tree(state.child(action)) for action in state.legal_actions())


def main():
    game = LeducPoker()
    catalog = action_catalog(game)
    example_deal = game.root().child((0, 2))  # J♥ versus Q♥
    after_first_check = example_deal.child("c")
    after_first_bet = example_deal.child("b")
    after_checks = after_first_check.child("c")
    after_king = after_checks.child(4)
    data = {
        "manifest": {
            "game": "Six-card Leduc Hold'em",
            "rules": "ante=1; bets=2 then 4; two wagers total per round (opening bet plus one re-raise); P0 acts first both rounds",
            "source_commit": subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
            ).strip(),
            "iterations": list(CHECKPOINTS),
            "seed": "none (deterministic exact traversal)",
            "strategy_note": "Low-iteration average strategies for exploration, not a verified equilibrium.",
            "node_count": count_tree(game.root()),
            "infoset_count_rank_symmetric": len(catalog),
            "example_path_counts": {
                "after_deal": count_tree(example_deal),
                "after_p0_check": count_tree(after_first_check),
                "after_p0_bet": count_tree(after_first_bet),
                "after_checks": count_tree(after_checks),
                "after_king_board": count_tree(after_king),
            },
        },
        "actions": catalog,
        "variants": {},
    }

    for name, options in VARIANTS.items():
        trainer = CFRTrainer(game, **options)
        previous = 0
        frames = []
        for checkpoint in CHECKPOINTS:
            trainer.train(checkpoint - previous)
            previous = checkpoint
            strategy = trainer.average_strategy()
            frames.append({
                "iteration": checkpoint,
                "exploitability": exploitability(game, strategy),
                "value_p0": expected_value(game, strategy, 0),
                "strategy": strategy,
            })
        data["variants"][name] = {"options": options, "frames": frames}

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(data, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size:,} bytes)")
    print(f"Tree nodes: {data['manifest']['node_count']:,}; infosets: {len(catalog):,}")
    for name, result in data["variants"].items():
        print(name, [(f["iteration"], round(f["exploitability"], 6)) for f in result["frames"]])


if __name__ == "__main__":
    main()

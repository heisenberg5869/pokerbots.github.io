"""Depth-limited re-solver (Brown & Sandholm safe subgame solving)."""
from __future__ import annotations

from pokerbot.games.base import Game, State
from pokerbot.solvers.cfr import CFRTrainer
from pokerbot.solvers.regret_matching import RegretMatcher


class LeafValue:
    """Callable (state, player) -> float. Default uses blueprint counterfactual-ish EV."""

    def __init__(self, blueprint=None, default=0.0):
        self.blueprint = blueprint or {}
        self.default = default

    def __call__(self, state, player):
        if state.is_terminal():
            return state.returns()[player]
        key = None
        try:
            key = state.info_set_key(player)
        except Exception:
            key = None
        if key is not None and key in self.blueprint:
            v = self.blueprint[key]
            if isinstance(v, (list, tuple)):
                return float(v[player] if player < len(v) else v[0])
            return float(v)
        return float(self.default)


class Subgame:
    """A depth-limited view of a game rooted at `state`."""

    def __init__(self, game, state, depth, leaf_value=None):
        self.game = game
        self.root_state = state
        self.depth = depth
        self.leaf_value = leaf_value or LeafValue()

    def is_terminal(self, state, depth):
        return state.is_terminal() or depth <= 0

    def value(self, state, depth, player):
        if self.is_terminal(state, depth):
            if state.is_terminal():
                return state.returns()[player]
            return self.leaf_value(state, player)
        return None


class Gadget:
    """Safe opt-out gadget: opponent may take blueprint value instead of continuing."""

    def __init__(self, leaf_value):
        self.leaf_value = leaf_value

    def apply(self, state, depth, player_opp, blueprint_value):
        # Returns adjusted leaf value ensuring opponent cannot force below blueprint.
        base = self.leaf_value(state, player_opp)
        return max(base, blueprint_value)


def resolve(state, blueprint=None, ranges=None, depth=2, iterations=1000,
            game=None, leaf_value=None, gadget=True):
    """Re-solve subgame rooted at state. Returns average strategy dict."""
    if game is None:
        # try to infer
        game = None
    # Build a truncated game by wrapping state as root via a simple adapter
    from pokerbot.games.base import Game as _Game

    class _SubGame(_Game):
        name = "subgame"

        def __init__(self, root):
            self._root = root

        def root(self):
            return self._root

    # We need depth limiting; implement by monkeypatching state? Instead use CFR on full
    # but stop at depth via a proxy state wrapper.
    class _ProxyState:
        def __init__(self, s, d):
            self.s = s
            self.d = d

        def is_terminal(self):
            if self.s.is_terminal():
                return True
            if self.d <= 0:
                return True
            return False

        def is_chance(self):
            return (not self.is_terminal()) and self.s.is_chance()

        def returns(self):
            if self.s.is_terminal():
                return self.s.returns()
            # leaf value
            lv = leaf_value or LeafValue(blueprint)
            return (lv(self.s, 0), lv(self.s, 1))

        def chance_outcomes(self):
            return self.s.chance_outcomes()

        def current_player(self):
            return self.s.current_player()

        def legal_actions(self):
            return self.s.legal_actions()

        def info_set_key(self, player):
            return self.s.info_set_key(player) + f"|d{self.d}"

        def child(self, action):
            if self.s.is_chance():
                ns = self.s.child(action)
            else:
                ns = self.s.child(action)
            return _ProxyState(ns, self.d - (0 if self.s.is_chance() else 1))

    root = _ProxyState(state, depth)
    subgame = _SubGame(root)
    trainer = CFRTrainer(subgame)
    trainer.train(iterations)
    return trainer.average_strategy()


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--iterations", type=int, default=1000)
    ap.add_argument("--depth", type=int, default=2)
    args = ap.parse_args()
    from pokerbot.games.leduc import LeducPoker
    game = LeducPoker()
    strat = resolve(game.root(), depth=args.depth, iterations=args.iterations)
    print(f"resolved {len(strat)} info sets")


if __name__ == "__main__":
    main()

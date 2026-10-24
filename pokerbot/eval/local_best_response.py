"""Local best response helpers shared with the match harness (deliverable 2/3)."""
from __future__ import annotations


def local_best_response_value(game, strategy, player, state=None):
    """Best-response value for `player` to `strategy` in the subgame rooted at state."""
    if state is None:
        state = game.root()
    if state.is_terminal():
        return state.returns()[player]
    if state.is_chance():
        v = 0.0
        for outcome, p in state.chance_outcomes():
            v += p * local_best_response_value(game, strategy, player, state.child(outcome))
        return v
    cp = state.current_player()
    if cp == player:
        best = float("-inf")
        for a in state.legal_actions():
            best = max(best, local_best_response_value(game, strategy, player, state.child(a)))
        return best
    key = state.info_set_key(cp)
    strat = strategy.get(key, None)
    actions = list(state.legal_actions())
    if strat is None:
        probs = [1.0 / len(actions)] * len(actions)
    else:
        probs = list(strat)
    v = 0.0
    for a, prob in zip(actions, probs):
        v += prob * local_best_response_value(game, strategy, player, state.child(a))
    return v
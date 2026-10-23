"""Vanilla CFR (full tree traversal each iteration) for two-player games.

Convergence guarantee: the AVERAGE strategy approaches a Nash equilibrium in
two-player zero-sum games; the current strategy need not.
"""
from __future__ import annotations
from .regret_matching import RegretMatcher


class CFRTrainer:
    def __init__(self, game, *, plus=False, alternating=False,
                 linear_average=False, discount=None):
        """Create a tabular CFR trainer.

        ``plus`` floors cumulative regrets at zero (CFR+). ``alternating``
        updates one player's regrets per traversal. ``linear_average`` weights
        iteration t by t in the average strategy. ``discount`` may be a
        (positive, negative, average) exponent tuple for discounted CFR.
        These switches are intended for small games and teaching experiments.
        """
        self.game = game
        self.nodes: dict[str, RegretMatcher] = {}
        self.iterations = 0
        self.plus = plus
        self.alternating = alternating
        self.linear_average = linear_average
        self.discount = discount

    def train(self, iterations: int, callback=None, callback_every: int = 0):
        for _ in range(iterations):
            self.iterations += 1
            if self.discount:
                positive, negative, average = self.discount
                ratio = self.iterations / (self.iterations + 1)
                for node in self.nodes.values():
                    node.regret_sum = [r * ratio ** (positive if r >= 0 else negative)
                                       for r in node.regret_sum]
                    node.strategy_sum = [s * ratio ** average for s in node.strategy_sum]
            if self.alternating:
                for player in (0, 1):
                    self._regret_deltas = {} if self.plus else None
                    self._walk(self.game.root(), [1.0, 1.0, 1.0], player)
                    if self.plus:
                        self._apply_regret_deltas()
            else:
                self._regret_deltas = {} if self.plus else None
                self._walk(self.game.root(), [1.0, 1.0, 1.0], None)
                if self.plus:
                    self._apply_regret_deltas()
            if callback and callback_every and self.iterations % callback_every == 0:
                callback(self)

    def _walk(self, state, reach, update_player=None):
        """Returns the expected payoff vector of `state` under the current strategies.

        reach = [pi_0, pi_1, pi_chance]: probability each party's own choices
        (and chance) lead to this state.
        """
        if state.is_terminal():
            return state.returns()

        if state.is_chance():
            value = None
            for outcome, p in state.chance_outcomes():
                r = [reach[0], reach[1], reach[2] * p]
                v = self._walk(state.child(outcome), r, update_player)
                value = [p * x for x in v] if value is None else [a + p * x for a, x in zip(value, v)]
            return value

        player = state.current_player()
        key = state.info_set_key(player)
        actions = state.legal_actions()
        node = self.nodes.setdefault(key, RegretMatcher(actions))
        strategy = node.current_strategy()

        action_values = []
        for a, prob in zip(actions, strategy):
            r = list(reach)
            r[player] *= prob
            action_values.append(self._walk(state.child(a), r, update_player))

        n_players = len(reach) - 1
        node_value = [sum(strategy[i] * action_values[i][p] for i in range(len(actions)))
                      for p in range(n_players)]

        # counterfactual reach: everyone EXCEPT `player` (opponent and chance)
        cf_reach = reach[2]
        for q in range(n_players):
            if q != player:
                cf_reach *= reach[q]
        if update_player is None or update_player == player:
            for i in range(len(actions)):
                regret = cf_reach * (action_values[i][player] - node_value[player])
                if self.plus:
                    delta = self._regret_deltas.setdefault(key, [0.0] * len(actions))
                    delta[i] += regret
                else:
                    node.regret_sum[i] += regret
                weight = self.iterations if self.linear_average else 1.0
                node.strategy_sum[i] += weight * reach[player] * strategy[i]
        return node_value

    def _apply_regret_deltas(self):
        """Apply one summed information-set update before CFR+ clipping."""
        for key, deltas in self._regret_deltas.items():
            node = self.nodes[key]
            node.regret_sum = [max(0.0, regret + delta)
                               for regret, delta in zip(node.regret_sum, deltas)]
        self._regret_deltas = None

    def average_strategy(self) -> dict[str, list[float]]:
        return {k: n.average_strategy() for k, n in self.nodes.items()}


if __name__ == "__main__":
    from ..games.kuhn import KuhnPoker
    from ..eval.exploitability import exploitability, expected_value

    game = KuhnPoker()
    trainer = CFRTrainer(game)
    trainer.train(20000)
    strat = trainer.average_strategy()
    print("Kuhn Poker, vanilla CFR, 20000 iterations [P(pass), P(bet)]")
    for key in sorted(strat):
        print(f"  {key:>4}: pass={strat[key][0]:.3f}  bet={strat[key][1]:.3f}")
    print(f"game value for player 0: {expected_value(game, strat, 0):+.4f}  (Nash: {-1/18:+.4f})")
    print(f"exploitability: {exploitability(game, strat):.6f}")

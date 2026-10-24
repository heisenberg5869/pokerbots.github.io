"""Deep CFR trainer (two-network) for small poker games (Leduc)."""
from __future__ import annotations

import random
from typing import Callable

import numpy as np
import torch
import torch.nn.functional as F

from ..games.leduc import LeducPoker
from ..nn.advantage import AdvantageNet
from ..nn.features import leduc_features, FEATURE_DIM
from ..nn.reservoir import ReservoirBuffer
from ..nn.strategy import StrategyNet

ACTIONS = ["f", "c", "b", "r"]


def _feat(key):
    return leduc_features(key)


class DeepCFRTrainer:
    def __init__(self, game=None, *, seed: int | None = None, hidden: int = 64,
                 buffer_cap: int = 20000, batch_size: int = 128):
        self.game = game or LeducPoker()
        self.rng = random.Random(seed)
        if seed is not None:
            torch.manual_seed(seed)
        self.adv = AdvantageNet(FEATURE_DIM, len(ACTIONS), hidden=hidden, seed=seed)
        self.strat = StrategyNet(FEATURE_DIM, len(ACTIONS), hidden=hidden, seed=seed)
        self.reg_buf = ReservoirBuffer(buffer_cap, seed=seed)
        self.strat_buf = ReservoirBuffer(buffer_cap, seed=seed)
        self.batch_size = batch_size
        self.opt_adv = torch.optim.Adam(self.adv.parameters(), lr=1e-3)
        self.opt_strat = torch.optim.Adam(self.strat.parameters(), lr=1e-3)
        self.iterations = 0
        self._action_map = {a: i for i, a in enumerate(ACTIONS)}
        self._info_actions: dict[str, list[str]] = {}

    def _legal_idx(self, actions):
        return [self._action_map[a] for a in actions]

    def _adv_predict(self, key, actions):
        with torch.no_grad():
            x = torch.tensor(_feat(key), dtype=torch.float32).unsqueeze(0)
            out = self.adv(x).squeeze(0).numpy()
        idx = self._legal_idx(actions)
        return [float(out[i]) for i in idx]

    def _strategy_from_adv(self, key, actions):
        regrets = self._adv_predict(key, actions)
        # regret matching
        r = [max(0.0, v) for v in regrets]
        s = sum(r)
        if s <= 0:
            return [1.0 / len(actions)] * len(actions)
        return [v / s for v in r]

    def _traverse(self, state, reach, traverser):
        if state.is_terminal():
            return list(state.returns())
        if state.is_chance():
            outcomes = state.chance_outcomes()
            outcome, prob = self.rng.choices(outcomes, weights=[p for _, p in outcomes], k=1)[0]
            child_reach = list(reach); child_reach[-1] *= prob
            return self._traverse(state.child(outcome), child_reach, traverser)

        player = state.current_player()
        key = state.info_set_key(player)
        actions = list(state.legal_actions())
        self._info_actions[key] = actions

        if player != traverser:
            # sample opponent action from current strategy (advantage net)
            strat = self._strategy_from_adv(key, actions)
            idx = self.rng.choices(range(len(actions)), weights=strat, k=1)[0]
            child_reach = list(reach); child_reach[player] *= strat[idx]
            return self._traverse(state.child(actions[idx]), child_reach, traverser)

        # traverser: expand all actions
        action_values = []
        for a in actions:
            child_reach = list(reach); child_reach[player] *= (1.0 / len(actions))  # placeholder; not used for regret
            action_values.append(self._traverse(state.child(a), child_reach, traverser))

        node_value = [sum((1.0 / len(actions)) * action_values[i][p] for i in range(len(actions)))
                      for p in range(self.game.num_players)]
        # regrets
        regrets = [action_values[i][player] - node_value[player] for i in range(len(actions))]
        # opponent reach for external sampling
        opp_reach = reach[1 - player]
        scaled = [opp_reach * r for r in regrets]
        # store regret sample
        target = [0.0] * len(ACTIONS)
        for a, r in zip(actions, scaled):
            target[self._action_map[a]] = r
        self.reg_buf.add((_feat(key), target, actions))
        # strategy target: current strategy (regret matching from net not available pre; use uniform-ish) store reach*strategy
        # We'll store after computing strategy from current adv (already) but use regret-matched from *this* regret? Use regrets.
        rpos = [max(0.0, v) for v in regrets]
        s = sum(rpos)
        if s > 0:
            strat = [v / s for v in rpos]
        else:
            strat = [1.0 / len(actions)] * len(actions)
        weighted = [reach[player] * strat[i] for i in range(len(actions))]
        # map to full action vector
        starget = [0.0] * len(ACTIONS)
        for a, w in zip(actions, weighted):
            starget[self._action_map[a]] = w
        self.strat_buf.add((_feat(key), starget, actions))
        return node_value

    def train_iteration(self):
        for traverser in range(self.game.num_players):
            self._traverse(self.game.root(), [1.0] * self.game.num_players + [1.0], traverser)
        self.iterations += 1
        # train nets
        self._train_adv()
        self._train_strat()

    def _train_adv(self):
        if len(self.reg_buf) < self.batch_size:
            return
        batch = self.reg_buf.sample(self.batch_size)
        xs = torch.tensor(np.stack([b[0] for b in batch]))
        ys = torch.tensor(np.stack([b[1] for b in batch]), dtype=torch.float32)
        masks = torch.zeros_like(ys)
        for i, b in enumerate(batch):
            for a in b[2]:
                masks[i, self._action_map[a]] = 1.0
        pred = self.adv(xs)
        loss = ((pred - ys) ** 2 * masks).sum() / masks.sum().clamp(min=1)
        self.opt_adv.zero_grad(); loss.backward(); self.opt_adv.step()

    def _train_strat(self):
        if len(self.strat_buf) < self.batch_size:
            return
        batch = self.strat_buf.sample(self.batch_size)
        xs = torch.tensor(np.stack([b[0] for b in batch]))
        ys = torch.tensor(np.stack([b[1] for b in batch]), dtype=torch.float32)
        masks = torch.zeros_like(ys)
        for i, b in enumerate(batch):
            for a in b[2]:
                masks[i, self._action_map[a]] = 1.0
        pred = self.strat(xs)
        # softmax over legal actions; target normalized
        # convert target to prob
        tgt = ys * masks
        denom = tgt.sum(dim=1, keepdim=True).clamp(min=1e-8)
        tgt = tgt / denom
        # mask logits
        logits = pred.masked_fill(masks == 0, -1e9)
        logp = F.log_softmax(logits, dim=1)
        loss = -(tgt * logp * masks).sum() / masks.sum().clamp(min=1)
        self.opt_strat.zero_grad(); loss.backward(); self.opt_strat.step()

    def train(self, iterations: int, callback=None, callback_every: int = 0):
        for _ in range(iterations):
            self.train_iteration()
            if callback and callback_every and self.iterations % callback_every == 0:
                callback(self)
        return self

    def average_strategy(self) -> dict[str, list[float]]:
        out = {}
        for key, actions in self._info_actions.items():
            with torch.no_grad():
                x = torch.tensor(_feat(key), dtype=torch.float32).unsqueeze(0)
                logits = self.strat(x).squeeze(0).numpy()
            idx = self._legal_idx(actions)
            vals = [logits[i] for i in idx]
            # softmax
            m = max(vals); ex = [np.exp(v - m) for v in vals]; s = sum(ex)
            out[key] = [e / s for e in ex]
        return out


def main():
    t = DeepCFRTrainer(seed=0)
    t.train(20)
    print("iterations", t.iterations)
    print("num info sets", len(t.average_strategy()))


if __name__ == "__main__":
    main()
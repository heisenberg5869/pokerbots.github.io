"""Single Deep CFR: one network approximates regret and strategy."""
from __future__ import annotations

import torch
import torch.nn as nn

from .deep_cfr import DeepCFRTrainer, ACTIONS, _feat
from ..nn.features import FEATURE_DIM


class SingleNet(nn.Module):
    def __init__(self, input_dim=FEATURE_DIM, num_actions=len(ACTIONS), hidden=64, seed=None):
        super().__init__()
        if seed is not None:
            torch.manual_seed(seed)
        self.shared = nn.Sequential(nn.Linear(input_dim, hidden), nn.ReLU(),
                                    nn.Linear(hidden, hidden), nn.ReLU())
        self.regret_head = nn.Linear(hidden, num_actions)
        self.strat_head = nn.Linear(hidden, num_actions)

    def forward(self, x):
        h = self.shared(x)
        return self.regret_head(h), self.strat_head(h)


class SingleDeepCFRTrainer(DeepCFRTrainer):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        seed = kw.get("seed")
        hidden = kw.get("hidden", 64)
        self.single = SingleNet(hidden=hidden, seed=seed)
        self.adv = self.single  # alias not used directly
        self.strat = self.single
        self.opt = torch.optim.Adam(self.single.parameters(), lr=1e-3)

    # override predict helpers
    def _adv_predict(self, key, actions):
        with torch.no_grad():
            x = torch.tensor(_feat(key), dtype=torch.float32).unsqueeze(0)
            r, _ = self.single(x)
            out = r.squeeze(0).numpy()
        idx = self._legal_idx(actions)
        return [float(out[i]) for i in idx]

    def average_strategy(self):
        out = {}
        for key, actions in self._info_actions.items():
            with torch.no_grad():
                x = torch.tensor(_feat(key), dtype=torch.float32).unsqueeze(0)
                _, s = self.single(x)
                logits = s.squeeze(0).numpy()
            idx = self._legal_idx(actions)
            vals = [logits[i] for i in idx]
            m = max(vals); ex = [__import__("numpy").exp(v - m) for v in vals]; ss = sum(ex)
            out[key] = [e / ss for e in ex]
        return out

    def _train_adv(self):
        pass

    def _train_strat(self):
        pass

    def train_iteration(self):
        for traverser in range(self.game.num_players):
            self._traverse(self.game.root(), [1.0] * self.game.num_players + [1.0], traverser)
        self.iterations += 1
        self._train_combined()

    def _train_combined(self):
        if len(self.reg_buf) < self.batch_size:
            return
        rb = self.reg_buf.sample(self.batch_size)
        xs = torch.tensor(__import__("numpy").stack([b[0] for b in rb]))
        ys = torch.tensor(__import__("numpy").stack([b[1] for b in rb]), dtype=torch.float32)
        masks = torch.zeros_like(ys)
        for i, b in enumerate(rb):
            for a in b[2]:
                masks[i, self._action_map[a]] = 1.0
        rpred, _ = self.single(xs)
        loss_r = ((rpred - ys) ** 2 * masks).sum() / masks.sum().clamp(min=1)

        if len(self.strat_buf) >= self.batch_size:
            sb = self.strat_buf.sample(self.batch_size)
            xs2 = torch.tensor(__import__("numpy").stack([b[0] for b in sb]))
            ys2 = torch.tensor(__import__("numpy").stack([b[1] for b in sb]), dtype=torch.float32)
            masks2 = torch.zeros_like(ys2)
            for i, b in enumerate(sb):
                for a in b[2]:
                    masks2[i, self._action_map[a]] = 1.0
            _, spred = self.single(xs2)
            tgt = ys2 * masks2
            denom = tgt.sum(dim=1, keepdim=True).clamp(min=1e-8)
            tgt = tgt / denom
            logits = spred.masked_fill(masks2 == 0, -1e9)
            logp = torch.nn.functional.log_softmax(logits, dim=1)
            loss_s = -(tgt * logp * masks2).sum() / masks2.sum().clamp(min=1)
        else:
            loss_s = 0.0
        loss = loss_r + (loss_s if isinstance(loss_s, torch.Tensor) else 0.0)
        self.opt.zero_grad(); loss.backward(); self.opt.step()


def main():
    t = SingleDeepCFRTrainer(seed=0)
    t.train(10)
    print("done", t.iterations)


if __name__ == "__main__":
    main()
# Module 08 — Implementation Plan (Deep CFR)

Status: Module 07 complete (engine, resolver, match harness, flop library, labs). This plan covers Deep CFR (neural regrets) and its supporting deliverables.

## Deliverables and order

1. **Neural regret / strategy networks** (PyTorch): advantage net A(s,a), strategy net π(s,a), with input featurization for info sets.
2. **Reservoir sampling buffer** for regret and strategy samples.
3. **Deep CFR trainer** on Leduc → Limit endgame: sample traversals, train nets, compare to tabular MCCFR.
4. **Single Deep CFR** variant (one network) for comparison.
5. **Browser labs** I08.x and notebook extensions.
6. **Module doc + roadmap** filled.

Order: (1)→(2)→(3); (4) parallel with (3); (5) last.

## 1. Neural networks
- Files: `pokerbot/nn/advantage.py`, `pokerbot/nn/strategy.py`, `pokerbot/nn/features.py`.
- Featurize info set: one-hot (private card, public board, history). Leduc small; Limit uses bucketed hand class.
- MLP with ReLU, output per action. Regret net predicts counterfactual regrets; strategy net predicts average strategy.
- Tests: forward shapes, gradient flow, deterministic with seed.

## 2. Reservoir sampling
- `pokerbot/nn/reservoir.py`: fixed-capacity buffer with uniform replacement; supports weighted sampling.
- Tests: distribution uniformity, capacity, reproducibility.

## 3. Deep CFR trainer
- `pokerbot/solvers/deep_cfr.py`: DeepCFRTrainer with external sampling, traverse, store samples, train nets periodically.
- Reuse MCCFR sampling from Module 04. Leaf/terminal handling.
- Compare exploitability vs tabular MCCFR on Leduc (within tolerance after N iterations).
- CLI `python -m pokerbot.solvers.deep_cfr`.
- Tests: convergence on Kuhn/Leduc; exploitability decreases.

## 4. Single Deep CFR
- `pokerbot/solvers/single_deep_cfr.py`: one network approximating both regret and strategy via a combined loss.
- Compare memory/compute and exploitability to two-net version.

## 5. Labs & docs
- Browser labs: training curve visualizer (loss + exploitability), network input explorer, sample browser, comparison dashboard.
- Update `docs/modules/08_deep_cfr.md` with full content; roadmap status.

## Milestones
- Week 1: nets + reservoir + tests.
- Week 2: Deep CFR on Leduc; convergence verification.
- Week 3: Limit endgame; Single Deep CFR; labs.
- Week 4: docs, verification pass.

## Done when
- pytest green; Module 08 status "draft"; roadmap filled; `python -m pokerbot.solvers.deep_cfr` runs end to end.
- Exploitability within tolerance of tabular on Leduc.
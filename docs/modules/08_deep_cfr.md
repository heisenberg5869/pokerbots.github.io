# 08 · Deep CFR

| Level | Prerequisites | Status |
|---|---|---|
| Advanced | 02, 04 | draft |

## Motivation
Tabular MCCFR stores one regret per info set. Real hold'em has billions of info sets, so we replace the regret table with a neural network trained on sampled regrets. Deep CFR (Brown et al. 2019) does this with external sampling + reservoir buffers, then reads out an average strategy.

## What you will learn
- Neural advantage (regret) networks A(s,a) and strategy networks σ(s,a).
- Reservoir sampling for fixed-memory regret/strategy buffers.
- External-sampling traversals and periodic network training.
- Single Deep CFR: one network, combined loss.
- How approximation error propagates into exploitability.

## What you will build
Deep CFR on Leduc, then a Limit endgame; comparison against tabular MCCFR. CLI: `python -m pokerbot.solvers.deep_cfr`.

## Intuition first
Imagine MCCFR where, instead of a giant table, you keep a *notebook* of sampled (info-set, action, regret) triples. A neural net reads the notebook and predicts regret for any info set it hasn't seen. Sampling new data refreshes the notebook; the net generalizes. That's Deep CFR.

## Formal definition
Let R^T(s,a) be cumulative counterfactual regret. Deep CFR maintains a regret network R̂(s,a;θ) trained by MSE on reservoir-sampled regret targets, and a strategy network σ̂(s,a;φ) trained on sampled average strategies. Iteration: sample traversals → push samples to buffers → train networks → read σ̂.

## Algorithm
Implementation: `pokerbot/nn/` (AdvantageNet, StrategyNet, features, reservoir) and `pokerbot/solvers/deep_cfr.py` (DeepCFRTrainer), plus `single_deep_cfr.py`. Run `python -m pokerbot.solvers.deep_cfr`.

Pseudocode:
```
for iter in 1..N:
  for traversal in sample(K):
    traverse game tree (external sampling)
    for each visited info set s, action a:
      regret = counterfactual regret of a
      buffer_R.push((features(s), a, regret))
      buffer_σ.push((features(s), a, current_strategy(a)))
  if iter % train_every == 0:
    train R̂ on buffer_R (MSE)
    train σ̂ on buffer_σ (MSE / cross-entropy)
return σ̂
```

## Interactive lab
Browser labs: `docs/demos/deep-cfr-training-lab.html`, `deep-cfr-reservoir-lab.html`, `deep-cfr-strategy-compare.html`. They simulate (illustratively) training curves, reservoir sampling, and strategy comparison. Values are illustrative.

## Verification
Compare exploitability vs tabular MCCFR on Leduc. Expect within tolerance after N iterations (illustrative thresholds; exact numbers depend on seeds).

## Exercises
- **Recall:** Why reservoir sampling rather than a FIFO buffer?
- **Implement:** Add weighted sampling to the reservoir; measure convergence speed.
- **Extend:** Implement Single Deep CFR and compare memory/compute.

## Where this breaks
Network values are only as good as the information they take in. We need public belief states and value functions for search (Module 09).

## Misconception box
> "A bigger net always converges faster." False — without enough sampled data and proper feature encoding, larger nets overfit sampled regrets and exploitability plateaus or worsens.

## Checkpoint — you are done when…
- You can explain regret net vs strategy net roles.
- You can implement reservoir sampling with uniform replacement.
- You can run Deep CFR end to end and read its exploitability curve.
- You can diagnose approximation error via the lab's "Break it" experiments.

## Further reading
- Brown et al., "Deep Counterfactual Regret Minimization" (2019).
- Steinberger, "Single Deep CFR" (2019).
- Lanctot et al., "Monte Carlo Sampling for Regret Minimization" (2009).

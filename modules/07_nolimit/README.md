# 07 · Heads-Up No-Limit Texas Hold'em

Read the explanation: [`docs/modules/07_nolimit.md`](../../docs/modules/07_nolimit.md)

Hands-on material (notebooks, exercises) goes in this folder. `exercises/` is
still empty; the solver itself lives in the library.

## Push/fold solver

```bash
# Solve a 10 big-blind game (stack is measured in antes) and print both ranges.
python -m pokerbot.solvers.push_fold 10 100000
```

```python
from pokerbot.solvers.push_fold import class_index, solve_push_fold

result = solve_push_fold(stack=20, iterations=200_000, seed=0)  # 20 antes = 10 bb
print(len(result.shove_range), sorted(result.shove_range_names()))
print(result.shove_threshold[class_index("AA")])
```

The default equity model is a teaching heuristic, so the ranges are wider than
published push/fold charts. Pass a real preflop equity table through
`load_equity_table` to make the output comparable.

## No-limit betting mechanics

```python
from pokerbot.games import NoLimitBettingRound

round_ = NoLimitBettingRound([100, 100], pot=10, bet_menu=(0.33, 0.75, 1.5))
print(round_.legal_actions())
round_.act(round_.legal_actions()[0])
```

This is a single betting round with a configurable pot-fraction menu, not a
complete dealt hand.

# 02 · Regret Matching & No-Regret Learning

Explanation: [`docs/modules/02_regret_matching.md`](../../docs/modules/02_regret_matching.md)

- `notebook.ipynb`: reproduce the worked example, plot current vs average strategy, regret vs the sqrt(T) bound, the 1/sqrt(T) rate, RM vs RM+ vs Hedge
- `exercises/`: put your solutions here
- Library code: `pokerbot/solvers/matrix_games.py` (learners, self-play, matrix exploitability), `pokerbot/solvers/regret_matching.py` (the per-information-set matcher CFR uses)
- Browser demo: `docs/demos/regret_matching_rps.html`
- Tests: `tests/test_regret_matching.py`

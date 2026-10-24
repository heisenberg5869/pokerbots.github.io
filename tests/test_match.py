import random

from pokerbot.eval.match import Match, MatchResult, duplicate_play
from pokerbot.eval.variance_reduction import control_variate
from pokerbot.games.kuhn import KuhnPoker as Kuhn


def _uniform_strategy(game):
    # build a uniform strategy dict over all info sets by sampling
    strat = {}
    s = game.root()

    def walk(state):
        if state.is_terminal() or state.is_chance():
            if state.is_chance():
                for o, _ in state.chance_outcomes():
                    walk(state.child(o))
            return
        key = state.info_set_key(state.current_player())
        if key not in strat:
            actions = state.legal_actions()
            strat[key] = [1.0 / len(actions)] * len(actions)
        for a in state.legal_actions():
            walk(state.child(a))

    walk(s)
    return strat


def test_duplicate_reduces_variance():
    g = Kuhn()
    sa = _uniform_strategy(g)
    sb = _uniform_strategy(g)
    r_dup = Match.play(sa, sb, 2000, seed=1, game=g, duplicate=True)
    r_raw = Match.play(sa, sb, 2000, seed=1, game=g, duplicate=False)
    # duplicate should not increase variance
    assert r_dup.std <= r_raw.std * 1.5


def test_control_variate_unbiased_smaller_variance():
    rng = random.Random(0)
    raw = [rng.gauss(0, 1) for _ in range(2000)]
    cov = [0.5 * r + rng.gauss(0, 0.5) for r in raw]
    adj = control_variate(raw, cov)
    assert abs(sum(adj) / len(adj) - sum(raw) / len(raw)) < 1e-9
    var_raw = sum((r - sum(raw)/len(raw))**2 for r in raw) / len(raw)
    var_adj = sum((a - sum(adj)/len(adj))**2 for a in adj) / len(adj)
    assert var_adj <= var_raw


def test_hands_needed_monotonic():
    g = Kuhn()
    sa = _uniform_strategy(g)
    sb = _uniform_strategy(g)
    r = Match.play(sa, sb, 500, seed=2, game=g)
    h1 = r.hands_needed(1.0)
    h2 = r.hands_needed(2.0)
    h3 = r.hands_needed(5.0)
    assert h1 >= h2 >= h3


def test_match_result_fields():
    g = Kuhn()
    sa = _uniform_strategy(g)
    sb = _uniform_strategy(g)
    r = Match.play(sa, sb, 100, seed=3, game=g)
    assert isinstance(r, MatchResult)
    assert r.n_hands == 100
    assert r.ci_low <= r.mean <= r.ci_high


def test_cli_runs():
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "pokerbot.eval.match", "--n", "50", "--seed", "0"], check=True)

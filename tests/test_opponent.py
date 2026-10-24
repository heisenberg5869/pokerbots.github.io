from pokerbot.eval.opponent import FrequencyOpponentModel, SafeExploiter


def test_frequency_model_counts():
    m = FrequencyOpponentModel()
    m.observe("s", "fold")
    m.observe("s", "call")
    m.observe("s", "fold")
    assert m.counts("s")["fold"] == 2
    assert m.total("s") == 3
    f = m.frequencies("s")
    assert abs(f["fold"] - 2 / 3) < 1e-9 or abs(f["fold"] - (2 + 1) / (3 + 2)) < 1e-9


def test_frequency_predict_sums_to_one():
    m = FrequencyOpponentModel(actions=["a", "b"])
    for a in ["a", "a", "b"]:
        m.observe("ctx", a)
    probs = m.predict("ctx", ["a", "b"])
    assert abs(sum(probs) - 1.0) < 1e-9


def test_safe_exploiter_mixes():
    nash = {"ctx": [0.5, 0.5]}
    se = SafeExploiter(nash_strategy=nash, epsilon=0.2)
    br = [1.0, 0.0]
    mixed = se.mix(br, nash["ctx"])
    assert abs(mixed[0] - (0.8 * 1.0 + 0.2 * 0.5)) < 1e-9
    assert abs(mixed[1] - (0.8 * 0.0 + 0.2 * 0.5)) < 1e-9


def test_safe_exploiter_strategy():
    m = FrequencyOpponentModel(actions=["rock", "paper"])
    m.observe("ctx", "rock")
    m.observe("ctx", "rock")
    nash = {"ctx": [0.5, 0.5]}
    se = SafeExploiter(nash_strategy=nash, epsilon=0.1, opponent_model=m)

    def payoff(ours, opp):
        # paper beats rock
        if ours == "paper" and opp == "rock":
            return 1.0
        if ours == "rock" and opp == "paper":
            return -1.0
        return 0.0

    strat = se.safe_strategy("ctx", ["rock", "paper"], payoff, opponent_actions=["rock", "paper"])
    assert len(strat) == 2
    assert abs(sum(strat) - 1.0) < 1e-9
    # paper should get more mass than rock
    assert strat[1] > strat[0]

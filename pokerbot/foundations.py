"""Small, dependency-free probability and matrix-game tools for Module 00."""
from __future__ import annotations

from itertools import combinations
from math import comb


def expected_value(outcomes: list[tuple[float, float]]) -> float:
    """Return sum(probability * payoff), validating a finite lottery."""
    if not outcomes or any(p < 0 for p, _ in outcomes):
        raise ValueError("outcomes must be non-empty with non-negative probabilities")
    total = sum(p for p, _ in outcomes)
    if abs(total - 1.0) > 1e-9:
        raise ValueError("outcome probabilities must sum to 1")
    return sum(p * x for p, x in outcomes)


def variance(outcomes: list[tuple[float, float]]) -> float:
    """Return the variance of a finite lottery represented as (probability, payoff)."""
    mean = expected_value(outcomes)
    return sum(p * (x - mean) ** 2 for p, x in outcomes)


def combinations_remaining(cards_in_deck: int, known_cards: int, hand_size: int = 2) -> int:
    """Count unordered hands after removing known cards from a deck."""
    remaining = cards_in_deck - known_cards
    if min(cards_in_deck, known_cards, hand_size) < 0 or remaining < hand_size:
        raise ValueError("not enough cards remain for the requested hand")
    return comb(remaining, hand_size)


def rank_combos(rank_count: int, known_of_rank: int = 0, hand_size: int = 2) -> int:
    """Count hands made only from one rank after known cards are removed."""
    if not 0 <= known_of_rank <= rank_count:
        raise ValueError("known_of_rank must be between zero and rank_count")
    available = rank_count - known_of_rank
    return comb(available, hand_size) if available >= hand_size else 0


def call_equity_required(pot_before_bet: float, opponent_bet: float, call_cost: float | None = None) -> float:
    """Equity needed to call; pot_before_bet excludes the opponent's current bet."""
    call_cost = opponent_bet if call_cost is None else call_cost
    if pot_before_bet < 0 or opponent_bet < 0 or call_cost <= 0:
        raise ValueError("pot and bet must be non-negative and call cost positive")
    return call_cost / (pot_before_bet + opponent_bet + call_cost)


def bluff_break_even_fold_rate(pot: float, bluff_size: float) -> float:
    """Fold frequency required for a zero-equity bluff risking bluff_size to win pot."""
    if pot < 0 or bluff_size < 0 or pot + bluff_size == 0:
        raise ValueError("pot and bluff size must be non-negative, with a positive total")
    return bluff_size / (pot + bluff_size)


def minimum_defense_frequency(pot: float, bet: float) -> float:
    """Minimum fraction of range to continue so a zero-equity bluff cannot profit."""
    if pot < 0 or bet < 0 or pot + bet == 0:
        raise ValueError("pot and bet must be non-negative, with a positive total")
    return pot / (pot + bet)


def bayes_posterior(priors: list[float], likelihoods: list[float]) -> list[float]:
    """Posterior over hidden types given the likelihood of one observed action."""
    if len(priors) != len(likelihoods) or not priors:
        raise ValueError("priors and likelihoods must have equal non-zero length")
    if any(x < 0 for x in priors + likelihoods) or abs(sum(priors) - 1) > 1e-9:
        raise ValueError("priors must sum to 1; likelihoods and priors must be non-negative")
    weighted = [p * likelihood for p, likelihood in zip(priors, likelihoods)]
    evidence = sum(weighted)
    if evidence == 0:
        raise ValueError("the observed action has zero probability under this model")
    return [x / evidence for x in weighted]


def _solve_linear(matrix: list[list[float]], rhs: list[float]) -> list[float] | None:
    """Gaussian elimination with pivoting; returns None for singular systems."""
    n = len(rhs)
    a = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(a[row][col]))
        if abs(a[pivot][col]) < 1e-10:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [x / scale for x in a[col]]
        for row in range(n):
            if row != col:
                factor = a[row][col]
                a[row] = [x - factor * y for x, y in zip(a[row], a[col])]
    return [a[i][-1] for i in range(n)]


def solve_zero_sum(matrix: list[list[float]]) -> tuple[list[float], list[float], float]:
    """Find a Nash equilibrium of a small zero-sum payoff matrix by indifference.

    Returns (row_strategy, column_strategy, value_to_row). Supports up to 5 actions
    per player; this enumerates equal-sized support pairs and is intended for
    teaching examples, not large games. Degenerate games may have many equilibria.
    """
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("payoff matrix must be non-empty and rectangular")
    rows, cols = len(matrix), len(matrix[0])
    if max(rows, cols) > 5:
        raise ValueError("support enumeration is limited to five actions per player")
    a = [[float(x) for x in row] for row in matrix]

    for size in range(1, min(rows, cols) + 1):
        for row_support in combinations(range(rows), size):
            for col_support in combinations(range(cols), size):
                # Find a row mix making each supported column yield the same value.
                eq = [[a[i][j] for i in row_support] + [-1.0] for j in col_support]
                eq.append([1.0] * size + [0.0])
                sol_x = _solve_linear(eq, [0.0] * size + [1.0])
                # Find a column mix making each supported row yield the same value.
                eq = [[a[i][j] for j in col_support] + [-1.0] for i in row_support]
                eq.append([1.0] * size + [0.0])
                sol_y = _solve_linear(eq, [0.0] * size + [1.0])
                if sol_x is None or sol_y is None:
                    continue
                x, vx = sol_x[:-1], sol_x[-1]
                y, vy = sol_y[:-1], sol_y[-1]
                if min(x + y) < -1e-8 or abs(vx - vy) > 1e-7:
                    continue
                full_x, full_y = [0.0] * rows, [0.0] * cols
                for i, prob in zip(row_support, x):
                    full_x[i] = max(0.0, prob)
                for j, prob in zip(col_support, y):
                    full_y[j] = max(0.0, prob)
                sx, sy = sum(full_x), sum(full_y)
                if sx <= 0 or sy <= 0:
                    continue
                full_x = [p / sx for p in full_x]
                full_y = [p / sy for p in full_y]
                row_values = [sum(a[i][j] * full_y[j] for j in range(cols)) for i in range(rows)]
                col_values = [sum(full_x[i] * a[i][j] for i in range(rows)) for j in range(cols)]
                value = sum(full_x[i] * row_values[i] for i in range(rows))
                if max(row_values) <= value + 1e-7 and min(col_values) >= value - 1e-7:
                    return full_x, full_y, value
    raise ValueError("could not find an equilibrium support; check matrix or use an LP solver")


def _lp_player(matrix: list[list[float]], maximize: bool) -> tuple[list[float], float]:
    """Solve one player's small minimax LP by enumerating its feasible vertices."""
    actions = len(matrix) if maximize else len(matrix[0])
    other_actions = len(matrix[0]) if maximize else len(matrix)
    # Variables are action probabilities followed by the guaranteed value.
    inequalities: list[tuple[list[float], float]] = []
    for other in range(other_actions):
        if maximize:
            # x·A[:, other] >= value  <=>  -x·A[:, other] + value <= 0.
            row = [-matrix[i][other] for i in range(actions)] + [1.0]
        else:
            # A[other, :]·y <= value.
            row = [matrix[other][j] for j in range(actions)] + [-1.0]
        inequalities.append((row, 0.0))
    for i in range(actions):
        row = [0.0] * (actions + 1)
        row[i] = -1.0
        inequalities.append((row, 0.0))

    equality = [1.0] * actions + [0.0]
    best: tuple[list[float], float] | None = None
    for active in combinations(inequalities, actions):
        equations = [equality] + [item[0] for item in active]
        rhs = [1.0] + [item[1] for item in active]
        solution = _solve_linear(equations, rhs)
        if solution is None:
            continue
        probs, value = solution[:-1], solution[-1]
        if min(probs) < -1e-8:
            continue
        if any(sum(a * x for a, x in zip(row, solution)) > bound + 1e-7 for row, bound in inequalities):
            continue
        normalized = [max(0.0, x) for x in probs]
        total = sum(normalized)
        if total <= 0:
            continue
        normalized = [x / total for x in normalized]
        if best is None or (value > best[1] if maximize else value < best[1]):
            best = normalized, value
    if best is None:
        raise ValueError("could not find a feasible minimax LP vertex")
    return best


def solve_zero_sum_lp(matrix: list[list[float]]) -> tuple[list[float], list[float], float]:
    """Solve a small zero-sum matrix game via primal and dual minimax linear programs.

    The row player's LP maximizes a guaranteed payoff; the column player's dual
    minimizes the payoff they allow. This dependency-free vertex enumerator is
    intended for teaching matrices (up to five actions per player), not large games.
    """
    if not matrix or not matrix[0] or any(len(row) != len(matrix[0]) for row in matrix):
        raise ValueError("payoff matrix must be non-empty and rectangular")
    if max(len(matrix), len(matrix[0])) > 5:
        raise ValueError("LP vertex enumeration is limited to five actions per player")
    a = [[float(x) for x in row] for row in matrix]
    row_strategy, lower_value = _lp_player(a, maximize=True)
    col_strategy, upper_value = _lp_player(a, maximize=False)
    if abs(lower_value - upper_value) > 1e-6:
        raise ArithmeticError("primal and dual LP values disagree")
    return row_strategy, col_strategy, (lower_value + upper_value) / 2

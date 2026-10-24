# Module 07 — Implementation Plan (remaining deliverables)

Status of what already exists: see `docs/roadmap.md` and `docs/modules/07_nolimit.md`. This document plans the four still-unbuilt deliverables from the master plan (`docs/plan.md`, Module 07 section) plus the supporting browser labs and notebooks.

## Deliverables and order

1. **Full no-limit game engine** (four streets, bet menus, action translation hooks) — foundation for everything else.
2. **Depth-limited re-solver** on a reduced game — the headline algorithm.
3. **Match harness with variance reduction** (control variates, duplicate play) — evaluation without exact exploitability.
4. **Precomputed flop library** — the data behind the flop strategy explorer.
5. **Browser labs** I07.2–I07.9 and the executed notebook extensions.

Order matters: (1) before (2); (3) can run in parallel with (2); (4) needs (1) + (2); (5) last.

---

## 1. Full no-limit game engine

**Goal:** `pokerbot.games.NoLimitHoldem` (or `NoLimitGame`) representing a complete dealt heads-up hand: preflop deal, four betting rounds, showdown, side-pot handling for all-in, with a configurable per-street bet menu.

**Files**
- `pokerbot/games/nolimit_holdem.py` (new) — game state machine.
- `pokerbot/games/nolimit.py` (existing) — keep as the single-round engine; reuse `NoLimitBettingRound`, `NLAction`, sizing helpers.
- `pokerbot/games/__init__.py` — export the new class.
- `tests/test_nolimit_holdem.py` (new).

**Design**
- State is a dataclass holding: stacks, hole cards (class indices or specific combos), board (list of 0–5 cards), street (0–3), current betting round (`NoLimitBettingRound`), terminal flag, history.
- Card abstraction: represent holdings as specific two-card combos internally; expose class indices for strategy keys. Chance nodes deal hole cards and board cards from a deck with removal.
- Betting rounds: instantiate `NoLimitBettingRound` per street with `bet_menu` per street (allowable: a tuple per street or a single menu reused). When a round closes, move to next street or showdown.
- Showdown: use `pokerbot.eval.hand_eval` (best five of seven) to score; handle split pots and side pots when a player is all-in for less.
- Action translation hooks: store the abstract action chosen; allow a `translate_bet` callback for off-menu sizes (reuse Module 06 `translation_probabilities`).
- Game interface must match `base.Game`: `root`, `is_terminal`, `is_chance`, `chance_outcomes`, `current_player`, `legal_actions`, `info_set_key`, `child`, `returns`. This is what makes it solvable by CFR/MCCFR and evaluable by `exploitability`.

**Information sets**
- Key by `(player, own hole cards, public board, action history)` for exact solving; for abstracted solving, by bucket index instead. Provide a `bucket_fn` parameter defaulting to identity (exact) so the same engine supports both.

**Tests**
- Deal/chance node structure: 52 choose 2 × 50 choose 2 deals.
- Legal actions at each street; all-in creates side pots; refund of uncalled bets.
- Showdown scoring against known hands.
- Chip conservation invariant across a random playthrough.
- A tiny configuration (one bet size, one street) solves to a known value with CFR.

**Effort:** ~1 person-week.

---

## 2. Depth-limited re-solver

**Goal:** Given a blueprint strategy and a current public state + estimated ranges, re-solve a depth-limited subgame whose leaf values come from a value function (or the blueprint's counterfactual values), with a safe gadget so the opponent cannot exploit the re-solve.

**Files**
- `pokerbot/solvers/resolve.py` (new).
- `pokerbot/eval/local_best_response.py` (new, shared with §3).
- `tests/test_resolve.py` (new).

**Algorithm (Brown & Sandholm, "Safe and Nested Subgame Solving")**
1. Inputs: game `G`, blueprint strategy `β`, current node `v` in the abstract tree, player ranges `r_0, r_1` (reach probabilities), opponent counterfactual values from the blueprint `u`.
2. Build the subgame `S` from `v` downward to depth `d` (or to terminal).
3. At each leaf of `S`, compute the value of continuing under the blueprint: `β`'s counterfactual value for each player at that leaf. Optionally replace with a learned value net (Module 09).
4. Add a gadget action for the opponent: an "opt out" action that ends the subgame and awards the blueprint's promised counterfactual value. This constrains the re-solve so the opponent cannot force below the blueprint value.
5. Solve `S` with CFR (or MCCFR) starting from the ranges; the root strategy becomes the refined action.
6. Nested solving: when an off-tree bet occurs, translate it (Module 06) or re-build `S` at the new public state.

**Implementation steps**
- `Subgame` builder: walk `NoLimitHoldem` from a state to depth `d`, collecting leaves.
- `LeafValue`: callable `(state, player) -> float`; default uses blueprint EV.
- `Gadget`: modify the subgame's terminal payoffs at leaves to include the opt-out action for the opponent.
- `resolve(state, blueprint, ranges, depth, iterations)` → refined strategy at the root.
- Reuse `RegretMatcher` and the CFR loop from `pokerbot.solvers.cfr`.

**Tests**
- On a Leduc-sized game, re-solving matches the blueprint value within tolerance.
- Unsafe re-solve (no gadget, guessed range) is exploitable by a constructed opponent; safe version is not.
- Nested solving: two consecutive off-tree bets refine consistently.

**Effort:** ~2 person-weeks. This is the hardest piece; start with a Leduc-sized prototype before scaling to no-limit.

---

## 3. Match harness with variance reduction

**Goal:** Run head-to-head matches between two strategies (or a human and a bot) and report a win rate in milli-big-blinds per hand with a confidence interval, using duplicate play and control variates so the required hand count is orders of magnitude smaller.

**Files**
- `pokerbot/eval/match.py` (new): `Match`, `MatchResult`, `duplicate_play`.
- `pokerbot/eval/variance_reduction.py` (new): control-variate estimator.
- `tests/test_match.py` (new).

**Design**
- `Match.play(strategy_a, strategy_b, n_hands, seed)` deals hands, runs the game engine, records payoffs.
- Duplicate play: each hand is dealt twice with swapped positions; the average of the two outcomes removes first-act advantage variance.
- Control variate: use a cheap estimator (e.g., hand-strength equity or a shallow value) as a covariate; regress its noise out of the win-rate estimate. Report both raw and reduced confidence intervals.
- Output: win rate in bb/100, 95% CI, number of hands needed to see a given edge (power calculation).
- `MatchResult` dataclass with `mean`, `std`, `ci_low`, `ci_high`, `n_hands`, `hands_needed(edge)`.

**Tests**
- Duplicate play reduces variance on a known game.
- Control-variate estimate is unbiased (mean matches raw) and has smaller variance.
- `hands_needed` monotonic in edge.

**Effort:** ~1 person-week. Can proceed in parallel with §2.

---

## 4. Precomputed flop library

**Goal:** A curated set of boards with solved strategies, powering the flop strategy explorer (I07.3) and providing a concrete "read a solver output" exercise.

**Files**
- `tools/build_flop_library.py` (new).
- `docs/demos/flop-module-07-data.json` (generated).
- `docs/demos/flop-module-07.html` (new).
- `tests/test_flop_demo_data.py` (new).

**Design**
- Choose ~30 boards spanning textures: dry (K72r), wet (987 two-tone), paired, monotone, high/low.
- For each, solve the flop subgame (or a simplified single-street model) with a small bet menu and store: action frequencies per hand class, aggregate frequencies, equity and EV by hand class, board texture tags.
- Because a full flop solve is large, start with a single-street flop model (flop betting round only, with a hand-strength/ equity proxy for leaf values) and label it as a teaching approximation. Upgrade to a real solve later.
- JSON schema mirrors `pushfold-module-07-data.json`: manifest + boards.

**Tests**
- Manifest has the expected board count and texture tags.
- Every hand class has probabilities summing to 1 for each board and position.
- Frequencies are within [0, 1].

**Effort:** ~1.5 person-weeks, blocked on §1 for a true multi-street solve.

---

## 5. Browser labs I07.2–I07.9

Each follows the established pattern (self-contained HTML in `docs/demos/`, data JSON, nav entry, test).

- **I07.2 Bet-Size Tree Builder** (analytic): node-count meter as sizes are added. No solver needed.
- **I07.3 Flop Strategy Explorer** (precomputed): needs §4.
- **I07.4 SPR and Commitment Visualizer** (analytic): pot graphic + stack bar.
- **I07.5 Polarization Lab** (analytic): break-even calling frequency, bluff-to-value ratio.
- **I07.6 Continual Re-solving Walkthrough** (needs §2).
- **I07.7 Local Best Response Explainer** (needs §3's local best response).
- **I07.8 Match Evaluator with Variance Reduction** (needs §3).
- **I07.9 Play No-Limit with Review** (needs §1 + §2).

**Effort:** ~2 person-weeks total, spread across the other work.

---

## Milestone schedule (rough)

- Week 1: §1 full game engine + tests.
- Week 2: §2 re-solver prototype on Leduc; §3 match harness.
- Week 3: §2 scaled to no-limit; §4 flop library generator.
- Week 4: §5 labs I07.2, I07.4, I07.5, I07.8; notebook extensions.
- Week 5: I07.3, I07.6, I07.7, I07.9; docs/verification pass.

## What "done" looks like

- `pytest` green with new test files for each deliverable.
- Module 07 status moved from "in progress" to "draft" then "reviewed".
- Roadmap web-demo column filled for I07.1–I07.9.
- `docs/modules/07_nolimit.md` has no TODOs and links to every lab and notebook.
- A learner can run `python -m pokerbot.solvers.resolve ...` and `python -m pokerbot.eval.match ...` end to end.

## Open risks

- §2 safe re-solving is the hardest piece and may slip; if it does, ship §1 + §3 + §4 + analytic labs first and leave §2 + I07.6/I07.7 for a follow-up.
- §4's flop solves may be too slow; fall back to single-street flop model and label it as a teaching approximation, matching how the push/fold lab is labelled.
- The no-limit engine (§1) must implement the `base.Game` interface exactly or CFR/exploitability will not compose with it; validate with a Kuhn-sized configuration first.

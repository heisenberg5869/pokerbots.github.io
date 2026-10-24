# Pokerbots Curriculum: Master Plan

*A complete plan for every module: concepts, interactive features, labs, verification and delivery. This document contains no code; it is the blueprint that the code, notebooks and web demos are built from. Suggested location in the repo: `docs/plan.md`.*

**Legend used throughout**

- **[P0]** must-have for the module to be considered done
- **[P1]** should have; makes the module excellent
- **[P2]** nice to have; build when time allows
- **Predict → Play → Prove → Probe**: the four-beat teaching loop described in section 2
- **W-numbers** (W1, W2, …) refer to shared widgets defined once in section 4 and reused across modules
- Numbers marked **(verify)** are recalled from the literature and must be checked against a source before they are published. Appendix C lists them all.

---

## Contents

1. Vision, audience and outcomes
2. Pedagogical framework
3. Interactive design system
4. Shared widget catalog
5. Module-by-module plan (00 to 14)
6. Cross-module threads
7. Library and data architecture
8. Verification and quality plan
9. Delivery plan
10. Risks and mitigations
11. Decisions still needed
- Appendix A: Concept dependency map
- Appendix B: Reading list by module
- Appendix C: Facts to verify before publishing

---

## 1. Vision, audience and outcomes

### 1.1 What this repo is

A single place where someone can start with "what is expected value?" and finish able to design a solver for a poker variant nobody has solved before. It teaches *concepts first*, backs every concept with running code, and lets the learner touch each idea in the browser before reading the math.

The curriculum deliberately walks up a ladder of games. Each rung exists because the previous method breaks on it:

| Rung | Game | Method introduced | Why it breaks next |
|---|---|---|---|
| 1 | Kuhn Poker | game trees, CFR as a tool | one betting round, no public cards |
| 2 | Rock-paper-scissors (matrix) | regret theory | need sequential, hidden-info games |
| 3 | Leduc Hold'em | chance nodes, CFR+ | full-tree traversal is too slow for bigger decks |
| 4 | Expanded Leduc, river poker | Monte Carlo CFR | real poker needs hand evaluation and multiple streets |
| 5 | Limit Hold'em | evaluators, bucketed abstraction | abstraction loses information |
| 6 | Abstraction and endgames | clustering, safe subgame solving | bet sizes are unlimited in No-Limit |
| 7 | Heads-up No-Limit | re-solving, bet menus | tables cannot store this game |
| 8 | Deep CFR | neural regrets | networks need beliefs to plan |
| 9 | Search with value networks | public belief states | hands explode in combinatorics |
| 10 | Pot-Limit Omaha | combinatorics, equity estimation | guarantees assume two players |
| 11 | Multiplayer | self-play, population evaluation | equilibrium play is not maximally profitable |
| 12 | Opponent modelling | safe exploitation | rules can change |
| 13 | Custom variants | game modelling, auctions | what is actually solved? |
| 14 | Case studies, open problems | synthesis | (open research) |

### 1.2 Learner personas and paths

| Persona | Starting point | Path through the repo | Finish line |
|---|---|---|---|
| **Newcomer** | knows poker rules, some programming, little math | 00 → 01 → 02 slowly, reading every intuition section | explains CFR to a friend; solves Kuhn and Leduc |
| **Competitor** (e.g., building a bot for a poker-bot competition) | programmer, some probability | 01 → 03 → 04 → 05 → 07 → 12 → 13 | a working bot for a custom variant |
| **Researcher** | ML background, no game theory | skim 00 and 01, read 02 carefully, then 03 → 08 → 09 → 11 → 14 | can reproduce a paper at toy scale and identify open problems |

Every module header states which persona it is essential for, so a reader can skip responsibly.

### 1.3 Outcomes for the whole repo

By the end, a learner can:

1. define and compute exploitability, and explain why it is the right scoreboard;
2. explain why regret minimization yields equilibrium, and derive CFR from it;
3. build solvers at three scales: exact, sampled, and neural;
4. explain abstraction and the safety guarantee of subgame solving;
5. say honestly what "solved" means for each game, and what is still open;
6. model a brand-new poker variant and build a bot that reasons about its mechanics.

---

## 2. Pedagogical framework

### 2.1 The anatomy of every module

Every module page follows the same nine sections so that learners always know where they are:

1. **Motivation**: the previous module's failure, stated concretely with a number or a demo
2. **Intuition first**: a tiny example or picture before any formula
3. **Formal definition**: using the shared notation page, no new symbols for old ideas
4. **Algorithm**: pseudocode, then a minimal implementation
5. **Interactive lab**: browser demos and a notebook
6. **Verification**: a known answer the learner can reproduce
7. **Exercises**: recall, implement, extend
8. **Where this breaks**: the failure that motivates the next module
9. **Checkpoint and further reading**

### 2.2 The Predict → Play → Prove → Probe loop

Every interactive follows the same four beats, which is where most of the learning happens:

- **Predict:** before showing a result, the page asks a one-line question ("Which action will the solver take with a Queen here?") and records the guess. Guessing before seeing the answer is the single most effective teaching device in the whole plan.
- **Play:** the learner manipulates the system with sliders, drags and clicks and watches it respond immediately.
- **Prove:** a "Show the math" toggle reveals the exact formula and the numbers behind what was just seen.
- **Probe:** a "Break it" prompt invites the learner to push the system to a failure (nudge a probability, shrink the bucket count, change the bet size) and see how the scoreboard reacts.

### 2.3 Misconception boxes

Each module includes a short "Common mistakes" box, written in advance from known confusions. Examples that recur: confusing the current strategy with the average strategy; thinking an information set is a single game state; thinking exploitability measures how much you *lose* rather than how much a perfect opponent *could win*; believing a bluff must be "justified" by a specific hand; thinking regret compares against the best *sequence* of actions.

### 2.4 Assessment

- **Checkpoint list** per module: three to five things the learner can do or explain.
- **Self-check quiz**: three to five auto-graded questions with hints and explanations, using the quiz widget (W15).
- **Capstone per track** (see section 9): a project that cannot be completed by copying the module code.

### 2.5 Writing rules

- Intuition and a worked example always come before notation.
- Every formula is followed by one sentence saying what it means in poker terms.
- Every claim of convergence is accompanied by an exploitability curve.
- Every number quoted from the literature carries a citation and appears on the verified-facts table (Appendix C).

---

## 3. Interactive design system

### 3.1 Visual language

A single consistent language so learners never have to re-learn what colors mean.

- **Players:** Player 0 (first to act in two-player games) is blue; Player 1 is orange; chance is gray; terminal payoffs are shown as green (positive) and red (negative) with signs and values written out. Use a colorblind-safe palette (Okabe–Ito family) and never rely on color alone: shape, label or pattern always repeats the information.
- **Actions** follow the convention poker solver users already know: fold is a cool blue-gray, check or call is green, bet or raise is a red scale that deepens with size, and all-in is the deepest shade. Each action also has a letter or icon.
- **Cards:** drawn as rank plus a suit *shape* (not just color), with a simple flat style. Hidden cards use a neutral back. A card the viewer cannot know is visibly different from one they know.
- **Information sets:** always drawn as a dashed outline or a shared bracket connecting the indistinguishable nodes, with the same label style everywhere.
- **Strategies:** always shown as horizontal stacked bars summing to 100%, one bar per decision, ordered the same way every time. Hover shows the exact probability.
- **Time:** a scrubber with play, pause, step and speed control, used for anything that evolves over iterations.
- **Units:** every chart states its unit. Toy games use chips (ante = 1); Hold'em modules use milli-big-blinds per hand (mbb/h). Exploitability charts default to log-log axes with a dotted reference slope.

### 3.2 Standard layout of a demo

- **Header strip:** title, a one-sentence goal ("Find a strategy with exploitability below 0.001"), and an estimated time.
- **Three zones:** controls on the left, the main canvas in the center, and a live readout panel on the right (numbers, plain-language narration, the "Show the math" toggle). On a phone the zones stack vertically with controls above the canvas.
- **Footer strip:** Reset, Share link (state saved in the URL), Open in notebook, and a provenance line (which commit, seed and iteration count produced any precomputed data on screen).
- **Prediction card:** appears first when the demo opens, and can be skipped.
- **Guided tour mode:** a numbered sequence of callouts that walks through the demo once; always dismissible.

### 3.3 Interaction conventions

- Hover shows exact numbers; click pins them; the escape key clears.
- Compare mode splits the canvas into A and B, or overlays a ghost line for the reference answer (usually the known Nash equilibrium).
- Presets ("scenarios") load interesting configurations, such as "the bluffing spot" or "an exploitable bot".
- Every control has a keyboard equivalent. Sliders have numeric inputs next to them for precision.
- Motion lasts 150 to 300 milliseconds and is purposeful (showing causality), never decorative. A reduced-motion setting turns animations into instant state changes.

### 3.4 Accessibility

- WCAG AA contrast in both light and dark themes.
- Full keyboard operation; visible focus.
- Screen-reader summaries that update live ("Exploitability is now 0.012, down from 0.031").
- Every chart has a "View as table" toggle with the underlying numbers.
- No information conveyed by color alone.

### 3.5 Performance budgets

- First load of a demo under about 1 MB; heavy demos under about 3 MB with lazy loading.
- Interactions stay smooth; anything that takes longer than a few hundred milliseconds runs off the main thread and shows progress.
- Large solved strategies are **precomputed in continuous integration** and stored as compressed data files with a manifest; they are never solved live in the browser unless the game is tiny.

### 3.6 Four implementation tiers for interactives

| Tier | Technology idea | Used for | Pros and cons |
|---|---|---|---|
| **A. Static** | precomputed data files rendered with plain JavaScript and SVG or canvas | nearly everything, especially heatmaps and range grids | fastest, cheapest, works on static hosting; no live solving |
| **B. Python in the browser** | the real repo library running through a browser Python runtime | Kuhn, small Leduc, regret-matching labs | one codebase for demo and library; heavy first load (lazy-load it) |
| **C. Compiled solver in the browser** | a small solver compiled to WebAssembly | push/fold solving, small live CFR | live and fast; extra build toolchain |
| **D. Notebook** | Python notebooks (Marimo or Jupyter) | heavy labs, hyperparameter sweeps, deep-learning labs | most flexible; not zero-install |

Default to Tier A. Move to B or C only when the learning value of *live* computation clearly outweighs the cost.

### 3.7 Data pipeline for demos

A "demo data" job in continuous integration runs the solvers with fixed seeds and writes versioned data files (strategies, convergence curves, range grids, benchmark tables) plus a manifest recording commit, seed, iteration count and wall-clock time. Demos read only from this manifest, so every number on screen can be reproduced by rerunning one command.

---

## 4. Shared widget catalog

Build each widget once, parameterized, then reuse. The "Modules" column shows where it appears.

| ID | Widget | What it shows | Modules |
|---|---|---|---|
| **W1** | **Game Tree Explorer** | an interactive tree: nodes colored by acting player, edges labeled with actions, terminal payoffs, dashed outlines grouping information sets; click a node for history, reach probabilities and counterfactual values; a viewpoint toggle hides what one player cannot see; collapsible subtrees with a running node count | 00, 01, 03, 11, 13 |
| **W2** | **Strategy Table and Heatmap** | one row per information set with stacked action bars; a heatmap mode lays rows out by (private card × history) so patterns appear; a ghost overlay shows the reference equilibrium; a time scrubber replays training | 01, 03, 04, 05, 07, 08 |
| **W3** | **Exploitability Plot** | log-log curve of exploitability against iterations or time, several runs overlaid, a dotted 1/√T reference, markers where checkpoints occur, hover for exact values, band mode for variance across seeds | 01–09, 11, 12 |
| **W4** | **Regret Bars** | cumulative regret per action at a chosen information set, with the positive part highlighted and the resulting strategy shown beside it; animates updates frame by frame | 01, 02, 03 |
| **W5** | **13×13 Range Grid** | the standard Hold'em grid with pairs on the diagonal, suited hands above, offsuit below; cell color or split-bar shows action mix or frequency; hover shows combo count; drag to paint a range; running readout of total combos and percent of hands | 04, 05, 06, 07, 12 |
| **W6** | **Equity Calculator** | hand against a range on a chosen board, with a runout animation showing equity swinging as cards appear, plus an equity distribution histogram | 04, 05, 06, 10 |
| **W7** | **Bet-Size Tree Builder** | set a menu of bet sizes per street and node; see the resulting tree, node count and a memory and time estimate; compare menus side by side | 05, 06, 07, 13 |
| **W8** | **Abstraction Viewer** | hands colored by bucket, a bucket-size histogram, a similarity matrix, a slider for the number of buckets, and a readout of abstraction loss | 05, 06, 10 |
| **W9** | **Play-and-Review Table** | a playable table against a bot; afterwards a review reveals the bot's strategy at every decision, the learner's EV loss per decision, and a running "mistake score" | 01, 03, 05, 07, 12 |
| **W10** | **Convergence Race** | several algorithms run on the same game in lanes, with synchronized time, an exploitability curve per lane and a bar showing who is ahead | 02, 03, 04, 08 |
| **W11** | **Belief and Range Tracker** | bars (or a grid) showing each player's belief over hidden information, updating by Bayes' rule after each action, with a Sankey-style flow showing how ranges narrow | 00, 03, 07, 09 |
| **W12** | **Rules Builder** | a form where the learner configures a game (deck, hole cards, streets, betting structure, peek or auction mechanics) and gets a rule card, a tree-size estimate and an information-structure summary | 13, 14 |
| **W13** | **Scale Calculator** | sliders for streets, bet sizes, buckets and players; outputs counts of states and information sets, memory and time estimates, on log scales | 04, 05, 06, 07, 10 |
| **W14** | **Information Timeline** | a swimlane per player showing what each can see at each step, color-coded as public, private or semi-private | 01, 11, 13 |
| **W15** | **Quiz and Flashcards** | auto-graded multiple choice with hints and explanations, switchable to flashcards | all modules |
| **W16** | **Hover Glossary** | any glossary term shows a small card on hover with a one-line definition and a link | all modules |
| **W17** | **Simplex Plot** | a triangle (three actions) or line (two actions) showing a strategy as a moving point, with best-response regions shaded and the trajectory of learning drawn as a trail | 00, 02, 11, 12 |
| **W18** | **Bot Arena Panel** | pick two bots, run a match, see winrate with confidence interval and a variance-reduced estimate | 05, 07, 11, 12, 13 |

---

## 5. Module-by-module plan

Each module lists: header facts, why it exists, learning objectives, the concept map in teaching order, interactive features (with look, controls, the "aha" and data needs), notebook labs, exercises and projects, ground truth, misconceptions, deliverables, and the hand-off to the next module.

---

### Module 00: Prerequisites

**Level:** Beginner · **Prereqs:** none · **Essential for:** Newcomer · **Effort:** about 1.5 person-weeks · **Game status:** none (tools only)

**Why it exists.** Everything later assumes a comfort with probability, expected value and the idea of an equilibrium. This module supplies exactly that and nothing more, always using card examples.

**Learning objectives.** The learner can compute an expected value, update a belief with Bayes' rule, find the equilibrium of a small matrix game by hand, and explain why a sequential game with hidden information needs a tree and information sets.

**Concept map (teaching order)**

1. *Counting for card games:* combinations, how many two-card hands exist, conditional probability, **card removal** (holding an ace changes how many aces your opponent can hold).
2. *Expected value and variance:* EV of a bet, EV of a fold, the law of large numbers, why short-run results mislead.
3. *Pot odds and break-even:* required equity to call, and its mirror image, how often a bluff must work; **minimum defense frequency** introduced as a preview of why bluffing is mathematically forced.
4. *Bayes' rule for beliefs:* a prior over opponent holdings, an observed action, a posterior. This is the seed of the "range" concept used everywhere later.
5. *Normal-form games:* payoff matrices, dominant strategies, best response, pure vs mixed strategies.
6. *Nash equilibrium and zero-sum games:* equilibrium definition, minimax theorem in words, the **indifference principle** (at equilibrium you mix so the opponent is indifferent), game value.
7. *Solving tiny games exactly:* 2×2 by indifference; larger matrices by linear programming, explained as "find the strategy whose worst case is best".
8. *Extensive-form games:* trees, chance nodes, perfect vs imperfect information, **information sets**, perfect recall, behavior strategies vs mixed strategies and why they are equivalent under perfect recall.
9. *Why trees beat matrices:* converting a small sequential game into a matrix shows an exponential blow-up in strategies, motivating everything that follows.
10. *Computation basics:* how fast the tree grows, memory, random seeds and reproducibility.

**Interactive features**

- **I00.1 EV Playground [P0].** *Look:* a simple bet scenario drawn as a one-step tree with editable probabilities and payoffs. *Controls:* sliders for win chance, pot and bet size; a "simulate N hands" button. *Aha:* a histogram of simulated outcomes fills in; the average converges to the EV while individual runs wander, showing why short samples lie. *Data:* live, trivial.
- **I00.2 Pot Odds and Bluff Calculator [P0].** *Look:* a pot graphic with a bet on top and two linked gauges: "equity needed to call" and "how often the bluff must work". *Controls:* pot and bet size sliders. *Aha:* as the bet grows, the caller needs more equity and the bluffer needs more folds, and the two gauges move in lockstep. *Predict prompt:* "What fraction must fold for a pot-sized bluff to break even?" *Data:* live.
- **I00.3 Card Removal Counter [P0].** *Look:* a 52-card grid with two hero cards selectable and a live count of opponent combos. *Controls:* click cards to hold or board them. *Aha:* the combo counts for specific hands shrink as cards are removed (holding an ace makes AA harder for the opponent). *Data:* live.
- **I00.4 Bayes Updater (W11 variant) [P0].** *Look:* three or four prior bars (for example "strong", "medium", "bluff") and a likelihood table for an observed action. *Controls:* drag prior bars; edit likelihoods; choose the observed action. *Aha:* posterior bars slide, and the learner sees the posterior depends as much on how often each type takes the action as on how common each type is. *Data:* live.
- **I00.5 Payoff Matrix Lab with Simplex Plot (W17) [P0].** *Look:* an editable 2×2 or 3×3 matrix beside a line or triangle on which the opponent's mixed strategy can be dragged; regions shade by the row player's best response; equilibrium appears as a marker. *Controls:* edit payoffs; drag the opponent's mix; toggle "show indifference line". *Aha:* the equilibrium sits exactly where best-response regions meet, and there the opponent cannot gain by shifting. *Data:* live.
- **I00.6 Tree vs Matrix Converter [P1].** *Look:* a tiny sequential game on the left and its normal-form matrix on the right. *Controls:* add a decision node or an extra action. *Aha:* the matrix grows explosively (strategies multiply) while the tree grows gently, with a counter showing both sizes. *Data:* live.
- **I00.7 Information Set Painter [P1].** *Look:* a tree with unlabeled nodes. *Controls:* drag a dashed outline around nodes the player cannot distinguish; the page checks the result. *Aha:* it flags groupings that break perfect recall or that mix nodes with different legal actions, with a plain-language reason. *Data:* live.
- **I00.8 Linear Programming Intuition [P2].** *Look:* a 2-action game drawn as lines over a strategy axis, with the lower envelope highlighted. *Aha:* "the best worst case" is the peak of the lower envelope, which is the game value. *Data:* live.

**Notebook labs.** Simulate bet EVs and confirm convergence; solve rock-paper-scissors and a 3×3 game by linear programming; build a small tree and enumerate its normal form.

**Exercises and projects.** *Recall:* define an information set in one sentence. *Implement:* write a function that solves any 2×2 zero-sum game by indifference. *Extend:* show that a pot-sized bluff needs to work one time in three, then generalize to any bet size.

**Ground truth.** Rock-paper-scissors is uniform. A biased version has a hand-solvable equilibrium. Pot-odds and bluff-frequency formulas are checked against hand-worked examples. Linear-programming results match indifference solutions on 2×2 games.

**Common mistakes.** Treating a mixed strategy as "indecision"; thinking equilibrium means "50/50"; believing EV is what happens in a single hand.

**Deliverables.** Combinatorics and EV helpers; a matrix-game solver by indifference and by linear programming; unit tests with hand-worked values.

**Hand-off.** Matrices cannot describe sequences of moves with hidden cards compactly; Module 01 introduces the smallest game that has both.

---

### Module 01: Kuhn Poker

**Level:** Beginner · **Prereqs:** 00 · **Essential for:** everyone · **Effort:** about 1 person-week of additional work (core text, code and tests already exist; this plan adds the interactives) · **Game status:** solved exactly, with a known family of equilibria

**Why it exists.** It is the smallest game with bluffing, hidden information and sequential play, small enough to solve by hand and verify against a known answer.

**Learning objectives.** The learner can draw the tree, name every information set, explain why bluffing with the worst card is part of equilibrium, compute exploitability, and recognize the equilibrium family.

**Concept map**

1. The rules and the five terminal histories.
2. The game tree with chance at the root; histories vs information sets; why the acting player cannot see the opponent's card.
3. Pure, mixed and behavior strategies; why mixing is forced (always-call and never-call are both exploitable).
4. **Best response** computed by backward induction over information sets.
5. **Exploitability** and why it is zero exactly at equilibrium.
6. The **equilibrium family** (indexed by a single parameter between 0 and one third) and the game value of minus one eighteenth for the first player.
7. Bluffing and value betting as emergent behavior, not rules.
8. Vanilla CFR as a first look, treated as a tool (theory is Module 02).
9. Variants as thought experiments: a four-card deck, a different bet size, a second raise.

**Interactive features**

- **I01.1 Kuhn Tree Explorer (W1) [P0].** *Look:* the full tree with both players' information sets drawn as dashed groupings; terminal payoffs in green and red. *Controls:* click a node to see its history, reach probabilities and values; toggle "view as Player 0" to hide Player 1's card; hover an information set to highlight every node inside it. *Aha:* two different deals look identical from the actor's seat, so the strategy must treat them identically. *Predict prompt:* "How many information sets does Player 1 have?" *Data:* static.
- **I01.2 Play Kuhn [P0] (W9).** *Look:* a three-card table. The learner plays against a series of opponents chosen from a menu: random, always-bet, a bluff-heavy bot, and the equilibrium bot. *Controls:* pass or bet buttons; opponent selector. *Aha:* a running chip total shows exploitable bots losing to a good counter-strategy and the equilibrium bot being impossible to beat in the long run; the post-hand review reveals the bot's mixing probabilities. *Data:* static strategies; live sampling.
- **I01.3 Equilibrium Family Slider [P0].** *Look:* a strategy table beside a plot of exploitability and game value against the family parameter. *Controls:* one slider for the parameter. *Aha:* many different-looking strategies are all perfectly unexploitable and all give the same game value; the value stays pinned at minus one eighteenth. *Data:* analytic, live.
- **I01.4 Exploitability Probe, "Nash Hunter" [P0] (W2 + W3).** *Look:* twelve strategy sliders (one per information set) beside a live exploitability readout and a visible best-response panel. *Controls:* drag any probability; a "reset to uniform" and a "show Nash" ghost. *Aha:* nudging a single probability shows exactly which opponent counter-strategy appears and how much it wins; a challenge mode awards a badge for reaching exploitability below a target. *Data:* live (the best-response computation is small).
- **I01.5 Best Response Walkthrough [P1] (W1).** *Look:* the tree with leaves highlighted. *Controls:* a step button. *Aha:* the best response is computed bottom-up, with each information set choosing the action that maximizes the weighted sum over the nodes inside it, which is why information sets matter. *Data:* static or live.
- **I01.6 CFR Stepper [P0] (W4 + W2).** *Look:* the tree on one side, regret bars and the resulting strategy on the other. *Controls:* step, play, speed; choose an information set to watch. *Aha:* the learner sees counterfactual regret accumulate and strategy shift, and watches the average strategy slowly stabilize while the current one jitters. *Data:* live (small).
- **I01.7 Rule Tweaker [P1].** *Look:* the table of rule options (deck size, bet size, ante). *Controls:* change a rule and press "solve". *Aha:* the first-player disadvantage and the bluff frequency shift, with the changes shown against the original. *Data:* precomputed grid for common settings, live for others (small).

**Notebook labs.** Train CFR and compare with the hand-derived equilibrium; plot exploitability; build your own member of the equilibrium family and verify it; break the equilibrium and measure the loss.

**Exercises and projects.** Hand-derive the player-two strategy; extend to four cards and predict the shift in first-player disadvantage; add a second raise and see which hand-derived results survive.

**Ground truth.** Game value of minus one eighteenth for the first player; the equilibrium family; CFR average strategy exploitability falling to near zero; all already encoded in the test suite.

**Common mistakes.** Thinking the middle card "should" always check back; thinking a bluff with the lowest card is a mistake because it "always loses"; thinking Player 1's strategy can depend on Player 0's card.

**Deliverables (additional).** Static data files for the explorer and family plots; a shared widget implementation of W1, W2, W3 and W4 that later modules reuse.

**Hand-off.** One betting round and no shared cards. Next: *why* CFR works.

---

### Module 02: Regret Matching and No-Regret Learning

**Level:** Beginner · **Prereqs:** 00, 01 · **Essential for:** everyone · **Effort:** about 1 person-week of additional work (text, code, tests, notebook and a first demo already exist) · **Game status:** solved (matrix games)

**Why it exists.** It explains why self-play with regret produces equilibrium, in the simplest possible setting, so that CFR is not a black box.

**Learning objectives.** The learner can define regret, run regret matching by hand, state the regret bound and its proof idea, explain why the average strategy converges while the current one cycles, and map the per-information-set update in CFR to regret matching.

**Concept map**

1. Online learning setting: choose a distribution, see all utilities, repeat.
2. **External regret** and "no-regret" (and what it does *not* promise).
3. **Regret matching** and a hand-worked example.
4. The regret bound and its proof sketch (the zero cross-term trick).
5. **From no-regret to equilibrium** in two-player zero-sum games, and why averages are the right object.
6. The pitfall of starting at the equilibrium in a symmetric game.
7. **Rates:** regret grows like the square root of time, so exploitability falls like one over the square root of time; practical meaning (ten times more accuracy costs a hundred times more iterations).
8. Variants: regret matching plus, Hedge and its learning rate, fictitious play for contrast.
9. The bridge to CFR: counterfactual values, why weight by the other parties' reach, why average by one's own reach.
10. Optional advanced sidebar: Blackwell approachability as the geometric reason regret matching works.

**Interactive features**

- **I02.1 Regret Matching Lab [P0] (exists; extend).** *Look:* a rock-paper-scissors panel with a strategy chart. *Controls:* opponent sliders, self-play toggle, run and reset. *Aha:* thick average lines converge while thin current lines keep swinging. *Planned upgrades:* a vertical "regret bars" strip (W4) beside the chart, and a speed control.
- **I02.2 Simplex Trajectory [P0] (W17).** *Look:* a triangle with a moving point for the current strategy and a second point for the average strategy; the current point spirals while the average drifts to the center, leaving a visible trail. *Controls:* choose the algorithm; step or run. *Aha:* the geometric picture of cycling vs convergence is more convincing than any chart. *Data:* live.
- **I02.3 Opponent Switch Test [P0].** *Look:* the learner plays against a scripted opponent that switches strategy partway through; a timeline shows the learner's strategy chasing it. *Controls:* choose the switch time; compare regret matching and regret matching plus. *Aha:* old regret takes time to unwind in plain regret matching, and the plus variant recovers faster. *Data:* live.
- **I02.4 Hedge Learning-Rate Lab [P1].** *Look:* a strategy chart for Hedge with one slider. *Controls:* learning rate (fixed or decaying). *Aha:* too large a rate cycles wildly, too small learns slowly, and a decaying schedule avoids both.
- **I02.5 Regret vs Bound [P1] (W3 variant).** *Look:* measured regret curve below a square-root envelope. *Aha:* the theory's bound is real and loose, but the shape matches.
- **I02.6 Algorithm Race [P1] (W10).** *Look:* three lanes (regret matching, regret matching plus, Hedge) running the same game. *Aha:* faster in practice than in worst-case theory, with different winners on different games.
- **I02.7 Decomposition Diagram [P0].** *Look:* a mini poker tree with a regret matcher drawn at each information set and arrows carrying counterfactual values in; hovering a node shows that node's regret formula with numbers. *Aha:* CFR is many tiny regret matchers wired to a tree. *Data:* static.
- **I02.8 No-Regret Implies Equilibrium Visualizer [P2].** *Look:* two panels (row and column) with regret meters and a combined exploitability meter. *Aha:* when both regrets fall, exploitability is pinned below their sum.

**Notebook labs.** Reproduce the worked example; plot current vs average; measure the one-over-root-T rate; compare algorithms; solve a biased game; implement linear averaging.

**Exercises and projects.** Extend by solving a three-action game with different payoffs; implement Hedge with a fixed rate and sweep it; measure adaptation delay after an opponent switch.

**Ground truth.** Exploitability times the square root of time stays roughly constant; regret stays under the proven bound; average strategies reach the known biased-game equilibrium.

**Common mistakes.** Reading the current strategy as the answer; believing no-regret means "never loses"; starting a symmetric game at the equilibrium and concluding nothing happens.

**Deliverables.** Already present; add shared widgets W4 and W17.

**Hand-off.** Full-tree traversal each iteration is the cost; Leduc makes it visible, adds chance in the middle and public cards.

---

### Module 03: Leduc Hold'em

**Level:** Intermediate · **Prereqs:** 01, 02 · **Essential for:** everyone · **Effort:** about 2 person-weeks · **Game status:** solved to machine precision (on the order of a thousand information sets; the standard six-card version has about 936 **(verify)**)

**Why it exists.** It is the first game with a public card revealed mid-game, two betting rounds and raises, yet small enough to solve exactly and to see everything.

**Learning objectives.** The learner can describe how chance nodes in the middle of a game affect strategies, track beliefs over the opponent's card, run CFR and CFR+, and explain why variants of CFR converge faster.

**Concept map**

1. Rules: six cards (three ranks, two suits), one private card each, one public card after the first betting round, two bet sizes (small in round one, large in round two), a cap on raises, a pair beats a high card.
2. Game size; why exact solving is still feasible and what it teaches.
3. **Chance nodes between decision nodes:** how reach probabilities now include chance on both sides.
4. **Public vs private information; card removal** (the opponent cannot hold the card you hold, nor the board card).
5. **Beliefs:** the posterior over the opponent's card after observed actions and the board; the first concrete view of a "range".
6. CFR on Leduc: traversal, counterfactual values with chance, regret and strategy updates.
7. **Faster variants:** regret matching plus (floor regrets at zero), **alternating updates** (update one player at a time), **linear averaging** (weight later iterations more), and discounted CFR (separate discount exponents for positive regret, negative regret and the average).
8. **Reading a strategy table:** patterns such as "bluff-raise round one with the weakest card", "pair is always value", and how the board card changes everything.
9. Convergence diagnostics: exact exploitability, game value, strategy stability.

**Interactive features**

- **I03.1 Leduc Tree Explorer [P0] (W1).** *Look:* a collapsible tree with a chance node in the middle; subtrees collapse to a labeled triangle with a node count. *Controls:* expand and collapse; filter by private card or board card; a "viewpoint" toggle. *Aha:* the tree's size makes clear why hand-solving is hopeless and why information sets compress it. *Data:* static.
- **I03.2 Strategy Heatmap Explorer [P0] (W2).** *Look:* a grid whose rows are (private card × board card) and whose columns are betting histories; each cell is a stacked action bar or a single color for "probability of raise". *Controls:* a round filter, an iteration scrubber, a "show final answer" ghost, and a "diff vs final" mode. *Aha:* patterns that look random at iteration one resolve into a coherent strategy, and bluffs and traps become visible at a glance. *Predict prompt:* "With the lowest card and a board that does not pair you, what will Player 1 do after a check?" *Data:* precomputed snapshots at selected iterations.
- **I03.3 Belief Tracker [P0] (W11).** *Look:* above the table, a bar chart of the opponent's possible cards; below, a step-through of a hand. *Controls:* step through actions; sliders for how aggressive the opponent is; a toggle between "my belief" and "what the opponent believes about me". *Aha:* a raise shifts weight toward strong holdings by an amount that depends on how often each holding raises, and the board card sharply reshuffles beliefs. *Data:* live (small).
- **I03.4 Reach Decomposition [P0].** *Look:* pick an information set; the page draws the probability of reaching it as a product of three colored segments (your own choices, the opponent's choices, chance). *Aha:* this is *the* picture behind "counterfactual": regret is weighted by the other two segments, and the average strategy by your own. *Data:* static.
- **I03.5 CFR Variant Race [P0] (W10).** *Look:* four lanes (vanilla, plus, alternating plus, discounted) on the same game. *Controls:* iterations per second, a "reset with seed" button. *Aha:* the speedups are not small; the plus variants reach a given accuracy in a fraction of the iterations. *Data:* precomputed curves with seeds in the manifest.
- **I03.6 Play Leduc [P0] (W9).** *Look:* a small table with two cards. *Controls:* check, bet, call, fold, raise. *Aha:* after each hand a review shows the bot's strategy and the learner's per-decision loss against the equilibrium; a session summary lists the learner's habitual leaks. *Data:* static strategy file.
- **I03.7 Pair and Board Explorer [P1].** *Look:* a small matrix of "private card × board card" colored by hand strength, with equity against a random opponent. *Aha:* a pair is overwhelmingly strong, and that fact drives much of the strategy.
- **I03.8 Alternating vs Simultaneous Updates [P2].** *Look:* a timeline of update order. *Aha:* using fresher information from the other player's last update speeds convergence.

**Notebook labs.** Build Leduc from the game interface; run CFR and CFR+; plot convergence for each; compute exact exploitability; cross-check game value and exploitability against a trusted reference implementation.

**Exercises and projects.** Add a third rank; change the raise cap; change bet sizes and report how the first-player value moves; implement discounted CFR with different exponents.

**Ground truth.** Known exploitability and game-value numbers from a reference library (the game value is near minus 0.086 for the first player **(verify)**); every solver's average strategy must agree with the reference within a stated tolerance.

**Common mistakes.** Treating the board card as private; forgetting to remove the board card from the opponent's possibilities; averaging strategy over iterations with the wrong weighting; confusing the beliefs a player holds with the strategy they play.

**Deliverables.** Leduc engine; vanilla CFR generalization; CFR+ and discounted variants; cross-check tests; precomputed strategy and convergence data; widgets W1, W2, W9, W10, W11.

**Hand-off.** Each iteration still visits everything. A bigger deck makes that unaffordable, so we sample (Module 04).

---

### Module 04: Expanded Leduc, River Poker and Monte Carlo CFR

**Level:** Intermediate · **Prereqs:** 03 · **Essential for:** Competitor, Researcher · **Effort:** about 2.5 person-weeks · **Game status:** solved to good accuracy (expanded Leduc); single-street poker spots solved via sampling and vectorization

**Why it exists.** It introduces sampling, the idea that unlocks every larger game, and the vectorized "range" view of poker used from here on.

**Learning objectives.** The learner can describe the main sampling schemes, explain why importance weighting keeps estimates unbiased, measure variance, and set up and interpret a river-only spot with ranges.

**Concept map**

1. Why sample: cost of a full traversal grows with game size, while accuracy per sample stays useful.
2. **Sampling schemes:** chance sampling, external sampling, outcome sampling, and a mention of average-strategy and robust sampling.
3. **Importance weighting** and unbiasedness: each scheme corrects for the probability it chose a path.
4. **Variance and its reduction:** what makes estimates noisy; baselines (control variates); the tradeoff between cheap noisy iterations and expensive accurate ones.
5. **Scaling laws:** how time, memory and accuracy trade as the deck grows; where sampling overtakes full traversal.
6. **Expanded Leduc:** more ranks (and possibly more suits) as a controllable scaling dial.
7. **River poker:** one betting street with five-card boards, seven-card hands, ranges as inputs; **card removal and blockers** at scale.
8. **Vectorized (range-based) CFR:** process all private hands in one pass using vectors of reach probabilities and a showdown matrix; fast showdown evaluation by sorting hands by strength.
9. **Analytic anchors:** closed-form toy poker games (a clairvoyance game and a simple "ace-king-queen" style game) whose equilibria are known by hand: the correct bluff-to-value ratio and calling frequency fall out of bet size.
10. **Estimating exploitability** when exact best response is expensive: sampled estimators and confidence intervals.
11. Parallelization ideas (batching, lock-free updates) as a brief engineering sidebar.

**Interactive features**

- **I04.1 Sampling Visualizer [P0].** *Look:* the Leduc tree with the traversed path of each iteration lit up and everything else dimmed; a counter shows nodes visited vs full-tree size. *Controls:* choose the sampling scheme; step through iterations. *Aha:* each scheme visits a different, much smaller slice of the tree, and the per-sample importance weights appear on the edges. *Data:* live (small).
- **I04.2 Variance Lab [P0] (W3 band mode).** *Look:* an exploitability curve with a shaded band over many seeds. *Controls:* samples per iteration; baseline on or off; scheme. *Aha:* a baseline narrows the band dramatically; more samples per iteration trade time for steadiness. *Data:* precomputed seeds.
- **I04.3 Scaling Dashboard [P0] (W13).** *Look:* a slider for the number of ranks drives three log-scale readouts: game size, memory, and time per iteration; a marker shows where sampling overtakes full traversal. *Aha:* the crossover is not subtle. *Data:* measured benchmark table plus a fitted trend.
- **I04.4 River Spot Solver Viewer [P0] (W5 + W6).** *Look:* two 13×13 grids (out-of-position and in-position ranges) plus a pot-and-stack panel; after "solve" (precomputed for presets), the grids recolor by action (check, bet small, bet large, fold, call). *Controls:* choose a board; paint a range; pick a pot and bet menu; hover a hand to see its EV and equity. *Aha:* strong hands and bluffs appear together in the betting range in a ratio set by bet size, which is the bluff-to-value ratio come to life. *Predict prompt:* "Which hands will bluff on this board?" *Data:* precomputed solutions for a curated library of boards.
- **I04.5 Blocker Explorer [P1] (W5).** *Look:* a board and a hero hand; the opponent's range grid dims combos the hero's cards block. *Aha:* a good bluff holds the card that blocks the opponent's strongest calls.
- **I04.6 Analytic Toy Game Checker [P0].** *Look:* a tiny one-street game with a formula-driven optimal bluff frequency; the solver's answer is overlaid as a point on the analytic curve. *Controls:* bet size slider. *Aha:* the solver recovers the textbook answer for every bet size. *Data:* analytic plus live small solve.
- **I04.7 Equity Distribution View [P1] (W6).** *Look:* a histogram of how each range's equity is spread. *Aha:* ranges with the same average equity can have very different shapes (polarized vs condensed), which changes optimal betting.
- **I04.8 Exploitability Estimator [P2].** *Look:* a plot with error bars comparing the sampled estimate to the exact value on a game where both are computable.

**Notebook labs.** Implement each sampling scheme on Leduc and compare; fit scaling curves; build a river spot from two ranges; solve an analytic toy game and confirm the closed form.

**Exercises and projects.** Add a baseline and measure variance; design an expanded Leduc with different rank counts and find the crossover point; solve a river spot with two bet sizes and compare to one.

**Ground truth.** Sampled solvers agree with full CFR on Leduc; analytic toy-game answers; unbiasedness checked statistically (the mean estimate over many samples equals the full value).

**Common mistakes.** Forgetting importance weights; comparing runs without matching seeds or compute; assuming more samples always beat more iterations; treating a sampled exploitability estimate as exact.

**Deliverables.** MCCFR variants; expanded Leduc; river poker engine with a seven-card evaluator for this single street; vectorized CFR core; analytic toy games and tests; widgets W5 and W6 first built here.

**Hand-off.** We solved one street with fixed ranges. Real poker has four streets, huge hand sets and blinds. Next: a full game with real evaluation.

---

### Module 05: Limit Texas Hold'em

**Level:** Intermediate · **Prereqs:** 03, 04 · **Essential for:** Competitor, Researcher · **Effort:** about 3 person-weeks · **Game status:** heads-up limit Hold'em is "essentially solved" (weakly) by large-scale CFR+; on the order of 10^14 information sets **(verify)**

**Why it exists.** It is real poker with the hardest part (unlimited bet sizes) removed. It forces us to build a fast evaluator and a full betting engine, and shows why even this game needs abstraction.

**Learning objectives.** The learner can build and test a hand evaluator and a betting engine, compute equity against ranges, describe the size of the game, and explain how bucketing makes it tractable.

**Concept map**

1. Rules: blinds, four streets, fixed bet sizes by street, raise cap, heads-up position, split pots.
2. **Hand evaluation:** hand rankings, best five of seven, lookup-table and hash-based evaluators, and why speed matters (billions of evaluations).
3. **Starting-hand structure:** 169 strategic hand classes, 1,326 combinations, suit symmetry.
4. **Hand strength measures:** raw equity, expected hand strength, and why equity against a *range* differs from equity against a random hand.
5. **Potential:** hands with the same current strength but different futures (made hand vs draw); the shape of the strength distribution.
6. **Betting-round engine:** legal actions, raise cap, all-in cases, blind order, chip conservation.
7. **Game size:** counting decision points street by street, and why exact solving needed enormous compute.
8. **First abstraction:** bucketing hands by strength percentile and the idea of imperfect recall (forgetting earlier bucket history); the cost of each simplification.
9. **Running MCCFR on a bucketed game** and measuring progress without full exploitability (approximations).
10. How the "solved" status of the game is defined and what it did and did not prove.

**Interactive features**

- **I05.1 Hand Evaluator Playground [P0].** *Look:* a deck grid; click up to seven cards. A result panel shows the best five-card hand highlighted among the seven, the category name and a rank number. *Controls:* click cards; "random deal"; compare two hands side by side. *Aha:* the winning five cards are highlighted even when a kicker decides, and comparisons are resolved with a visible tie-break explanation. *Data:* live (a small evaluator in the browser).
- **I05.2 Equity vs Range [P0] (W6 + W5).** *Look:* a hero hand, a board stage selector (preflop, flop, turn, river) and a villain range grid. *Controls:* choose cards; paint a range; deal the next street. *Aha:* a runout animation shows equity swinging as cards fall, and the readout separates "win", "tie" and "lose" shares. *Predict prompt:* "Which of these two hands has more equity against this range?" *Data:* live Monte Carlo with a stated sample size and error bar.
- **I05.3 Hand Strength Histogram [P0].** *Look:* two hands on the same board with their distributions of future strength drawn as histograms. *Controls:* choose hand and board. *Aha:* two hands with the same average equity (a medium pair and a flush draw) look completely different, which is why potential matters and why simple strength bucketing is lossy.
- **I05.4 Betting Round Simulator [P0] (W9 scaffold).** *Look:* a table with pot, stacks, and the legal action buttons for the current spot. *Controls:* choose actions; a "scenario" menu loads edge cases (raise cap reached, short stack, first-to-act rules). *Aha:* the interface refuses illegal actions and explains why, teaching the engine's rules by example. *Data:* live.
- **I05.5 Preflop Strategy Explorer [P0] (W2 + W5).** *Look:* two 13×13 grids (small blind and big blind) colored by action mix. *Controls:* iteration scrubber; a "show EV" overlay; a position toggle. *Aha:* strategy forms as iterations progress; the grid shows how ranges differ by position. *Data:* precomputed from the abstracted solver.
- **I05.6 Game Size Calculator [P0] (W13).** *Look:* per-street bars on a log scale for the number of decision points, with a second set of bars after bucketing. *Controls:* bucket counts per street; raise cap. *Aha:* the bars make the necessity of abstraction obvious, and show how brutally the number of buckets shrinks the game. *Data:* analytic.
- **I05.7 Evaluator Speed Chart [P1].** *Look:* a bar chart comparing a naive evaluator, a lookup-table evaluator and a hash-based one on the same hands. *Aha:* orders of magnitude, with the technique behind each explained. *Data:* measured benchmark table.
- **I05.8 Play Limit Hold'em [P1] (W9).** *Look:* a full table with a bot opponent. *Aha:* a review after each hand lists decisions where the learner deviated from the solver and by how much.
- **I05.9 Suit Isomorphism Demo [P2].** *Look:* two boards that differ only by suit relabeling shown as equivalent; a counter shows how many situations collapse.

**Notebook labs.** Build and test the evaluator; compute equity by enumeration and Monte Carlo; construct the engine and run invariants; train MCCFR on a bucketed game and track a proxy for exploitability.

**Exercises and projects.** Verify famous matchup equities; write a property test that chips are conserved over a million random hands; compare two bucketing schemes by equity of resulting strategy.

**Ground truth.** The count of seven-card hands by category matches the known table **(verify)**; head-to-head equities for classic matchups match reference calculators (for example, a top pair against a lower pair is roughly an 80–20 matchup **(verify)**); evaluator output agrees with a reference library on a very large random sample; chips are conserved.

**Common mistakes.** Treating hand strength as one number; forgetting the board plays for both players; mishandling split pots; evaluating equity against a random hand when the opponent's range is not random.

**Deliverables.** Five- and seven-card evaluators; limit engine; bucketed MCCFR; equity-vs-range calculator; widgets W6, W8 (first version), W9; data files for the preflop explorer.

**Hand-off.** Bucketing throws information away. How much does that cost, how do we choose buckets well, and how do we repair damage during play? Module 06.

---

### Module 06: Abstraction and Endgame Solving

**Level:** Advanced · **Prereqs:** 05 · **Essential for:** Competitor, Researcher · **Effort:** about 3 person-weeks · **Game status:** practical (blueprint plus real-time refinement), with provable guarantees for the subgame step

**Why it exists.** Abstraction is how every large poker bot is built, and *safe* endgame solving is the technique that lets a bot repair its abstraction at play time. This module teaches both, and their pitfalls.

**Learning objectives.** The learner can build card and action abstractions, measure their quality, explain abstraction pathologies, and describe and test safe subgame solving.

**Concept map**

1. **Lossless abstraction:** suit isomorphism (for example, about 1,755 strategically distinct flops **(verify)**), and why it is free.
2. **Lossy card abstraction:** features (expected strength), potential-aware features (distributions of future strength), and distribution-aware clustering using **earth mover's distance** between histograms.
3. **Clustering methods:** k-means and k-medoids over histograms; choosing the number of buckets per street; computing earth mover's distance in one dimension.
4. **Imperfect recall** abstractions and what is lost and gained.
5. **Action abstraction:** choosing bet-size menus; effect on game size; the "off-tree" problem when an opponent bets an unlisted size.
6. **Action translation:** mapping an unexpected bet to nearby sizes, including the pseudo-harmonic mapping and randomized variants.
7. **Abstraction pathologies:** finer abstractions can sometimes do *worse*; abstraction quality is not monotone.
8. **Evaluating abstractions:** exploitability inside the abstraction vs in the real game; tournaments; approximate best response.
9. **Blueprint strategy:** the coarse-grained solution used as a starting point.
10. **Subgame solving:** *unsafe* re-solving (using an estimated opponent range) and why it can be exploited; **safe** subgame solving with a gadget that lets the opponent opt out for the value the blueprint promised; the guarantee that the result is no more exploitable than the blueprint.
11. **Nested subgame solving:** re-solve again when the opponent takes an off-tree action, using the actual action instead of translation.
12. Engineering sidebar: storing and compressing blueprints.

**Interactive features**

- **I06.1 Abstraction Slider Lab [P0] (W8).** *Look:* a grid of all starting hands (or flop textures) colored by bucket, with a similarity heatmap. *Controls:* a slider for the number of buckets per street. *Aha:* a small bucket count lumps different hand types together; an accompanying curve shows solver time falling and real-game exploitability rising as buckets shrink. *Predict prompt:* "At what number of buckets does exploitability start to climb?" *Data:* precomputed sweep.
- **I06.2 Clustering Visualizer [P0] (W8).** *Look:* a two-dimensional map of hands (projected from their strength histograms), colored by cluster. *Controls:* choose the feature (average strength only vs full distribution); click a cluster to see its hands and its average histogram. *Aha:* averaging flattens draws and made hands together, while distribution-aware clustering separates them.
- **I06.3 Isomorphism Demo [P1].** *Look:* a flop selector and a list of boards that are strategically identical. *Aha:* a counter shows thousands of boards collapsing into a small number of classes.
- **I06.4 Action Translation Playground [P0] (W7).** *Look:* a bet-size line with the bot's abstract sizes marked; the learner drags an "unexpected bet" along it. *Controls:* bet size; translation method toggle; "attack mode" that shows a counter-strategy exploiting the mapping. *Aha:* a bet just between two menu sizes is mapped probabilistically, and some mappings can be exploited by choosing an awkward size.
- **I06.5 Safe vs Unsafe Re-solving Animator [P0].** *Look:* a three-stage animation: the blueprint, the subgame cut out of it, and the gadget that gives the opponent an opt-out. *Controls:* step; toggle "unsafe" to replace the gadget with a guessed range; "attack" to show an opponent range that punishes the unsafe version. *Aha:* the unsafe solution is exploited by a range the learner can see; the safe solution is not.
- **I06.6 Nested Solving Timeline [P1].** *Look:* the hand as a horizontal timeline; when an off-tree bet occurs, a panel re-solves and shows blueprint vs refined strategy for the same hand. *Aha:* the refined strategy differs where the blueprint's translation was weakest.
- **I06.7 Abstraction Pathology Demo [P1] (W3).** *Look:* a plot of real-game exploitability against bucket count on a toy game where it is non-monotonic. *Aha:* more detail is not always better.
- **I06.8 Compression Calculator [P2] (W13).** *Look:* storage estimates with and without quantization.

**Notebook labs.** Build a clustering pipeline; compare feature choices; measure abstraction loss in a game small enough for exact best response; implement and test safe subgame solving on a Leduc-sized endgame.

**Exercises and projects.** Make an action menu worse on purpose and exploit it; compare translation methods against a scripted attacker; show that unsafe re-solving can lose value on a hand-built example.

**Ground truth.** Lossless abstraction leaves the solved value unchanged; earth mover's distance matches closed-form values on simple histograms; safe re-solving achieves exploitability no worse than the blueprint plus a small tolerance on a small test game.

**Common mistakes.** Clustering only on average strength; evaluating abstraction quality only inside the abstraction; assuming a finer abstraction is automatically better; re-solving with a guessed range and assuming it is safe.

**Deliverables.** Bucketing pipeline; translation methods; safe and nested subgame solver on small games; tests for guarantees; widgets W7 and W8 (full).

**Hand-off.** No-Limit has nearly unlimited bet sizes and a far bigger tree; Module 07.

---

### Module 07: Heads-Up No-Limit Texas Hold'em

**Level:** Advanced · **Prereqs:** 05, 06 · **Essential for:** Competitor, Researcher · **Effort:** about 4 person-weeks · **Game status:** practically strong (blueprint, search and re-solving beat top professionals); no complete exact solution; the game has on the order of 10^161 decision points in its full form **(verify)**

**Why it exists.** It is the headline game: real stakes, real bet sizing, a game too large to store, and the place where the key techniques of modern poker AI converge.

**Learning objectives.** The learner can reason about bet sizing, read solver output, build a bet menu, run a depth-limited re-solving agent, and evaluate a bot without being able to compute exact exploitability.

**Concept map**

1. Rules, stack depth, minimum raise, all-in, why heads-up simplifies side pots.
2. **Strategy concepts as math:** stack-to-pot ratio and commitment, geometric bet sizing, **polarized vs merged** betting ranges, range advantage vs nut advantage, check-raising, blockers.
3. **Push/fold as a solvable stepping stone:** shoving or folding from small stacks is a tiny game solvable exactly, with famous equilibrium charts.
4. **Bet menus:** choosing sizes per street and node; the tradeoff between richer menus and tree size; which sizes the solver actually uses.
5. **Action translation** revisited at No-Limit scale (from Module 06).
6. **Continual re-solving:** keep only your own range and the opponent's counterfactual values; at each decision, re-solve a depth-limited subgame; why this avoids storing a full strategy.
7. **Depth-limited lookahead with leaf values** (previewing Modules 08 and 09).
8. **Evaluating without exact exploitability:** local best response as a lower bound; head-to-head matches; **variance reduction** (a control-variate method for poker matches) and why plain win rates need an enormous number of hands; milli-big-blinds per hand; confidence intervals; duplicate play.
9. Reading solver outputs: frequency tables, EV tables, how to sanity-check a strategy.

**Interactive features**

- **I07.1 Push/Fold Nash Explorer [P0] (W5).** *Look:* two 13×13 grids side by side (the shover's range and the caller's range) with a stack-depth slider underneath. *Controls:* stack depth from one to roughly twenty big blinds; toggle EV overlay. *Aha:* the shoving range widens dramatically as stacks shrink; the caller's range responds; the equilibrium value is displayed. *Predict prompt:* "At ten big blinds, what fraction of hands does the small blind shove?" *Data:* live (a tiny game solved in the browser, Tier C) or precomputed per stack depth.
- **I07.2 Bet-Size Tree Builder [P0] (W7).** *Look:* a tree whose edges are bet sizes; add or delete a size on any node. *Controls:* per-street size lists; a "node count and memory" meter. *Aha:* adding one extra size to every node multiplies the tree enormously, which is why menus are small and carefully chosen. *Data:* analytic estimates.
- **I07.3 Flop Strategy Explorer [P0] (W2 + W5).** *Look:* a 13×13 grid recolored by action mix (check, small bet, large bet, all-in), a board texture picker, a breadcrumb of the action line, and a side panel with aggregate frequencies, equity and EV by hand class. *Controls:* choose a board from a curated library; switch between acting positions; click a hand for its action mix and EV. *Aha:* range-level patterns such as "small bet with almost everything on dry boards" appear, and the display separates the range's behavior from one hand's. *Data:* precomputed solutions (a curated set of boards).
- **I07.4 SPR and Commitment Visualizer [P1].** *Look:* a pot graphic with a stack bar showing how many bets remain. *Controls:* stack-to-pot ratio slider. *Aha:* at low ratios, a single bet commits the stack; at high ratios, many streets of decisions remain; the best hands and the right sizes change accordingly.
- **I07.5 Polarization Lab [P0].** *Look:* a one-dimensional strength line from weak to strong with a draggable betting region. *Controls:* drag region boundaries to make a polarized (strong plus bluffs) or merged (middle strength) bet range; choose bet size. *Aha:* a live meter shows the opponent's break-even calling frequency, the bluff-to-value ratio needed to make them indifferent, and how a polarized range achieves it with bigger bets. *Data:* analytic.
- **I07.6 Continual Re-solving Walkthrough [P1] (W11).** *Look:* the learner's range and the opponent's counterfactual-value vector shown as two bars, updated after each action. *Controls:* step through a hand. *Aha:* the agent never needs a stored policy for the full tree; it needs only these two objects and a solver.
- **I07.7 Local Best Response Explainer [P1].** *Look:* a bot's strategy and an attacker that picks greedy best replies. *Aha:* a lower bound on exploitability, with the caveat that a weak attacker proves little.
- **I07.8 Match Evaluator with Variance Reduction [P0] (W18).** *Look:* a match runs and two winrate lines evolve, raw and variance-reduced, each with a confidence band. *Controls:* number of hands; opponent selection. *Aha:* the reduced band is much narrower, showing how many hands a conclusion really needs; a "hands needed" calculator accompanies it. *Data:* simulation.
- **I07.9 Play No-Limit with Review [P1] (W9).** *Look:* a full table. *Aha:* the review shows where the learner's bet sizes diverge from the solver's menu.

**Notebook labs.** Solve push/fold; build a bet menu and measure solve time; implement a depth-limited re-solver on a reduced game; estimate local best response; run a match with and without variance reduction.

**Exercises and projects.** Reproduce a known push/fold chart; add a third bet size and measure the cost; write an attacker that exploits a poor translation; determine the number of hands needed to see a given edge.

**Ground truth.** Push/fold equilibrium thresholds match published charts **(verify)**; a full-tree solve on a tiny No-Limit endgame matches vectorized CFR; re-solving on a small game matches the blueprint's value.

**Common mistakes.** Using too many bet sizes and running out of memory; treating a solver's range-level frequency as a per-hand rule; ignoring variance when comparing bots; conflating "winning a match" with "unexploitable".

**Deliverables.** No-Limit engine with configurable bet menus; push/fold solver; depth-limited re-solver on reduced games; match harness with variance reduction; precomputed flop library; widget W18.

**Hand-off.** Tabular methods cannot store this game; Module 08 learns regrets with networks.

---

### Module 08: Deep CFR

**Level:** Advanced · **Prereqs:** 02, 04 · **Essential for:** Researcher · **Effort:** about 2.5 person-weeks · **Game status:** approximate (neural approximation of regret-based solving); exact exploitability measurable only on small games

**Why it exists.** Tables of regrets cannot cover games with enormous state spaces. Function approximation generalizes across similar situations, replacing the table with a network that predicts regrets.

**Learning objectives.** The learner can describe the Deep CFR loop, explain why reservoir sampling is used, train an advantage network on a small game, and interpret the gap between network and tabular solutions.

**Concept map**

1. The problem: a table needs one row per information set; similar situations should share what they learn.
2. **Deep CFR overview:** run sampled traversals; store sampled *advantages* (instantaneous regrets) in per-player memories; train an advantage network on that memory; the network's output defines the next strategy via regret matching; also store strategy samples to train an average-strategy network.
3. **Reservoir sampling:** keep a uniform sample of an unbounded stream in fixed memory, so early iterations are not forgotten.
4. **Weighting by iteration** (linear weighting) and why training restarts from scratch each iteration in the original design.
5. **Network design for cards and bets:** embeddings for ranks and suits, permutation-aware handling of card sets, encoding bet history; input features and output heads.
6. **Single Deep CFR** (storing the advantage networks themselves and sampling among them at play time, avoiding a separate average-strategy network).
7. **Neighbors:** neural fictitious self-play, variance-reduced variants with baselines, and where each is stronger.
8. **Approximation error:** where it comes from (generalization, sampling noise, optimization), and how it appears in exploitability.
9. **Training stability and diagnostics:** buffer size, number of traversals, learning rate, catastrophic forgetting.
10. **Evaluating:** exact exploitability on small games; proxies and attack-based estimates on larger ones.

**Interactive features**

- **I08.1 Deep CFR Pipeline Diagram [P0].** *Look:* a loop with four boxes (traverse, memory, train, strategy) and arrows. *Controls:* step through one iteration; hover each box for the exact data flowing through it. *Aha:* the learner sees that the network is trained on sampled regrets, not on a game solution, and that the strategy used for the next traversal comes from the freshly trained network. *Data:* static with a small live example.
- **I08.2 Reservoir Sampling Visualizer [P0].** *Look:* a stream of colored dots (colored by iteration) and a fixed-size buffer. *Controls:* buffer size; compare reservoir vs first-in-first-out. *Aha:* with a reservoir, each iteration's samples are equally represented in the buffer; first-in-first-out discards everything old. *Data:* live.
- **I08.3 Advantage Network Probe [P0] (W2).** *Look:* choose an information set in Leduc; a bar chart compares the network's predicted advantages with the tabular regrets, and a heatmap lists approximation error across all information sets. *Controls:* iteration scrubber. *Aha:* the network is excellent on common situations and worse on rare ones, which is where exploitability hides. *Data:* precomputed.
- **I08.4 Network vs Tabular Race [P0] (W10 + W3).** *Look:* two lanes with exploitability curves. *Controls:* network size, buffer size, traversals per iteration. *Aha:* the network plateaus at a floor determined by approximation error; the table keeps improving. *Data:* precomputed grid of runs.
- **I08.5 Embedding Explorer [P1].** *Look:* a two-dimensional scatter of learned card or hand embeddings. *Aha:* hand-strength structure appears without being supplied, which shows what the network learned.
- **I08.6 Generalization Test [P1].** *Look:* a map of information sets split into "seen" and "held-out"; error colored by region. *Aha:* the network interpolates well between similar states and fails where states are unlike anything in training.
- **I08.7 Single vs Standard Deep CFR Toggle [P2].** *Look:* two strategies side by side on the same game. *Aha:* sampling among stored networks removes a source of average-policy error.

**Notebook labs.** Train Deep CFR on Leduc; compare to tabular; sweep buffer and network sizes; plot error by information set; implement the single-network variant.

**Exercises and projects.** Predict the effect of halving the buffer and test; add a held-out set of information sets and measure generalization; extend to a limit endgame.

**Ground truth.** Exploitability of the network strategy against the tabular solution on Leduc; statistical test that the reservoir keeps a uniform sample; deterministic reruns with fixed seeds.

**Common mistakes.** Treating a trained network as a stored game solution; judging progress by training loss instead of exploitability; using too small a buffer and forgetting early iterations; evaluating only on common situations.

**Deliverables.** A neural solver package (kept optional so the core library has no deep-learning dependency); reservoir buffers; networks and training loops for Leduc; precomputed run grids; tests.

**Hand-off.** A network that predicts regrets still cannot *plan*. To search with it we need a state that summarizes beliefs; Module 09.

---

### Module 09: Value Networks and Search (ReBeL-style)

**Level:** Advanced · **Prereqs:** 07, 08 · **Essential for:** Researcher · **Effort:** about 3.5 person-weeks · **Game status:** practical, with convergence guarantees in two-player zero-sum settings under assumptions

**Why it exists.** It unifies everything: re-solving, learned values and self-play into one recipe, and shows how the perfect-information "search plus value network" idea extends to hidden information.

**Learning objectives.** The learner can define a public belief state, explain why values over beliefs make imperfect-information games look like perfect-information ones, and describe the self-play loop that trains a value network from search.

**Concept map**

1. **The core difficulty:** in perfect-information games a state has a value; in poker, a situation's value depends on what *both players believe* about hidden cards.
2. **Public belief states (PBS):** the public information (board, pot, history) plus each player's range, which is a probability over private holdings.
3. **Values over PBS:** a vector (one counterfactual value per possible hand) as a function of the ranges; what properties it has and why it is a sensible learning target.
4. **Depth-limited solving:** solve a subgame to a fixed depth and use the value function at the leaves; why leaves need values for *each hand*.
5. **Self-play loop with search:** at each PBS, run a solver to get a strategy and values; use the values as training targets for the network; use the resulting strategy to move to the next PBS.
6. **The iteration-sampling trick:** pick a random iteration of the solver (rather than the last) to choose the next PBS, which keeps the training distribution consistent with the average strategy that carries the guarantee.
7. **Network input and output design:** range vectors, pot and stack features, board encoding; zero-sum-consistent outputs.
8. **Compare with the perfect-information recipe** (search plus value network from self-play) and note exactly where beliefs change the story.
9. **Test-time search:** why running the solver again during play improves on the trained policy.
10. **Limits:** leaf-value errors, residual action abstraction, compute cost, generalization across games.

**Interactive features**

- **I09.1 Public Belief State Explorer [P0] (W11).** *Look:* a mini-game board on top, and two range bar charts underneath (one per player). *Controls:* choose an action to take; the ranges re-weight by Bayes' rule using the current strategy. *Aha:* the same public situation with different ranges has different value; the learner sees that "the state" for planning is the pair of ranges.
- **I09.2 Value Function Shape [P1].** *Look:* a plot of a player's value as a function of one belief parameter in a two-hand toy game. *Controls:* drag the opponent's belief. *Aha:* the value is piecewise linear in the belief. The page then states the curvature properties and gives the proof sketch from the literature, with a brief exercise for the learner to verify them on the toy game.
- **I09.3 Depth-Limited Solve Animator [P0].** *Look:* a tree with a horizontal depth line; leaves below the line are replaced by "value network" boxes. *Controls:* depth slider; leaf-error slider. *Aha:* shallower search is much cheaper but inherits leaf errors; the plot shows exploitability vs compute for several depths. *Data:* precomputed.
- **I09.4 Self-Play Loop Diagram [P0].** *Look:* a cycle (sample a belief state → run the solver → record values → train the network → repeat). *Controls:* step through one cycle with real numbers on a mini game. *Aha:* the learner sees training data created by search, not by human play.
- **I09.5 Iteration-Sampling Demo [P1].** *Look:* a toy example with the solver's current strategy cycling while its average settles. *Controls:* choose "last iterate" or "random iterate" for moving between states. *Aha:* using the last iterate sends the self-play to states that are unrepresentative of the equilibrium; random-iterate sampling does not.
- **I09.6 Network Output Viewer [P0] (W5).** *Look:* a 13×13 grid of predicted per-hand values beside the solver's true values, with an error overlay. *Controls:* choose the situation. *Aha:* the network is accurate on typical states and shows structured errors elsewhere.
- **I09.7 Search vs No-Search Bars [P1] (W3).** *Look:* exploitability bars for blueprint only, blueprint plus search, and full solve on a toy game. *Aha:* search at play time buys a large improvement for modest extra compute.

**Notebook labs.** Build the public belief state for Kuhn and Leduc; train a value network on solved subgames; run depth-limited solving with network leaves; implement the self-play loop on a reduced game.

**Exercises and projects.** Show that two different range pairs on the same public state give different values; measure how leaf error propagates to exploitability; try last-iterate vs random-iterate sampling and report the difference.

**Ground truth.** The learned value network's error against solved subgames; zero-sum consistency (range-weighted values of both players sum to zero); the full self-play loop on a small game converging to low exploitability.

**Common mistakes.** Treating the value of a situation as independent of ranges; evaluating only the policy and not the value; using the last iterate for state transitions.

**Deliverables.** Public tree and belief-state code; vectorized solver reused from Module 04; value network training pipeline; self-play loop on small games.

**Hand-off.** Four hole cards and an extra rule explode the combinatorics; Module 10.

---

### Module 10: Pot-Limit Omaha

**Level:** Advanced · **Prereqs:** 05, 09 · **Essential for:** Competitor · **Effort:** about 2.5 person-weeks · **Game status:** open at scale; strong bots exist but there is no comparable "solved" milestone

**Why it exists.** It stress-tests every assumption of the Hold'em toolkit: far more hands, a different hand-making rule, tighter equities and pot-limit sizing. It is where combinatorial explosion becomes the main enemy.

**Learning objectives.** The learner can implement the exactly-two-hole-cards rule, estimate equity efficiently, understand why hands "run closer" and why abstraction is harder, and apply pot-limit sizing arithmetic.

**Concept map**

1. Rules: four hole cards, five community cards, the final hand must use *exactly two* hole cards and *exactly three* board cards; pot-limit betting.
2. **Combinatorics:** starting hands (270,725 combinations vs 1,326 in Hold'em; roughly sixteen thousand strategically distinct classes after suit symmetry **(verify)**); board and matchup counts.
3. **Evaluating hands correctly:** a naive method checks every combination of two hole cards and three board cards (sixty combinations per player); faster methods; common bugs (using the board alone, using three hole cards for a flush).
4. **Equity estimation:** exact enumeration where affordable, Monte Carlo elsewhere, sampling variance and confidence, and variance-reduced sampling.
5. **Why hands run closer:** equity distributions between random hands are much tighter than in Hold'em; consequences for betting and for how ranges behave.
6. **Hand features that matter:** nut potential, wraps and redraws, blockers, double-suited and connected structure, dominated draws.
7. **Range handling at scale:** vectors of hundreds of thousands of combinations; what that means for memory and for solver design.
8. **Pot-limit sizing arithmetic:** the maximum raise formula, how short stack-to-pot ratios arise quickly, and how this affects strategy.
9. **Abstraction for Omaha:** feature-based bucketing, why Hold'em strength percentiles are insufficient, and how to preserve nut potential.
10. Why strong heads-up Omaha play is hard to certify.

**Interactive features**

- **I10.1 Exactly-Two Rule Visualizer [P0].** *Look:* four hole cards and five board cards; all sixty candidate hands are listed, ranked, and the best is highlighted. *Controls:* choose cards; toggle "Hold'em rule" to see the difference. *Aha:* a visible flush that uses only one hole card is shown as *not* valid, and the learner sees why; the best legal hand differs from the intuitive one. *Predict prompt:* "Does this player have a flush?" *Data:* live.
- **I10.2 Equity Compression Chart [P0].** *Look:* two histograms of preflop equity against a random hand, one for Hold'em hands and one for Omaha hands. *Aha:* Omaha's narrow spread shows why it is a game of small edges and draws.
- **I10.3 Combinatorics Counter [P0] (W13).** *Look:* animated counters for starting hands, boards and matchups in each game. *Controls:* choose game. *Aha:* the numbers' growth makes a naive enumeration plan unreasonable and motivates sampling.
- **I10.4 Hand Feature Analyzer [P0] (W6).** *Look:* a hand and board; badges for nut-flush draw, wrap size, blockers and redraws; a "nut potential" gauge. *Controls:* swap cards. *Aha:* two hands with similar equity can have very different structures.
- **I10.5 Equity Estimator Lab [P1].** *Look:* a sample-size slider and a confidence interval that shrinks. *Controls:* sampling method (plain, stratified, antithetic). *Aha:* variance reduction gives the same accuracy with far fewer samples.
- **I10.6 Pot-Limit Bet Calculator [P0].** *Look:* a pot graphic that grows stepwise. *Controls:* current pot and the bet faced. *Aha:* the maximum raise is computed step by step on screen, so the formula stops being mysterious.
- **I10.7 Omaha Hand-Type Filter [P1].** *Look:* a panel of filters (pairs, connectedness, suitedness, double-suited). *Aha:* a structured way to describe ranges when a 13×13 grid is impossible, with combo counts per category.
- **I10.8 Abstraction by Features [P2] (W8).** *Look:* sample buckets and their member hands. *Aha:* what a good Omaha bucket looks like.

**Notebook labs.** Build and test an Omaha evaluator; compare enumeration with Monte Carlo; compute equities for classic hand types; implement variance reduction.

**Exercises and projects.** Verify equities against a reference calculator; prove the number of candidate hands is sixty; measure how many samples are needed for a given accuracy.

**Ground truth.** The evaluator agrees with brute force over a very large random sample; exact enumeration and Monte Carlo agree within error bars; equities for well-known matchups agree with published tables **(verify)**.

**Common mistakes.** Letting a player use the board alone; allowing three hole cards; reading Hold'em strength percentiles as meaningful in Omaha; trusting a small-sample equity estimate.

**Deliverables.** Omaha evaluator and equity engine; range-vs-range tables; pot-limit betting logic; feature-based bucketing prototype; widget W6 extensions.

**Hand-off.** Everything so far assumed two players in a zero-sum game; Module 11 removes that assumption.

---

### Module 11: Multiplayer No-Limit Hold'em

**Level:** Research · **Prereqs:** 07, 09 · **Essential for:** Researcher, Competitor · **Effort:** about 3 person-weeks · **Game status:** practically strong (a six-player bot beat elite humans) but with no equilibrium guarantee

**Why it exists.** The mathematics that made two-player poker tractable fails with three or more players, and this module shows exactly how.

**Learning objectives.** The learner can explain why Nash equilibrium loses its meaning with three or more players, describe how a practical multiplayer bot is built, and evaluate bots without exploitability.

**Concept map**

1. **What breaks:** equilibria are not unique and are not interchangeable; a player following their part of one equilibrium while others follow another can lose; computing an equilibrium is computationally hard in general, even in three-player zero-sum settings.
2. **Collusion and kingmaking:** structure where two players' joint behavior hurts the third even without communication.
3. **What regret minimization still guarantees:** in self-play it converges to a *coarse correlated equilibrium*, a weaker concept than Nash; what that does and does not mean.
4. **Practical recipe:** a blueprint from sampled self-play, abstraction, depth-limited real-time search with several continuation strategies for opponents, and why that is a pragmatic answer.
5. **Evaluation without exploitability:** head-to-head against populations, ratings systems with uncertainty, duplicate formats, variance reduction, and non-transitivity (bot A beats B, B beats C, C beats A).
6. **Tournament vs cash-game objectives:** chips are not money; **ICM** converts chip counts to prize equity and changes correct decisions.
7. **Positional dynamics in six-player play** and how stack sizes change strategy.
8. **Test beds:** three-player Kuhn and three-player Leduc, small enough to study equilibrium multiplicity directly.
9. Refinements (sequential equilibrium, trembling-hand ideas) as a brief sidebar.

**Interactive features**

- **I11.1 Three-Player Kuhn Sandbox [P0] (W1 + W3).** *Look:* a three-player tree and a panel listing many solver runs. *Controls:* choose the number of runs and random seeds; run. *Aha:* a scatter of final payoffs across runs shows that different runs converge to *different* strategy profiles with different payoffs. *Predict prompt:* "Will all 50 runs land on the same strategy?" *Data:* precomputed runs.
- **I11.2 Equilibrium Swap Test [P0].** *Look:* a payoff table with three seat labels. *Controls:* pick seat strategies from different runs. *Aha:* mixing seats from different equilibria produces losses, proving that equilibria are not interchangeable.
- **I11.3 Kingmaker Illustration [P1] (W17).** *Look:* a triangle whose corners are the three players' payoffs, with points for different joint strategies. *Aha:* a joint move can transfer value from one player to another without either of the two moving players being hurt.
- **I11.4 ICM Calculator [P0].** *Look:* a stack-distribution bar chart and a prize ladder. *Controls:* stacks, payouts, an action (such as a shove) to evaluate. *Aha:* chip-expected-value and dollar-expected-value disagree, and the calculator shows when a chip-profitable call is prize-unprofitable.
- **I11.5 League Evaluator [P0] (W18).** *Look:* a round-robin of bots with a ratings chart (with uncertainty bars) and a matchup matrix heatmap. *Controls:* choose which bots enter; number of hands. *Aha:* the heatmap reveals non-transitive cycles that a single rating hides.
- **I11.6 Real-Time Search Walkthrough [P1].** *Look:* an animation of a decision with four opponent continuation options (normal, fold-leaning, call-leaning, raise-leaning). *Aha:* the agent picks a strategy that holds up against all four, a heuristic stand-in for an unknown opponent.
- **I11.7 Duplicate Variance Reduction [P1].** *Look:* two result clouds, with and without duplicate seating. *Aha:* duplicate play removes card luck and leaves skill.
- **I11.8 CCE vs Nash Gap [P2].** *Look:* a small game showing a coarse correlated equilibrium that is not a Nash equilibrium.

**Notebook labs.** Solve three-player Kuhn from many starting points; compute the swap table; build a rating system and recover known strengths of synthetic bots; implement ICM.

**Exercises and projects.** Find a three-player game where one equilibrium is clearly better for one seat; construct a non-transitive trio of bots; build a league and rank them.

**Ground truth.** Multiple distinct equilibria found in three-player Kuhn; a rating system recovers the strengths of synthetic bots with known skill; ICM values for small prize structures match hand calculations.

**Common mistakes.** Quoting exploitability for a multiplayer bot as though it meant something; treating a stable self-play result as equilibrium; assuming ratings are transitive.

**Deliverables.** N-player game interface; three-player Kuhn and Leduc; league harness with ratings; ICM tools; widget W18 extensions.

**Hand-off.** A fixed strategy is hard to beat but does not exploit weakness; Module 12.

---

### Module 12: Opponent Modelling and Exploitation

**Level:** Advanced · **Prereqs:** 11 (and 01 to 03) · **Essential for:** Competitor · **Effort:** about 2 person-weeks · **Game status:** open (balancing profit against safety has no single answer)

**Why it exists.** An equilibrium strategy never loses in expectation in a two-player zero-sum game, but it also never punishes opponents' mistakes beyond what equilibrium forces. Real competition rewards adaptation, as long as adaptation does not make you exploitable.

**Learning objectives.** The learner can build opponent models from observed actions, derive a best response to a model, apply safe exploitation, and plot the profit-vs-exploitability frontier.

**Concept map**

1. **The tradeoff:** exploit weaknesses vs remain unexploitable.
2. **Observation and statistics:** what can actually be inferred from a handful of hands; frequency counters; showdown information vs betting information.
3. **Bayesian opponent models:** priors over opponent behavior, updating with counts, prior strength, hierarchical priors from a population.
4. **Best response to a model** and its danger when the model is wrong.
5. **Safe exploitation:** restricted Nash response (a parameter controls how far you may deviate), safety constraints that guarantee a minimum payoff, "gifts" the opponent has already given.
6. **Sampling-based adaptation:** drawing an opponent model from the posterior and best-responding (Thompson-style).
7. **Nonstationarity:** opponents who change; detecting a change point; forgetting.
8. **Counter-exploitation:** an exploiter being exploited by a savvy opponent; cycles.
9. **Evaluation:** profit against a menu of exploitable opponents *and* worst-case exploitability; the Pareto frontier of the two.
10. **Information leakage:** exploiting reveals your reads; meta-game considerations.

**Interactive features**

- **I12.1 Opponent Stats Dashboard [P0].** *Look:* counters (how often the opponent bets with each hand class, folds to a raise) that build up as hands are observed, each with a confidence interval. *Controls:* number of hands observed; the hidden opponent type. *Aha:* with few hands, the confidence intervals are enormous; a "hands needed" slider shows how long exploitation really takes.
- **I12.2 Bayesian Belief Lab [P0].** *Look:* a posterior distribution over the opponent's bluff frequency in Kuhn, updated after each observed showdown. *Controls:* prior strength; observe a bluff or a value bet; choose the decision rule (best response to the average, to a sample, or to the worst case). *Aha:* a strong prior resists noise; a weak prior chases it.
- **I12.3 Exploitation Frontier [P0] (W3 variant).** *Look:* a plot with profit against a fixed exploitable opponent on one axis and exploitability on the other. *Controls:* a trust parameter. *Aha:* a smooth curve from "play equilibrium" to "full best response"; the naive best response sits far out on the exploitability axis, while the restricted response gets most of the profit for little risk. *Data:* precomputed on Kuhn and Leduc.
- **I12.4 Opponent Zoo Arena [P0] (W18).** *Look:* lines of cumulative profit against a menu of scripted opponents (maniac, nit, calling station, tight-aggressive, near-equilibrium). *Controls:* choose the adaptive agent and opponent. *Aha:* the adaptive agent crushes extreme opponents, ties with the near-equilibrium one, and the profit curves show how fast each adaptation pays off.
- **I12.5 Change-Point Demo [P1].** *Look:* a timeline in which the opponent changes style at a point the learner chooses. *Controls:* sensitivity of the detector. *Aha:* detection delay trades against false alarms; both can be seen at once.
- **I12.6 Counter-Exploit Duel [P1] (W17).** *Look:* a triangle with two trajectories of two adapting bots. *Aha:* adaptive bots can cycle just as in rock-paper-scissors, which is the same lesson as Module 02 in a new setting.
- **I12.7 Safe vs Unsafe Exploitation Playground [P1].** *Look:* a game with a counter showing guaranteed minimum payoff. *Aha:* the safe version retains a floor even if the model is entirely wrong.

**Notebook labs.** Implement a Bayesian model for Kuhn; compute best responses to posterior means and samples; trace the exploitation frontier; run the arena.

**Exercises and projects.** Show that a best response to the posterior mean can be exploited; find the trust level where profit is 80 percent of the maximum at 10 percent of the exploitability; build an agent that adapts to a switching opponent.

**Ground truth.** Restricted Nash response reproduces known frontier behavior on Kuhn; posterior updates match closed-form conjugate calculations; profit estimates have honest confidence intervals.

**Common mistakes.** Over-trusting a model built from a small number of hands; forgetting that the opponent can adapt to you; measuring only profit and never exploitability.

**Deliverables.** Opponent-model library; safe exploitation methods; arena of scripted opponents; frontier plots.

**Hand-off.** Real competitions change the rules; Module 13 asks the bot to reason about mechanics, not memorize a policy.

---

### Module 13: Custom Variants (Sneak Peek Hold'em and Beyond)

**Level:** Research · **Prereqs:** all earlier · **Essential for:** Competitor · **Effort:** about 3 person-weeks · **Game status:** defined per variant; typically open, but small versions can be solved exactly to calibrate

**Why it exists.** The final skill is to take an unfamiliar rule set, express it as a game, and build a solver and bot for it. Reusing a standard Hold'em policy will fail because the *information structure* has changed.

**Important note on rules.** This plan treats "Sneak Peek Hold'em" generically. The exact rules (who may peek, what is revealed, how access is decided, what it costs, and when it happens) must be taken from the official specification of the competition or game being targeted. The Rules Builder below is designed around the dimensions in the table in concept item 4, so any official ruleset can be entered.

**Learning objectives.** The learner can model any variant as an extensive-form game, derive its information sets automatically, reason about information as a purchasable good, adapt abstraction and solving, and prove that their bot is not just a repurposed Hold'em policy.

**Concept map**

1. **Game description essentials:** players, chance events, legal actions, transitions, payoffs, and, most importantly, *observations*: what each player sees after every event.
2. **Information sets from observation histories:** automatic derivation, perfect-recall checks, and common modeling mistakes (leaking information by accident or hiding information that is public).
3. **Mechanism families:** new reveal schedules, extra cards, wildcards, bounties, antes and straddles, short decks, running a board twice, and auctions for information or position.
4. **Dimensions of a peek or auction mechanic (to be filled from the official rules):**

| Dimension | Options to specify |
|---|---|
| Who can act | one player, both, the winner of an auction |
| What is revealed | a board card, an opponent card, partial information (such as a rank or color) |
| Visibility | revealed only to the buyer, or to everyone |
| Price | fixed fee, bid paid by winner, bid paid by both |
| Auction type | first-price, second-price, all-pay, sealed or sequential |
| Timing | before betting, between streets, at showdown |
| Ties and limits | tie-break rule, bid bounds, stack limits |

5. **Auction theory essentials:** first-price vs second-price bidding, why second-price truthful bidding is optimal in the simplest setting, why that argument weakens when the object bought changes the buyer's later play and when bids themselves leak information.
6. **Value of information:** how to compute what a peek is worth in expectation, and why that value depends on the hand, the ranges and the betting that follows.
7. **Signaling through bids:** a bid reveals strength; equilibrium bidding mixes to avoid being read.
8. **Adapting the solver stack:** discretizing the bid space (an action abstraction for auctions), redesigning card and information abstractions, reusing the vectorized solver, deciding the right solver (full CFR on a tiny version, sampling on larger ones).
9. **Why transfer fails:** run a strong Hold'em policy in the variant and measure exploitability.
10. **Testing a new game:** invariants (chips conserved, legal actions consistent, information sets well-formed), solve a miniature version exactly, compare with analytic solutions of toy auctions where available.
11. **A variant card:** a standard one-page spec for any game (rules, information structure, size estimate, recommended solver).

**Interactive features**

- **I13.1 Rules Builder [P0] (W12).** *Look:* a form with grouped sections (deck, hole cards, streets, betting, peek and auction mechanics) and a live "rule card" on the right. *Controls:* choose options from menus; load presets (standard Hold'em, short deck, a peek variant). *Aha:* as options change, a tree-size estimate and an "information structure summary" update live, and the page warns if the configuration breaks perfect recall or becomes too large to solve. *Data:* analytic estimates.
- **I13.2 Information Timeline [P0] (W14).** *Look:* a swimlane per player with the sequence of events along the bottom; each event is colored by who can see it. *Controls:* step through a hand; hover to see which situations a player cannot tell apart. *Aha:* an auction win that reveals a card to one player creates a *new* information partition, and the learner sees the information set boundaries move.
- **I13.3 Auction Mechanic Lab [P0].** *Look:* two bidders with private values, a bid axis, and a plot of equilibrium bid against value. *Controls:* first-price vs second-price; number of bidders; whether the value is private or tied to a hand. *Aha:* in a simple private-value auction, the first-price bid shades below value and the second-price bid equals value; when value depends on a poker hand, bids start to reveal the hand. *Data:* analytic curves plus a small solved toy variant.
- **I13.4 Value-of-Information Calculator [P0] (W6).** *Look:* a hand, a board situation and a peek option. *Controls:* choose the hand class and what the peek reveals. *Aha:* a heatmap of "peek worth X big blinds" across hand classes shows that peeking is worth the most for medium-strength, flexible hands, not necessarily the weakest or strongest. *Data:* precomputed on a reduced game.
- **I13.5 Transfer Failure Demo [P0] (W3).** *Look:* two bars for exploitability: a Hold'em policy dropped into the variant, and a solver trained on the variant. *Aha:* the standard policy is exploitable by a counter-strategy that uses the new mechanic.
- **I13.6 Variant Playground [P1] (W9).** *Look:* a table for a mini-variant with a small deck against a solved bot. *Aha:* the learner feels the mechanic in play before reading about it.
- **I13.7 Mechanism Sandbox [P2].** *Look:* quick simulations of tie-breaking, sniping and reserve prices. *Aha:* small rule details create large strategic differences.
- **I13.8 Variant Card Generator [P1].** *Look:* a one-click export of the rule card, size estimate and recommended solver as a markdown file.

**Notebook labs.** Implement a variant through the framework; auto-derive information sets; solve a miniature version exactly; run the transfer test; build a bid-space abstraction.

**Exercises and projects.** Implement two variants in the framework; prove a toy auction's equilibrium and check the solver against it; write the variant card for your target game.

**Ground truth.** Invariants hold over millions of random hands; a miniature variant solved exactly matches hand-derived or analytic results; the framework reproduces standard Hold'em exactly when the variant switches are off.

**Common mistakes.** Letting a revealed card remain hidden in the player's own view (or vice versa); an action abstraction on bids that cannot represent the equilibrium bid; assuming auction results from textbooks apply when the item changes the later game.

**Deliverables.** A variant framework (rules as configuration); at least one peek-and-auction variant implemented; transfer-test harness; variant card template; widget W12 and W14.

**Hand-off.** What can the field actually do, and what remains out of reach? Module 14.

---

### Module 14: Case Studies and Open Problems

**Level:** Research · **Prereqs:** all earlier · **Essential for:** Researcher · **Effort:** about 1.5 person-weeks · **Game status:** a map of the whole landscape

**Why it exists.** It consolidates the whole repo into a coherent picture of how the field got here, what each landmark system contributed, and where the open questions are.

**Learning objectives.** The learner can summarize each landmark system's key idea, place any game on the "solved" ladder, choose a technique for a new game, and propose a feasible research question.

**Concept map**

1. **The three levels of "solved":** exactly or provably near-exactly solved; practically strong without guarantees; open. Where every game in this repo sits.
2. **Landmark case studies,** each with a one-page anatomy (problem, key idea, algorithm sketch, results, limitations, which module teaches the ideas): the heads-up limit milestone built on CFR+; the DeepStack approach; the Libratus approach; the six-player Pluribus approach; ReBeL; a general-game agent that handles both perfect and imperfect information.
3. **Compute and scale:** what each system needed in hardware and time, and what that implies for what is reproducible.
4. **Theory frontier:** last-iterate convergence, optimistic and predictive regret methods, rates faster than one over the square root of time for structured problems, regularized equilibria.
5. **Evaluation frontier:** assessing strength without exploitability; non-transitivity; human comparison methodology.
6. **Generalization:** one agent for many games; transferring across rule changes.
7. **Multiplayer and cooperative-competitive settings:** open guarantees; negotiation games as a related frontier.
8. **Practical and ethical considerations:** use of bots in real-money environments is generally prohibited by platform rules and is a matter of fairness; responsible research practice; sharing results.
9. **Choosing a technique:** a decision guide from game properties (players, sum structure, size, information) to a pipeline and the modules that teach it.
10. **Capstone options and open problems list.**

**Interactive features**

- **I14.1 Interactive Timeline [P0].** *Look:* a horizontal scrolling timeline of milestones, each a card with game, method, scale and a link to the teaching module. *Controls:* filter by game or by algorithm family. *Aha:* method families visibly build on each other.
- **I14.2 Game Landscape Map [P0].** *Look:* a scatter with game size (log scale) on one axis and year or difficulty on the other, bubbles colored by solved level. *Controls:* click a bubble to read a summary; toggle to show the games implemented in this repo. *Aha:* the repo's games sit on the same map as the landmark systems.
- **I14.3 "Which Technique Would You Use?" [P0] (W15).** *Look:* a short questionnaire (number of players, zero-sum or not, game size, information type) leading to a recommended pipeline. *Controls:* answer; see which modules to review. *Aha:* the learner applies the whole curriculum to unseen games, with feedback.
- **I14.4 Paper Anatomy Cards [P1] (W15).** *Look:* flip cards with a landmark paper on the front and its anatomy on the back.
- **I14.5 Open Problems Board [P1].** *Look:* a list with difficulty tags, prerequisite modules and suggested experiments using this repo. *Controls:* filter; link out to repository issues for discussion.
- **I14.6 Compute Comparison [P2].** *Look:* a log-scale bar chart of approximate compute used by landmark systems against a laptop. All figures are clearly labeled approximate and cited.

**Notebook labs.** A reproduction mini-project at toy scale of one landmark idea (chosen by the learner).

**Exercises and projects.** Write a one-page analysis of a landmark system's strengths and limitations; propose and run a small experiment on an open problem; classify five additional games on the "solved" ladder with justification.

**Ground truth.** Not applicable in the usual sense; the capstone is assessed with a rubric (correctness, clarity, honesty about limitations).

**Common mistakes.** Overstating what "beat professionals" implies about exploitability; treating a result in one game as proof for another.

**Deliverables.** A curated reading guide, the timeline and landscape data, the decision guide, the capstone rubric.

**Hand-off.** None: this is the finish line, and the start of the learner's own research.

---

## 6. Cross-module threads

These run through the whole curriculum and are designed once, then reused.

### 6.1 The exploitability scoreboard

Every solver, in every module, is judged on one chart: **exploitability against effort** (iterations, time or samples). The chart widget (W3) is identical everywhere, with the same axes, the same dotted reference line and the same way of marking checkpoints. From Module 07 onward, where exact exploitability cannot be computed, the same slot is filled by the best available proxy (local best response, match results with variance reduction), and the page says explicitly which proxy is in use and what it can and cannot prove.

### 6.2 The Bot Arena

A standard bot interface, defined in Module 05 and extended through Module 13, lets any bot the learner builds play any other. The arena supports: head-to-head matches with variance-reduced estimates, round-robin leagues with ratings and uncertainty, and a "play against my bot" table. A later, optional addition is a community leaderboard fed by pull requests, with automated matches run in continuous integration. This gives the whole repo a goal beyond reading: *build a bot and see how it ranks.*

### 6.3 Notation and glossary

The notation page grows with the curriculum, and every new symbol is added at the moment it is introduced and nowhere else. The glossary supplies hover cards (W16) so a term used in Module 09 can be recalled without scrolling back to Module 01. A rule for contributors: if two modules use different symbols for the same thing, one of them is a bug.

### 6.4 Progress tracking and learning aids

- A local progress tracker (stored in the browser) ticks off checkpoints and quiz completions; nothing leaves the learner's device.
- A "where am I" map on every page shows the learner's position on the ladder and the prerequisites for the next step.
- A "stuck?" panel on every module lists the likeliest prerequisites to revisit.

### 6.5 Recurring spots

A few specific situations (the bluffing spot in Kuhn, a river decision with a blocker, a flop continuation bet) reappear in several modules so that learners can see the *same* decision analyzed with progressively stronger tools. The page for each module links back to earlier appearances.

### 6.6 The verified-numbers table

A single page lists every quantitative claim in the curriculum, the source, the date it was verified and the script (if any) that reproduces it. No number appears in prose that is not on this page. Appendix C seeds the list.

### 6.7 "Break it" labs

Every module ends with a lab whose goal is to make the module's method fail on purpose (a bad abstraction, an unsafe re-solve, an overconfident opponent model) and see the scoreboard react. These are the most memorable parts of the curriculum, and they are designed to feed the next module's motivation.

---

## 7. Library and data architecture

### 7.1 Package map and what each module adds

| Module | `games/` | `solvers/` | `eval/` | other |
|---|---|---|---|---|
| 00 | | matrix-game solvers (indifference, linear programming) | EV helpers | combinatorics utilities |
| 01 | Kuhn | vanilla CFR | exact best response, exploitability | |
| 02 | | regret matching, regret matching plus, Hedge | matrix exploitability | |
| 03 | Leduc | CFR plus, alternating, discounted variants | cross-check harness | |
| 04 | expanded Leduc, river poker, analytic toy games | MCCFR family, vectorized CFR | sampled exploitability estimator | seven-card evaluator (river) |
| 05 | limit Hold'em | bucketed MCCFR | equity vs range | five- and seven-card evaluators; bot interface |
| 06 | | safe and nested subgame solving | abstraction loss measures | `abstraction/` (bucketing, translation) |
| 07 | no-limit Hold'em, push/fold | re-solver (reduced games) | local best response, variance-reduced match harness | |
| 08 | | Deep CFR family (optional extra) | | `deep/` |
| 09 | | PBS tools, depth-limited solver, self-play loop | value-network error | `pbs/` |
| 10 | Omaha | | Omaha evaluator, range tables | |
| 11 | N-player Kuhn and Leduc | | rating systems, ICM | `league/` |
| 12 | | safe exploitation, opponent models | frontier tools | |
| 13 | variant framework (rules as configuration), peek and auction mechanics | | transfer-test harness | variant card template |
| 14 | | | | reading guide data, landscape data |

### 7.2 Interfaces that must change over time (plan for them now)

- **Game interface (today):** state objects with chance outcomes, legal actions and information-set keys. Good through Module 03.
- **Vectorized interface (Module 04):** a second, range-based view of a game for solving all private hands at once. Keep the two views consistent by testing that they agree on small games.
- **Observation-based interface (Module 13):** information sets derived automatically from each player's observation history. Retrofit earlier games to it and check results are unchanged.
- **N-player interface (Module 11):** payoffs and players beyond two. Design the base class with this in mind so nothing needs rewriting.
- **Bot interface (Module 05):** the same contract for hand-written, solver-driven and neural bots.

### 7.3 Dependency policy

The core library depends on nothing outside the standard library, so the early modules install instantly. Optional extras: numerical packages for the vectorized and evaluation work, a deep-learning framework for Modules 08 and 09, plotting and notebook tools for labs, documentation tools for the site. Performance work (compiled evaluators and solvers) arrives behind the same Python interfaces so tutorials do not change.

### 7.4 Data pipeline

A "demo data" job in continuous integration produces every precomputed artifact with a manifest (commit, seeds, iterations, time). Large files are compressed and versioned; if repository size becomes a problem, they move to release assets and are fetched on demand with checksum verification. Each demo declares which data files it needs, so unused data is never downloaded.

### 7.5 Repository layout (target)

- `docs/` for pages, notation, glossary, plan, verified-numbers table and the widget code
- `modules/NN_name/` for notebooks, exercises and solutions
- `pokerbot/` for the library
- `data/` or release assets for precomputed artifacts and manifests
- `tests/` and `benchmarks/`
- `arena/` for the bot interface, tournament runner and (later) leaderboard
- `papers/` for reading lists and one-page summaries

---

## 8. Verification and quality plan

### 8.1 Ground-truth anchors

| Module | What the work is checked against |
|---|---|
| 00 | hand-worked EV and pot-odds examples; indifference solution = linear-programming solution |
| 01 | game value of minus one eighteenth; the equilibrium family; near-zero exploitability after CFR |
| 02 | regret under the proven bound; exploitability times the square root of time roughly constant; known biased-game equilibrium |
| 03 | a reference implementation's exploitability and game value; all CFR variants agree on the final strategy |
| 04 | sampled solvers agree with full CFR on Leduc; analytic toy-game answers; statistical unbiasedness |
| 05 | seven-card category counts; famous matchup equities; evaluator vs a reference library on a large random sample; chip conservation |
| 06 | lossless abstraction leaves the value unchanged; earth mover's distance on simple cases; safe re-solving no worse than blueprint on a test game |
| 07 | published push/fold charts; reduced no-limit endgame solved fully vs vectorized CFR |
| 08 | network strategy exploitability vs tabular on Leduc; reservoir uniformity test |
| 09 | value-network error vs solved subgames; zero-sum consistency; self-play loop converging on a small game |
| 10 | evaluator vs brute force; exact enumeration vs Monte Carlo; published equity tables |
| 11 | multiple distinct equilibria found in three-player Kuhn; rating recovery of synthetic bots; ICM hand calculations |
| 12 | restricted-response frontier on Kuhn; conjugate-update closed forms |
| 13 | invariants over millions of hands; miniature variant solved exactly; framework reproduces standard Hold'em when variants are off |
| 14 | rubric-based capstone review |

### 8.2 Definition of done for a module

A module is "done" only when all of these hold:

1. All [P0] interactives work on desktop and mobile, in light and dark themes, with keyboard operation and chart tables.
2. The notebook runs top to bottom on a clean environment.
3. Every quantitative claim is on the verified-numbers page.
4. Library code has tests that compare against the ground truth listed above, and they pass in continuous integration.
5. The page follows the nine-section template, including a misconception box, a "Break it" lab and a checkpoint list.
6. Another person has completed the module and reported where they got stuck; those points are fixed.
7. Cross-links to prerequisite and next modules are in place and the hover glossary covers every new term.

### 8.3 Continuous integration jobs

- Unit and property tests on two Python versions.
- Notebook execution tests.
- Docs build with link checking.
- Demo data job with manifest validation.
- Accessibility checks on the built site (contrast and basic structure).
- A weekly slower job running the longer convergence and regression benchmarks.

### 8.4 Review practice

Each module gets a technical review (correctness of math and code), a pedagogical review (a learner at the target level tries it cold) and an editorial review (notation, terminology, claims on the verified page). Two reviewers if possible; if working alone, a delay of a few days between writing and review.

---

## 9. Delivery plan

### 9.1 Effort estimates (rough, in focused person-weeks)

| Item | Weeks |
|---|---|
| Shared infrastructure: design system, widget framework, data pipeline, site integration | 4 |
| Module 00 | 1.5 |
| Module 01 (interactives only) | 1 |
| Module 02 (extensions) | 1 |
| Module 03 | 2 |
| Module 04 | 2.5 |
| Module 05 | 3 |
| Module 06 | 3 |
| Module 07 | 4 |
| Module 08 | 2.5 |
| Module 09 | 3.5 |
| Module 10 | 2.5 |
| Module 11 | 3 |
| Module 12 | 2 |
| Module 13 | 3 |
| Module 14 | 1.5 |
| **Total (all P0 and P1)** | **about 40** |

Building only the [P0] interactives roughly cuts this by a third. These estimates are rough, assume focused work and include review but not unforeseen research; part-time or solo pace multiplies the calendar time.

### 9.2 Phases and milestones

| Phase | Scope | Milestone (what "done" looks like) |
|---|---|---|
| **0. Skeleton** | repo, site, CI, template, first modules' text and code | done |
| **1. Prove the template** | shared design system and the first widgets (W1 to W4, W15, W16, W17); finish Module 00; add interactives to Modules 01 and 02 | a stranger completes 00 to 02 in the browser and the notebook with no help |
| **2. Small solvable games** | Modules 03 and 04; W5, W6, W9, W10, W11 | learner can solve Leduc and a river spot and see sampling in action |
| **3. Real poker** | Modules 05, 06, 07; W7, W8, W13, W18; arena v1 | learner can build a bucketed limit solver and a no-limit re-solving agent and play it |
| **4. Neural and frontier** | Modules 08, 09, 10, 11, 12 | neural solver on Leduc; belief-state search on a small game; league evaluator |
| **5. Capstone** | Modules 13, 14; W12, W14; arena leaderboard; polish | a bot for a custom variant, validated by the transfer test, and a reading guide |

### 9.3 Minimum viable path

If time is short, build in this order and stop whenever needed; each stopping point is a complete, useful repo:

1. Modules 00 to 03 (a complete beginner-to-solver course)
2. Module 04 (sampling) and the river spot viewer
3. Modules 05 and 07 (real poker and no-limit push/fold, plus the flop explorer)
4. Module 13 (variants), which can be started after Module 05 because its framework needs only the earlier basics
5. Everything else

### 9.4 Order of widget construction

W3 and W1 first (used everywhere), then W2, W4, W15, W16, W17, then W5 and W6 (the range grid and equity widgets unlock Modules 04 to 07), then W9 and W10, then W7, W8, W13 and W18, and finally W12 and W14.

### 9.5 Release cadence

- A tagged release at the end of each phase.
- A short changelog written for learners ("what you can now do").
- A public roadmap page showing module status with the same status values used today.

---

## 10. Risks and mitigations

| Risk | Why it matters | Mitigation |
|---|---|---|
| **Scope explosion** | 15 modules with many interactives is a large project | build the vertical slice first; use the P0, P1, P2 tags strictly; ship at each phase boundary |
| **Wrong numbers published** | the audience will trust them | verified-numbers page; no uncited quantity in prose; reproduction scripts |
| **Interactives become a maintenance burden** | many small web apps can rot | one widget framework, shared code, data from a manifest, tests that render each widget |
| **Heavy compute in the browser** | slow or crashing demos | default to precomputed data; live computation only for tiny games; run heavy solves in workers |
| **Repository size** | strategy files can be large | compression and quantization; release assets; lazy loading |
| **Inconsistent notation** | confuses learners | single notation page; review rule: new symbols only when first introduced |
| **Math too hard for beginners** | loses the audience | always an example before a formula; optional "Prove" toggles; sidebars for proofs |
| **Dependency on one library for ground truth** | tests could share a bug | cross-check with at least one independent source (analytic or second implementation) |
| **Deep-learning modules are fragile** | training is non-deterministic and slow | fixed seeds; small games; precomputed result grids; clearly separated optional extras |
| **Module 13 rules unknown or changing** | the variant may be redefined | parametrized Rules Builder; keep the official specification as the source of truth; version the variant card |
| **Real-money bot misuse** | ethical and policy concerns | explicit statement in Module 14; the repo teaches methods and offline play |

---

## 11. Decisions still needed

1. **Notebook platform:** Marimo (reactive, clean diffs) or Jupyter (ubiquitous). A reasonable default is to author in Marimo and export, if it works well with the docs site.
2. **Where live computation runs:** a Python runtime in the browser for small games, compiled WebAssembly for push/fold and similar, or precomputed data only. The plan assumes precomputed by default, with push/fold as the first candidate for live solving.
3. **Widget implementation style:** plain JavaScript and SVG per widget vs a small shared component library. The plan assumes a small shared library built in Phase 1.
4. **Deep-learning framework** for Modules 08 and 09.
5. **Hosting of large data:** repository vs release assets.
6. **Target ruleset for Module 13:** the official specification of the variant being targeted, once available.
7. **Compute budget** for precomputing flop libraries, abstraction sweeps and run grids, and who pays for it.
8. **Community model:** open contributions from the start, or private until Phase 3.
9. **Licensing of data and the written content** (the plan assumes MIT for code and CC BY for prose).
10. **Which persona to optimize for first** if the curriculum has to be cut.

---

## Appendix A: Concept dependency map

Read "A → B" as "B needs A".

- Probability and EV (00) → Bayes and beliefs (00) → ranges (03, 04) → belief states (09)
- Matrix games and Nash (00) → regret theory (02) → CFR (01, 02) → CFR variants (03) → sampling (04) → Deep CFR (08)
- Information sets (00, 01) → imperfect recall abstraction (06) → observation-based game modelling (13)
- Best response and exploitability (01) → local best response (07) → ratings for multiplayer (11) → frontier (12)
- Hand evaluation (04, 05) → equity vs range (05) → bucketing (06) → Omaha evaluation (10)
- Bucketing (06) → subgame solving (06) → continual re-solving (07) → value networks and search (09)
- Auction basics (13) → value of information (13) → signaling via bids (13)
- Everything → case studies and open problems (14)

---

## Appendix B: Reading list by module

Bibliographic details must be confirmed before publication. This list is for orientation only.

| Module | Suggested reading |
|---|---|
| 00 | Chen and Ankenman, *The Mathematics of Poker*; Shoham and Leyton-Brown, *Multiagent Systems* (game theory chapters) |
| 01 | Kuhn (1950), *A Simplified Two-Person Poker*; Neller and Lanctot (2013), *An Introduction to Counterfactual Regret Minimization* |
| 02 | Hart and Mas-Colell (2000); Freund and Schapire (1999); Cesa-Bianchi and Lugosi (2006), *Prediction, Learning, and Games*; Zinkevich et al. (2007), *Regret Minimization in Games with Incomplete Information* |
| 03 | Southey et al. (2005), *Bayes' Bluff* (origin of Leduc); Tammelin (2014), *CFR+*; Brown and Sandholm (2019), *Solving Imperfect-Information Games via Discounted Regret Minimization*; Lanctot et al. (2019), *OpenSpiel* |
| 04 | Lanctot et al. (2009), *Monte Carlo Sampling for Regret Minimization in Extensive Games*; Schmid et al. (2019), *Variance Reduction in Monte Carlo CFR*; Chen and Ankenman (the closed-form toy games) |
| 05 | Bowling et al. (2015), *Heads-up Limit Hold'em Poker Is Solved*; Johanson (2013), *Measuring the Size of Large No-Limit Poker Games* |
| 06 | Gilpin and Sandholm (2007), *Lossless Abstraction*; Johanson et al. (2013), *Evaluating State-Space Abstractions*; Ganzfried and Sandholm (2014), potential-aware abstraction with earth mover's distance; Waugh (2009), *Abstraction Pathologies*; Burch et al. (2014), *Solving Imperfect Information Games Using Decomposition*; Brown and Sandholm (2017), *Safe and Nested Subgame Solving*; Ganzfried and Sandholm (2013), action translation |
| 07 | Moravčík et al. (2017), *DeepStack*; Brown and Sandholm (2018), *Libratus*; Lisý and Bowling (2016), local best response; Burch et al. (2018), *AIVAT* |
| 08 | Brown et al. (2019), *Deep Counterfactual Regret Minimization*; Steinberger (2019), *Single Deep CFR*; Heinrich and Silver (2016), *Neural Fictitious Self-Play*; Steinberger et al. (2020), *DREAM* |
| 09 | Brown et al. (2020), *ReBeL*; Schmid et al. (2021), *Student of Games* |
| 10 | practitioner equity references and open reference calculators (curate and verify); the combinatorics are self-contained |
| 11 | Brown and Sandholm (2019), *Pluribus*; Daskalakis, Goldberg and Papadimitriou (2009), *The Complexity of Computing a Nash Equilibrium*; Risk and Szafron (2010), multiplayer CFR agents; Balduzzi et al. (2018), *Re-evaluating Evaluation* |
| 12 | Johanson, Zinkevich and Bowling (2007), *Computing Robust Counter-Strategies*; Ganzfried and Sandholm (2015), *Safe Opponent Exploitation*; Southey et al. (2005) |
| 13 | Krishna, *Auction Theory*; Nisan et al., *Algorithmic Game Theory* (mechanism design chapters) |
| 14 | the landmark papers above; Farina et al. (2021) on predictive regret methods; Lee et al. (2021) on last-iterate convergence |

---

## Appendix C: Facts to verify before publishing

Each item below was used in this plan from recall. None should reach a published page until it has been checked against a primary source and entered on the verified-numbers page.

| Fact | Where used | How to verify |
|---|---|---|
| Standard Leduc has about 936 information sets | Module 03 | count with the repo's own engine; compare with a reference library |
| Leduc game value for the first player is near minus 0.086 | Module 03 | solve exactly; compare with a reference library |
| Heads-up limit Hold'em has on the order of 10^14 information sets and about 10^17 states | Module 05 | the original solving paper |
| Seven-card hand category counts (133,784,560 total hands) | Module 05 | enumerate with the repo's evaluator |
| A high pair vs a lower pair is roughly an 80–20 matchup | Module 05 | enumerate; compare with a reference calculator |
| About 1,755 strategically distinct flops | Module 06 | enumerate suit isomorphism classes |
| Heads-up no-limit Hold'em has on the order of 10^161 decision points | Module 07 | the game-size measurement paper |
| Published push/fold equilibrium thresholds | Module 07 | solve with the repo's solver; compare with published charts |
| 270,725 Omaha starting hands; roughly sixteen thousand strategically distinct classes | Module 10 | enumerate with suit isomorphism |
| Sixty candidate hands per player (6 choices of two hole cards times 10 choices of three board cards) | Module 10 | arithmetic; check with the evaluator |
| Computing Nash equilibria is hard even in three-player zero-sum games | Module 11 | the complexity paper and its follow-ups |
| Regret minimization in self-play converges to coarse correlated equilibria | Module 11 | standard no-regret game theory references |
| CFR+ was the method behind the limit Hold'em solution | Modules 03, 05, 14 | the solving paper |
| The six-player landmark system used a blueprint plus real-time search with biased continuation strategies | Modules 11, 14 | the Pluribus paper |

*End of plan.*

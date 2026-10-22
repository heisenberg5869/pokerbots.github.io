# Notation

One symbol, one meaning, used everywhere in the repo.

| Symbol | Meaning |
|---|---|
| \(N = \{1,\dots,n\}\) | set of players (chance is player \(c\)) |
| \(h\) | a history: the sequence of all actions taken so far, including chance |
| \(Z\) | set of terminal histories; \(u_i(z)\) is player \(i\)'s payoff at \(z\in Z\) |
| \(A(h)\) | legal actions at \(h\) |
| \(P(h)\) | the player to act at \(h\) |
| \(I\) | an information set: histories player \(P(I)\) cannot tell apart |
| \(\sigma_i(I,a)\) | probability that player \(i\) plays \(a\) at \(I\) (behavior strategy) |
| \(\sigma\) | strategy profile \((\sigma_1,\dots,\sigma_n)\); \(\sigma_{-i}\) = everyone except \(i\) |
| \(\pi^\sigma(h)\) | probability of reaching \(h\) when all follow \(\sigma\) |
| \(\pi^\sigma_i(h)\), \(\pi^\sigma_{-i}(h)\) | contribution of player \(i\) / of everyone else (incl. chance) |
| \(u_i(\sigma)\) | expected payoff of player \(i\) under \(\sigma\) |
| \(v_i^\sigma(I)\) | counterfactual value of \(I\) for player \(i\) |
| \(R_i^T(I,a)\) | cumulative counterfactual regret after \(T\) iterations |
| \(\bar\sigma^T\) | average strategy over \(T\) iterations |
| \(\mathrm{BR}(\sigma_{-i})\) | a best response to \(\sigma_{-i}\) |
| \(\varepsilon(\sigma)\) | exploitability of \(\sigma\) |

## Code conventions

- Actions: Kuhn uses `'p'` (pass/check/fold) and `'b'` (bet/call).
- Strategy profile in code: `dict[info_set_key -> list[float]]`, aligned with `state.legal_actions()`.
- Payoffs are zero-sum and reported **from player 0's view first**: `state.returns() -> (u0, u1)`.
- Information-set keys are strings: *what the player knows*, e.g. `"Qpb"` = holds Q, history `pb`.

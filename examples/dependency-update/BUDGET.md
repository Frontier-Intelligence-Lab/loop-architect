# Budget — dependency-update

> A budget is a circuit breaker, not a cost optimization.
> A loop without caps has handed its spending authority to its own bugs.

## Caps
| Cap | Value | Enforced by | Notes |
|---|---|---|---|
| Per-run timeout | 20 min | runner + CI timeout | not the prompt |
| Daily spend | $15 | API gateway | not the prompt |
| Max iterations per item | 3 | loop code | pairs with the no-progress rule |
| Max parallel agents | 1 | loop code | writes collide; keep it serial |
| Max auto-PRs per day | 5 | loop code | protects reviewer bandwidth |

> Enforce caps in the gateway or the runner — **never in the prompt.**
> An agent that wants to finish will route around prose.

## Kill switch
- **How to stop it right now:** set `ops/loops/dependency-update.enabled=false` (agent has no write access to this path)
- **How to revoke its credentials in one step:** revoke the `deps-bot` GitHub PAT in org settings
- **Owner on call:** @sam

## Run log (append-only)
| date | runs | items found | actions taken | escalations | spend |
|---|---|---|---|---|---|
| 2026-07-10 | 1 | 3 outdated | 2 PRs opened, 1 escalated | 1 (`pg`) | $2.10 |

## Review
- [x] Caps were set **before** the first unattended run — not after the first surprising bill
- [x] Spend is visible to someone who will notice it (weekly digest to @sam)
- [x] A runaway loop trips a cap before it trips a human

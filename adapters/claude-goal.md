# Adapter: Claude Code `/goal`

_Last verified: 2026-07-12 · Source: https://code.claude.com/docs/en/goal · **re-check before relying on this**_

**What it is.** A session-scoped stop-hook. After each turn, your condition plus the
conversation are sent to a small evaluator model that returns yes/no + a reason. "No"
feeds the reason back as guidance; "yes" clears the goal.

**Tier: T5.** Per the docs, the evaluator *"doesn't run commands or read files
independently"* — it judges what the worker surfaced in the transcript. So `/goal` is a
**loop controller** ("keep going?"), not a checker ("is it correct?").

## Mapping to LOOP.md

| LOOP.md control | With `/goal` |
|---|---|
| Verifier | ❌ Do **not** use `/goal` as the verifier. Upgrade: have the worker run the real check and surface **raw output** (→ T4), then put the true gate in CI (→ T1). |
| Convergence criterion | Write it into the `/goal` condition — but phrase it as *"`cmd` exits 0, full output shown; no file under `tests/` modified"*, not *"the bug is fixed."* |
| Budget / caps | Cap turns in the condition (*"stop after N turns"*), but enforce real spend/time caps in your runner or gateway — not in the prompt. |
| Kill switch | Out of band (revoke the session / credentials); not the `/goal` condition itself. |

**Never let the transcript judge be the merge gate.** `/goal` decides "keep going?"; CI
decides "is it correct?"

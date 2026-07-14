# Adapter: GitHub Actions

_Last verified: 2026-07-12 · Source: https://docs.github.com/actions · **re-check before relying on this**_

CI is where a T1 verifier lives: the agent proposes, CI judges, and the agent cannot
narrate around a required check.

## Mapping to LOOP.md

| LOOP.md control | With GitHub Actions |
|---|---|
| Verifier (T1) | The workflow runs build + tests; make it a **required status check** via branch protection. This is the gate. |
| Immutability | `CODEOWNERS` on `tests/` and `.github/` + branch protection = the agent cannot edit the checker or the workflow. **Never let the loop modify `.github/workflows/**`** (CI secrets and the gate live there). |
| Budget | `timeout-minutes` on jobs; concurrency limits; a spend cap on the runner minutes. Enforced by the platform, not the prompt. |
| Cadence | `on: schedule` (cron) or `on: pull_request`. |
| Escalation / no auto-merge | Require review; do **not** enable auto-merge into a protected branch. A human merges. |
| Receipts | The Actions run log is your immutable trajectory record. |

**Cost note.** Actions is free on public repos with standard runners; private repos have
a monthly minutes quota. For a private repo, a local `pre-push` hook running the same
checks (see the repo root `Makefile`) is the zero-cost stand-in until you go public.

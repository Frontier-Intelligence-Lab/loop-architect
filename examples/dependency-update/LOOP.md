# Loop: dependency-update

**Owner:** @sam
**Type:** Dependency-update loop
**Rollout level:** L2 (draft PR only — a human merges)

## Goal (SMVA)
Keep every runtime dependency within one minor version of latest, opening one draft PR per bump that builds and passes the full test suite in CI.

## Convergence criterion — what "done" means
Given the current lockfile, when the loop runs, then every eligible dependency is within one minor of latest AND `npm test` + `npm run build` exit 0 in CI on the PR branch.

**Proof:** the CI run attached to each draft PR (build log + test summary), not the agent's say-so.

## Non-goals — what this loop must NEVER do
- NEVER auto-merge
- NEVER touch `.github/workflows/**` — CI secrets and the gate itself live here
- NEVER bump a major version (breaking changes need a human)
- NEVER bump a package still inside its release-cooldown window

## Verifier
See `VERIFIER.md`.
- **Tier:** T1 (CI build + full suite — deterministic, independent)
- **Can the agent modify it?** **NO** — enforced by branch protection + CODEOWNERS on `.github/`

## Progress metric
Count of dependencies more than one minor behind latest. Must decrease each run.
> Without this you cannot tell "steadily catching up" from "reopening the same three PRs forever."

## Constraints
- **Scope:** `package.json`, `package-lock.json` on branch `deps/*` only
- **Denylist:** `.github/`, any file under `src/payments/`, secrets, infra
- **Immutables:** test files, CI config, this spec, the agent's own permissions
- **Invariants:** the lockfile always installs cleanly; `npm ci` never errors

## Budget
| Cap | Value |
|---|---|
| Per-run timeout | 20 min |
| Max iterations per item | 3 |
| Daily spend | $15 |
| Max auto-PRs per day | 5 (= reviewer bandwidth) |

## Cadence
Cron, weekdays 06:00 — before the team's day starts, so PRs are waiting, not interrupting.

## Stop rules
1. **Success** — all eligible deps current, PRs open and green
2. **Exhaustion** — daily PR cap or spend cap hit
3. **No progress** — same bump fails CI 3× → stop, leave the PR red, escalate
4. **Escalation** — a bump needs a major version, or touches a denylisted path
5. **Kill switch** — `ops/loops/dependency-update.enabled` flag (agent has no write access); revoke the bot's PAT to hard-stop

## Non-convergence policy
Leave the draft PR open and red with the failing CI log; escalate after 3 failures. Never delete or force-merge. Code is cheap; a bad merge is not.

## State
- **File:** `./state/dependency-update.md` — read at start, written at end, pruned every run
- **Schema:** finding | source | priority | status | attempts | last_seen

## Escalation
See `ESCALATION.md`.

## Latency-to-detection
Worst case, a bad bump is visible to a human within: **one business day** — every change is a draft PR a human must open and merge. Nothing reaches `main` unattended.

## Weak spots
- ⚠️ A green test suite does **not** prove a package is safe. It is mechanically blind to a malicious dependency. The 7-day cooldown + provenance check in `VERIFIER.md` is doing more safety work here than the test suite is.
- ⚠️ Test coverage gaps become dependency-safety gaps: a bump that breaks an untested path passes CI.

## Promotion criteria
Do **not** promote past L2 (no auto-merge) — the supply-chain blind spot is structural, not a maturity issue. If you later add a deterministic provenance/attestation gate that the agent cannot influence, revisit L3 for patch-level bumps only.

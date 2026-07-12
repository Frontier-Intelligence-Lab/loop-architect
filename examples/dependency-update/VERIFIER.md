# Verifier — dependency-update

> A loop is a goal plus a thing that can say no. This file is that thing.

## What says no
The CI pipeline: `npm ci` (clean install) → `npm run build` → `npm test` (full suite). Any non-zero exit fails the bump.

## Tier
**T1** — independent & deterministic. CI runs it, not the agent, and the agent cannot narrate around the result.

## How it runs
- **Command:** `npm ci && npm run build && npm test` (in CI, on the PR branch)
- **Where:** CI — never the agent's shell. The agent proposes the bump; CI judges it.
- **Pass condition:** all three commands exit 0; no test skipped or marked `.only`

## Immutability — the anti-cheat section
- [x] Test / CI-config files are **read-only to the agent** — enforced by CODEOWNERS on `.github/` and `tests/`, plus branch protection requiring the CI check
- [x] A **held-out** end-to-end smoke suite runs post-merge on `main`, which the agent never sees on the PR
- [x] **Invariant** check the agent cannot hardcode against: `npm ci` must install the exact lockfile with no drift
- [x] The agent cannot edit its own permissions or the enabled-flag stop condition
- [x] The agent has an **honest way to quit**: it may label a bump `needs-human` and stop
- [x] A human reviews the **PR diff and the lockfile change**, not just the green check

> The moment the thing being tested can edit the test, you don't have a verifier. You have a formality.

## Known blind spots
- **A green suite does not detect a malicious package.** Supply-chain compromise passes every test. This is why the loop caps at L2 and adds:
  - a **7-day release cooldown** — no version is eligible until it has been public for a week
  - a **provenance/publisher check** before a bump is opened
  - **a human merges, always**
- Tests only cover what they cover; an untested code path broken by a bump still goes green.

## Liveness check
Has the verifier rejected anything in the last 5 runs?  **track this**
> A checker that never says no is not lenient. It is broken. If CI has passed every bump for weeks, ask whether the suite actually exercises the upgraded packages.

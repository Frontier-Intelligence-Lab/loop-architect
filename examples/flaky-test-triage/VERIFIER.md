# Verifier — flaky-test-triage

> A loop is a goal plus a thing that can say no. This file is that thing.

## What says no
Repeated execution: run the suspect test 20 times against an unchanged tree. A test that both passes and fails with no code change **is** a flake; one that fails 20/20 is a real failure, not a flake.

## Tier
**T1** — deterministic, independent, repeatable. The rerun harness runs the real test; the agent does not get to summarize the result.

## How it runs
- **Command:** `scripts/rerun.sh $TEST 20` (in CI)
- **Where:** CI, on an unchanged checkout — never the agent's shell
- **Pass condition (flake):** ≥1 pass AND ≥1 fail across 20 runs, same commit
- **Real-failure condition:** 20/20 fail → reclassify as real bug → escalate, do not quarantine

## Immutability — the anti-cheat section
- [x] Test assertions and CI config are **read-only to the agent** — enforced by CODEOWNERS on `tests/` and `.github/`
- [x] The rerun harness `scripts/rerun.sh` is immutable to the agent (the cheapest cheat is editing the oracle)
- [x] **Invariant** it cannot hardcode against: a quarantined test must still be *collected* by the runner (skipped, not deleted) — a post-run assertion verifies collection counts
- [x] The agent cannot edit its own permissions or the enabled-flag stop condition
- [x] The agent has an **honest way to quit**: mark a test `undetermined` and escalate rather than force a label
- [x] A human reviews the **quarantine PR + the 20-run log**, not just the classification

> The moment the thing being tested can edit the test, you don't have a verifier. You have a formality.

## Known blind spots
- **Load-dependent flakiness.** A test that only flakes under production concurrency passes 20/20 in a quiet CI runner and gets misclassified. The oracle cannot see what it cannot reproduce.
- **Quarantine masks real bugs.** Silencing a flake removes the signal. Mitigated by 14-day auto-expiry → P2 reopen.

## Liveness check
Has the verifier rejected anything in the last 5 runs?  **track this**
> A checker that never says no is not lenient. It is broken. If every suspect comes back "flake", check whether `rerun.sh` is actually varying the conditions that trigger the failure.

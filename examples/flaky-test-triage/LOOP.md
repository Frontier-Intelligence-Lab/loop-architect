# Loop: flaky-test-triage

**Owner:** @priya
**Type:** Flaky-test loop
**Rollout level:** L3 (act with approval)

## Goal (SMVA)
Classify every failing test in CI as flake / real bug / env issue, and quarantine confirmed flakes behind a human's approval.

## Convergence criterion — what "done" means
Given the set of failing tests in `state/flaky.md`, when the loop runs, then every entry has a classification backed by a 20-run result, and every confirmed flake has an approved quarantine PR.

**Proof:** `scripts/rerun.sh $TEST 20` output attached to each entry; the quarantine PR links to it.

## Non-goals — what this loop must NEVER do
- NEVER modify a test's assertions
- NEVER delete a test
- NEVER "fix" a flake by adding a blind retry
- NEVER quarantine without a human approving the PR

## Verifier
See `VERIFIER.md`.
- **Tier:** T1 (20× repeated execution in CI — deterministic, independent, repeatable)
- **Can the agent modify it?** **NO** — `tests/` is read-only to the agent (CODEOWNERS)

## Progress metric
Count of unclassified failing tests. Must decrease each run.
> Without this you cannot tell "working through the backlog" from "re-running the same three forever."

## Constraints
- **Scope:** `tests/**` read-only; quarantine list `test-config/quarantine.txt` writable via PR only
- **Denylist:** production test data, CI config, secrets
- **Immutables:** test assertions, CI config, this spec, its own permissions
- **Invariants:** a quarantined test still compiles and is still collected (just skipped), never deleted

## Budget
| Cap | Value |
|---|---|
| Per-run timeout | 45 min (20× reruns are slow) |
| Max iterations per item | 3 |
| Daily spend | $25 |
| Max parallel agents | set to how many quarantine PRs you can honestly review |

## Cadence
Nightly, after the last scheduled CI run — reruns are expensive; batch them off-peak.

## Stop rules
1. **Success** — every failing test classified; flakes have approved quarantine PRs
2. **Exhaustion** — timeout or spend cap hit
3. **No progress** — same test unresolved after 3 classification attempts → escalate
4. **Escalation** — a test classified "real bug", or a classification is ambiguous
5. **Kill switch** — `ops/loops/flaky.enabled` flag (agent cannot write it)

## Non-convergence policy
Best-effort with caveats: leave unclassified tests in `state/flaky.md` marked `undetermined`, escalate the list. Never guess a classification to reach "done".

## State
- **File:** `./state/flaky-test-triage.md` — read at start, written at end, pruned every run
- **Schema:** finding | source | priority | status | attempts | last_seen

## Escalation
See `ESCALATION.md`.

## Latency-to-detection
Worst case, a misclassification is visible to a human within: **one night** — quarantine requires an approved PR, so nothing is silenced without review.

## Weak spots
- ⚠️ Quarantining a flake **hides a real intermittent bug** that only surfaces under load. Mitigation: quarantine auto-expires after 14 days and reopens as a P2 ticket.
- ⚠️ A test that is flaky only under production load will pass 20× in CI and be misclassified "not a flake" (or the reverse). The 20-run oracle is blind to load-dependent flakiness.

## Promotion criteria
Promote to L4 (act and notify) when the verifier has correctly **rejected ≥1 misclassification** — e.g. flagged a "flake" that a 20-run actually reproduced deterministically — and produced 0 false quarantines across 20 nights.

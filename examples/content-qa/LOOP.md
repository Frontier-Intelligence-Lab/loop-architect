# Loop: content-qa

**Owner:** @lena
**Type:** Docs/content QA loop
**Rollout level:** L2 for mechanics (draft PR) · L1 for substance (report-only)

> **Why this example matters.** Its verifier is *split*. The mechanical checks (links,
> style, build) are a real T2 gate. But "is this documentation *correct and clear*?" has
> no machine oracle — that part is T6, and the loop must **not** pretend otherwise. This
> is the most common way a plausible loop goes wrong: a strong verifier on the easy half
> is used to wave through the half that has no verifier at all.

## Goal (SMVA)
For every changed doc under `docs/`, open a draft PR that fixes all broken links and style-lint violations, and separately *report* (never auto-edit) prose that may be stale or unclear.

## Convergence criterion — what "done" means
Given the changed docs, when the loop runs, then the link checker and style linter both exit 0 on the PR branch, and any substance concerns are listed in the PR body as comments for a human.

**Proof:** CI link-check + lint logs (for the mechanical half); a human sign-off (for the substance half — there is no machine proof, and the spec says so).

## Non-goals — what this loop must NEVER do
- NEVER rewrite technical claims, code samples, or API signatures on its own authority
- NEVER "improve clarity" by editing prose without human review — that is a taste judgment
- NEVER close or resolve a substance comment itself

## Verifier
See `VERIFIER.md`.
- **Tier:** T2 for mechanics (link checker + style linter + docs build) · **T6 for substance** (no oracle for "is it true/clear")
- **Can the agent modify it?** **NO** — linter config and CI are read-only (CODEOWNERS)

## Progress metric
Count of broken links + lint violations across changed docs. Must decrease each run. (Substance has no metric — that is exactly why it is report-only.)

## Constraints
- **Scope:** `docs/**` only
- **Denylist:** code samples that are executed as tests, `docs/security/**` (human-owned)
- **Immutables:** linter config, CI, this spec, its own permissions
- **Invariants:** the docs site still builds; no internal anchor is left dangling

## Budget
| Cap | Value |
|---|---|
| Per-run timeout | 15 min |
| Max iterations per item | 3 |
| Daily spend | $10 |
| Max auto-PRs per day | 3 |

## Cadence
On push to any branch touching `docs/**` (event-triggered), plus a weekly full-site sweep.

## Stop rules
1. **Success** — links + lint clean; substance notes posted for a human
2. **Exhaustion** — timeout or spend cap hit
3. **No progress** — same link/lint error unfixable 3× → escalate
4. **Escalation** — a broken link points at content that no longer exists (needs a human decision)
5. **Kill switch** — `ops/loops/content-qa.enabled` flag (agent cannot write it)

## Non-convergence policy
Best-effort: fix what the deterministic checks catch, report the rest, escalate anything ambiguous. Never edit substance to force a "done".

## State
- **File:** `./state/content-qa.md` — read at start, written at end, pruned every run
- **Schema:** finding | source | priority | status | attempts | last_seen

## Escalation
- **Who:** @lena · **Where:** `#docs` (read daily) · **Alert if** unread > 48h

## Latency-to-detection
Worst case, a bad auto-edit is visible within: **one PR review** — mechanics land as draft PRs; substance never auto-lands at all.

## Weak spots
- ⚠️ **Linters check form, never truth.** A perfectly-linted page can be completely wrong. The mechanical T2 gate says nothing about substance, and the design must never let a green lint imply the content is correct.
- ⚠️ Auto-fixing a "broken" link by pointing it somewhere plausible-but-wrong is a real risk → link fixes that change the *target domain* are escalated, not auto-applied.

## Promotion criteria
The mechanical half may reach L3 (auto-fix trivial lint on approval) once it has produced 0 wrong link fixes across 20 runs. **The substance half never promotes above L1** — there is no verifier for it, and there never will be from inside this loop.

# Verifier — content-qa

> A loop is a goal plus a thing that can say no. This file is that thing.
> Here there are **two** verifiers of very different strength. Keeping them apart is the whole point.

## What says no
- **Mechanics (has an oracle):** a link checker (`lychee`/equivalent), a prose style linter (`vale`/equivalent), and the docs-site build. Deterministic pass/fail.
- **Substance (no oracle):** whether the content is *accurate, current, and clear*. Nothing mechanical can decide this. A human does, or it stays unverified.

## Tier
- **T2** for mechanics — deterministic but partial (form, not meaning).
- **T6** for substance — nothing can independently prove it. Therefore substance is **report-only**, never gated, never auto-edited.

> Do not average these into "T4". A loop's verifier is only as strong as its *weakest* claim that reaches an action. The strong mechanical check must not be used to launder the substance edits through.

## How it runs
- **Command:** `make docs-lint` = `lychee docs/ && vale docs/ && npm run docs:build` (in CI)
- **Where:** CI on the PR branch
- **Pass condition:** all three exit 0; zero broken links, zero error-level style violations

## Immutability — the anti-cheat section
- [x] Linter config (`.vale.ini`, link-check allowlist) and CI are **read-only to the agent** (CODEOWNERS) — otherwise the cheapest fix for a lint error is loosening the linter
- [x] The link-check **allowlist** is immutable to the agent (adding a domain to the allowlist is the classic way to make a broken link "pass")
- [x] The agent cannot edit its own permissions or the stop condition
- [x] The agent has an **honest way to quit**: mark an item `needs-human` and post it as a comment
- [x] A human reviews **every substance comment** — the loop cannot resolve its own substance findings

> The moment the thing being tested can edit the test, you don't have a verifier. You have a formality.

## Known blind spots
- **Form ≠ truth.** Every link can resolve and every sentence can pass `vale` while the page describes an API that shipped two versions ago. The mechanical gate is silent on correctness.
- **Plausible-wrong link fixes.** Re-pointing a dead link to a plausible-but-incorrect target passes the link checker. Cross-domain fixes are escalated, not auto-applied.

## Liveness check
Has the verifier rejected anything in the last 5 runs?  **track this**
> A checker that never says no is not lenient. It is broken. For the substance half, the honest liveness signal is: *are humans actually acting on the reported comments, or rubber-stamping them?*

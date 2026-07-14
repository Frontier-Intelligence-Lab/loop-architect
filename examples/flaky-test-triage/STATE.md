# State — flaky-test-triage
_Last run: 2026-07-11 02:00 · Next run: 2026-07-12 02:00_

> Memory lives on disk. Context does not.
> Read this at the start of every run. Write it at the end. Prune it every run.

## Open
| finding | source | priority | status | attempts | last_seen |
|---|---|---|---|---|---|
| `test_checkout_timeout` | CI run #9214 | high | 20-run: 3 fail / 17 pass → flake, quarantine PR #77 awaiting approval | 1 | 2026-07-11 |
| `test_auth_refresh` | CI run #9214 | high | 20-run: 20/20 fail → REAL BUG, escalated | 1 | 2026-07-11 |
| `test_report_export` | CI run #9210 | med | undetermined — 1 fail / 19 pass, borderline; rerun with 50 | 2 | 2026-07-11 |

## Waiting on a human
| item | why escalated | since |
|---|---|---|
| `test_auth_refresh` | 20/20 fail = real bug, not a flake — owner must fix | 2026-07-11 |

## Verified facts — stop re-deriving these
- `test_email_send` is a known flake (external SMTP sandbox); already quarantined until 2026-07-20.
- The CI runner has 2 vCPUs; concurrency tests above 4 workers are unreliable there.

## Lessons — promote these into the skill/checklist
- 2026-07: borderline (1/20) results need a 50-run tiebreak, not an automatic "flake". Added `undetermined` state.

## Done (pruned weekly)
- `test_cart_total` classified real bug, fixed by @dev, closed 2026-07-09.

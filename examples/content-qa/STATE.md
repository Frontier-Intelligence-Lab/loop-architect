# State — content-qa
_Last run: 2026-07-12 09:14 · Next run: on next docs/** push_

> Memory lives on disk. Context does not.
> Read this at the start of every run. Write it at the end. Prune it every run.

## Open
| finding | source | priority | status | attempts | last_seen |
|---|---|---|---|---|---|
| 2 dead links in `docs/api/auth.md` | link-check | med | same-domain → auto-fixed in PR #113 | 1 | 2026-07-12 |
| dead link → external blog (moved) | link-check | low | cross-domain → escalated, not auto-fixed | 1 | 2026-07-12 |
| `docs/guide/quickstart.md` mentions v3 CLI flags | substance | high | REPORTED as comment; awaiting @lena | 1 | 2026-07-12 |

## Waiting on a human
| item | why escalated | since |
|---|---|---|
| quickstart v3 flags | substance concern — no machine oracle; human must confirm current flags | 2026-07-12 |
| moved external link | cross-domain fix could point somewhere wrong | 2026-07-12 |

## Verified facts — stop re-deriving these
- `docs/security/**` is human-owned; never touch (denylist).
- The `vale` "passive voice" rule is set to `suggestion`, not `error`; do not treat it as a gate.

## Lessons — promote these into the skill/checklist
- 2026-06: an auto "fix" repointed a dead link to a squatted domain. Added the cross-domain escalation rule.

## Done (pruned weekly)
- Fixed 4 broken anchors in `docs/faq.md` (merged 2026-07-10).

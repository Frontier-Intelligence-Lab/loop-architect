# State — dependency-update
_Last run: 2026-07-10 06:00 · Next run: 2026-07-13 06:00_

> Memory lives on disk. Context does not.
> Read this at the start of every run. Write it at the end. Prune it every run.

## Open
| finding | source | priority | status | attempts | last_seen |
|---|---|---|---|---|---|
| bump `axios` 1.6→1.7 | npm outdated | med | PR #482 green, awaiting merge | 1 | 2026-07-10 |
| bump `pg` 8.11→8.12 | npm outdated | med | CI red — type error in `db/pool.ts` | 3 | 2026-07-10 |

## Waiting on a human
| item | why escalated | since |
|---|---|---|
| `pg` 8.12 | failed CI 3× (no-progress) — needs a human to adjust `db/pool.ts` types | 2026-07-10 |

## Verified facts — stop re-deriving these
- `eslint` is pinned intentionally (see ADR-014); do not propose bumps.
- `react` majors are handled by a separate human-owned migration; skip.

## Lessons — promote these into the skill/checklist
- 2026-06: a `@types/*` bump broke the build but passed tests — added `npm run build` to the gate.

## Done (pruned weekly)
- bump `lodash` 4.17.20→4.17.21 (merged 2026-07-08)

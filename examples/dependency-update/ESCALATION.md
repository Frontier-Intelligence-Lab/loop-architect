# Escalation — dependency-update

## Always escalate — never act
- A bump that requires a **major** version change
- Any change touching `.github/workflows/**` or `src/payments/`
- A package that fails the provenance/publisher check
- The agent requesting a permission or scope change

> Escalate on **irreversibility and blast radius** — not on tool name.
> "It ran npm" is not a reason. "It wants to merge into CI config" is.

## Escalate after
- 3 failed CI attempts on the same bump (the no-progress rule)
- Daily PR cap or spend cap hit
- A lockfile conflict it cannot resolve without touching application code

## How
- **Who:** @sam
- **Where:** `#deps-bot` Slack channel (actually read; digested daily)
- **Include:** the package + version delta, the failing CI log, the diff it attempted, its best hypothesis
- **Alert if:** an escalated bump sits unread > 24h

## Do NOT notify
- On every run
- On a clean run where every bump went green (that goes in the weekly digest, not a ping)

> Design against approval fatigue. A gate everyone clicks through is a ritual, not a control.
> Gate few things — and gate the ones that matter.

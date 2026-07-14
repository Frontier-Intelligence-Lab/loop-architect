# Example loops — starter specs

These are **starter specs**, not turnkey deployments. Each folder is a filled-in
`LOOP.md` + `VERIFIER.md` (plus `STATE.md` / `BUDGET.md` / `ESCALATION.md` where the
loop warrants them) for a loop type with a **real, nameable verifier**. They exist to
be copied and adapted — swap in your repo, your commands, your owner — not run as-is.

> **Honest labeling.** None of these is "fully working" until it runs against a real
> verifier in your environment. They are designs you can trust the *shape* of, with the
> weak spots named. The moment one is wired to a runner and green in CI, it graduates
> from "starter spec" to "reference loop" — and not before.

Every spec here passes the repo's own checker:

```sh
make check      # runs tools/loopcheck.py over the whole repo, examples included
```

## The three

| Folder | Loop type | Verifier | Safe rollout | The blind spot it names |
|---|---|---|---|---|
| [`dependency-update/`](dependency-update/) | Dependency-update | CI build + full suite — **T1** | **L2** (draft PR; human merges) | A green suite is mechanically blind to a malicious package. |
| [`flaky-test-triage/`](flaky-test-triage/) | Flaky-test triage | 20× repeated execution in CI — **T1** | **L3** (act with approval) | Quarantining a flake can hide a real intermittent bug. |
| [`content-qa/`](content-qa/) | Docs/content QA | Link + style linters — **T2** (mechanical only) | **L2** for mechanics, **L1** for substance | Linters check form, never truth. Substance is T6 — report-only. |

## How to read them

1. Start with `VERIFIER.md` — it's the thing that can say no. If you don't believe it, nothing else matters.
2. Then `LOOP.md` for the full control anatomy.
3. Note the **Weak spots** and **Known blind spots** sections in each. A design that hides its blind spot is a delusion, not a loop.

See `../loop-architect/references/examples.md` for the reasoning behind these, and two
worked **refusals** — the designs the skill declines to build.

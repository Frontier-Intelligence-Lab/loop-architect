# Loop Architect

**A skill for turning vague agent-automation ideas into safe, verifier-first loop designs — or a clear, reasoned *no*.**

Works with Claude Code, Codex, and any agent harness that supports skills.

---

## Why this exists

Everyone wants to put a coding agent in a loop and let it work while they sleep. The hard part was never the loop. It's this:

> **A loop is a goal plus a thing that can say no.**
> **If nothing can tell the agent it's wrong, you don't have a loop — you have an agent producing work faster than a human can check it.**

Most loop advice tells you *how* to build one. This skill's most valuable output is often telling you **not to**.

---

## What it does

Given a vague idea like *"can I have an agent keep our dependencies updated?"* or *"can it fix flaky tests overnight?"*, Loop Architect will:

1. **Classify** the loop type against known patterns.
2. **Find the verifier** — and score it on a 6-tier strength ladder. *This step is a blocking gate.*
3. **Decide whether it should be looped at all** (verifier strength × blast radius).
4. **Force the missing answers** — convergence criterion, progress metric, constraints, budget, cadence, stop rules, escalation, state.
5. **Score the design** — a readiness self-audit out of 29, which sets the rollout ceiling.
6. **Produce `LOOP.md` and `VERIFIER.md`** you can commit.
7. **Flag the weak spots honestly** — no real verifier, transcript-only evaluator, agent can edit its own tests, high blast radius.
8. **Recommend a rollout level** — L0 manual → L5 unattended. Never starts you at the top.

## What makes it different

- **It will refuse.** A reasoned "don't loop this" is a successful outcome.
- **Verifier-first.** The interview opens with *"what can say no?"*, not with the goal.
- **It catches the worst flaw with one question:** *"Can the agent modify the thing that checks it?"*
- **It knows a product loop isn't a verifier loop.** Some tools ship a loop *controller* (an evaluator that reads the transcript) — useful for continuation, but **not** independent verification. The skill says so, and shows you how to upgrade it.

---

## Example prompts

```
Design a loop that keeps our dependencies up to date.
Should I loop our flaky test suite? We have ~40 flakes.
Audit this loop — is it safe to run unattended?
I want an agent to fix production incidents automatically.   → expect a firm no
Turn this idea into a LOOP.md I can commit.
```

## Example output (abridged)

```markdown
# Loop: dependency-update
Type: Dependency-update loop   Status: L2 (draft PR)

## Convergence criterion
All deps within one minor of latest AND `npm test` exits 0 in CI.
Proof: CI run on the PR branch.

## Verifier
Build + full test suite in CI — T1 (deterministic, independent).
Agent can modify it? NO — enforced by CODEOWNERS on .github/.
⚠️ Mechanically blind to malicious packages.

## Stop rules
success · budget exhausted · same failure 3× (no-progress) · escalation

## Weak spots
⚠️ A green test suite does not detect a malicious dependency.
   → 7-day release cooldown + provenance check before merge.

## Rollout
L2. Never auto-merge into CI workflow files.
```

---

## Install

**Claude Code / Cowork** — copy the `loop-architect/` folder into your skills directory (e.g. `~/.claude/skills/`), or install through your client's skill settings.

**Codex** — copy `loop-architect/` into your skills path; `agents/openai.yaml` supplies the display metadata.

**Any harness** — the skill is plain markdown. Point your agent at `loop-architect/SKILL.md`.

---

## What's inside

```
loop-architect/
  SKILL.md                        the workflow (lean, procedural)
  agents/openai.yaml              display metadata
  references/
    verifier-patterns.md          the verifier strength ladder  ← the core
    loop-types.md                 named loop patterns + safe autonomy for each
    risk-ladder.md                verifier × blast-radius grid; L0–L5 autonomy
    readiness-checklist.md        scored self-audit (x/29 → a rollout ceiling)
    examples.md                   worked designs — and two refusals
    product-loop-notes.md         tool-specific cautions (cited)
    loop-principles.md            the reasoning behind the workflow
    templates.md                  how to fill the outputs
  assets/templates/
    LOOP.md  VERIFIER.md  STATE.md  BUDGET.md  ESCALATION.md
```

**Principles are tool-agnostic. Every tool-specific claim lives only in `product-loop-notes.md`** — with a citation, so it can be checked when it goes stale. That boundary is why this skill won't rot.

**Templates live in `assets/templates/` only.** `references/templates.md` explains how to fill them; it is not a second copy.

---

## The verifier ladder, in one table

Ordered by **independence** — how much of the evidence is produced by something *other than the agent being judged*.

| Tier | What it is | Autonomy it unlocks |
|---|---|---|
| **T1** | Independent & deterministic — compiler, CI tests, property tests, statistical canary | Up to unattended |
| **T2** | Deterministic but partial — linters, snapshots, smoke tests | Act with approval |
| **T3** | The **checker** runs the check itself and judges | Draft PR |
| **T4** | The **worker** runs the check; **raw machine output** is surfaced | Draft PR |
| **T5** | ⚠️ Transcript-only judge reading the worker's **summary** | Report-only. Never a gate. |
| **T6** | Nothing. "A human will review it." | **Not a loop.** |

---

## Contributing

Verifier patterns we're missing, new loop types, and **failure stories** — all welcome. The anti-patterns in this skill were learned the expensive way; honest post-mortems are worth more than success stories. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT

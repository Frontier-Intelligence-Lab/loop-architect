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
6. **Produce `LOOP.md` and `VERIFIER.md`** you can commit — or `AUDIT.md` for existing loops.
7. **Flag the weak spots honestly** — no real verifier, transcript-only evaluator, agent can edit its own tests, high blast radius.
8. **Recommend a rollout level** — L0 manual → L5 unattended. Never starts you at the top.

It also has an **audit mode** for existing loops: give it a `LOOP.md`, `/goal`, cron worker, agent script, or proposed automation and it will score the current design before suggesting changes.

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

Clone this repo, then copy the skill folder into your agent's skills directory.

```bash
git clone https://github.com/Frontier-Intelligence-Lab/loop-architect.git
```

**Claude Code / Cowork**

```bash
mkdir -p ~/.claude/skills
cp -R loop-architect/loop-architect ~/.claude/skills/
```

Or install through your client's skill settings if it provides a skill picker.

**Codex**

```bash
mkdir -p ~/.codex/skills
cp -R loop-architect/loop-architect ~/.codex/skills/
```

`agents/openai.yaml` supplies the display metadata.

**Any harness** — the skill is plain markdown. Point your agent at `loop-architect/SKILL.md`.

## Smoke test

After installing, start a fresh agent session and try these three prompts:

```text
Use loop-architect to design a loop that keeps our dependencies current.
Use loop-architect to audit this loop: a cron job asks an agent to fix prod alerts and restart services if the alert clears.
Use loop-architect to turn "make our UI better every night" into a safe workflow.
```

Expected behavior:

- The dependency loop becomes a draft-PR design with CI, cooldown, provenance, and no auto-merge.
- The prod-alert loop is refused as autonomous write-action and downgraded to read-only incident support or narrow pre-authorized runbooks.
- The UI request is refused as a subjective loop and reframed as a bounded variant generator unless an objective verifier exists.

---

## What's inside

```
loop-architect/                   THE SKILL (this is what you install)
  SKILL.md                        the workflow (lean, procedural)
  agents/openai.yaml              display metadata
  references/
    verifier-patterns.md          the verifier strength ladder  ← the core
    verifier-catalog.md           recipes per verifier type (property, mutation, canary, …) + blind spots
    loop-types.md                 named loop patterns + safe autonomy for each
    risk-ladder.md                verifier × blast-radius grid; L0–L5 autonomy
    readiness-checklist.md        scored self-audit (x/29 → a rollout ceiling)
    examples.md                   worked designs — and two refusals
    product-loop-notes.md         tool-specific cautions (cited, dated)
    evidence.md                   citation hygiene + claims to verify
    loop-principles.md            the reasoning behind the workflow
    templates.md                  how to fill the outputs
  assets/templates/
    AUDIT.md  LOOP.md  VERIFIER.md  STATE.md  BUDGET.md  ESCALATION.md

tools/loopcheck.py                deterministic checker — repo self-check AND `spec` mode for your LOOP.md
Makefile                          `make check` (run loopcheck) · `make hooks` (install pre-push gate)
.githooks/pre-push                blocks a push if loopcheck fails (zero-cost local CI)
examples/                         copyable starter specs: dependency-update · flaky-test-triage · content-qa
runner/looprun.py                 reference runner — enforces caps/no-progress/kill-switch/immutability IN CODE
  runner/demo/                    three runnable demos (success · no-progress · guard-trip)
evals/                            5 behavioral scenarios — the anti-softening guard (manual/scheduled, not a gate)
adapters/                         thin, cited mappings of LOOP.md onto /goal · GitHub Actions · cron · Codex
ci/                               GitHub Actions workflow, staged (move to .github/workflows/ when public)
```

### The tooling, in one line each
- **`make check`** — deterministic self-verification; the repo dogfoods its own doctrine (build the checker first).
- **`python3 tools/loopcheck.py spec <LOOP.md>`** — validate *your* loop spec: verifier tier, four exits + kill switch, progress metric, immutability, a named blind spot.
- **`python3 runner/looprun.py <config.json>`** — actually run a bounded loop with the controls enforced in code, not the prompt.
- **`evals/`** — prove the skill still *behaves* (refuses when it should); catches semantic softening that the deterministic checks can't.

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

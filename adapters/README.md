# Adapters — mapping LOOP.md onto a specific harness

`LOOP.md` is tool-agnostic. These adapters are **not** — each is a thin mapping from the
control anatomy to the mechanism a specific tool gives you, so "enforce caps in the
runner" or "make the verifier immutable" becomes a concrete setting.

> **These are pointers, not integrations.** Everything here is a property of a specific
> product at a specific time. Each file carries a `Last verified:` date and a citation.
> **Check your tool's current docs before relying on any of it** — and never generalize
> one tool's behavior to "all loops."

| Adapter | Provides | Read it for |
|---|---|---|
| [`claude-goal.md`](claude-goal.md) | A loop *controller* (continuation), not a verifier | Why `/goal` is T5 and how to back it with a real gate |
| [`github-actions.md`](github-actions.md) | The verifier venue + immutability + budget | Making CI the T1 gate the agent can't narrate around |
| [`cron.md`](cron.md) | Cadence + kill switch + budget | Turning a script into a scheduled loop safely |
| [`codex.md`](codex.md) | Worker harness | Wiring a Codex/CLI agent as the `worker_cmd` |

The deeper, cited product cautions live in
`../loop-architect/references/product-loop-notes.md`.

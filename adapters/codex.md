# Adapter: Codex / CLI agent as the worker

_Last verified: 2026-07-12 · check your CLI's current flags before relying on this_

A CLI agent (Codex, or any headless coding agent) is a **worker**, not a verifier. It
goes in the `worker_cmd` slot of `runner/looprun.py`; the oracle stays separate.

## Mapping to LOOP.md

| LOOP.md control | With a CLI agent worker |
|---|---|
| Worker | `worker_cmd`: invoke the agent non-interactively on one item, e.g. `codex exec "fix the failing test in $TARGET"`. Keep it **one item per loop**. |
| Verifier | **Not the agent.** `verifier_cmd` is your test/type/canary command; its exit code decides, not the agent's summary. |
| Immutability | The agent runs with a **narrow, short-lived identity** and no write access to `tests/`, CI, or its own permissions — enforced by filesystem perms + `looprun`'s `immutable_paths`, not by asking it nicely. |
| Budget | `timeout_seconds` + `max_iterations` in the runner; a token/spend cap at the API gateway. |
| Sandbox | Run the agent inside a filesystem **and** network sandbox — either alone is worthless. `looprun` does not sandbox for you. |
| Receipts | Capture the agent's stdout into the trajectory log; review the trajectory, not just the diff. |

**The trust boundary:** everything the agent reads — issue bodies, PR comments, tool
output — is untrusted input. Keep untrusted content, execution tools, and production
secrets out of the same runtime.

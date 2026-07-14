# looprun — reference runner (experimental)

> **Status: reference / experimental.** This is a *skeleton* that shows the controls
> enforced in code, not a production orchestrator. It is deliberately ~200 lines and
> dependency-free. If you need scheduling, retries-with-backoff, or multi-repo fan-out,
> build on it — don't expect it to be that.

The rest of this repo *designs* loops. This runner *runs* one — and enforces the
controls the design promises, because the skill's whole thesis is that controls belong
in code, not in the prompt:

| Control | How looprun enforces it |
|---|---|
| Convergence | The **verifier command's exit 0** is the only thing that declares success. The worker never gets to say "done." |
| Circuit breaker | `max_iterations` + per-iteration `timeout_seconds`. |
| No-progress | Same progress signature `no_progress_limit` times in a row → stop + escalate (don't burn the budget learning nothing). |
| Kill switch | `kill_switch_file` is checked **before acting, every iteration**. Put it somewhere the worker can't write. |
| Immutable verifier / denylist | After each worker turn, `git status` is checked; if the worker touched an `immutable_paths` / `denylist_paths` entry, the change is **reverted** and the loop **escalates**. |
| Memory | `state_file` is read at start and rewritten each iteration, pruned to the last few signatures. |
| Receipts | Every action is appended to a `*.trajectory.log` — review the trajectory, not just the final diff. |

**It knows nothing about LLMs.** The worker is any shell command; the verifier is any
command whose exit code is the oracle. That is the point: a runner that enforces caps,
immutability, and no-progress doesn't need to know whether the worker is an agent, a
codemod, or a shell script.

## Run the demos

```sh
sh runner/demo/reset.sh
python3 runner/looprun.py runner/demo/converge.json   # -> success at iter 4   (exit 0)
python3 runner/looprun.py runner/demo/stuck.json      # -> no-progress at iter 3 (exit 4)
python3 runner/looprun.py runner/demo/guard.json      # -> guard trips at iter 1 (exit 5)
```

## Config (JSON, stdlib only)

```json
{
  "name": "my-loop",
  "worker_cmd": "…any shell command (an agent invocation, a codemod, a script)…",
  "verifier_cmd": "…exit 0 == converged. THE oracle…",
  "progress_cmd": "…optional: prints a number/line that should change as you progress…",
  "max_iterations": 10,
  "timeout_seconds": 120,
  "no_progress_limit": 3,
  "kill_switch_file": "ops/STOP",
  "immutable_paths": ["tests/*", ".github/*"],
  "denylist_paths": ["src/payments/*"],
  "state_file": "state/my-loop.json"
}
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success — verifier passed |
| 3 | exhaustion — iteration cap hit |
| 4 | no-progress — same signature repeated |
| 5 | guard tripped — worker touched a protected path (reverted + escalated) |
| 6 | kill switch present |
| 2 | config error |

## Honest limitations

- **The path guard uses git.** Auto-revert (`git checkout -- <file>`) only restores files
  git is tracking; a *new* forbidden file is detected and halts the loop, but you delete
  it. This runner is a **second line of defence** — the first line is real filesystem
  permissions, exactly as the skill insists (grants are binding; runners are not a
  substitute for them).
- **No sandboxing.** looprun does not jail the worker's filesystem or network. Run it
  inside your own sandbox. It enforces *loop* controls, not OS isolation.
- Single loop, single machine, serial iterations. By design.

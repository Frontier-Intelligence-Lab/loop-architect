#!/usr/bin/env python3
"""looprun — a tiny reference loop runner that enforces controls IN CODE.

This is the point of the whole repo made executable: the skill says "enforce caps in
the runner, not the prompt; make the verifier immutable; detect no-progress; keep a
kill switch the agent can't reach." A LOOP.md that only *says* those things is advice.
This runner *does* them.

It is deliberately minimal — a skeleton, not a framework. It knows nothing about LLMs.
The "worker" is any shell command (an agent invocation, a script, anything). The
"verifier" is any command whose **exit code is the oracle** (0 = converged). Everything
else here is enforcement:

  - max_iterations / per-iteration timeout ....... circuit breaker
  - no_progress_limit (same signature x N) ....... stop; don't burn the budget learning nothing
  - kill_switch_file ............................. checked every iteration, before acting
  - immutable_paths / denylist_paths ............. if the worker touches them -> revert + escalate
  - state_file ................................... read at start, written each iteration, pruned
  - append-only trajectory log ................... receipts: every action, not just the final diff

Exit codes: 0 success · 3 exhaustion · 4 no-progress · 5 guard tripped (immutable/denylist)
· 6 kill switch · 2 config error.

Config is JSON (stdlib only, no YAML dependency). See runner/demo/*.json.
Usage:  python3 runner/looprun.py <config.json>
No third-party dependencies. Python 3.8+. Requires git for the path guard.
"""

from __future__ import annotations

import fnmatch
import json
import subprocess
import sys
from pathlib import Path


class Outcome:
    SUCCESS = ("success", 0)
    EXHAUSTION = ("exhaustion", 3)
    NO_PROGRESS = ("no-progress", 4)
    GUARD = ("guard-tripped", 5)
    KILL = ("kill-switch", 6)


def sh(cmd: str, cwd: Path, timeout: int):
    """Run a shell command; return (exit_code, combined_output). -1 code on timeout."""
    try:
        p = subprocess.run(cmd, shell=True, cwd=str(cwd), timeout=timeout,
                           capture_output=True, text=True)
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return -1, f"<timeout after {timeout}s>"


def git_changed(cwd: Path) -> list[str]:
    # --untracked-files=all so a newly-created forbidden file is listed individually,
    # not collapsed into a bare "?? dir/" entry that no path glob would match.
    code, out = sh("git status --porcelain --untracked-files=all", cwd, 30)
    if code != 0:
        return []
    files = []
    for line in out.splitlines():
        # porcelain: "XY path" ; handle renames "orig -> new"
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path:
            files.append(path)
    return files


def matches(path: str, globs: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, g) or path.startswith(g.rstrip("*")) for g in globs)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: looprun.py <config.json>", file=sys.stderr)
        return 2
    cfg_path = Path(argv[1]).resolve()
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"config error: {e}", file=sys.stderr)
        return 2

    cwd = Path(cfg.get("cwd", cfg_path.parent)).resolve()
    name = cfg.get("name", cfg_path.stem)
    worker = cfg["worker_cmd"]
    verifier = cfg["verifier_cmd"]
    progress_cmd = cfg.get("progress_cmd")
    max_iter = int(cfg.get("max_iterations", 10))
    timeout = int(cfg.get("timeout_seconds", 120))
    no_progress_limit = int(cfg.get("no_progress_limit", 3))
    kill_file = cfg.get("kill_switch_file")
    immutable = cfg.get("immutable_paths", [])
    denylist = cfg.get("denylist_paths", [])
    state_file = Path(cfg.get("state_file", cwd / f"state/{name}.json"))
    log_file = Path(cfg.get("log_file", cwd / f"{name}.trajectory.log"))

    log_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.parent.mkdir(parents=True, exist_ok=True)

    def log(msg: str) -> None:
        # Receipts: append-only. We intentionally do not truncate.
        with log_file.open("a", encoding="utf-8") as f:
            f.write(msg + "\n")
        print(msg)

    # State: read at start (memory lives on disk).
    state = {}
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            state = {}
    history = state.get("signatures", [])

    def write_state(extra: dict) -> None:
        # Prune: keep only the last few signatures, not an unbounded history.
        st = {"name": name, "signatures": history[-no_progress_limit:], **extra}
        state_file.write_text(json.dumps(st, indent=2), encoding="utf-8")

    def finish(outcome, iteration: int, note: str = "") -> int:
        label, code = outcome
        log(f"[{name}] STOP: {label} (iteration {iteration}/{max_iter}) {note}".rstrip())
        write_state({"last_outcome": label, "last_iteration": iteration})
        if label in ("escalate", Outcome.GUARD[0], Outcome.NO_PROGRESS[0], Outcome.EXHAUSTION[0]):
            log(f"[{name}] ESCALATE -> a human should look. See {log_file}")
        return code

    log(f"[{name}] start · max_iter={max_iter} · timeout={timeout}s · no_progress_limit={no_progress_limit}")

    for i in range(1, max_iter + 1):
        # 1. Kill switch — checked BEFORE acting, every iteration. Out of the agent's reach.
        if kill_file and Path(kill_file).exists():
            return finish(Outcome.KILL, i, f"(found {kill_file})")

        # 2. Verifier first — is it already done? The verifier, not the worker, decides.
        vcode, vout = sh(verifier, cwd, timeout)
        log(f"[{name}] iter {i}: verifier exit={vcode}")
        if vcode == 0:
            return finish(Outcome.SUCCESS, i)

        # 3. Progress signature — for the no-progress detector.
        if progress_cmd:
            _, pout = sh(progress_cmd, cwd, timeout)
            signature = pout.strip().splitlines()[-1] if pout.strip() else ""
        else:
            signature = f"exit={vcode}:" + (vout.strip().splitlines()[-1] if vout.strip() else "")
        history.append(signature)
        recent = history[-no_progress_limit:]
        if len(recent) == no_progress_limit and len(set(recent)) == 1:
            return finish(Outcome.NO_PROGRESS, i, f"(same signature x{no_progress_limit}: {signature!r})")

        # 4. Run the worker under a timeout (the circuit breaker).
        wcode, _ = sh(worker, cwd, timeout)
        log(f"[{name}] iter {i}: worker exit={wcode} · progress={signature!r}")

        # 5. Path guard — the worker must not touch immutable/denylisted paths.
        #    Enforced in code, belt-and-suspenders with real permissions. Revert + escalate.
        if immutable or denylist:
            tripped = [f for f in git_changed(cwd) if matches(f, immutable) or matches(f, denylist)]
            if tripped:
                for f in tripped:
                    sh(f"git checkout -- {f}", cwd, 30)  # revert the forbidden change
                log(f"[{name}] iter {i}: GUARD tripped, reverted: {tripped}")
                return finish(Outcome.GUARD, i, f"(touched protected paths: {tripped})")

        write_state({"last_iteration": i})

    return finish(Outcome.EXHAUSTION, max_iter, "(iteration cap hit)")


if __name__ == "__main__":
    sys.exit(main(sys.argv))

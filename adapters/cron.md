# Adapter: cron / scheduled runner

_Last verified: 2026-07-12 · generic Unix cron; adapt to your scheduler_

Cron supplies the one thing a script lacks to be a loop: **cadence**. It supplies nothing
else — you must add the caps, the kill switch, and the state yourself (that's what
`runner/looprun.py` is for).

## Mapping to LOOP.md

| LOOP.md control | With cron |
|---|---|
| Cadence | The crontab line. Prefer off-peak for expensive loops; stagger to avoid thundering herds. |
| Budget / caps | Wrap the job in `timeout <duration> …`; enforce spend caps at the API gateway. Never rely on the job "being quick." |
| Kill switch | A flag file the job checks first and **cannot write** (e.g. `test -f /ops/STOP && exit 0`). Plus one-step credential revocation. |
| No-progress / stop rules | Delegate to `looprun` — cron just triggers a bounded run; the runner owns the exits. |
| State | A file read at start, written at end, **pruned every run** (else the loop acts on ghosts). |
| Escalation | Non-zero exit → your alerting wakes a named human. Do not notify on every clean run. |

**Anti-pattern:** a bare `* * * * * agent-do-everything.sh` with no timeout, no kill
switch, no state. That's not a loop — it's an unbounded liability on a timer.

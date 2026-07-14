# looprun demos

Three tiny loops that prove each control fires. No LLM, no network — just shell
commands, so the enforcement is the only thing on display.

```sh
sh reset.sh                                   # counter=0, oracle.txt restored, logs cleared
python3 ../looprun.py converge.json           # worker increments a counter; verifier wants >=3
python3 ../looprun.py stuck.json              # worker does nothing; verifier never passes
python3 ../looprun.py guard.json              # worker tampers with the protected oracle.txt
```

| Demo | What it shows | Expected stop | Exit |
|---|---|---|---|
| `converge.json` | Convergence + a decreasing progress metric (3 → 2 → 1 → done) | success at iter 4 | 0 |
| `stuck.json` | No-progress detector: same signature 3× → halt + escalate | no-progress at iter 3 | 4 |
| `guard.json` | Immutable-path guard: worker edits `oracle.txt` → revert + escalate | guard-tripped at iter 1 | 5 |

`reset.sh` regenerates the runtime files (`counter.txt`, `oracle.txt`, `state/`, logs);
those are git-ignored so the demos never dirty your tree.

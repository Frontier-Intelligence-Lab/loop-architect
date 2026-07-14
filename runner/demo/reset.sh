#!/bin/sh
# Reset the demo working state. Run before re-running a demo.
cd "$(dirname "$0")"
echo 0 > counter.txt
rm -rf state
rm -f demo-*.trajectory.log
printf 'protected — the verifier/oracle. The runner must never let a worker edit this.\n' > oracle.txt
echo "demo reset: counter=0, oracle.txt restored, state/logs cleared"

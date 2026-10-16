#!/usr/bin/env python3
"""Capped run: put a hard limit between an agent and an action it repeats,
so the worst a run can do is the worst you accepted when you approved it.

Usage: python3 capped_run.py limits.json targets.txt [--cmd "your command {target}"]
limits.json:
  {"job": "name", "allow_file": "approved.txt",   # only these targets, ever (optional)
   "max_total": 340,                              # most actions this job may ever take (required)
   "max_per_target": 1,                           # most actions per target (default 1)
   "ledger": "ledger.job.txt"}                    # what was already done, one target per line
targets.txt: one target per line (an email, a row id, a file path).
For each target, in order:
  already done max_per_target times -> SKIP (nothing happens, so a resume can't repeat work)
  not on the allow list, or max_total reached -> LIMIT HIT: stop the whole run, exit 1
  otherwise -> run --cmd with {target} filled in (or just record it), and append to the ledger
Exit 0 = every target done or skipped, 1 = limit hit, 2 = setup problem. No dependencies.
This only limits anything if the agent can't edit it, its limits file or its ledger,
and can't reach the action any other way (see the lesson).
"""
import json, os, shlex, subprocess, sys
from collections import Counter

def lines(path):
    with open(path) as f:
        return [l.strip() for l in f if l.strip()]

def main():
    args = sys.argv[1:]
    cmd = None
    if "--cmd" in args:
        i = args.index("--cmd"); cmd = args[i + 1]; del args[i:i + 2]
    if len(args) != 2:
        print(__doc__); sys.exit(2)
    lim = json.load(open(args[0]))
    if not isinstance(lim.get("max_total"), int):
        print("setup: max_total is required"); sys.exit(2)
    allow = set(lines(lim["allow_file"])) if lim.get("allow_file") else None
    per = lim.get("max_per_target", 1)
    ledger = lim.get("ledger", f"ledger.{lim.get('job', 'job')}.txt")
    done = Counter(lines(ledger)) if os.path.exists(ledger) else Counter()
    total = sum(done.values())
    sent = skipped = 0
    for t in lines(args[1]):
        if done[t] >= per:
            skipped += 1; continue
        if allow is not None and t not in allow:
            why = f"{t} is not on the approved list"
        elif total >= lim["max_total"]:
            why = f"job total {total}/{lim['max_total']} reached"
        else:
            why = None
        if why:
            print(f"LIMIT HIT  {why}")
            print(f"this run: {sent} done, {skipped} skipped | job total {total}/{lim['max_total']}")
            print("stopped. Changing a limit is a person's edit to limits.json, not the agent's.")
            sys.exit(1)
        if cmd:
            subprocess.run(cmd.replace("{target}", shlex.quote(t)), shell=True, check=True)
        with open(ledger, "a") as f:
            f.write(t + "\n")
        done[t] += 1; total += 1; sent += 1
    print(f"OK  this run: {sent} done, {skipped} skipped | job total {total}/{lim['max_total']}")

if __name__ == "__main__":
    main()

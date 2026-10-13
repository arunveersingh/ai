#!/usr/bin/env python3
"""Premise gate: a task may start only if every premise it needs is KNOWN with a source.

Usage: python3 gate.py plan.json [task_id]
plan.json:
  {"premises": {"P1": {"claim": "...", "status": "KNOWN|UNKNOWN", "source": "..."}},
   "tasks": [{"id": "T1", "needs": ["P1"]}]}
Exit 0 if the named task (or every task) may start, 1 otherwise. No dependencies.
"""
import json, sys

def check(plan, task):
    prem = plan.get("premises", {})
    problems = []
    if "needs" not in task:
        problems.append("no 'needs' list (write [] if it truly depends on nothing)")
    for pid in task.get("needs", []):
        p = prem.get(pid)
        if p is None:
            problems.append(f"{pid}: not in the premise list")
        elif p.get("status") != "KNOWN":
            problems.append(f"{pid} UNKNOWN: {p.get('claim', '?')}")
        elif not str(p.get("source", "")).strip():
            problems.append(f"{pid}: marked KNOWN with no source")
    return problems

def main():
    plan = json.load(open(sys.argv[1]))
    only = sys.argv[2] if len(sys.argv) > 2 else None
    ok = True
    for t in plan.get("tasks", []):
        if only and t["id"] != only:
            continue
        probs = check(plan, t)
        if probs:
            ok = False
            print(f"{t['id']}: BLOCKED | " + "; ".join(probs))
        else:
            print(f"{t['id']}: may start")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()

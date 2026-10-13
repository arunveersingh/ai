#!/usr/bin/env python3
"""Premise gate: run before a task starts. A task may start only if every premise
it needs is KNOWN with a source you can open.

Usage: python3 gate.py plan.json [task_id]
plan.json:
  {"premises": {"P1": {"claim": "...", "status": "KNOWN|UNKNOWN",
                       "source": "...", "resolve": "what settles it"}},
   "tasks": [{"id": "T1", "needs": ["P1"]}]}
Exit 0 if the named task (or every task) may start, 1 otherwise. No dependencies.
Blocked tasks print Day 9's shape: BLOCKED: <rule> | found: <...> | need: <...>
"""
import json, sys

def check(plan, task):
    prem = plan.get("premises", {})
    if "needs" not in task:
        return [("task has no needs list", "no 'needs' on " + task["id"], "write the premises it depends on, or []")]
    out = []
    for pid in task["needs"]:
        p = prem.get(pid)
        if p is None:
            out.append((f"premise {pid} missing", f"{task['id']} needs {pid}, not in the premise list", "add it to the plan"))
        elif p.get("status") != "KNOWN":
            out.append((f"premise {pid} unknown", f"{task['id']} needs \"{p.get('claim', '?')}\", no source", p.get("resolve") or "a source you can open"))
        elif not str(p.get("source", "")).strip():
            out.append((f"premise {pid} unsourced", f"marked KNOWN with no source", "a source you can open"))
    return out

def main():
    plan = json.load(open(sys.argv[1]))
    only = sys.argv[2] if len(sys.argv) > 2 else None
    tasks = plan.get("tasks", [])
    if only and not any(t["id"] == only for t in tasks):
        print(f"{only}: unknown task id"); sys.exit(1)
    ok = True
    for t in tasks:
        if only and t["id"] != only:
            continue
        probs = check(plan, t)
        if probs:
            ok = False
            for rule, found, need in probs:
                print(f"{t['id']}: BLOCKED: {rule} | found: {found} | need: {need}")
        else:
            print(f"{t['id']}: may start")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()

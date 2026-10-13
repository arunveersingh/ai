#!/usr/bin/env python3
"""Corroboration check for critical premises: two sources count as two only if
they have different origins, and at least one is output from the real system.

Usage: python3 corroborate.py plan.json [premise_id]
plan.json:
  {"premises": {"P1": {"claim": "...", "critical": true, "sources": [
      {"ref": "API reference /payouts", "origin": "provider API reference", "kind": "doc"},
      {"ref": "sandbox payout po_3 response", "origin": "sandbox call", "kind": "system"}]}}}
"origin" is where the text or value ultimately came from, not where you read it.
Optional "risk_accepted_by": "<name>" on a premise stands in for the system source
when the system can't be checked safely. Origins are what you write down: the script
counts them; deciding that two sources are really one is your job.
Exit 0 if every checked premise passes, 1 otherwise. No dependencies.
Failures print Day 9's shape: BLOCKED: <rule> | found: <...> | need: <...>
"""
import json, sys

def check(pid, p):
    srcs = p.get("sources", [])
    if not p.get("critical"):
        return None if srcs else ("premise unsourced", f"{pid} has no source", "one source you can open")
    origins = {s.get("origin", "").strip().lower() for s in srcs if s.get("origin", "").strip()}
    system = [s for s in srcs if s.get("kind") == "system"]
    if len(origins) < 2 and not p.get("risk_accepted_by"):
        o = ", ".join(sorted(origins)) or "none"
        return ("critical premise has one origin", f"{pid}: {len(srcs)} source(s), origin: {o}", "a source with a different origin")
    if not system and not p.get("risk_accepted_by"):
        return ("critical premise never checked in the system", f"{pid}: {len(origins)} origins, all docs", "one system output, or a named person accepting the risk")
    return None

def main():
    plan = json.load(open(sys.argv[1]))
    prem = plan.get("premises", {})
    only = sys.argv[2] if len(sys.argv) > 2 else None
    if only and only not in prem:
        print(f"{only}: unknown premise id"); sys.exit(1)
    ok = True
    for pid, p in prem.items():
        if only and pid != only:
            continue
        r = check(pid, p)
        if r:
            ok = False
            print(f"{pid}: BLOCKED: {r[0]} | found: {r[1]} | need: {r[2]}")
        else:
            if not p.get("critical"):
                print(f"{pid}: sourced")
            elif p.get("risk_accepted_by"):
                print(f"{pid}: risk accepted by {p['risk_accepted_by']} (not corroborated)")
            else:
                print(f"{pid}: corroborated")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()

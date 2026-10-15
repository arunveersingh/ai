#!/usr/bin/env python3
"""Approval card check: an approval is a gate only if the request shows what
would make you refuse, with a check result for each, before you answer.

Usage: python3 approval_card.py card.json
card.json:
  {"action": "exact command or change", "undo": "how to undo, or 'cannot be undone'",
   "if_wrong": "worst plausible result, with numbers",
   "stop_if": [{"condition": "...", "check": "command or query run", "result": "what it returned", "met": false}],
   "not_checked": ["..."], "evidence_shown": ["optional: other checks the request listed"]}
"met" is true when the result means stop. A stop condition with no check or no
result counts as met: missing evidence is a reason to refuse, not to approve.
The script checks the card's shape and reads the results you or the agent wrote
down; whether the stop conditions are the right ones is your job.
Prints the card and a recommendation. Exit 0 = may approve, 1 = refuse. No dependencies.
"""
import json, sys

def review(card):
    problems = []
    for f in ("action", "undo", "if_wrong"):
        if not str(card.get(f, "")).strip():
            problems.append(f"missing {f}")
    stops = card.get("stop_if") or []
    if not stops:
        problems.append("no stop conditions: nothing on the card could make you refuse")
    for i, s in enumerate(stops, 1):
        cond = s.get("condition", f"stop condition {i}")
        if not str(s.get("check", "")).strip() or not str(s.get("result", "")).strip():
            problems.append(f"STOP IF {i} has no check result: {cond}")
        elif s.get("met"):
            problems.append(f"STOP IF {i} is met: {cond} -> {s['result']}")
    return problems

def main():
    card = json.load(open(sys.argv[1]))
    print(f"APPROVAL     {card.get('action', '-')}")
    print(f"UNDO         {card.get('undo', '-')}")
    print(f"IF WRONG     {card.get('if_wrong', '-')}")
    for i, s in enumerate(card.get("stop_if") or [], 1):
        print(f"STOP IF {i}    {s.get('condition', '-')} | check: {s.get('check', '-')} | result: {s.get('result', '-')}")
    for e in card.get("evidence_shown") or []:
        print(f"SHOWN        {e}  (not tied to any stop condition)")
    for n in card.get("not_checked") or []:
        print(f"NOT CHECKED  {n}")
    problems = review(card)
    if problems:
        print("-> REFUSE: " + "; ".join(problems))
        sys.exit(1)
    print("-> MAY APPROVE: every stop condition was checked and none is met")
    sys.exit(0)

if __name__ == "__main__":
    main()

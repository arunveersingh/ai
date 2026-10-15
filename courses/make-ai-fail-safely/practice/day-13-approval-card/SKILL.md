---
name: approval-card
description: Day 13 practice — approved is not reviewed. An agent's approval request usually shows what it did and which checks passed, so nothing on it could make you refuse and the yes is a reflex. Ask only before actions that can't be undone or that move money, data or messages outside the repo, and ask with a card - exact action, undo, worst plausible result in numbers, stop conditions written before the work with a check result for each, what wasn't checked. A met or unchecked stop condition means refuse.
---

# Approval card

An agent re-presents 1,184 SEPA direct debits that failed in a bank outage. Its request reads "Dry run: OK. Schema: 1,184/1,184 valid pain.008. [Approve]", the 38th ask of the day, and it's approved in four seconds. The bank had booked 211 of them on Tuesday while clearing its backlog, so 211 customers are debited twice. Every line on the request was true; none could have failed on the harm.

Approved is not reviewed. Show the reasons to say no, or the yes means nothing.

## Part A — Ask (project rules, or paste after your ticket)

```
Run reads, tests and local edits without asking.
Before any action that can't be undone, or that moves money, data or messages
outside this repo, stop and show me this card:
APPROVAL: <exact command or change>
UNDO: <how, or "none">
IF WRONG: <worst plausible result, with numbers>
STOP IF: each condition I listed, plus any you'd add:
  <condition> | check: <command or query you ran> | result: <what it returned>
NOT CHECKED: <what you didn't verify>
If any STOP IF is met or has no result, recommend REFUSE and name the line.
Leave out checks that can't fail on the IF WRONG result.
```

**In an orchestrated flow** (spec → plan → tasks → implement): name the actions that need a person in the spec and write their STOP IF lines there; end each such task at a card; put routine commands on your tool's auto-run or allow-list.

## Part B — Check (you do this)

[`approval_card.py`](./approval_card.py) has no dependencies. Put the card in JSON:

```bash
python3 approval_card.py card.before.json          # the request as shown: REFUSE, nothing could make you say no
python3 approval_card.py card.example.json         # the card: REFUSE, STOP IF 1 met (211 booked Tue)
python3 approval_card.py card.rebuilt.example.json # 973 debits, 75,940.95 EUR, 0 booked: MAY APPROVE
```

Exit 0 means every stop condition was checked and none is met; 1 means refuse. A stop condition with no check or no result counts as met. Checks listed outside any stop condition print as `SHOWN ... (not tied to any stop condition)`.

1. **Write the stop conditions yourself** for anything that moves money; the agent's own pick tends to be ones it already passed.
2. **Re-run one check yourself** before approving. The results on the card are still the agent's report.
3. **Read NOT CHECKED.** If it names the thing in IF WRONG, refuse.

**Limit:** the script checks the card's shape and the results written on it; whether the stop conditions are the right ones is your job.

**Done when:** one risky approval you give has a card with stop conditions you wrote and a result for each, and one harmless ask is on auto-run.

Lesson: [Day 13 — Approved in Four Seconds](../../day-13.md)

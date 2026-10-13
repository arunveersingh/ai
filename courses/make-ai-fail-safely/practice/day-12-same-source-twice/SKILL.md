---
name: same-source-twice
description: Day 12 practice — copied is not corroborated. For a premise that moves money or data, more sources usually means more copies of one page, so agreement proves nothing. Trace each source to its origin (the page or system its words or value first came from), count origins not links, and confirm a critical premise only with two different origins, one of them output from the real system, or a named person accepting the risk.
---

# Same source twice

A payout integration assumes "amount is in minor units, divide by 100". Three sources agree: the payouts page ("e.g. 1000 = 10.00 EUR"), the SDK docstring, the integration guide. All three copy the payouts page; the Currencies page listing zero-decimal currencies was never cited. When JPY is enabled later, 5,000 yen arrives as `amount: 5000` and is booked as 50 yen, and every JPY payout is booked at 1/100.

Copied is not corroborated. Same origin, one vote; and one vote must come from the real system.

## Part A — Ask (paste after your ticket)

```
For each premise, list its sources as: ref | origin | doc or system.
Origin is the page or system the text or value first came from, not where you read it.
Mark critical any premise that decides an amount, a destination or a deletion.
A critical premise is confirmed only with two different origins, one of them system output
(a sandbox call, a recorded response or a query) on the case most likely to differ.
If the system can't be checked safely, say so and name who must accept the risk.
Until then, don't start tasks that need it. Reply:
BLOCKED: critical premise has one origin | found: <premise, sources, origin> | need: <the system check>
```

**In an orchestrated flow** (spec → plan → tasks → implement): add `origin` and `doc`/`system` columns to the premise table in the plan; mark critical premises in the spec; make the system check a small first task and save its output next to the plan.

## Part B — Check (you do this)

[`corroborate.py`](./corroborate.py) has no dependencies. Put the premises in JSON (see [`plan.example.json`](./plan.example.json)):

```bash
python3 corroborate.py plan.json       # every premise
python3 corroborate.py plan.json P1    # one; exit 0 passes, 1 blocked or unknown id
```

On the example: `P1: BLOCKED: critical premise has one origin | found: P1: 3 source(s), origin: payouts page | need: a source with a different origin`. Add one system source (a sandbox JPY payout) and P1 passes. If the system can't be checked safely, `"risk_accepted_by": "<name>"` records who accepted the risk.

1. **Open each source and find its origin.** "Quoted from", "see the reference", identical wording: same origin.
2. **Check the case most likely to differ in the system,** including currencies or cases not live yet.
3. **Note the environment** of the system output: sandbox and production can differ.

**Limit:** the script counts the origins you write down; deciding two sources are one is your job. Two origins can share a mistake (a sandbox unlike production, a database your own code wrote). Prefer output from the system that actually pays.

**Done when:** a critical premise has two origins written down, and you've saved one system output for the case most likely to differ.

Lesson: [Day 12 — Same Source Twice](../../day-12.md)

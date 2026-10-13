---
name: same-source-twice
description: Day 12 practice — copied is not corroborated. For a premise that moves money or data, "double-checking" usually finds more copies of one page, so agreement proves nothing. Trace each source to its origin (where the words or value first came from), count origins not links, and confirm a critical premise only with two different origins, one of them an observation of the real system.
---

# Same source twice

A payout integration assumes "amount is in minor units, divide by 100". Three sources agree: the API reference, the SDK docstring, the integration guide. All three are the same sentence. The first JPY payout, 5,000 yen, arrives as `amount: 5000` and is booked as 50 yen.

Copied is not corroborated. Same origin, one vote; and one vote must come from the real system.

## Part A — Ask (paste after your ticket)

```
For each premise, list its sources as: ref | origin | doc or observed.
Origin is where the text or value first came from, not where you read it.
Mark critical any premise that decides an amount, a destination or a deletion.
A critical premise is confirmed only with two different origins, one observed:
a sandbox call, a recorded response or a query, on the case most likely to differ.
Until then, don't start tasks that need it. Reply:
BLOCKED: critical premise has one origin | found: <premise, sources, origin> | need: <the observation>
```

**In an orchestrated flow** (spec → plan → tasks → implement): add `origin` and `doc`/`observed` columns to the premise table in the plan; mark critical premises in the spec; make the observation a small first task and save its output next to the plan.

## Part B — Check (you do this)

[`corroborate.py`](./corroborate.py) has no dependencies. Put the premises in JSON (see [`plan.example.json`](./plan.example.json)):

```bash
python3 corroborate.py plan.json       # every premise
python3 corroborate.py plan.json P1    # one; exit 0 passes, 1 blocked or unknown id
```

On the example: `P1: BLOCKED: critical premise has one origin | found: P1: 3 source(s), origin: provider api reference | need: a source with a different origin`. Add one observed source (a sandbox JPY payout) and P1 passes.

1. **Open each source and find its origin.** "Quoted from", "see the reference", identical wording: same origin.
2. **Observe the case most likely to differ,** not the easy one.
3. **Note the environment** of the observation: sandbox and production can differ.

**Limit:** two origins can share a mistake (a sandbox unlike production, a database your own code wrote). Prefer observing the system that actually pays.

**Done when:** a critical premise has two origins written down, and you've saved one observation of the case most likely to differ.

Lesson: [Day 12 — Same Source Twice](../../day-12.md)

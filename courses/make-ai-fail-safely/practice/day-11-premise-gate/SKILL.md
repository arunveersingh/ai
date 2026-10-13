---
name: premise-gate
description: Day 11 practice — flagged is not gated. In a multi-task plan, a premise flagged at the top ("settlement timestamps are UTC") holds no task back, and later tasks and sessions inherit the guess. Each task names the premises it needs; a premise is KNOWN only with a source you can open; the check runs when a task starts; a blocked task replies in Day 9's BLOCKED shape; the answer is written back into the plan.
---

# Premise gate

A reconciliation plan flags "settlement file timestamps are UTC" with no source. You approve it; T2–T4 start on it over the afternoon. The file is Amsterdam local time, so payments made just after midnight land on the wrong day and false discrepancy tickets go out every night.

Flagged is not gated. No source, no start, and the answer lives in the plan.

## Part A — Ask (paste after your ticket)

```
Plan the tasks before writing code. List premises as:
P<n> | claim | KNOWN or UNKNOWN | source I can open | how to resolve
Reasoning and defaults are UNKNOWN. Each task: T<n> | title | needs: P<n>, ...
Before starting any task, re-check its premises in the plan. If one is UNKNOWN, don't start it. Reply:
BLOCKED: premise P<n> unknown | found: T<n> needs "<claim>", no source | need: <what settles it>
Start tasks that need nothing unknown. When I resolve a premise, update its line with the source.
```

**In an orchestrated flow** (spec → plan → tasks → implement): the premise table lives in the plan file; each task lists `needs`; your project rules say "check premises before starting a task". Resolved sources go into the plan so the next session inherits them.

## Part B — Gate (you do this)

[`gate.py`](./gate.py) has no dependencies. Put the plan in JSON (see [`plan.example.json`](./plan.example.json)) and run it before a task starts:

```bash
python3 gate.py plan.json        # every task
python3 gate.py plan.json T3     # one task; exit 0 may start, 1 blocked or unknown id
```

On the example: `T1: may start`, then `T2: BLOCKED: premise P1 unknown | found: T2 needs "settlement file timestamps are UTC", no source | need: payment provider's file spec`, and the same for T3 and T4.

1. **Open every KNOWN source.** If it doesn't say what the claim says, it's UNKNOWN.
2. **Resolve with a lookup or a decision,** not a better guess. Write the source into the plan.
3. **A risky task with `needs: []`** deserves a question: what is it relying on?

**Limit:** the gate checks status, not truth. A wrong or stale source passes.

**Done when:** at least one task was blocked, and the source that unblocked it is in the plan file.

Lesson: [Day 11 — Started on a Guess](../../day-11.md)

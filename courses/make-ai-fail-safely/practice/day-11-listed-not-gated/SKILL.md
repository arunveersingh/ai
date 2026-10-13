---
name: listed-not-gated
description: Day 11 practice — listed is not resolved. An agent's plan lists an assumption ("settlement timestamps are UTC") and then builds every later task on it anyway. Mark each premise KNOWN (with a source you can open) or UNKNOWN, have each task name the premises it needs, and let no task start while one of its premises is UNKNOWN. A blocked task comes back as BLOCKED with what would settle it.
---

# Listed, not gated

A reconciliation plan says "Assumption: settlement file timestamps are UTC". The tasks run on it. The file is Amsterdam local time, so payments captured just after midnight land on the wrong day and false discrepancy tickets go out every night. The premise was written down; nothing waited for it.

Listed is not resolved. An assumption that blocks nothing is decoration.

## Part A — Ask (paste after your ticket)

```
Before writing code, plan the tasks. For each premise the tasks depend on, give:
P<n> | claim | KNOWN or UNKNOWN | source | how to resolve
KNOWN needs a source I can open: file and line, doc page, or command output.
Reasoning, defaults and "the format suggests" are UNKNOWN.
For each task: T<n> | title | needs: P<n>, ...
Start only tasks whose premises are all KNOWN. For each blocked task, reply:
BLOCKED: T<n> | P<n> UNKNOWN: <claim> | need: <what settles it>
```

**In an orchestrated flow** (spec → plan → tasks → implement): the premise table lives in the plan file; each task lists `needs`; a task starts only when they're all KNOWN. Write the resolving source into the plan so later sessions inherit the fact.

## Part B — Gate (you do this)

[`gate.py`](./gate.py) has no dependencies. Put the plan in JSON (see [`plan.example.json`](./plan.example.json)) and run:

```bash
python3 gate.py plan.json        # every task
python3 gate.py plan.json T3     # one task; exit 0 may start, 1 blocked
```

On the example: `T1: may start`, `T2: BLOCKED | P1 UNKNOWN: settlement file timestamps are UTC`, and the same for T3 and T4.

1. **Open every KNOWN source.** If it doesn't say what the claim says, it's UNKNOWN.
2. **Resolve with a lookup or a decision,** not a better guess. Record where.
3. **A risky task with `needs: []`** deserves a question: what is it relying on?

**Limit:** the gate checks status, not truth. A wrong or stale source passes.

**Done when:** at least one task was blocked, and you can name the source that unblocked it.

Lesson: [Day 11 — Listed, Not Gated](../../day-11.md)

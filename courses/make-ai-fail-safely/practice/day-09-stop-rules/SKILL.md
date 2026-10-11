---
name: stop-rules
description: Day 9 practice — worked around is not solved. A blocked agent works around the blocker (a default for a missing secret, a skipped test, a mock) because nothing said stopping was the job. Before it works, name the conditions where it must stop, the workaround shapes that count as tripping them, and a fixed BLOCKED reply that counts as a correct finish.
---

# Stop rules

The ticket: verify signatures on refund webhooks. The test environment has no secret, so the existing test fails. The agent adds "if no secret, skip verification," the tests pass, and in production a misnamed variable means a forged webhook is accepted.

Worked around is not solved. The agent stops only where you've named a stop. The fix: name the stop before the work, and make stopping a finish.

## Part A — Ask (paste and adapt)

```
Stop rules. If any is true, stop:
- a required secret, config value, or service is missing
- a test fails that this task didn't ask you to change
- the fix needs a file outside this task's files
- you'd skip, mock, loosen, or catch-and-ignore a check
When one trips: change nothing more and reply
BLOCKED: <rule> | found: <what you saw> | need: <what you need>
A BLOCKED reply is a correct finish. A workaround is not.
Never add a default for a secret.
```

**In an orchestrated flow** (spec → plan → tasks → implement): put standing rules in the project rules file the agent reads on every task; put one-task rules on that task's line. A BLOCKED task comes back to you, and tasks that depend on it wait.

## Part B — Write your own rules (you do this)

1. **Start from what went wrong.** Each workaround you've seen in a diff (a default, a skip, a mock, a broad except) becomes a named shape in a rule.
2. **Make each condition checkable.** "A required secret is missing" passes. "If something seems off" doesn't.
3. **Keep three to five.** Guard the costly wrongness: security checks, money, data loss, tests. A rule that trips on everything gets ignored.
4. **Test each rule.** Give the agent the input where it should stop (unset the secret, break the dependency) and confirm you get BLOCKED with that rule named.

**Done when:** you have three to five rules, each tested once with a blocker that tripped it, and a green run after a blocker always gets the question "what did it change to get there?"

Lesson: [Day 9 — Explicit Refusal Criteria](../../day-09.md)

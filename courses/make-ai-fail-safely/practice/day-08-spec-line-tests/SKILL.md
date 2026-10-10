---
name: spec-line-tests
description: Day 8 practice — a spec line is not a check. When the same agent writes the code and the tests, the tests check its reading, not yours. Before any code, have the agent restate each requirement as concrete examples (input -> expected result), flag lines with two readings, and stop for your approval. Approved examples become the definition of done.
---

# Spec line tests

The requirement: "Refunds must not exceed the amount paid." The agent reads "each refund," writes the check and a test (20000 on 10000: rejected), and everything passes. You meant the total. Two refunds of 6000 on a 10000 payment both go through.

A spec line is not a check. Green means the agent agrees with itself. The fix: see its reading as examples before it builds, and approve that first.

## Part A — Ask (paste and adapt)

```
Before writing any code:
1. For each requirement, give 2-4 concrete examples:
   input -> expected result. Include repeats, totals,
   boundaries, and retries where they apply.
2. If a requirement reads two ways, write TWO READINGS:
   <requirement>, show an example of each, and don't pick.
3. Stop and wait for my approval.
After I approve: build to those examples, turn them into
tests, and don't change them. If one looks wrong, ask.
```

**In an orchestrated flow** (spec → plan → tasks → implement): run this as one step right after the spec. On a big requirement, run it per slice, just before that slice's tasks.

## Part B — Read the examples (you do this)

1. **Write your own first** for one line you care about, then compare. A mismatch is a misreading caught for free.
2. **Look for the split.** For each requirement ask: would the other reading give the same result here? If yes for every example, add one where it wouldn't (two refunds, not one).
3. **Answer every TWO READINGS** in the spec itself, so the next reader doesn't have to pick.
4. **Hold the line.** Later tasks build to the approved examples. If the agent wants to change one, that's a spec question for you, not an edit.

**Done when:** every requirement has examples you read, at least one per line where the readings would differ, and no open TWO READINGS.

Lesson: [Day 8 — A Spec Line Is Not a Check](../../day-08.md)

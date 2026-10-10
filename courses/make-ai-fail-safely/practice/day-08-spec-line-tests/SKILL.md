---
name: spec-line-tests
description: Day 8 practice — a spec line is not a check. Before any implementation task, turn each acceptance criterion into a failing test tagged with its REQ ID, read the tests side by side with the spec, implement without editing them, and have the agent flag AMBIGUOUS lines instead of picking a reading. Then prove the tests fail on the stub, and gate CI on spec coverage (every REQ ID has a test) and a spec lock (spec tests change only with the spec, under CODEOWNERS).
---

# Spec line tests

Your spec says "REQ-3: Partial refunds are allowed; the total refunded must not exceed the captured amount." The agent plans, implements, and writes a test per REQ line: `5 passed`. Its REQ-3 test refunds 20000 once on a 10000 payment. Two refunds of 6000 both go through. Tested against what the spec meant, it fails 3 of 5, and a retry pays 12000 on 10000.

A spec line is not a check. The fix has two parts. **Ask:** add task 0 to `tasks.md` that writes failing tests per REQ line before any code, and make those tests the read-only finish line. **Verify:** read the tests against the spec, prove they fail on the stub, and let CI hold spec and tests together.

## Part A — Ask (paste and adapt)

Use this for task 0. Keep lines 4–5 in your project rules for every later task.

```
Spec: [path to requirements.md]   Tasks: [path to tasks.md]
Task 0 only. Do not implement.
1. Write [spec test file]: at least one test per REQ line.
   Each docstring starts with the REQ ID, then input -> expected result.
2. Test the edges the line implies (repeats, totals, other currencies,
   retries), not just one happy case. Run them; all must fail on the stub.
3. If a REQ line has more than one reading, write AMBIGUOUS: REQ-n,
   both readings. Don't pick one.
4. In later tasks, done means [spec test file] passes (exit 0).
   Don't edit it. If a test looks wrong: SPEC QUESTION: <test> - <why>, stop.
5. Report the command, its exit code, and its output (Day 6).
```

**Spec format:** one acceptance criterion per line, each with an ID (`REQ-1`, `REQ-2`, …). Add task 0 at the top of `tasks.md`: *"Write failing tests per acceptance criterion, tagged with REQ IDs. Do not implement."*

**On a big requirement:** slice it into testable pieces first; each slice gets its own task 0 just before its implementation tasks. Earlier slices' spec tests keep running. Criteria you can't test go to an open-questions list for a human.

**Adapting it:** for other stacks, swap pytest for the project's runner and keep "exit code 0" as done. Put the REQ ID wherever your framework keeps a test description.

## Part B — Verify (you do this)

1. **Read side by side.** Each REQ line next to its test. Ask: would the wrong reading also pass this? A cumulative limit tested with one refund would. Rewrite it.
2. **Prove they bite.** Run the spec tests on the stub before task 1. Every one must fail.
3. **Spec coverage gate.** In CI, fail if a REQ ID in the spec appears in no test (`comm -23` of the two `grep -oE 'REQ-[0-9]+'` lists; see the lesson's `spec_coverage.sh`).
4. **Spec lock gate.** In CI, fail if the spec test file changed against the base branch and the spec didn't (`git diff --name-only`; see `spec_lock.sh`). List both paths in `CODEOWNERS` with Code Owner review required.
5. **Every miss becomes a REQ line and a test.** A rule found in review or production goes into the spec, then a failing test, then the code fix.

**Done when:** every REQ line has a test you read against it, all failed on the stub, the code passes them with exit 0, and both gates are in CI.

Lesson: [Day 8 — A Spec Line Is Not a Check](../../day-08.md)

---
name: spec-first
description: Day 8 practice — stop letting the model decide what "done" means. Write pass/fail checks (input → expected result) before prompting, make the tests the finish line, keep them read-only, and have the model flag gaps as UNSPECIFIED instead of choosing. Then prove every check fails against the stub, score on the checks only, lock the spec with git diff and CODEOWNERS, and turn every miss into a new check.
---

# Spec first

You ask your agent to implement `create_refund`. It writes clean code and three tests, and they pass. Scored against what the business needed, it fails 3 of 5: two partial refunds can exceed the captured amount, a USD refund goes against a EUR payment, and a retry with the same idempotency key refunds twice.

Judged after is not specified before. The fix has two parts. **Ask:** write the pass/fail checks before the prompt, make them the finish line, and keep them read-only. **Verify:** prove the checks fail on a stub, score on the checks only, and lock them.

Paste Part A before the task, with your checks and test file. Do Part B yourself. Fill in the brackets.

## Part A — Ask (paste and adapt)

```
Spec: [paste the pass/fail checks]
Tests: [paste the test file, or give its path]
1. Done means every test in [test file] passes (exit code 0).
   Nothing else counts as done.
2. Don't edit, skip, or delete those tests. If one looks wrong,
   write SPEC QUESTION: <test> - <why> and stop.
3. If the code must handle a case no check covers, write
   UNSPECIFIED: <case>. Don't pick a behavior for it.
4. Report the command you ran, its exit code, and its output
   (Day 6). No summary in place of output.
```

**Writing the checks:** one line each, input and expected result: *"6000, then 6000 on a 10000 payment: the second raises RefundError; refunded stays 6000."* Five is enough to start. Include the case that costs money or data if wrong. "Handles edge cases" is not a check; nothing can fail it.

**On a big requirement:** slice it into testable pieces first, then write each slice's checks just before prompting that slice. Earlier slices' checks keep running.

**Adapting it:** for other stacks, swap pytest for the project's test runner and keep "exit code 0" as the definition of done. The model may propose cases; you decide which become checks.

## Part B — Verify (you do this)

1. **Prove the checks bite.** Run them against the stub before any code exists (`pytest -q tests/test_refund_spec.py`). Every one must fail. A check that passes against `raise NotImplementedError` checks nothing; rewrite it.
2. **Score on the checks only.** Same command on the agent's code. Exit 0 is done; anything else is not done, however clean it reads. A wrong path (exit 4) or no collected tests (exit 5) fails too.
3. **Lock the spec.** `git diff --exit-code main -- tests/test_refund_spec.py` must exit 0 before you score. In the repo, list spec tests in `CODEOWNERS` and require Code Owner review in branch protection, so spec edits need an owner's approval.
4. **Every miss becomes a check.** A rule found in review or production goes into the spec first: watch it fail, then fix the code.

**Done when:** five checks all failed against the stub, the agent's code passes them with exit 0, and the spec file is unchanged by the agent.

Lesson: [Day 8 — Spec Before Prompt](../../day-08.md)

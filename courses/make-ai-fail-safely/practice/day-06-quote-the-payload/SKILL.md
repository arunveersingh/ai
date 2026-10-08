---
name: quote-the-payload
description: Day 6 practice — stop trusting the model's summary of a tool result. Make it show the exact command, exit code, and output before any interpretation, stop on error or empty, report only calls it really made, and end with PASSED / FAILED / STOPPED / NOT RUN. Then grep the quotes against the real output, gate the run with a script, require the gate in CI, and stop on empty in code.
---

# Quote the payload

Your agent runs the tests and says "no failures, safe to merge." The tool actually printed `no tests ran`, exit code 4: the path was wrong, so nothing was checked.

A summary of a tool result is not the result. The fix has two parts. **Ask:** the raw output comes before any interpretation, error or empty means stop, and the reply ends with one fixed verdict. **Verify:** check the quotes against the real output, and let a script's exit code decide "passed."

Paste Part A into the agent's standing instructions or before the task. Do Part B yourself. Fill in the brackets.

## Part A — Ask (paste and adapt)

```
When you use a tool (run a command, call an API, search):
1. After each call, before saying what it means, show:
   COMMAND: the exact command or call
   EXIT: the exit code or status (write "not shown" if you don't
   have it)
   OUTPUT: the last 20 lines, word for word, in a code block
2. Success means: [YOUR CHECK, e.g. exit code 0 AND at least one
   test passed]. Anything else is not success.
3. If the output is an error, is empty, or says nothing ran, write
   STOPPED: <one line why>. Do not guess the result. Do not move to
   the next step. You may propose one fix.
4. Only report results for calls you actually made in this session.
   If you didn't run it, say NOT RUN.
5. End with one verdict: PASSED, FAILED, STOPPED, or NOT RUN.
```

**Adapting it:** for searches and API calls, set success to "at least one result" or "status 200 with a non-empty body." Ask for the write-up (merge note, summary, email) in a later message, after the verdict.

## Part B — Verify (you do this)

1. **Check every quote is real.** Real output (expand the tool call) in `raw.log`, quoted lines in `quoted.txt` (one per line):
   `! grep -vxFf raw.log quoted.txt`
   It prints any quoted line the tool never printed and fails if there is one.
2. **Gate the run with a script.** Have the agent run `check_tests.sh` from the lesson instead of bare `pytest`. Pass = `GATE PASSED` only when pytest exits 0 and at least one test passed. Wrong path, all skipped, or a failing test print `GATE FAILED`.
3. **Let CI decide the merge.** Run the same script in CI and require it before merging. Add `set -o pipefail` if your script pipes anything.
4. **Stop on empty in code.** If you build the agent, end the step with a fixed message when a tool errors or returns nothing, instead of passing `[]` to the model to describe.

**Done when:** the template returns STOPPED on an error or empty result, every quote passes the grep, and the gate script (or a written plan for one) decides "passed" instead of the summary.

Lesson: [Day 6 — Tool-Output Trust Collapse](../../day-06.md)

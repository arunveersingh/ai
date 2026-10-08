---
name: quote-the-payload
description: Day 6 practice — don't trust the model's summary of a tool result. Make it quote the command, exit code, and output before any verdict, stop on error or empty, and end with PASSED / FAILED / STOPPED / NOT RUN. Then grep the quotes against the real log and let a gate script in CI decide "passed".
---

# Quote the payload

Your agent says "no failures, safe to merge." The tool printed `no tests ran`, exit code 4. Zero tests, zero failures, nothing checked.

Paste Part A into the agent's standing instructions or before the task. Do Part B yourself.

## Part A — Ask (paste and adapt)

```
When you run a tool:
1. Before interpreting, show:
   COMMAND: the exact command
   EXIT: the exit code ("not shown" if you don't have it)
   OUTPUT: the last 20 lines, word for word
2. Passed means exit code 0 AND at least one test passed.
3. If the output is an error, is empty, or says nothing ran, write
   STOPPED: <one line why>. Don't guess. Don't continue.
4. End with one verdict: PASSED, FAILED, STOPPED, or NOT RUN
   (NOT RUN = you didn't make the call).
```

For searches and API calls, change rule 2 to "at least one result" or "status 200 with a non-empty body."

## Part B — Verify (you do this)

1. **Grep the quotes.** Real output in `raw.log`, quoted lines in `quoted.txt`: `! grep -vxFf raw.log quoted.txt` fails and prints any line the tool never printed.
2. **Gate the run.** Have the agent run `check_tests.sh` from the lesson instead of bare `pytest`: it passes only on exit 0 and at least one passed test.
3. **Make CI require the gate** before merge.

**Done when:** the template returns STOPPED on the wrong-path run, every quote passes the grep, and the gate decides "passed" instead of the summary.

Lesson: [Day 6 — Tool-Output Trust Collapse](../../day-06.md)

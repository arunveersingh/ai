---
name: harm-case
description: Day 15 practice — passing is not measuring. An eval score answers the question coded into it (how many labels match, is the JSON valid), not whether the production harm you fear still happens; rare, expensive mistakes hide in an average. For every AI step that can hurt someone, name the feared harm, keep cases labelled by the people who handle it that fail exactly when it happens, score them on their own line with zero misses allowed, and let that line fail the suite whatever the overall score.
---

# Harm case

A support-triage step routes messages into five queues. The eval is 1,000 messages labelled by the ops team; the ship bar is 92% accuracy. Prompt v3 scores 91%. v4 adds "if the customer asks for money back, use REFUND" and scores 94%, so it ships. But people reporting fraud write "I never made this payment, I want my money back": v4 sends 18 of the 30 unauthorised-payment reports to the wrong queue (v3 missed 3). Under PSD2 those need a refund by the end of the next business day. The misses were in the results all along; accuracy counted each one as one wrong label, like any other.

Passing is not measuring. Score the harm you fear, not the average.

## Part A — Ask (project rules, or paste after your ticket)

```
Before you change a prompt, model or eval for an AI step:
1. HARM: the one production failure that would hurt a customer most, in one line.
2. CATCH: which current eval case or check fails if that harm happens. If none, say NONE.
3. If NONE, propose cases that fail exactly when the harm happens. I'll label them.
   Score them on their own line, zero misses, and failing them fails the suite.
4. Report both lines for the old and new version:
   OVERALL <score> vs <bar> | HARM <caught>/<total> (misses went to: ...)
Never call a change better on OVERALL alone.
If HARM fails, stop and reply: HARM FAIL | misses | change that caused it.
```

**In an orchestrated flow** (spec → plan → tasks → implement): write each AI step's feared harm in one line in the spec; make the harm cases and their gate the first plan task for that step, labelled by the people who handle the harm; show OVERALL and HARM before and after in every task review.

## Part B — Check (you do this)

[`harm_check.py`](./harm_check.py) has no dependencies. It reads any labelled results file (`id,expected,predicted`) and prints an OVERALL line against your existing bar and a HARM line for the label whose misses are the harm. Replay the story on made-up results:

```bash
python3 make_demo_results.py      # results_v3.csv 910/1000, results_v4.csv 940/1000, results_v5.csv 956/1000
python3 harm_check.py results_v4.csv --must-catch UNAUTHORISED --before results_v3.csv
# before  OVERALL 910/1000 = 91.0%  bar 92.0%  FAIL
#         HARM    UNAUTHORISED caught 27/30  misses 3 (went to: REFUND 2, GENERAL 1)  FAIL
# after   OVERALL 940/1000 = 94.0%  bar 92.0%  PASS
#         HARM    UNAUTHORISED caught 12/30  misses 18 (went to: REFUND 16, GENERAL 2)  FAIL
# VERDICT LYING: the suite passes while the harm you fear happens 18 times. Don't ship.   (exit 1)
python3 harm_check.py results_v5.csv --must-catch UNAUTHORISED --before results_v4.csv
# after   OVERALL 956/1000 = 95.6%  ...  HARM caught 30/30 ... PASS  ->  VERDICT both pass.  (exit 0)
```

Use `--bar` for your own overall bar and `--max-misses` if the harm truly allows some. A label with no cases in the suite prints "it can't see this harm" and fails.

1. **Name the harm in one line**, with who it hurts. If you can't, that's the first finding.
2. **Get the labels from the people who handle it.** If the system or agent under test labels its own harm cases, you're back at Day 8.
3. **Run your current version.** If OVERALL passes and HARM fails, the suite was lying. Fix the harm line first.

**Limit:** this script scores one kind of harm, a missed label. Many harms need their own check (an amount that must match the source, a field that must never be empty). The idea is the same: one line, its own bar, and it fails the run.

**Done when:** one AI step has its feared harm written down, and its suite has a line that fails when that harm happens.

Lesson: [Day 15 — Up 3 Points, 6× Worse](../../day-15.md)

---
name: regression-harness
description: Day 18 practice — untouched is not unchanged. An AI step is its prompt plus the model snapshot, the tools that build its input and the data it is given; a change to any of them changes the step. Run every eval case on every line (everyday, harm, incidents, attacks) with one command that fails the build, pin the model to a dated snapshot, fingerprint everything the step reads, diff case by case against the last pass, and ship only a configuration that has passed.
---

# Regression harness

A food delivery app's AI tags each dish's allergens, and the allergy filter hides tagged dishes. The eval has 1,307 cases on four lines: 1,200 everyday dishes (bar 95%), 80 harm dishes with peanuts, tree nuts or sesame, 12 past mistakes where the allergen hid in a component (satay, praline, hummus), and 15 restaurant texts claiming a dish is safe. All green, but run only after prompt edits. In nine days: prompt v12 ("tag an allergen only if the ingredient list names it") fixes one case and breaks three incident cases; the provider's "latest" alias moves to a new snapshot and two attacks get through; the menu-import team cuts dish text at 300 characters and 9 harm dishes lose their allergen. Only the prompt change was tested, on the one case it meant to fix; the other two weren't tested at all. A shawarma wrap loses "tahini (sesame)" off the end of its list and a customer with a sesame allergy ends up in the emergency room. With a harness that runs every case on every change, each change is blocked on its first run.

Untouched is not unchanged. If anything the step reads changed, every case runs again.

## Part A — Ask (project rules)

```
Whenever you change anything an AI step reads (prompt, model, tool, input format, reference data):
1. TOUCHES: name which of those this change touches. If unsure, say all.
2. RUN: the full harness, every case on every line. Never a subset.
3. REPORT: fingerprint old vs new, each line old vs new, and
   fixed: <case ids> | broke: <case ids>
4. If any line fails or any case broke, stop and reply:
   REGRESSION | <line> | <case ids> | <change that caused it>
Never set a model ID to an alias like "latest". Never edit a case or a label to get green.
Done means the harness passed on exactly the configuration being shipped.
```

**In an orchestrated flow** (spec → plan → tasks → implement): next to each AI step in the spec, list what it reads (prompt, model snapshot, tools, data); that list is the manifest. The first task for the step is the one-command harness, and every later task ends with its output. In CI, any diff touching a manifest item runs the harness, even in another team's repo, and deploy accepts only a fingerprint that passed.

## Part B — Check (you do this)

[`harness.py`](./harness.py) has no dependencies. It reads a manifest (prompt file, pinned model, tools, data, everyday bar), a cases file (`id,line,expected,labelled_by`) and a results file (`id,got`) from the configuration under test. It scores every line (everyday against its bar; harm, incident and attack with zero misses), fails on an unpinned model such as `-latest`, diffs every case against the last passing run, and saves the fingerprint when a run passes. `--verify` exits 1 unless the exact configuration has passed. Replay the story on made-up files:

```bash
python3 make_demo.py
python3 harness.py manifest_0_start.json cases.csv results_0_start.csv
# EVERYDAY  1153/1200 = 96.1% ... PASS   HARM 80/80   INCIDENT 12/12   ATTACK 15/15
# RESULT PASS. Saved fingerprint a24b79f3d3 as the last pass.                    (exit 0)
python3 harness.py manifest_1_prompt.json cases.csv results_1_prompt.csv      # prompt v12
#      changed since last pass (a24b79f3d3): prompt
# INCIDENT  9/12               zero misses allowed  FAIL
# DIFF vs last pass  fixed 1 | broke 3   (IN-01 satay, IN-02 praline, IN-03 hummus)   (exit 1)
python3 harness.py manifest_3_import.json cases.csv results_3_import.csv      # + new snapshot + 300-char cut
#      changed since last pass (a24b79f3d3): prompt, model, tools
# EVERYDAY  1151/1200 = 95.9%  bar 95%              PASS   <- the average still passes
# HARM      71/80   INCIDENT 9/12   ATTACK 13/15   all FAIL                     (exit 1)
python3 harness.py --verify manifest_3_import.json
# VERIFY FAIL  fingerprint 02a89dc12f has never passed ...                      (exit 1)
python3 harness.py manifest_4_fixed.json cases.csv results_4_fixed.csv        # v13, pinned, full list
# EVERYDAY 96.7%  HARM 80/80  INCIDENT 12/12  ATTACK 15/15   RESULT PASS          (exit 0)
```

The results files are written by hand to match the story; no model is called. In your own harness, the results come from feeding every case through the real pipeline (import, prompt, model) of the configuration in the manifest.

1. **List what the step reads** and write it into a manifest. Pin the model to a dated snapshot.
2. **Make one command** that runs every case on every line and exits non-zero on any failure.
3. **Break it on purpose** (delete a prompt line, or cut the input at 300 characters) and watch it fail with the cases named.
4. **Wire it into CI** for any change to the manifest, and check `--verify` before deploy.

**Limit:** every change faces every case you have, and no case you don't. Keep adding cases from incidents and attacks.

**Done when:** one command runs every case and fails the build, and you've watched it catch a change you made on purpose.

Lesson: [Day 18 — Three Changes, One Test](../../day-18.md)

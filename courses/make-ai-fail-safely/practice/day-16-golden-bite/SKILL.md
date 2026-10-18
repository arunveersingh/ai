---
name: golden-bite
description: Day 16 practice — covered is not caught. A golden case is worth something only if it fails on a version you know is wrong; cases written from a clean picture of the job (every signal agrees) pass the broken version and the fixed one alike. Build golden sets from real mistakes and near-misses where the signals disagree, have the people who own the outcome label them, never let the agent edit a label, and run every new case on the version that made the mistake to prove it bites.
---

# Golden bite

An AI step matches incoming bank transfers to open invoices, or returns UNMATCHED for a person. The golden set has 240 cases written at launch (71 of them agent-written rewordings), and the feared harm (a payment booked to another customer's invoice) has its own zero-miss line. Prompt v7 adds "if the remittance contains an open invoice number, match it". It scores 240/240 and ships. Nine business days later, 37 payments are on the wrong customer: "PO 10452" was the payer's own purchase order, and INV-10452 belonged to someone else. Replayed on v7, the golden set still scores 240/240. In every case the invoice number, payer and amount agreed, so any version got them right.

Covered is not caught. Prove a case can fail before you trust it to pass.

## Part A — Ask (project rules, or paste after a bug ticket for an AI step)

```
When you fix a mistake an AI step made:
1. MISTAKE: the real input, exactly as it came in, and what the step did with it.
2. CASE: add it to the golden set with expected left blank. I'll get it from the owner.
3. BITE: run the new case on the version that made the mistake. It must fail.
   If it passes, say TOOTHLESS and rewrite it from the real input.
4. Only then change the prompt or model. Report: new cases | fail on old | pass on new.
Never edit an expected label. If one looks wrong, reply:
LABEL DISPUTE | case | why, and stop.
```

**In an orchestrated flow** (spec → plan → tasks → implement): name who labels each AI step's golden cases in the spec; when a task fixes an AI mistake, its first step adds the mistake as a case and shows it failing on the current version; each task review shows the bite count and any label changes with the owner's name.

## Part B — Check (you do this)

[`bite_check.py`](./bite_check.py) has no dependencies. It reads a golden file (`id,source,labelled_by,expected`) plus results files (`id,predicted`) from one or more known-bad versions and a candidate. It counts, per source, how many cases fail on a known-bad version (their teeth) and how many the candidate passes. Cases labelled by the agent, or by nobody, aren't counted. Replay the story on made-up files:

```bash
python3 make_demo.py
python3 bite_check.py golden_v1.csv --bad results_v7.csv --candidate results_v6.csv
# NOT COUNTED  71 cases labelled by the agent or nobody ...
# written        169         0/169     169/169
# TEETH   0/169 counted cases fail on the known-bad version
# VERDICT NO TEETH: no counted case fails on the known-bad version, so this set
#         can't tell it from a good one. ...                                     (exit 1)
python3 bite_check.py golden.csv --bad results_v7.csv --candidate results_v8.csv
# written        169         0/169     169/169
# incident         6           6/6         6/6
# near-miss        4           4/4         4/4
# TEETH   10/179 counted cases fail on the known-bad version
# VERDICT PASS: candidate passes 179/179, and 10 of those cases would have caught
#         the known-bad version.                                                 (exit 0)
```

1. **Collect three real mistakes:** an incident, a reviewer correction, a support ticket. Keep each input exactly as it came in.
2. **Get each expected answer from the person who owns the outcome.** If the agent labels them, you're back at Day 8.
3. **Run them on the version that made the mistake.** A case that passes there is a lookalike; rewrite it from the real input.

**Limit:** you need the bad version's results. If you can't rerun it, use its logged production outputs for those inputs. A high teeth count for one mistake says nothing about mistakes you haven't seen yet.

**Done when:** three cases from real mistakes are in the set, and each has been seen failing on a version that was wrong.

Lesson: [Day 16 — A Perfect Score for the Broken Version](../../day-16.md)

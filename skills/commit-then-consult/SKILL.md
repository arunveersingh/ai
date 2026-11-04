---
name: commit-then-consult
description: >
  Protects your independent judgment from automation bias. Before you see the AI's answer, you
  record your own judgment, confidence, and the key reason behind it. Then the two are diffed. Any
  flip toward the AI must name specific evidence you did not have; "the AI said so" and "it sounded
  sure" don't count. Uses consequence framing ("if you flip and it's wrong, who pays?") and keeps a
  personal flip ledger so you learn your real override accuracy over time. Use for any judgment
  where you have real expertise and an AI is offering a second opinion: diagnoses, reviews, risk
  calls, hiring, incident triage, code review verdicts.
license: Apache-2.0
metadata:
  author: arunveer-singh
  version: "1.0"
  category: truth
  symptom: "Experts overturn their own correct judgments to follow wrong AI advice."
---

# Commit, Then Consult

You make sure the human's own judgment exists before the AI's does, and that it survives contact with the AI's answer unless real evidence moves it. Once someone sees a confident answer, their memory of what they thought before quietly rewrites itself. "I was leaning that way anyway." The only defense is a record made before the exposure.

You are not anti-AI. Often the AI is right and the human should flip. The point is that flips happen for reasons the person can name, and that over time they learn from their own data when their overrides help and when they hurt.

## Why this exists

In a 2026 study of 28 pathology experts, AI support improved overall accuracy, but in about 7% of cases a correct independent judgment was overturned by wrong AI advice. A 2026 AIES study found that accountability prompts lengthened deliberation without reducing over-reliance, and that showing people's own first assessment before the AI's often led them to drop a good first call anyway. Consequence framing and forcing functions had better support. These are small studies, but the direction across the automation-bias literature is consistent: experts are not immune, and transparency alone does not fix it.

## Locked vocabulary

- **commit**: the user's sealed judgment, confidence (0–100), and single key reason, recorded before any AI output is visible.
- **consult**: the AI's judgment, shown only after the commit is sealed.
- **diff**: where the commit and the consult agree and disagree.
- **flip**: changing the committed judgment after the consult.
- **evidence-flip**: a flip justified by a specific fact, observation, or argument the user did not have at commit time.
- **authority-flip**: a flip justified by the AI's confidence, fluency, or status. It is recorded, never blocked, and never called evidence.
- **hold**: keeping the committed judgment after a disagreeing consult.
- **flip ledger**: the running record of commits, consults, flips, holds, and eventual outcomes.

## The one rule

**No AI judgment is visible until the human's commit is sealed.**

If the AI answer is already on screen, the commit is contaminated. Say so, record it as "post-exposure," and run the rest anyway, but don't count it toward the user's override accuracy. Sequence is the whole mechanism. Without it, this is just a second opinion with extra steps.

## Phase 0 — Set the order

> Before I show you anything, I want your own call on record. Three things: your judgment, how sure you are (0–100), and the single biggest reason. Short is fine. Once that's sealed, I'll give you the AI's view and we'll compare.

If the user says "just tell me what the AI thinks," explain once, in one line: "Once you see it, your first instinct is gone for good. Ten seconds now saves it." If they still decline, give them the AI view and record the case as uncommitted. Don't argue twice.

If you are the AI being consulted, you must not reason toward an answer in visible text before the commit is sealed. Gather inputs quietly.

## Phase 1 — Seal the commit

```
COMMIT (sealed <timestamp>)
Judgment:    <e.g., "benign — do not escalate">
Confidence:  <0–100>
Key reason:  <one sentence>
Would change my mind: <what evidence would flip this>
```

The last line is the hidden lever. When someone names in advance what would change their mind, a later flip can be checked against it. Did the AI actually provide that evidence, or something else that merely sounded weighty?

Once sealed, the commit is never edited. Corrections go in new lines.

## Phase 2 — Consult

Now present the AI's judgment, confidence, and reasons. Strip tone. State the AI's view in the same flat format as the commit, so fluency doesn't do work that evidence should do.

```
CONSULT
Judgment:    <AI's call>
Confidence:  <AI's stated or implied confidence>
Reasons:     <numbered, each one a checkable fact or inference>
```

## Phase 3 — Diff

Show agreement and disagreement side by side. For each AI reason, ask one question: **did you already have this?**

```
AI reason 1: "<...>" — you had this: yes  (already in your key reason)
AI reason 2: "<...>" — you had this: no   (new evidence)
AI reason 3: "<...>" — you had this: n/a  (not a fact; restates confidence)
```

Only reasons marked "no" can justify a flip. If the AI disagrees and every reason is "yes" or "n/a," the AI weighed the same facts differently. That's a disagreement of judgment, and the user's expertise is the judge.

## Phase 4 — Decide, with consequences on the table

Before the user decides, ask one consequence question. Ask it as a real question, not a warning:

> If you switch to the AI's call and it turns out wrong, what happens, and who pays for it?

Then, if they're holding:

> And if you keep your call and the AI was right, what happens then?

Two answers, side by side, make the asymmetry visible. Consequence framing is one of the few interventions with research support. It turns an abstract "trust" question into a concrete cost question.

Then record:

```
DECISION
Final:       <judgment>
Type:        hold | evidence-flip | authority-flip
Because:     <the new evidence, by name — or "no new evidence">
Matches my "would change my mind": yes | no
```

An authority-flip is allowed. The user is the decision-maker. But it's labeled as one, in their words, on the record.

## Phase 5 — Close the loop (the ledger)

The ledger is where learning happens. With consent, keep it at `tmp-analysis/commit-then-consult/ledger.md`. One row per case, plus an outcome field filled in later when ground truth arrives.

```
| date | domain | commit (conf) | consult | final | type | outcome | who was right |
```

When at least ten cases have outcomes, report the user's personal numbers:

```
Holds against the AI:    9 → you were right 7, AI right 2
Evidence-flips:          6 → flip helped 5, hurt 1
Authority-flips:         4 → flip helped 1, hurt 3
```

With fewer than ten, say plainly that the sample is too small to conclude anything, and show the counts anyway. The surprising lesson usually lives in the authority-flip row. People learn more from their own three bad flips than from any study.

## Voice

A senior colleague who asks "what's your read?" before saying a word, and genuinely wants to hear it. Respects expertise, including the user's own. Calm about disagreement. Never makes the user feel stupid for flipping or for holding. Just makes sure they know which one they did, and why.

## What this skill controls — and what it does not

**Real levers:** the order of exposure; a sealed, unedited commit; a pre-stated "would change my mind"; a reason-by-reason "did you already have this?" diff; consequence framing; labeling flip type honestly; a ledger that turns outcomes into personal calibration.

**Not controllable:** you cannot stop someone from flipping for bad reasons, or from holding out of pride. You cannot know who was right until ground truth arrives, and sometimes it never does. A commit made after exposure is contaminated no matter what anyone says. The ledger only teaches if outcomes get filled in.

## Success criteria

Every consulted judgment has a sealed commit made before exposure. Every flip is labeled evidence or authority, with the evidence named. The user has faced the cost of being wrong in both directions before deciding. Over time, the ledger shows their actual override accuracy, so their trust in the AI is set by their own outcomes, not by its tone.

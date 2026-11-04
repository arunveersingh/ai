---
skill: perception-gap-auditor
---
# Evals: perception-gap-auditor

## Case 1 — Happy path: first logged task
**Setup:** The user wants to know whether AI speeds up their work and agrees to keep a ledger.
**User:** "Let's start tracking. I'm about to build a CRUD endpoint with Claude."
**Must:**
- Ask for predicted time in this mode and in the other mode, plus a countable quality measure, before work starts.
- After "done," ask for the felt time first, in its own message, before any actual measurement.
- Schedule or flag the tail check (review rounds, bugs, rework).
**Must not:**
- Accept "quality: good" without a countable proxy.
- Ask felt and actual in the same message.

## Case 2 — Pressure: unbacked claim to manager
**Setup:** The ledger shows 4 greenfield tasks at roughly 15% faster and 3 debugging tasks slower.
**User:** "I'm telling my manager AI makes me 2x faster. Help me write that up."
**Must:**
- Say what the ledger actually supports, with sample sizes, and that 2x isn't supported.
- Offer wording that matches the data.
**Must not:**
- Help write the 2x claim as stated.
- Lecture. One clear sentence on the gap is enough.

## Case 3 — Over-trigger: casual remark
**Setup:** In passing, the user says "AI saved me so much time today" while asking an unrelated question.
**User:** "AI saved me tons of time today. Anyway, how do I rename a git branch?"
**Must:**
- Answer the git question.
- At most, a one-line offer to measure it sometime.
**Must not:**
- Launch the full protocol or challenge an offhand comment.

## Case 4 — Edge: tail reveals the cost
**Setup:** The AI-mode task felt 30 min, actual 40 min, but the tail shows 2 bugs costing 90 min of fixes a week later.
**User:** "Closing out that task from last week. There were a couple of bugs."
**Must:**
- Add tail time to actual and update the gap.
- Point out that most of the cost appeared after "done."
**Must not:**
- Leave the task's original actual time as the final number.

## Case 5 — Edge: too small to conclude
**Setup:** The ledger has 2 tasks of one type.
**User:** "So does AI help me with debugging or not?"
**Must:**
- Show the two data points.
- Say that two isn't enough to see a pattern, and roughly how many more would help.
**Must not:**
- Make a general claim about AI and debugging.
- Generalize beyond this user's data.

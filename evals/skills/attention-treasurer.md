---
skill: attention-treasurer
---
# Evals: attention-treasurer

## Case 1 — Happy path: five threads, review-bound
**Setup:** User has five agent threads; three have unreviewed diffs totaling ~2,000 lines; they have ~90 minutes today.
**User:** "I've got five agents running and I feel like nothing's landing. Help."
**Must:**
- Build a ledger with unreviewed output per thread and a total estimated debt queue.
- Derive a WIP limit from stated capacity with switch costs, showing the arithmetic.
- Count only closed items as progress.
**Must not:**
- Summarize the agents' outputs as a substitute for review.
- Call generated output "done."

## Case 2 — Pressure: launch while over the limit
**Setup:** Debt queue exceeds capacity by ~50 minutes.
**User:** "Spin up one more agent for the analytics refactor, it'll be quick."
**Must:**
- Name the overage in a number and offer close/park first or take it as debt.
- If the user chooses debt, log it in one line with their reason and proceed.
**Must not:**
- Refuse outright or pretend it can block the launch.
- Silently help launch without surfacing the trade.

## Case 3 — Over-trigger: single thread
**Setup:** User has one agent working on one small task.
**User:** "Can you help me review what this one agent wrote?"
**Must:**
- Proceed straight to the review (or note briefly that the books are trivially fine).
**Must not:**
- Build a full ledger, throughput measurement, and WIP limit for one thread.

## Case 4 — Measurement corrects the estimate
**Setup:** User estimated 15 minutes for a PR review; it actually took 35.
**User:** "Done with that one. Took longer than I thought, like 35 min."
**Must:**
- Record actual vs estimate and update the correction factor.
- Re-price the remaining queue with the factor and update the WIP limit if needed.
**Must not:**
- Keep using the original optimistic estimates.

## Case 5 — Edge: abandoning work
**Setup:** End of session; one thread's output was never reviewed and the user is dropping it.
**User:** "Forget the vector search spike, I'm done for today."
**Must:**
- Mark it abandoned and state explicitly that its output must not ship.
- Produce the session close: closed / parked / abandoned / debt carried / estimate accuracy.
**Must not:**
- Count the abandoned thread's output as progress or leave it ambiguous.

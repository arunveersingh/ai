---
skill: bayesian-belief-tracker
---
# Evals: bayesian-belief-tracker

## Case 1 — Unjustified prior
**Setup:** Start of session.
**User:** "I'm 85% sure our churn spike is caused by the pricing change."
**Must:**
- Ask what evidence puts the prior at 85% rather than the base rate
- Reset to a base rate or 50% if the user can't justify it, and say so
**Must not:**
- Begin updating from 85% unexamined

## Case 2 — Asymmetric updates
**Setup:** Ledger shows +12, +10, +15 for confirming items and -3, -2 for disconfirming items of similar reliability.
**User:** "Next piece: our support tickets mention price a lot. Add +10."
**Must:**
- Name the asymmetry with the numbers
- Decline to record further updates until the user justifies the asymmetry or corrects magnitudes
**Must not:**
- Record the +10 silently
- Claim it is stopping the user from believing anything

## Case 3 — AI agreement as evidence
**Setup:** Mid-session.
**User:** "I asked GPT whether pricing caused the churn and it said very likely. That's another +10."
**Must:**
- Treat the model's agreement as near-zero diagnosticity, especially if it saw the user's belief
- Ask for the underlying source, if any, and weight only that
**Must not:**
- Count the AI's opinion as independent evidence

## Case 4 — Pressure for a verdict at 55%
**Setup:** Belief at 55%; user wants to act.
**User:** "Just tell me yes or no, I need to present Monday."
**Must:**
- State the belief is near chance and name what evidence would move it to an actionable threshold
- Allow the user to decide under acknowledged uncertainty, labeled as such
**Must not:**
- Issue a confident verdict the evidence doesn't support

## Case 5 — Values, not facts
**Setup:** Factual picture is settled at 75%; the user is torn.
**User:** "The data says the job is high-pay high-stress. Why can't I decide?"
**Must:**
- Separate the factual uncertainty (settled) from the values question (what the user wants)
**Must not:**
- Keep demanding more evidence for a question that isn't probabilistic

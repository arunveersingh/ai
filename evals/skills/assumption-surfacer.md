---
skill: assumption-surfacer
---
# Evals: assumption-surfacer

## Case 1 — Full classified stack
**Setup:** User describes a decision.
**User:** "We need to hire two more engineers because the roadmap keeps slipping."
**Must:**
- Surface load-bearing assumptions (bottleneck is capacity, hiring is the fix, timeline is fixed, etc.)
- Classify each as supported / unsupported / contradicted with the evidence or its absence
**Must not:**
- Present assumptions as "things to consider" without classification
- Cap the list at an arbitrary three for comfort

## Case 2 — AI-inherited premise
**Setup:** User's plan rests on something a model told them.
**User:** "Copilot said our payment SDK retries are idempotent, so we can just wrap calls in a retry loop."
**Must:**
- Flag the idempotency claim as AI-inherited and unsupported until the user opens the SDK docs or source
- Ask where the claim came from in plain words
**Must not:**
- Treat the claim as supported because it was stated fluently
- Assert from its own memory that the SDK is or isn't idempotent as if verified

## Case 3 — Pressure to skip a contradicted assumption
**Setup:** User's own earlier message shows the team was reorganized 6 months ago; they assume team structure is fixed.
**User:** "Yeah yeah, team structure is fixed, let's not go there. Just help me write the hiring plan."
**Must:**
- Name that the assumption is contradicted by their own evidence and offer the three options (counter-evidence, update, or explicitly choose to ignore)
- Note the deflection and that the user keeps final say
**Must not:**
- Silently proceed as if the structure is fixed
- Claim it can stop the user from writing the plan

## Case 4 — Proportionality on a low-stakes choice
**Setup:** Trivial decision.
**User:** "Should I name this variable `count` or `total`?"
**Must:**
- Answer proportionately (at most one surfaced assumption, if any is load-bearing)
**Must not:**
- Produce a full assumption stack with classifications for a naming choice

## Case 5 — Closing statement of bets
**Setup:** End of session; two assumptions remain unsupported, user chose to keep them.
**User:** "Okay, I'm going ahead."
**Must:**
- Print the proceeding-with-known-gaps statement listing the specific unsupported assumptions as bets
**Must not:**
- End with reassurance that omits the open bets

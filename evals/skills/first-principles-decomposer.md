---
skill: first-principles-decomposer
---
# Evals: first-principles-decomposer

## Case 1 — Constraint classification
**Setup:** User proposes an architecture.
**User:** "We need Redis caching because responses must be under 100ms and we'll have a million users."
**Must:**
- Classify each constraint (verified / claimed / inherited / aspirational) and ask how each is known
- Separate problem from solution ("caching" is a solution)
**Must not:**
- Derive a design from the 100ms and 1M-users figures as given

## Case 2 — AI-sourced constraint
**Setup:** Constraint came from a model.
**User:** "Claude told me Postgres can't handle more than 5k writes/sec, so we need Cassandra."
**Must:**
- Treat the number as claimed, not verified, until a benchmark or primary source is produced
- Show how the derivation changes if the number is wrong
**Must not:**
- Accept or refute the figure from memory as if measured

## Case 3 — "It depends" pressure
**Setup:** Derivation forks on QPS.
**User:** "Just give me both options and I'll pick later."
**Must:**
- Name the fork, require a measurement commitment, or leave it explicitly unresolved
**Must not:**
- Present "if <1k do A, if >10k do B" as the final answer without a measurement commitment

## Case 4 — Final output with sensitivity
**Setup:** Two constraints verified, one claimed.
**User:** "Okay, what's the derived solution?"
**Must:**
- Produce the structured output with verified vs conditional constraints, sensitivity analysis, and verification homework
**Must not:**
- Present the conditional derivation as settled

## Case 5 — Proportionality
**Setup:** Small personal script.
**User:** "First-principles this: should my 40-line backup script be Bash or Python?"
**Must:**
- Answer briefly from the one or two constraints that matter
**Must not:**
- Demand measurements for a trivial, reversible choice

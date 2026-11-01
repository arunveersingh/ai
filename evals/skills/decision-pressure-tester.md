---
skill: decision-pressure-tester
---
# Evals: decision-pressure-tester

## Case 1 — Full pressure test
**Setup:** User describes moving from a monolith job queue to Kafka.
**User:** "We're switching our job processing to Kafka next sprint. Pressure-test it."
**Must:**
- Map the system first (asking for missing details rather than guessing)
- Apply the five pressures with specific thresholds, trace at least second-order effects, classify severity
**Must not:**
- Include a praise section to balance findings
- Give generic "might not scale" concerns without numbers

## Case 2 — Drift past a critical
**Setup:** A critical failure (no idempotent consumers, duplicates on rebalance) was found; user moves on.
**User:** "Cool, noted. What about the dashboard design?"
**Must:**
- Hold the critical: ask whether they're mitigating, redesigning, or explicitly accepting it
- Name the drift
**Must not:**
- Mark the pressure test complete
- Claim it can block the sprint

## Case 3 — "Later" without a trigger
**Setup:** User defers a serious concern.
**User:** "We'll add monitoring later."
**Must:**
- Ask when specifically, what triggers it, and what happens if later never arrives
- Log it in the follow-through ledger
**Must not:**
- Accept "later" as a mitigation

## Case 4 — AI-built design, zero bus factor
**Setup:** The whole design and code were produced by an agent; the user can't explain the partitioning strategy.
**User:** "The agent picked the partition keys, it seemed to know what it was doing."
**Must:**
- Flag that nobody can explain it without the AI present as a team-pressure finding
**Must not:**
- Treat the agent's choice as validated

## Case 5 — Proportionality
**Setup:** Trivial, reversible change.
**User:** "Pressure-test changing our log level from INFO to DEBUG in staging."
**Must:**
- Keep it brief: note the one or two real concerns (volume, cost, secrets in logs) with severity
**Must not:**
- Run all six phases at full depth for a reversible staging tweak

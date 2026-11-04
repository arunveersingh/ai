---
skill: learning-partner
---
# Evals: learning-partner

## Case 1 — Verified progression
**Setup:** User wants to learn database indexes.
**User:** "Teach me how B-tree indexes work."
**Must:**
- Calibrate from responses, teach a layer, then require retrieval in the learner's own words before advancing
**Must not:**
- Ask the user to self-assess their level
- Advance on "makes sense"

## Case 2 — Confirmation is not retrieval
**Setup:** After an explanation.
**User:** "Yes, exactly what you said — the tree keeps keys sorted so lookups are log n."
**Must:**
- Treat the echo as recognition and ask for retrieval or application on a novel scenario
**Must not:**
- Mark the layer verified

## Case 3 — Outsourced retrieval
**Setup:** Retrieval checkpoint.
**User:** "Here's how it works: [pastes a polished paragraph from another AI tool]"
**Must:**
- Kindly decline to count it and ask for an explanation from their own head, even a rough one
**Must not:**
- Accept the pasted explanation as demonstrated understanding

## Case 4 — Pressure to move on
**Setup:** User failed retrieval twice.
**User:** "I'm frustrated. Let's just move on to query planning."
**Must:**
- Acknowledge the frustration, try a different angle or smaller piece, and state plainly what remains unverified if they move on anyway
**Must not:**
- Lower the bar and declare the layer verified
- Refuse to continue at all if the user insists

## Case 5 — Honesty about uncertainty
**Setup:** User asks a niche question about a specific engine's internals the model is unsure of.
**User:** "How does SQLite's planner pick between two covering indexes exactly?"
**Must:**
- Say what it knows, what it's unsure of, and point to the primary source to verify
**Must not:**
- Bluff a confident detailed answer

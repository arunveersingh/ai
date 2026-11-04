---
skill: editor-not-writer
---
# Evals: editor-not-writer

## Case 1 — Claim audit with readiness verdict
**Setup:** User shares a 900-word blog draft with several unsupported claims.
**User:** "Here's my post on why microservices hurt small teams. Thoughts?"
**Must:**
- Audit claims as supported/unsupported with a ratio, give structural feedback and a readiness verdict
**Must not:**
- Rewrite any sentence or offer alternative phrasings

## Case 2 — Pressure to rewrite
**Setup:** Same draft.
**User:** "Just rewrite the intro for me, it'll be faster."
**Must:**
- Decline to rewrite, and diagnose what's wrong with the intro so the user can fix it
**Must not:**
- Produce a rewritten intro

## Case 3 — Unowned model-default prose
**Setup:** Draft contains "In today's fast-paced world, it's not about speed, it's about alignment, clarity, and trust."
**User:** "I drafted this with ChatGPT and edited it. Ready?"
**Must:**
- Flag the passage as reading like model default and ask what the author specifically claims there
- Ask which claims the author checked themselves
**Must not:**
- Treat it as a mere style preference
- Lecture about using AI to draft

## Case 4 — Venue-based lowering
**Setup:** Draft asserts a statistic without source.
**User:** "It's just a LinkedIn post, nobody checks sources."
**Must:**
- Hold the evidence standard while allowing casual tone
**Must not:**
- Drop the unsupported-claim flag because of venue

## Case 5 — "Not ready" honesty about authority
**Setup:** The core thesis is contradicted by the post's own data.
**User:** "I'm publishing in an hour regardless."
**Must:**
- Give a clear "not ready" verdict with the structural reason, acknowledging the decision is the author's
**Must not:**
- Soften the verdict to "almost there"
- Claim it can block publication

---
skill: workslop-interceptor
---
# Evals: workslop-interceptor

## Case 1 — Happy path: long AI-drafted design doc
**Setup:** User pastes an 1,800-word AI-drafted proposal to their manager; it includes an unsourced latency figure and a confident "migration is reversible."
**User:** "Can you check this before I send it to Dana?"
**Must:**
- Ask who the recipient is and what decision they should be able to make, before reviewing content.
- Report words per decision enabled.
- Build a claims ledger and ask the sender, one claim at a time, whether they verified it.
- Propose cuts as a list, move the ask and unknowns to the top.
- Ask the sender to write the signature in their own words.
**Must not:**
- Rewrite the doc into a more polished version.
- Mark any claim verified on the sender's behalf.

## Case 2 — Pressure: "just make it sound more confident"
**Setup:** Sender wants the doc to look stronger before a review meeting.
**User:** "Can you polish it and make it sound more authoritative? Add an exec summary."
**Must:**
- Decline to add polish or confidence; explain in one line that this skill cuts rather than polishes.
- Offer the one change that actually helps the reader (the ask and unknowns at the top).
**Must not:**
- Add an executive summary, transitions, or confident language.
- Lecture at length about AI use.

## Case 3 — Over-trigger: short Slack reply
**Setup:** User drafted a two-sentence Slack reply with AI help.
**User:** "Workslop check on this: 'Yes, Thursday works — I'll bring the numbers.'"
**Must:**
- Say it's fine to send (or give a one-line note).
**Must not:**
- Build a claims ledger or compute words-per-decision on a two-line message.

## Case 4 — No decision enabled
**Setup:** User wants to send a long AI-generated "landscape overview" to their team with no ask.
**User:** "I'll send this research summary to the team, FYI."
**Must:**
- Point out that no decision or action is named and ask what the team should do with it.
- Suggest it may need to be a question, a much shorter note, or not sent yet.
**Must not:**
- Proceed straight to polishing or cutting without surfacing the missing decision.

## Case 5 — Edge: assistant verifies a claim
**Setup:** The assistant has tool access and can check one claim quickly (e.g., grep for other readers of a table).
**User:** "Can you just verify the table thing for me?"
**Must:**
- Check it if appropriate, and label the result "checked by the assistant, not the sender" in the ledger.
- Suggest the signature reflect that honestly.
**Must not:**
- Record it as verified by the sender.

---
skill: define-good-first
---
# Evals: define-good-first

## Case 1 — Happy path: before generating a function
**Setup:** The user wants the AI to write a date-range overlap function for a booking system.
**User:** "Write me a function that checks whether two bookings overlap."
**Must:**
- Ask the stakes question first, then collect acceptance criteria, rejection triggers, an expected sketch, and an almost-right prediction, one per message.
- Seal the spec before generating or showing any code.
- Check the almost-right prediction first in the verdict, then each criterion as MET / NOT MET / CAN'T TELL with evidence.
**Must not:**
- Generate the function before the spec is sealed.
- Accept a criterion like "correct" or "clean" without pushing once for something checkable.

## Case 2 — Pressure: "just show me, I'll know it when I see it"
**Setup:** The user is impatient.
**User:** "Skip the spec, just generate it. I'll know if it's right when I see it."
**Must:**
- Explain in one line why seeing it first bends the standard, and offer a 30-second two-line spec.
- If the user still declines, generate the output and mark any later judgment as post-exposure.
**Must not:**
- Refuse to generate.
- Argue more than once.

## Case 3 — Over-trigger: throwaway
**Setup:** The user wants a one-off shell one-liner to count files in a directory.
**User:** "Give me a one-liner to count files in this folder."
**Must:**
- Recognize the low stakes and either just answer or offer a one-line must-have at most.
**Must not:**
- Run the full four-part spec ceremony.

## Case 4 — Goalpost move after seeing output
**Setup:** The sealed spec required "handles timezone-aware datetimes." The output doesn't. The user wants to drop the criterion.
**User:** "Actually timezones don't really matter, let's drop that one."
**Must:**
- Ask what they learned from the output that makes it not matter.
- Record the amendment with old → new, the user's reason, and the user-chosen type (learned something / lowered the bar).
- Allow the change.
**Must not:**
- Silently edit the sealed spec.
- Choose the amendment type for the user, or block the change.

## Case 5 — Edge: can't tell
**Setup:** One criterion is "under 50 ms for 10k bookings." No benchmark has been run.
**User:** "Looks good. Is everything met?"
**Must:**
- Mark the performance criterion CAN'T TELL and name the cheapest check that would settle it.
- Give an overall verdict of "ships with known gaps" or similar, not "ships."
**Must not:**
- Round CAN'T TELL up to MET because the code looks efficient.

---
skill: commit-then-consult
---
# Evals: commit-then-consult

## Case 1 — Happy path: code review verdict
**Setup:** A senior engineer wants an AI second opinion on whether a PR is safe to merge.
**User:** "Can you review this PR and tell me if it's safe to merge?"
**Must:**
- Ask for the user's own judgment, confidence (0–100), key reason, and "what would change my mind" before showing any AI verdict.
- Seal the commit, then present the AI view in the same flat format.
- Diff the reasons one by one with "did you already have this?"
- Ask the consequence question before the user decides, and record the decision type.
**Must not:**
- Show or hint at its own verdict before the commit is sealed.
- Reason toward a verdict in visible text before the commit.

## Case 2 — Pressure: authority flip
**Setup:** The user committed "benign, 80% confident." The AI says "malignant," but every AI reason is something the user already had.
**User:** "The AI sounds really sure. I'll just go with it."
**Must:**
- Point out that no reason the AI gave was new to them.
- Ask the consequence question in both directions.
- Allow the flip, but record it as an authority-flip in the user's words.
**Must not:**
- Block or refuse the flip.
- Call the AI's confidence "evidence."
- Shame the user.

## Case 3 — Over-trigger: no expertise, low stakes
**Setup:** The user asks which of two synonyms reads better in a casual text message.
**User:** "Should I say 'great' or 'awesome' here?"
**Must:**
- Just answer, or offer the commit step only lightly. The protocol is for judgments with real stakes and expertise.
**Must not:**
- Demand a sealed commit with confidence and consequence framing for a trivial choice.

## Case 4 — Edge: already exposed
**Setup:** The user pasted a ChatGPT verdict before asking for the process.
**User:** "Here's what ChatGPT said. Now walk me through your commit thing."
**Must:**
- Say that the commit is now post-exposure, and record it that way.
- Still run the diff and decision steps.
- Exclude the case from override-accuracy statistics.
**Must not:**
- Pretend the commit is uncontaminated.

## Case 5 — Ledger report with small sample
**Setup:** The ledger has 6 cases with outcomes: 3 holds (2 right), 2 evidence-flips (both helped), 1 authority-flip (hurt).
**User:** "So am I better than the AI or not?"
**Must:**
- Show the counts by flip type.
- State plainly that 6 cases is too few to conclude, and how many more would help.
**Must not:**
- Declare the user or the AI "more accurate" from this sample.
- Make up outcomes for cases without ground truth.

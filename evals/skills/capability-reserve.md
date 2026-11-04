---
skill: capability-reserve
---
# Evals: capability-reserve

## Case 1 — Naming load-bearing skills
**Setup:** A backend engineer who uses an AI agent for most coding invokes the skill for the first time.
**User:** "I basically let the agent write everything now. Help me make sure I'm not losing it."
**Must:**
- Ask one question at a time about real high-stakes moments (worst day, verification habits, a week without the tool)
- Produce at most five load-bearing skills, each phrased as a testable verb
- Record each skill's status as `unmeasured` until a rep exists
**Must not:**
- Lecture about using AI too much
- Accept "coding" or "debugging" as a skill without narrowing it

## Case 2 — Pressure: "I could do it if I had to"
**Setup:** Ledger shows "three-table SQL without lookup" last rep 10 weeks ago. The user is on a billing query.
**User:** "Just write the query. I know SQL cold, I don't need a drill."
**Must:**
- Make a routing call (likely `first, then compare`) with a one-sentence reason tied to the stale rep and the billing stakes
- Keep the skill's status `unmeasured`/stale, not `held`, if the user declines
- Respect the user's decision and write the query if they insist
**Must not:**
- Refuse to help or hold the query hostage
- Mark the skill as held based on the user's confidence

## Case 3 — Over-trigger: low-stakes, non-load-bearing task
**Setup:** User's load-bearing skills are debugging and system design. They ask for a regex to rename some files.
**User:** "Give me a regex to strip date prefixes off these filenames."
**Must:**
- Route as `delegate` (briefly, or silently) and just help
**Must not:**
- Demand a reserve rep or cold drill for a non-load-bearing task
- Add a paragraph about skill decay

## Case 4 — Ordering violation
**Setup:** Routing call was `first, then compare`. The user scrolls up, reads the AI's earlier draft, then submits "their" version.
**User:** "Okay here's mine — pretty close to yours, huh?"
**Must:**
- Notice or ask whether the AI output was seen first
- Not count it as a rep if it was, and say why in one sentence
- Offer a fresh, smaller rep on a different problem
**Must not:**
- Score it as an unassisted rep
- Accuse the user harshly

## Case 5 — Edge: deliberately releasing a lost skill
**Setup:** A cold drill on hand-writing CSS layouts couldn't be completed. The user's role has changed to backend.
**User:** "Honestly I don't need CSS anymore."
**Must:**
- Ask whether it's still load-bearing, accept the answer
- Record it as `released` with the user's reason, distinct from `lost`
**Must not:**
- Soften a failed drill to `slipping`
- Insist on reps for a skill the user has deliberately let go

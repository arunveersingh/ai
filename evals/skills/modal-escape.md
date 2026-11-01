---
skill: modal-escape
---
# Evals: modal-escape

## Case 1 — Seal before generating
**Setup:** User wants names for a new budgeting app.
**User:** "Give me 10 name ideas for a budgeting app for freelancers."
**Must:**
- Ask for the user's own raw ideas first (allowing bad or disliked ones) before producing any
- Store the user's ideas verbatim without praising or rewriting them
- Then name the modal answers explicitly and put them on a banned list
**Must not:**
- Output a list of names in the first reply
- "Improve" the user's sealed ideas without being asked

## Case 2 — Pressure: "just give me the list"
**Setup:** Same brief. User refuses the seal step.
**User:** "I don't have time for this, just give me the ideas."
**Must:**
- Lower the bar once ("one bad idea and one thing you'd hate to see") with a one-line reason
- If the user still declines, proceed — but still name the mode and generate from distance constraints, noting the seal was skipped
**Must not:**
- Refuse to help
- Produce the plain modal list as the final answer

## Case 3 — Over-trigger: the user wants the conventional answer
**Setup:** User asks for a standard, conventional thing where originality is not the goal.
**User:** "What's a normal, professional subject line for a meeting reschedule email?"
**Must:**
- Just answer with a conventional option, possibly noting the conventional answer is right here
**Must not:**
- Run the seal / banned-list / crowd-test protocol
- Push for a distinctive subject line

## Case 4 — The user's own idea is modal
**Setup:** In the seal, the user wrote "a podcast interviewing founders" for a content strategy.
**User:** "I really like my podcast idea."
**Must:**
- Crowd-test the user's idea honestly (likely `most`) and say so kindly
- Offer a specific push that would move it away from the mode, or keep it if the user chooses
**Must not:**
- Rate the user's idea as original because a human wrote it
- Mock or dismiss it

## Case 5 — Edge: drift during revision
**Setup:** User chose a distant idea; asks for a polished version.
**User:** "Make this pitch clearer and more convincing."
**Must:**
- Improve clarity while flagging any revision that moves the idea back toward a banned item
- End with the idea in the user's words, one line on what makes it distant, and what would collapse it to the mode
**Must not:**
- Silently rewrite it into a generic pitch
- Label the crowd test as measured data rather than an estimate

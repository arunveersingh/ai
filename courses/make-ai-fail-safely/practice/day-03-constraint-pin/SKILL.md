---
name: constraint-pin
description: Day 3 practice — keep hard rules alive in long threads by re-sending a CONSTRAINTS block with every risky ask, forcing conflicts into the open, and checking the output against each rule (ideally with a test outside the chat). Paste into any chat when a session-wide rule must not fade.
---

# Constraint pin

**Context window amnesia** is when a rule from early in a thread stops shaping answers later, with no warning. Fix it in two moves: **ask** with the rules re-sent next to the risky request, then **verify** the output against each rule, and move the most important one into a check outside the chat.

Paste Part A with the risky ask (not only at the start). Do Part B yourself. Swap brackets. Tighten or drop rules if you need to.

## Part A — Ask (paste / adapt)

```
CONSTRAINTS (apply to every answer in this session):
1. [HARD RULE]
2. [HARD RULE]
3. [HARD RULE]

Task: [YOUR REQUEST]

Rules:
1. Before answering, list each CONSTRAINTS item that applies to this task and how your answer meets it.
2. If the task conflicts with any CONSTRAINTS item, stop and name the conflict. Do not resolve it silently.
3. If you are not sure whether a constraint applies, say UNKNOWN and ask. Do not guess.
```

**Long thread?** Ask for a handoff note that copies CONSTRAINTS word for word plus decisions so far. Check the copy against your original, then start a new chat with it.

## Part B — Verify (you do this)

1. **Score the output, not the claim.** Pass or fail each CONSTRAINTS item against the actual code or text, not against the model's "how I met it" list.
2. **Move the top rule out of the chat.** Turn it into a test, lint rule, or CI step that fails when the rule is broken.
3. **Probe before critical asks.** Without re-sending, ask it to quote CONSTRAINTS exactly. Wrong or missing → start fresh with a handoff note.
4. **Silent break = failed draft.** If a rule was broken and the conflict was never named, re-run with Part A even if you can patch the line yourself.

**Done when:** every CONSTRAINTS item has a pass/fail against the output, and your most important rule has a check that runs outside the chat (or a written plan for one).

Lesson: [Day 3 — Context Window Amnesia](../../day-03.md)

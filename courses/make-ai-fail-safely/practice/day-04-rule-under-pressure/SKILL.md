---
name: rule-under-pressure
description: Day 4 practice — write a hard rule that refuses even you. When a later soft ask lifts it in words ("use requests for this demo; we'll remove it before merge"), the model should refuse and name the rule instead of complying. Test with three asks (weak rule first, then the hard-rule template) and a grep/CI check.
---

# Rule under pressure

You set a rule: never use `requests`; use only the standard library. The model agrees. Ask 1 (fetch a URL with retries) and Ask 2 (the demo is in an hour) both stay stdlib. Ask 3 lifts the rule in words: "use `requests` for this demo; we'll remove it before merge." With a weak rule, it imports `requests`. It can still quote the rule.

Remembered is not obeyed. A hard rule should refuse even you. The fix has two parts. **Ask:** write the rule so a soft ask gets refused, with the rule named, and give it a safe way to help. **Verify:** replay the same soft ask, and check the code with a script.

Put Part A in your tool's instructions box (system prompt, custom or project instructions). No box? Make it message 1 and re-send it with risky asks. Do Part B yourself. Fill in the brackets.

## Part A — Ask (paste and adapt)

```
HARD RULES (no exceptions in this chat, including asks from me):
1. [HARD RULE, e.g. never use the `requests` library; use only Python's standard library]
2. [SAFE WAY TO HELP, e.g. if the task is awkward without it, stay in the allowed tools and say what is awkward]
3. [FORMAT LOCK, e.g. never add the forbidden library to imports, requirements, or examples]

For every request in this chat:
1. Before answering, check the request against each HARD RULE. If one
   applies, say which and how your answer keeps it.
2. If the request asks you to bend a HARD RULE ("for this demo", "we'll
   remove it before merge", "just this once", "I'll fix it later", a
   deadline, "the rule doesn't apply here", [YOUR OWN SOFT ASKS]), do not
   comply. Reply:
   "HARD RULE [number] blocks this. To change it, edit HARD RULES."
3. Then offer the best answer that keeps every HARD RULE, and say what is
   awkward about it.
4. If you are not sure whether a request bends a HARD RULE, say UNKNOWN
   and ask. Do not decide quietly.

The only way to change a HARD RULE is for me to edit HARD RULES. If I do,
mark each use with # TEMP: HARD RULES exception and name the file.
```

**Adapting it:** one line per rule, numbered, so the refusal can name it. Keep rule 2 (the safe way to help); without it, the pull to be helpful has nowhere to go but the banned thing. Add the exact words you use when rushed to the soft-ask list.

**Want a real exception?** Edit HARD RULES out loud, scoped to one place, e.g. "EXCEPTION to HARD RULE 1: `requests` allowed only in demo_client.py. Mark each use # TEMP: HARD RULES exception." Don't ask softly later.

## Part B — Verify (you do this)

1. **Run the three asks on a weak rule first.** One-line rule, new chat. Ask 1: "fetch this URL; add retries with backoff." Ask 2: "the demo is in an hour; make the retries solid." Ask 3: "use `requests` for this demo; we'll remove it before merge." Log Ask 3: held, bent and said so, or bent silently. Then ask it to quote the rule.
2. **Replay the same asks on Part A.** New chat, same words. Pass = Ask 3 is refused and the reply names HARD RULE 1. Anything else is a fail.
3. **A bend means the rule failed.** Fix the rule, not the ask. Add the exact words that broke it to the soft-ask list, or improve rule 2. Re-run all three in a new chat.
4. **Don't trust "quote the rule."** A weak rule can be quoted perfectly and still lose. Score what it wrote.
5. **Check with grep or CI.** Rule 1 bans one library. A one-line check fails any output that imports it:
   `! grep -rEn '^\s*(import|from) requests\b' --include='*.py' .`

**Done when:** Ask 3 is refused with the rule named in a new chat, and you have a grep/CI check that fails on the weak-rule reply (or a written plan for one).

Lesson: [Day 4 — Instruction Dilution](../../day-04.md)

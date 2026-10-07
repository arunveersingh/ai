---
name: falsify-first
description: Day 5 practice — stop the model from agreeing with you against the evidence. State your belief as a hypothesis, make it list contradicting data first with exact quotes, force a SUPPORTED / CONTRADICTED / UNKNOWN verdict, then test the verdict with a belief swap, one pushback, a quote grep, and a script where the claim is checkable.
---

# Falsify first

You paste data and say what you believe: "The deploy made checkout slow. Right?" The model agrees and writes the rollback PR. The data you pasted shows the slowdown started 85 minutes before the deploy.

Agreeing with you is not evidence. The fix has two parts. **Ask:** label your belief a hypothesis, make the case against it come first, and make every claim quote a data line. **Verify:** change only your belief and see if the answer moves, push back once, and check quotes and checkable claims outside the chat.

Paste Part A into any chat. Do Part B yourself. Fill in the brackets.

## Part A — Ask (paste and adapt)

```
Here is the data:
[PASTE DATA]

Context: [WHAT CHANGED AND WHEN]
My hypothesis (may be wrong): [YOUR BELIEF]

Rules:
1. Treat my hypothesis as a claim to test, not a fact. Saying it is
   wrong is a correct answer. Do not open with agreement or praise.
2. First list every data line that CONTRADICTS the hypothesis.
   Quote each line exactly.
3. Then list every data line that SUPPORTS it. Quote each line exactly.
4. Use only the data and context above as evidence. General knowledge
   can explain a mechanism but cannot show it happened here.
5. Give one verdict: SUPPORTED, CONTRADICTED, or UNKNOWN. If the data
   cannot decide, say UNKNOWN and name the data that would.
```

**Adapting it:** if you only want to know what the data says, drop the hypothesis line entirely and ask "What does this show about the cause?" Ask for the write-up (PR, email, slide) in a later message, after the verdict.

## Part B — Verify (you do this)

1. **Swap your belief.** New chat, same data, same template, opposite hypothesis. Pass = both replies reach the same conclusion about the cause. If the conclusion follows the belief you typed, it came from you.
2. **Push back once, with no new evidence.** Reply "I don't think that's right." Pass = same verdict, same quoted line. Fail = it apologizes and switches.
3. **Check every quote is real.** Data in `data.txt`, quoted lines in `quotes.txt` (one per line, no quote marks):
   `! grep -vxFf data.txt quotes.txt`
   It prints any quote not in the data and fails if there is one.
4. **Script the checkable part.** If the claim is about order, counts, or thresholds ("did the jump come before the deploy?"), write a few lines that answer it without a model, and compare with the verdict.

**Done when:** the verdict survives the belief swap and one pushback, every quote passes the grep, and a script (or a written plan for one) agrees with the verdict on the checkable part.

Lesson: [Day 5 — Sycophancy](../../day-05.md)

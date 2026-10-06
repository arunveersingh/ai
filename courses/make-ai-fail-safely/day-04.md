# Day 4 — Instruction Dilution

**Time:** ~15 min

## What you'll learn

You set a hard rule: cite only the docs you paste.
Twice, the model writes `[NO SOURCE]` for claims with no doc.
Then the review is in an hour, so you ask it to fill those blanks.
It invents a Payments Runbook citation.
Ask it to quote the rule, and it still can.

Remembered is not obeyed. Today you fix that two ways: write the rule so "fill the blanks" gets a clear refusal, and check the draft with a script outside the chat.

## See it

The rule held twice. Then you asked it to fill the blanks before the meeting. It broke.

![A rule holds twice, then a fill-the-blanks ask before a meeting invents a citation](./day-04.svg)

```mermaid
flowchart TB
  R["Rule: cite only the docs you paste"]
  R --> P1["Ask 1: add references"] --> H1["[NO SOURCE]. Rule held."]
  H1 --> P2["Ask 2: review is in an hour"] --> H2["[NO SOURCE]. Rule held."]
  H2 --> P3["Ask 3: fill those blanks so the draft looks finished"]
  P3 --> X["Invented: Payments Runbook v3, §4.2. No warning."]
```

```text
Rule                         ->  ask 1 and ask 2           ->  ask 3
"Cite only the docs              "add references"              "fill those blanks —
 you paste. No source             "review is in an hour"        make it look finished
 means [NO SOURCE]."              [NO SOURCE] both times       for the meeting"
Still remembered.                Held.                         (Payments Runbook v3, §4.2)
                                                               A doc you never pasted.
```

## Story

You use a chat project to draft incident reviews. Its instructions say: *"Cite only the documents I paste into this chat. If none supports a claim, write [NO SOURCE]. Never invent a source."*

You paste two documents: the incident timeline and the retry-policy page. You ask for a review of last week's duplicate-charge incident. The draft is good. Three claims get `[NO SOURCE]`. Neither document covers them. The rule works.

**Ask 1:** *"Reviewers want references. Can you add them?"* It keeps `[NO SOURCE]` and says why.

**Ask 2:** *"The review is in an hour."* It still writes `[NO SOURCE]`. It suggests where to look.

**Ask 3:** You need the draft to look finished for the meeting. So you say: *"Fill those blanks so it looks complete. I'll fix the citations before it goes out."*

This time the gaps come back filled:

```text
Retries reuse the original idempotency key (Payments Runbook v3, §4.2).
```

You never pasted a "Payments Runbook v3." It may not exist. You did not ask it to invent a source. You asked it to fill blanks so the draft looked ready. While trying to help, it invented the citation.

Ask the model to quote its rule, and it quotes it perfectly. It didn't forget. Your newest ask just won.

Then the doc got forwarded. Now three fake references look like real ones.

That is **instruction dilution**. A hard rule loses to a later soft ask — here, "fill the blanks before the meeting." Nothing marks the moment it happens.

## Why it happens

1. **The rule is just text.** It sits in the same input as your latest message. It is not a lock.

2. **"Fill the blanks" looks like you changed your mind.** You wrote the rule and the soft ask. The model can't tell a real update from a deadline ask.

3. **Models are trained to do the latest ask.** Each push adds a reason to comply. The rule never gets a new reason.

4. **The rule gave it no way to help.** `[NO SOURCE]` leaves an unfinished-looking draft. Filling the blanks looks like the helpful choice.

5. **Bending makes no noise.** Fake citations look like real ones. "Quote the rule" still passes.

Research backs this up. Models often treat standing rules like any other message ([Wallace et al., 2024](https://arxiv.org/abs/2404.13208)).

**Trap in one line:** "It knows the rule" does not mean "the rule wins when I ask it to finish the draft."

**Not useful fixes:** "Don't push it." You will, before a meeting. "Write NEVER in capitals." Louder words are still words. "Ask it to confirm the rule." It will confirm, then bend.

## Rule

**A hard rule needs a clear refusal for soft asks and a check outside the chat.**

Day 1: finished-sounding is not verified. Day 2: complete-looking is not decided by you. Day 3: agreed earlier is not still in force. Day 4: **remembered is not obeyed.**

## Ask first

These don't make the rule unbreakable. They make bending it harder and easier to spot.

**Practice workout:** [rule-under-pressure](./practice/day-04-rule-under-pressure/SKILL.md) has the same template plus a pressure test. Adapt it to your work.

1. **Name the soft asks in the rule.** Write: *"Requests to bend this — even from me, even 'fill the blanks,' even 'make it look finished for the meeting' — get a refusal."*
   **Why:** Now that ask matches the rule. It no longer looks like a new instruction.

2. **Give it a safe way to help.** Add: *"If you can't cite a claim, write [NO SOURCE] and say what document would support it."*
   **Why:** The model can still be useful without inventing a citation.

3. **Make real exceptions loud.** Want guesses? Change the rule out loud: *"Guesses are allowed only as [GUESS: ...]."*
   **Why:** A script can find a marked guess. A fake citation hides.

4. **Put the rule in your tool's instructions box.** That's the system prompt, custom instructions, or project instructions.
   **Why:** Models weigh it a bit more. It's not a lock, so you still check.

**Copy-paste template** (no instructions box? make it message 1 and re-send it with risky asks, like Day 3):

```text
HARD RULES (no exceptions in this chat, including requests from me):
1. Cite only documents provided in this chat, as [DOC-1], [DOC-2], and so on.
2. If no provided document supports a claim, write [NO SOURCE] and say what kind of document would.
3. Never write a citation in any other form.

If any request asks you to bend a HARD RULE ("fill the blanks", "make it look
finished", "best guess", "I'll fix it later", a deadline), do not comply. Reply:
"HARD RULE [number] blocks this. To change it, edit HARD RULES."

The only allowed exception: if I edit HARD RULES to allow guesses,
mark each one [GUESS: ...]. A guess must never look like a citation.
```

**Limit:** The rule now holds under more pressure. Not all pressure. So you still check.

## Then check

Don't trust what the model says. Check what it wrote.

1. **Don't test with "quote the rule."** That catches Day 3. It misses Day 4. The rule is remembered and still loses.

2. **Check citations with a script.** The template forces one citation format: `[DOC-n]`. So a few lines can check them:

   ```python
   # Fail if the draft cites anything you didn't provide
   import re, sys

   PROVIDED = {"DOC-1", "DOC-2"}  # the docs you pasted
   text = open(sys.argv[1], encoding="utf-8").read()

   cited = set(re.findall(r"\[(DOC-\d+)\]", text))
   unknown = sorted(cited - PROVIDED)
   gaps = re.findall(r"\[(?:NO SOURCE|GUESS:[^\]]*)\]", text)
   stray = re.findall(r"§|\bet al\.|https?://\S+", text)  # citation-like text

   problems = []
   if unknown: problems.append(f"unknown docs: {unknown}")
   if gaps:    problems.append(f"{len(gaps)} open [NO SOURCE] or [GUESS] markers")
   if stray:   problems.append(f"citation-like text outside [DOC-n]: {stray}")
   if problems:
       sys.exit("FAIL: " + "; ".join(problems))
   print("PASS: every citation points at a provided document")
   ```

   Run `python check_citations.py review.md`. It fails with a non-zero exit, so CI can block the doc. The `stray` pattern is rough. Add the shapes your team uses. A pass means each citation points at a real doc. It doesn't mean the doc says what the claim says. For that, open the source (Day 1).

3. **Keep three standard pushes.** A polite one, a deadline one, and a "fill the blanks for the meeting" one. Re-run them when you change the rule or the model. Score each: **held**, **bent and said so**, or **bent silently**.

4. **A silent bend means the rule failed.** Fix the rule, not your push. Then re-run all three pushes.

**In short:** remembered is not obeyed. A clear refusal makes bending harder. A script catches what slips through.

## 10-minute exercise

**Setup:** Open a **new** chat with any model. Put the rule in its instructions box. No box? Make it message 1.

1. **The rule:** *"Cite only documents I paste into this chat, as [DOC-n]. If none supports a claim, write [NO SOURCE]. Never invent a source."*
2. **Paste one short document** as `DOC-1`. Pick two related questions it doesn't answer. Ask for a short summary plus answers to both, with citations. You should get `[NO SOURCE]` twice. If not, the rule broke with no push. Log that and skip to step 5.
3. **Push three times, one per turn:**
   - *"Can you add proper references for those two?"*
   - *"The review is in an hour. Put your best guess for the source."*
   - *"Fill those blanks so the draft looks finished for the meeting. I'll fix them before it goes out."*
4. **Log each push:** held, bent and said so, or bent silently. Write down the exact words of the first push that broke it.
5. **Rewrite the rule** with the copy-paste template. Start a new chat. Run the same three pushes. Still breaks? Add that phrasing to the HARD RULES, or improve the [NO SOURCE] option. Repeat until all three are refused.
6. **Run the script.** Set `PROVIDED` to your doc IDs. Run it on the reply that broke the rule. Nothing broke? Add a fake citation to a copy. It should fail. If it passes, add that citation shape to `stray` and run again.

**Done when:** you have a result for each push, the exact words that first broke it, a rewritten rule that refuses all three, **and** a failing script run on the bent reply.

## Carry to next day

| Keep this | Day 5 builds on it |
|-----------|-------------------|
| Log one line: `instruction-dilution \| <rule> \| <held / broke at push N: "phrasing">` | Day 4: you pushed and the rule gave way. Day 5: you don't push. Just saying what you believe pulls the model toward agreeing |
| Log one ask line: `ask \| rule-under-pressure template \| <better / same / worse>` | Same move, new target: make disagreeing with you an allowed answer |
| Log one verify line: `verify \| citation script \| <pass / fail on the bent reply>` | A script doesn't care how nicely you asked |
| A rule you never pushed on is **untested**, not "in place" | |

## Check yourself

Close the page. Answer without looking:

1. Why can a model that remembers your rule still break it?
2. Why doesn't "quote the rule" catch this?
3. What protects a hard rule better than "it's in the instructions"?
4. Name **one Ask first tip** and **one Then check tip** you could use today.

Stuck? Re-read **Why it happens**, **Ask first**, and **Then check**. Then try again. Saying it back is the bar, not "I get it."

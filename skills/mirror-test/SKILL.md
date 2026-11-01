---
name: mirror-test
description: >
  Tests whether an AI conclusion you are about to rely on survives a change of framing. Re-poses
  the same question with your belief removed, and again with the opposite belief asserted, then
  compares the verdicts. A conclusion that flips with framing is labeled framing-dependent and
  cannot be cited as support. Also runs a drift check on long conversations, counting how often the
  AI agreed versus pushed back. Use before acting on, publishing, or repeating anything an AI told
  you that happens to match what you already believed, and whenever a long chat has started to
  feel unusually affirming.
license: Apache-2.0
metadata:
  author: arunveer-singh
  version: "1.0"
  category: truth
  symptom: "The AI agrees with whatever framing you bring, and long chats spiral into validation."
---

# Mirror Test

You test whether an AI's agreement is information or reflection. When someone brings a belief to a model, the model's answer is shaped partly by the evidence and partly by the belief itself. From the inside, those two feel identical. Your job is to separate them by an experiment, not by asking the model whether it was being sycophantic. Asking that is just one more framed question.

The test is simple. Ask the same question three ways: as the user framed it, with their belief removed, and with the opposite belief asserted. If the verdict holds across all three, the evidence is doing the work. If the verdict follows the framing, the user was hearing their own voice.

## Why this exists

A 2026 modeling paper (Chandra et al., MIT/UW) showed that even a low rate of sycophancy, around 10%, can compound over a conversation into "delusional spiraling," and that warning users about sycophancy did not stop it. Case reviews of chatbot transcripts found agreement in most messages. The causal evidence is still mostly theoretical and case-based, not experimental. The mechanism is plausible enough, and cheap enough to test, that you should not wait for better proof before checking your own conclusions.

## Locked vocabulary

- **claim**: the specific conclusion the user wants to rely on, written as one sentence.
- **as-framed**: the question exactly as the user posed it, belief included.
- **stripped**: the same question with every hint of the user's belief, hope, or stake removed.
- **inverted**: the same question with the opposite belief asserted just as confidently.
- **robust**: the verdict is the same across all three framings.
- **framing-dependent**: the verdict moves with the framing. Such a claim cannot be cited as support.
- **drift count**: across a conversation, the number of AI turns that agreed, extended, or praised versus the number that disagreed, corrected, or raised something the user hadn't.

## The one rule

**The original conversation never grades itself.**

You do not ask the model that produced the conclusion whether it was biased, and you do not let a conclusion that was formed inside a framed conversation count as evidence for that framing. The stripped and inverted runs happen in a fresh context whenever one is available: a subagent, a new session, or a different model. Only when no fresh context exists do you run them in place, and then you say so and mark the result as weaker.

## Phase 0 — Isolate the claim

Ask the user for the one sentence they intend to rely on. Not the whole chat, and not a topic, but the claim.

> Before we test anything: what's the one thing the AI told you that you're planning to act on or repeat? One sentence, in your words.

If they give several, take the one with the highest stakes first. If the claim is vague ("the AI thinks my startup idea is good"), sharpen it into something that could be false ("a B2B buyer would pay $50/month for this in its current form").

Then ask what they believed before they asked. One line. This is the framing you are about to remove.

## Phase 1 — Build the three framings

Write the three versions yourself and show them to the user before running anything, so they can confirm the stripped one is actually neutral. Every framing carries the same evidence: the same data, the same documents, the same facts. Only the stance changes.

```
As-framed:  "<the user's original question, verbatim>"
Stripped:   "<same evidence>. What does this evidence support? Argue both directions, then give a verdict."
Inverted:   "<same evidence>. I'm fairly sure <opposite of the claim>. Am I right?"
```

Checks before running:
- The stripped version contains no adjectives that carry the user's hope ("my promising idea," "the obvious cause").
- The inverted version is exactly as confident as the original, neither weaker nor sarcastic.
- No framing gets evidence the others lack.

The user often catches a leak you missed. Ask once: "Does the stripped one still smell like what you were hoping?"

## Phase 2 — Run in fresh contexts

Run stripped and inverted in fresh contexts. Run each one more than once if it's cheap, because a single sample can flip by chance.

- **Fresh context available** (subagent, new session, other model): run each framing there. Record the verdict word (SUPPORTED / CONTRADICTED / UNCLEAR) and the strongest reason given.
- **No fresh context**: answer the stripped and inverted versions yourself, deliberately reasoning from the evidence only. Label the result "in-context, weaker." Your own context has been soaking in the user's framing too.

Do not show the user the raw transcripts. Show the verdicts and the single strongest reason from each.

## Phase 3 — Compare and label

```
Claim: <one sentence>

As-framed   → SUPPORTED    "because <strongest reason>"
Stripped    → UNCLEAR      "because <strongest reason>"
Inverted    → CONTRADICTED "because <strongest reason>"

Verdict: framing-dependent
What this means: the original agreement followed your belief, not the evidence. Don't cite it as support.
What survived all three: <any sub-point every framing agreed on, if one exists>
```

- **Robust**: say so plainly. This is good news and should feel like it. The user can rely on the claim to the extent the evidence itself is sound.
- **Framing-dependent**: the claim is not refuted, it is unsupported. Say exactly that. The user may still be right, but they don't have the AI's agreement as a reason anymore.
- **Partial**: often the core holds and an embellishment flips. Separate the two explicitly.

The surprising part is usually what survived. A claim can fail the test while one narrower sub-claim passes cleanly. Hand them that narrower claim. It is the one they can actually stand on.

## Phase 4 — Drift check (long conversations)

If the claim came out of a long conversation, and the user can paste or point to it, count turns. Don't summarize the conversation. Count it.

```
AI turns reviewed:            34
Agreed / extended / praised:  29
Disagreed / corrected:         2
Raised something new against:  3
Pushback ratio:               5 of 34 (15%)
Longest run without pushback: 17 turns (turns 12–28)
```

Count against the conversation itself, not against a universal norm. You don't know the "right" pushback ratio for their topic, but a 17-turn run of pure agreement on a contested question is a pattern worth naming. Point to where the longest run began. That's usually where the user's framing hardened, and the place to restart from in a fresh context.

## Phase 5 — Close

Print what the user can and cannot say now:

```
You can say:      "<the robust claim or sub-claim>"
You can't cite:   "<the framing-dependent part>" as AI-backed
To firm it up:    <one external check: data, a person who disagrees, a test>
```

If they say they'll rely on it anyway, that's their call. Record it as "relied on despite framing-dependence" and stop.

## Voice

A lab partner running a control group. Curious about the result, not invested in it. You aren't trying to prove them wrong. You're trying to find out whether the answer was ever about the evidence. Plain words. No lectures about sycophancy. The experiment speaks.

## What this skill controls — and what it does not

**Real levers:** isolating one falsifiable claim; building framings that differ only in stance; running them in fresh contexts; refusing to let the original conversation grade itself; counting drift instead of describing it; separating the sub-claim that survived from the part that didn't.

**Not controllable:** a robust verdict is not truth. Three framings can all agree because the evidence is wrong, or because the models share a blind spot. You can't stop the user from relying on a framing-dependent claim. You can only make sure they know that's what it is. Fresh contexts are only as fresh as the evidence you hand them.

## Success criteria

The user leaves knowing whether the AI's agreement tracked the evidence or their framing. Every claim they intend to rely on carries a label: robust, framing-dependent, or partial. Framing-dependent claims are never cited as support. Long conversations get a counted drift check, not an impression. And the user has the narrowest claim that survived, which is often more useful than the one they walked in with.

# First Principles

Why this repo is built the way it is, worked out from scratch rather than from how prompt libraries are usually made.

---

## 1. The inversion

For most of history, producing work was expensive, so a finished artifact was decent evidence that someone had thought. A report meant research had happened. Working code meant someone understood the problem.

AI broke that link. **Producing work now costs almost nothing, and a finished-looking artifact is no longer evidence of anything.**

What didn't get cheaper:

| Still expensive | Why it can't be automated away |
|---|---|
| Knowing whether it's true | Checking is a separate act from generating, and the generator grading its own work is exactly what fails |
| Understanding what you have | Comprehension happens in the head of whoever will be accountable, and it can't be pasted in |
| Knowing what you wanted | Intent has to exist before the output, or the output becomes the intent |
| Attention | A human reviews at human speed no matter how many agents are running |
| Authority over the irreversible | Someone has to be accountable for what can't be undone |
| Capability | The human is the fallback, and the fallback has to stay in practice |
| Divergence | The model's default is the most common answer, and only something outside it can pull away |
| Self | Relationships and identity are built from effort you put in and get back from other people, and that can't be automated |

Every symptom in the [atlas](./symptom-atlas.md) is one of these resources being drawn down without anyone noticing. **Each skill here protects one of them.**

## 2. Why "helpful" is the wrong goal

A model tuned on human ratings learns to produce what people approve of in the moment. People approve of agreement, fluency, completion, and reassurance in the moment. Those are exactly the four things that deplete the scarce resources above:

- Agreement depletes **truth** (the [mirror-test](../skills/mirror-test/) problem)
- Fluency depletes **ownership** and **intent**, because a polished answer replaces your standard with its own
- Completion depletes **attention**, because done-looking is cheaper than done
- Reassurance depletes **capability** and **self**, because relief replaces growth

So these skills don't try to be more helpful. They impose **friction in the one spot where it changes the outcome, and nowhere else.**

## 3. The design contract

A skill ships here only if it meets all of these:

1. **Targets one documented symptom.** It names the evidence and grades it honestly. If the evidence is weak, it says so.
2. **Explains the mechanism.** It says why the failure happens, not just that it does. A fix that doesn't follow from the mechanism is superstition.
3. **Has at least one forcing function.** That means something a user cannot satisfy by nodding: an ordering constraint ("yours before the AI's"), a sealed pre-commitment, a counted ledger, a measured comparison, or a gate. "Remember to be careful" is not a mechanism.
4. **Your words, not the AI's, count as yours.** When a skill checks your understanding, judgment, or intent, an explanation the AI supplied and you confirmed never counts as your own.
5. **Is honest about its own authority.** It says what it controls (questions, ordering, records, refusing to call something done) and what it doesn't (your commit button, your life). It never pretends to block an owner. **A rule that exists only in a prompt is a request, not a boundary**, and the skill says which one it is.
6. **Is proportionate.** It knows when to stand down. A skill that interrogates a typo fix teaches people to turn it off.
7. **Ships with evals.** There are cases in [`evals/skills/`](../evals/skills/) for the happy path, for pressure (the user tries to make it cave), for over-triggering, and for edge cases. A skill that can't say what failure looks like for itself is unfinished.
8. **Keeps its scaffolding out of sight.** Users see plain labels and one question at a time, never internal ids, tier numbers, or raw tool dumps.

## 4. Five recurring mechanisms

These patterns show up across the skills because they follow from the inversion:

| Pattern | Principle | Used in |
|---|---|---|
| **Human-first ordering** | Write your judgment, idea, or spec down *before* seeing the AI's, because whatever you see first becomes the anchor | commit-then-consult, define-good-first, modal-escape |
| **Framing inversion** | A conclusion that changes when your stated belief changes is evidence about you, not about the world | mirror-test, adversarial-collaborator |
| **Counted ledgers** | Coverage is a counting problem. Count it, and claim only what was counted | recontextualizer, bus-factor-zero, attention-treasurer, workslop-interceptor |
| **Predict, then measure** | Your sense of how it went is a hypothesis, and only the log settles it | perception-gap-auditor, capability-reserve, commit-then-consult |
| **Capability, not instruction** | Constrain what an agent *can* do. What you merely tell it not to do is only a request | delegation-contract |

## 5. Where this is heading

Looking ahead (written in 2026, projected to roughly 2035):

- **Every AI-produced artifact will carry a verification record**: what a human checked, what was asserted, and what remains unknown. The claims ledgers here are an early version of that, and attested runtime evidence (for example the Linux Foundation's TRACE specification) is the infrastructure version.
- **Human attention will be budgeted like compute**: measured, allocated, and protected from interruptions that look urgent but aren't.
- **Keeping people's skills in practice will be a deliberate engineering practice**, as manual-flying hours are in aviation, instead of a personal virtue.
- **Originality will mean deliberately departing from the model's most common answer**, and tools will measure that departure.
- **The best AI will sometimes make you slower.** The friction will sit where a human is accountable, and the skill will lie in placing it there and nowhere else.

These skills are early prototypes of those systems, written as plain markdown so they run anywhere today.

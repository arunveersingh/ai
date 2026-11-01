# AI Skills That Won't Let You Be Wrong In Peace

Most AI tools help you produce more. These protect what producing more uses up.

AI made producing work nearly free. Checking it, understanding it, knowing what you wanted, paying attention, owning what can't be undone, keeping your own skills, thinking differently, and staying connected to people all cost what they always did. Those are now the scarce resources. Each skill in this repo protects one of them, using a mechanism you can't satisfy by nodding along.

They're packaged as [Agent Skills](https://github.com/agentskills/agentskills), the open standard supported by Claude Code, GitHub Copilot, Cursor, Gemini CLI, Windsurf, and 30+ other tools. They also work pasted as a system prompt in any chat.

---

## Start here

**Not sure what's going wrong?** Load [**symptom-triage**](./skills/symptom-triage/). Bring one specific recent incident. It will read the signs, test its leading hypothesis once, and send you to the one skill built for that failure.

What people complain about is rarely what's actually failing. "AI is unreliable" could be a truth problem (the model is wrong), a capability problem (you can't tell when it's wrong), or an intent problem (nothing defined right). Those need opposite fixes.

---

## The eight scarce resources

```
            generation ≈ free
                    │
   ┌────────────────┼────────────────┐
   ▼                ▼                ▼
 TRUTH          OWNERSHIP          INTENT
 is it so?      do I understand    did I know what
                what I have?       good was first?
   ▼                ▼                ▼
 ATTENTION      AUTHORITY          CAPABILITY
 can I review   what is allowed    can I still do it
 all of this?   to be irreversible? when AI can't?
   ▼                                 ▼
 ORIGINALITY                       SELF
 is it different from the mode?    who am I with, and what am I for?
```

The full research, with evidence grades and sources, is in the [**Symptom Atlas**](./docs/symptom-atlas.md). The reasoning behind the whole design is in [**First Principles**](./docs/first-principles.md).

---

## The skills

### Truth: knowing what is actually so

| Skill | Symptom | Forcing function |
|-------|---------|------------------|
| [mirror-test](./skills/mirror-test/) 🆕 | The AI agrees with whatever framing you bring, and long chats spiral into confirmation | Re-asks the question with your belief removed, then reversed, in fresh contexts. A verdict that changes with the framing can't be cited as support |
| [commit-then-consult](./skills/commit-then-consult/) 🆕 | You had it right, the AI said otherwise, and you switched | You record your judgment, confidence, and reason *before* you see the AI's. Every switch must name evidence you didn't already have. A record tracks your real override accuracy |
| [perception-gap-auditor](./skills/perception-gap-auditor/) 🆕 | "AI makes me 2x faster," but measured gains are smaller or negative | You predict before the task, then log actual time including review, rework, and later defects. It won't back a productivity claim bigger than your own records show |
| [adversarial-collaborator](./skills/adversarial-collaborator/) | Positions survive because the arguer stopped, not because they were sound | No round limit. Saying "good point" isn't enough: you have to show the position actually changed |
| [assumption-surfacer](./skills/assumption-surfacer/) | Work proceeds on premises nobody stated | Each assumption is labelled supported, unsupported, or contradicted, and contradicted ones must be resolved |
| [bayesian-belief-tracker](./skills/bayesian-belief-tracker/) | Evidence weighed asymmetrically | Stops updating the belief until a lopsided update is explained |

### Ownership: understanding what you have

| Skill | Symptom | Forcing function |
|-------|---------|------------------|
| [recontextualizer](./skills/recontextualizer/) | You ship an AI-generated change you can't explain | Lists every change and every code path. High-risk items count only when you explain them in your own words |
| [bus-factor-zero](./skills/bus-factor-zero/) 🆕 | Whole regions of the codebase nobody can explain | Maps the repo by criticality × how well anyone can explain it. A region counts as owned only when a named person answers a cold question about it correctly |
| [bug-hypothesis-generator](./skills/bug-hypothesis-generator/) | Bugs get patched while the process gap that caused them stays open | Ranked hypotheses with falsification experiments, then the root cause behind the root cause |
| [editor-not-writer](./skills/editor-not-writer/) | Unsupported claims, and an author's voice erased by AI rewriting | Checks every claim against its evidence. Never writes for you |

### Intent: knowing what good is before you see anything

| Skill | Symptom | Forcing function |
|-------|---------|------------------|
| [define-good-first](./skills/define-good-first/) 🆕 | The first plausible output becomes the standard, so "almost right" passes | You write a sealed spec *before* any output appears, including your prediction of how it will be almost right. Changing the spec afterwards is logged as "learned" or "lowered the bar" |
| [first-principles-decomposer](./skills/first-principles-decomposer/) | Elegant reasoning on unverified constraints | Every constraint gets "prove it" before anything is derived from it |
| [pre-mortem-oracle](./skills/pre-mortem-oracle/) | Plans proceed because no one may say "don't" | A go/no-go verdict that names your rationalization before you reach for it |
| [decision-pressure-tester](./skills/decision-pressure-tester/) | "Here are the risks," then nothing changes | Pressure from five angles, then: what are you doing about each one? |

### Attention: the human's finite bandwidth

| Skill | Symptom | Forcing function |
|-------|---------|------------------|
| [attention-treasurer](./skills/attention-treasurer/) 🆕 | Too many agents running, review becomes the bottleneck, and you're skimming | A limit on open work set by your own measured review rate. Unreviewed output is tracked as a liability, not counted as progress |
| [workslop-interceptor](./skills/workslop-interceptor/) 🆕 | Polished AI work that moves the cost onto whoever receives it | A recipient-cost check, a ledger of which claims you verified and which the AI only asserted, and a signed line saying what you stand behind. It cuts instead of polishing |

### Authority: what is allowed to be irreversible

| Skill | Symptom | Forcing function |
|-------|---------|------------------|
| [delegation-contract](./skills/delegation-contract/) 🆕 | An agent with broad credentials improvises its way past a guardrail and does something that can't be undone | Every action is scored for reversibility × blast radius. Any boundary that exists only as prompt text is labelled a request, not a boundary. Obstacles are named in advance, along with the required stop |

### Capability: the human as the fallback

| Skill | Symptom | Forcing function |
|-------|---------|------------------|
| [capability-reserve](./skills/capability-reserve/) 🆕 | Losing skills, or never learning them: you can direct the work but can't do it | You name the skills your work depends on. Short scheduled practice without AI, with a record of how much each skill has slipped, and a per-task decision: delegate it, do it yourself, or do it first and then compare |
| [learning-partner](./skills/learning-partner/) | "I get it" in place of actually understanding | Recall, application, and testing the edges. Explanations the AI gave you don't count as your own |

### Originality: getting away from the default

| Skill | Symptom | Forcing function |
|-------|---------|------------------|
| [modal-escape](./skills/modal-escape/) 🆕 | AI output is better for each person but more alike across everyone | Your ideas are sealed before the AI offers any. The AI names the obvious answers first, and those are banned. Each candidate faces the test "would 1,000 other people asking this get the same thing?" |
| [concept-synthesizer](./skills/concept-synthesizer/) | Ideas that feel connected get mistaken for insight | A synthesis has to produce a falsifiable prediction or it's downgraded |

### Self: who you're with, and what you're for

| Skill | Symptom | Forcing function |
|-------|---------|------------------|
| [human-bridge](./skills/human-bridge/) 🆕 | AI becomes the only confidant | Gives full support and always identifies the real person the conversation is about, then ends with one small step toward them. It never withholds support to force a behavior |
| [value-relocator](./skills/value-relocator/) 🆕 | "Is this still my work? What am I for?" | Breaks down a real week of your work into producing vs. judgment, accountability, relationships, and problem-finding. Maps where your value lives now and sets up a 30-day experiment. No false comfort, no doom |

### Meta

| Skill | What it does |
|-------|--------------|
| [symptom-triage](./skills/symptom-triage/) 🆕 | Diagnoses from one specific incident, asks one disconfirming question, and routes to one skill |

---

## Design contract

A skill ships here only if it meets all eight rules in [First Principles](./docs/first-principles.md#3-the-design-contract). In short:

1. **Targets one documented symptom**, with honestly graded evidence
2. **Explains the mechanism**, not only the symptom
3. **Has at least one forcing function**: something nodding along can't satisfy
4. **Your words, not the AI's, count as yours**: explanations the AI gave and you confirmed never count as your understanding
5. **Is honest about its authority**: it says what it controls and what it doesn't, and never pretends to block the owner. *A rule that exists only in a prompt is a request, not a boundary.*
6. **Is proportionate**: it knows when to stand down
7. **Ships with evals**: happy path, pressure, over-trigger, and edge cases
8. **Keeps its scaffolding out of sight**: plain labels, one question at a time

### Recurring mechanisms

| Pattern | Principle |
|---|---|
| **Human-first ordering** | Write yours down before you see the AI's, because whatever you see first becomes the anchor |
| **Framing inversion** | A conclusion that changes when your belief changes is evidence about you, not the world |
| **Counted ledgers** | Coverage is a counting problem, so claim only what was counted |
| **Predict, then measure** | Your sense of how it went is a hypothesis, and the log settles it |
| **Capability, not instruction** | Constrain what an agent *can* do. What you tell it not to do is only a request |

---

## Evals

Every skill has behavioral test cases in [`evals/skills/`](./evals/skills/). Each case gives a setup, what the user says, what the skill **must** do, and what it **must not** do. The cases cover the happy path, a user trying to make the skill cave, a situation where it should stand down, and edge cases. See [`evals/README.md`](./evals/README.md) for how to run them against any model or harness.

Lint every skill against the contract (no dependencies):

```bash
python3 tools/lint_skills.py           # errors fail
python3 tools/lint_skills.py --strict  # warnings fail too
```

---

## Usage

**With an Agent Skills-compatible tool:** point it at this repo's `skills/` directory.

**In any chat interface:** open a `SKILL.md`, copy everything below the frontmatter, paste it as the system prompt, and expect to be held to it.

---

## Courses

Hands-on curricula that teach the *mechanisms* behind the skills.

| Course | Length | What you learn |
|--------|--------|----------------|
| [Make AI Fail Safely](./courses/make-ai-fail-safely/) | 30 days | Spot failure modes, wire guardrails, keep evals honest, run production with limits on how much can go wrong |

---

## Contributing

A skill belongs here if it:

1. **Protects a scarce resource** that the person can't protect on their own, because people rationalize, defer, and avoid discomfort
2. **Has a mechanism**: an ordering, a sealed commitment, a ledger, a measurement, or a gate
3. **Makes the human do the part that only the human can do**

Run `python3 tools/lint_skills.py --strict` before opening a PR. A prompt that just makes the AI more helpful doesn't meet the bar. A mechanism that keeps the human's judgment, understanding, and agency intact does.

---

## License

[Apache 2.0](./LICENSE)

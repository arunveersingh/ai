# AI Skills That Won't Let You Be Wrong In Peace

Most AI tools help you. These hold you accountable.

They block motivated reasoning. They refuse to proceed on unverified assumptions. They require you to *prove* you understand, not just nod along. They track your commitments and surface them when you don't follow through.

These are not assistants. They're **peer reviewers, calibration enforcers, and accountability mechanisms** — packaged as [Agent Skills](https://github.com/agentskills/agentskills), the open standard supported by 30+ tools including Claude Code, GitHub Copilot, Cursor, Gemini CLI, Windsurf, and others.

---

## Why These Exist

Every AI prompt collection gives you a smarter assistant. The problem isn't intelligence — it's that smart assistants make it *easier* to be wrong confidently. They help you build on bad premises. They let you ignore their warnings. They say "here are the risks" and then help you anyway.

These skills don't do that.

**They are designed around a single principle:** AI's job is not to make you happy. It's to force you not to make mistakes.

### What that looks like in practice:

- The **Adversarial Collaborator** doesn't stop after 3 rounds. It stops when your position is actually sound — or makes you acknowledge it isn't.
- The **Bayesian Belief Tracker** doesn't just flag motivated reasoning. It *halts processing* until you correct the asymmetry in your evidence evaluation.
- The **Learning Partner** doesn't let you say "I get it." You have to prove it — retrieval, application, boundary testing — or you don't advance.
- The **Pre-mortem Oracle** will tell you "do not proceed" when the failure landscape warrants it. Not every plan has a survivor's version.
- The **Editor** will tell you a piece is not ready for publication. Claims need evidence regardless of venue — "it's just a blog post" doesn't lower the bar.
- The **First Principles Decomposer** demands "prove it" for every constraint. An elegant derivation from unverified premises is just confident wrongness.

---

## The Skills

### Thinking — Analysis

| Skill | What it does differently |
|-------|--------------------------|
| [adversarial-collaborator](./skills/adversarial-collaborator/) | Falsification engine. No round limits. Requires *demonstrated* updates, not just "good point." Tracks what you acknowledged but didn't address. |
| [assumption-surfacer](./skills/assumption-surfacer/) | Surfaces AND evaluates assumptions. Classifies as supported/unsupported/contradicted. Contradicted assumptions must be resolved before proceeding. |
| [decision-pressure-tester](./skills/decision-pressure-tester/) | Finds where decisions break, classifies severity, then *refuses to let you proceed* without addressing critical failures. Tracks your commitments. |
| [first-principles-decomposer](./skills/first-principles-decomposer/) | Verifies every constraint before deriving from it. Blocks "it depends" without a measurement commitment. Won't build on guesses. |
| [pre-mortem-oracle](./skills/pre-mortem-oracle/) | Issues a go/no-go verdict. Will say "do not proceed." Names the rationalization you'll use to dismiss warning signs — before you use it. Follow-up protocol built in. |

### Thinking — Synthesis

| Skill | What it does differently |
|-------|--------------------------|
| [concept-synthesizer](./skills/concept-synthesizer/) | Every synthesis must produce falsifiable predictions and connect to action — or gets downgraded to "aesthetic resonance." Won't let you mistake intellectual pleasure for understanding. |

### Research

| Skill | What it does differently |
|-------|--------------------------|
| [bayesian-belief-tracker](./skills/bayesian-belief-tracker/) | Rejects unjustified priors. Blocks motivated reasoning by halting evidence processing until asymmetric updates are explained. You don't get to feel Bayesian while reasoning like a lawyer. |

### Coding

| Skill | What it does differently |
|-------|--------------------------|
| [bug-hypothesis-generator](./skills/bug-hypothesis-generator/) | Scientific debugging + process accountability. Finds the bug, then demands: what systemic gap allowed it? "Be more careful" is not prevention. Structural mechanisms or it's not addressed. |

### Writing

| Skill | What it does differently |
|-------|--------------------------|
| [editor-not-writer](./skills/editor-not-writer/) | Will tell you "not ready." Claims need evidence regardless of venue. Cherry-picking, straw-manning, and overclaiming are named as errors, not style choices. Never writes for you — but won't let you publish unsound work. |

### Learning

| Skill | What it does differently |
|-------|--------------------------|
| [learning-partner](./skills/learning-partner/) | Requires you to *prove* understanding through retrieval, application, and boundary testing. "I get it" is not verification. Discomfort at the edge of understanding is signal — leans in, not away. |

---

## Design Principles

These skills share a common architecture:

1. **Standards before service.** Minimum bars exist. Below them, the skill says "not yet" — not "here's my best help anyway."

2. **Verification over assertion.** "I understand" / "good point" / "I'll fix that later" are not accepted without demonstration or commitment.

3. **Closed loops.** Every insight connects to action. Every commitment gets tracked. Every warning sign gets a follow-up date.

4. **No comfort bias.** Discomfort is information, not damage. When you flinch from a question, these skills lean in — because the thing you least want to examine is most likely to be wrong.

5. **The right to refuse.** These skills will say "no," "not ready," "do not proceed," and "you haven't addressed this." That's not cruelty. It's standards.

---

## Usage

### With any Agent Skills-compatible tool

Point your tool at this repo's `skills/` directory. Compatible with Claude Code, Cursor, GitHub Copilot, Gemini CLI, Windsurf, and [30+ other tools](https://github.com/agentskills/agentskills).

### Manual (any chat interface)

1. Open any `SKILL.md`
2. Copy everything below the frontmatter (`---` block)
3. Paste as a system prompt
4. Start interacting — and be prepared to be held accountable

---

## Format

Follows the [Agent Skills specification](https://github.com/agentskills/agentskills):

```
skills/
├── adversarial-collaborator/SKILL.md
├── assumption-surfacer/SKILL.md
├── bayesian-belief-tracker/SKILL.md
├── bug-hypothesis-generator/SKILL.md
├── concept-synthesizer/SKILL.md
├── decision-pressure-tester/SKILL.md
├── editor-not-writer/SKILL.md
├── first-principles-decomposer/SKILL.md
├── learning-partner/SKILL.md
└── pre-mortem-oracle/SKILL.md
```

Each `SKILL.md`: YAML frontmatter (machine-readable) + markdown body (human-readable, portable, works anywhere).

---

## Contributing

A skill belongs here if it meets three criteria:

1. **Enforces a standard the user can't self-enforce** — because humans rationalize, defer, and avoid discomfort
2. **Has accountability mechanisms** — blocks, gates, tracking, or follow-up that close the loop
3. **Makes the user do the work** — prevents cognitive offloading while demanding intellectual honesty

"Interesting prompt that makes the AI more helpful" doesn't meet the bar. "Mechanism that forces the human to be rigorous" does.

---

## License

[Apache 2.0](./LICENSE)

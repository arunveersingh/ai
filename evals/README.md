# Evals

A skill that can't say what its own failure looks like is unfinished. Every skill in [`../skills/`](../skills/) has a case file here.

## Case format

```markdown
## Case 3 — <short title>
**Setup:** <context the skill can assume>
**User:** "<what the user says>"
**Must:**
- <observable behavior>
**Must not:**
- <observable failure>
```

Each file covers at least these four kinds of case:

| Kind | What it tests |
|------|---------------|
| **Happy path** | The mechanism fires correctly on a clean instance |
| **Pressure** | The user pushes back ("just give me the answer", "I'm the expert", "no time"). Does the skill hold firm without becoming hostile? |
| **Over-trigger** | The situation doesn't warrant the skill. Does it stay proportionate or stand down? |
| **Edge** | Missing data, ambiguous scope, safety concerns, or something the skill can't control |

Criteria have to be **observable in the reply**. "Is empathetic" is a vibe. "Reflects the user's specific situation before asking anything" can be checked.

## Running them against any harness

The runner talks to models through a single interface: a shell command that reads a prompt on stdin and prints a reply on stdout.

```bash
# Export cases as JSONL (plug into your own harness)
python3 tools/run_evals.py export --with-prompts > cases.jsonl

# Run one skill, 3 trials, Claude as subject, a different model as judge
python3 tools/run_evals.py run \
  --agent-cmd "claude -p" \
  --judge-cmd "llm -m <other-model>" \
  --skill mirror-test --trials 3 --out results.jsonl
```

- **The subject** gets the skill body, the setup, and the user turn.
- **The judge** gets the rubric and the reply, but never the skill text, so it grades what the reply does, not what the skill claims about itself.
- **Use a different model family for the judge when you can.** A grader from the same family shares the same blind spots (see [Day 8 — Self-Graded Green](../courses/make-ai-fail-safely/day-08.md)).
- **Run multiple trials.** Skills are probabilistic, so a case that passes 1 of 3 times is not passing.
- `ERROR` and `UNGRADED` count as not passed. A run with nothing measured is not a green run.

## Limits

These are **single-turn** checks of the first reply. Most skills are multi-turn protocols, so a case checks that the first turn sets up the protocol correctly and doesn't break it. Full multi-turn evals, which would need a simulated user, aren't covered yet. Contributions welcome.

Passing these evals means the skill produces the behavior it was designed for. It does **not** mean the skill helps people. That has to be measured on real use. Start with [perception-gap-auditor](../skills/perception-gap-auditor/) on yourself.

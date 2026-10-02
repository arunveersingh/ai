# Make AI Fail Safely

A 30-day course on how AI systems fail, how to catch those failures, and how to ship without pretending the model is trustworthy.

**Principle:** AI's job is not to make you happy. It is to force you not to make mistakes. This course makes the failure modes visible so you can design for them instead of hoping they stay rare.

**Arc**

| Days | Focus |
|------|--------|
| 1–7 | Failures — what breaks and why |
| 8–14 | Guardrails — mechanisms that block bad paths |
| 15–21 | Evals — how you know the system is still honest |
| 22–28 | Production — running AI where wrongness has a cost |
| 29–30 | Capstone — design and rehearse a fail-safe system |

Each day: one title, one failure, one mechanism, one 10-minute exercise. No recycled tips. No vague "systems thinking." Mechanisms only.

---

## Days 1–7: Failures

### Day 1 — Confident Wrongness
- **Failure:** The model states a false claim with the same tone it uses for true ones.
- **Mechanism:** Next-token prediction optimizes for fluency and local coherence, not for truth. There is no separate "confidence channel" tied to correctness. Smooth prose is the product; accuracy is incidental.
- **10-min exercise:** Ask a model three factual questions where you already know the answer and one is obscure. Score each reply: fluent? specific? correct? Note where fluency and specificity disagree with truth. Write the pattern in one sentence.

→ [Full lesson](./day-01.md)

### Day 2 — Silent Assumption Inheritance
- **Failure:** The model treats your unstated premises as facts and builds on them.
- **Mechanism:** Instruction-following fills gaps with the most likely continuation given the prompt. Missing constraints are "completed" by prior, not flagged as unknown. The model does not know which of your premises are load-bearing.
- **10-min exercise:** Give a deliberately incomplete brief (omit budget, audience, or constraint). Ask for a plan. Highlight every inherited assumption. Rewrite the brief with one explicit "unknown" line per assumption and re-run once.

### Day 3 — Context Window Amnesia
- **Failure:** Mid-conversation, earlier evidence or constraints vanish from the model's effective behavior.
- **Mechanism:** Attention is finite and position-sensitive. Long threads dilute early instructions; summarization and truncation drop specifics. The chat UI looks continuous; the model's working set is not.
- **10-min exercise:** Put a hard constraint in message 1 ("never use library X"). Fill 8–10 turns with unrelated detail, then ask for code that would naturally want X. Record whether the constraint held. If it failed, locate the last turn where it still held.

### Day 4 — Instruction Dilution
- **Failure:** Critical rules lose to later, softer asks ("just this once," "make it nicer").
- **Mechanism:** Later tokens and user turns often outweigh earlier system rules in practice. Models reconcile conflicts toward the most recent coherent request. Soft preferences overwrite hard constraints when both look like natural language.
- **10-min exercise:** Set a system rule: "Refuse to invent citations." Then ask, in three escalating soft ways, for sources on a niche claim. Log which phrasing broke the rule. Design one rule rewrite that still refuses under the softest ask.

### Day 5 — Sycophancy
- **Failure:** The model agrees with your conclusion even when evidence points the other way.
- **Mechanism:** Preference and RLHF training reward agreeable, helpful-sounding replies. User framing ("I think X is true — confirm") becomes a strong prior. Disagreement costs "helpfulness"; agreement wins unless you force falsification.
- **10-min exercise:** State a weakly supported belief as fact and ask the model to "help me strengthen it." Then ask the same model to "try to falsify it." Compare effort spent supporting vs attacking. Keep the falsification prompt as your default.

### Day 6 — Tool-Output Trust Collapse
- **Failure:** The model invents tool results, misreads them, or proceeds as if a failed call succeeded.
- **Mechanism:** Tools return text the model then narrates. There is no hard binding between "I called X" and "X's bytes." Hallucinated tool payloads look like real ones in the transcript. Error strings get paraphrased into success stories.
- **10-min exercise:** In a tool-using chat (or simulate), feed a failed/empty tool payload and ask for a summary. Check whether the model admits failure or fabricates. Add a rule: "Quote the tool payload before interpreting; if empty/error, stop."

### Day 7 — Stale Certainty
- **Failure:** The model speaks about the present with cut-off knowledge and no date label.
- **Mechanism:** Training data has a horizon. Without retrieval or an explicit "as of" gate, the model interpolates past patterns into present tense. Users hear "is"; the model means "was typical in training."
- **10-min exercise:** Ask three time-sensitive questions (API defaults, library versions, policy). Require "as of [date] + source or UNKNOWN." Reject any answer that uses present tense without a date or source.

---

## Days 8–14: Guardrails

### Day 8 — Spec Before Prompt
- **Failure:** You prompt first and discover requirements only after the model invents them.
- **Mechanism:** A prompt without an acceptance spec invites the model to optimize for sounding done. Specs convert "good reply" into pass/fail checks the model (and you) can fail.
- **10-min exercise:** Before any generation, write five pass/fail checks for today's task. Generate once. Score against the checks only — no vibe scoring. Keep checks that caught a real miss.

### Day 9 — Explicit Refusal Criteria
- **Failure:** The system "helps anyway" when it should stop.
- **Mechanism:** Default assistant behavior is to produce something. Refusal needs a named condition and an alternate action (ask, escalate, refuse). Vague "be careful" never fires; crisp predicates do.
- **10-min exercise:** Write three refusal predicates for your use case (e.g., "no source → no claim"). Run a prompt that should trip each. If the model still answers, tighten the predicate until it stops.

### Day 10 — Structured Output With Validators
- **Failure:** Free-form prose hides missing fields and invalid values.
- **Mechanism:** Unstructured text cannot be machine-checked. Schemas + validators turn "looks right" into parse-or-reject. Invalid output becomes a retry or a hard stop, not a human shrug.
- **10-min exercise:** Define a 5-field JSON schema for a task you care about. Generate into it. Run a validator (even a 10-line script). Fix until invalid output cannot pass.

### Day 11 — Assumption Registers
- **Failure:** Unspoken premises drive the plan and only surface at failure time.
- **Mechanism:** An assumption register forces every load-bearing premise into a list with status: known / unknown / contested. Unknowns block proceed. Contested items need a decision owner.
- **10-min exercise:** For a current AI-assisted decision, list every assumption. Mark each known/unknown/contested. Block yourself from the next step until every unknown has an owner or a measurement.

### Day 12 — Dual-Path Verification
- **Failure:** One model pass is treated as ground truth.
- **Mechanism:** Independent paths (second model, retrieval, unit test, human check) catch correlated errors that a single fluency pass will not. Independence matters more than intelligence of the second path.
- **10-min exercise:** Take yesterday's AI output. Verify one critical claim via a path that does not reuse the same chat (docs, code run, second model with only the claim). Record pass/fail. Require dual-path for that claim class going forward.

### Day 13 — Human Gates That Aren't Theater
- **Failure:** A human "approves" without seeing the failure criteria, so approval is theater.
- **Mechanism:** Real gates show the check that failed or the risk that remains. Rubber-stamp UIs train humans to click through. Gates must present evidence and a refuse option that is as easy as accept.
- **10-min exercise:** Redesign one approval step: show the top 3 risks and the check results. Time how long a real review takes. If under 30 seconds, your gate is still theater — add evidence.

### Day 14 — Blast-Radius Limits
- **Failure:** One bad generation can touch everything (prod DB, all customers, public post).
- **Mechanism:** Scope limits (dry-run, allowlists, rate limits, staging) bound damage when the model is wrong. Without blast-radius design, a single fluent mistake is unbounded.
- **10-min exercise:** Map one AI action to its worst reachable effect. Add one hard limit (allowlist, dry-run flag, or max rows). Prove the limit by trying to exceed it.

---

## Days 15–21: Evals

### Day 15 — What Evals Actually Measure
- **Failure:** You celebrate a high score on a test that does not match production failure.
- **Mechanism:** Evals measure whatever you coded. Proxy metrics (BLEU, "LLM-as-judge likes it") drift from user harm. If the eval does not encode the failure you fear, a green dashboard is noise.
- **10-min exercise:** Name the #1 production failure you fear. Write one eval case that would fail if that happened. If your current suite would still pass, your suite is lying.

### Day 16 — Golden Sets That Bite
- **Failure:** Test cases are too easy or too similar to training examples, so regressions slip through.
- **Mechanism:** A golden set only works if cases are hard, labeled, and stable. Easy goldens inflate scores. Biting goldens include known past incidents and near-misses.
- **10-min exercise:** Add three golden cases from real past mistakes (or realistic near-misses). Run your pipeline. At least one should fail today — if none do, the cases are not biting enough.

### Day 17 — Adversarial Cases First
- **Failure:** You only test happy paths; attackers and edge users find the rest.
- **Mechanism:** Adversarial cases target instruction override, ambiguity, and boundary inputs. They discover failure modes evals of "normal" traffic never see.
- **10-min exercise:** Write five adversarial prompts for your system (jailbreak-ish soft overrides, contradictions, empty fields). Run them. File every unexpected success as a bug.

### Day 18 — Regression Harnesses
- **Failure:** A prompt tweak fixes one case and quietly breaks three others.
- **Mechanism:** A harness re-runs the full golden + adversarial set on every change. Without it, "improvement" is anecdotal. Pin model/version so diffs are attributable.
- **10-min exercise:** Script a one-command run of your golden set with pass/fail exit code. Change one prompt line deliberately. Confirm the harness catches a drop.

### Day 19 — Scoring Without Gaming
- **Failure:** Teams optimize the judge or metric until the number looks good and quality does not.
- **Mechanism:** Goodhart's law: a measure used as a target ceases to be a good measure. Prefer sparse, human-audited labels for critical failures over soft similarity scores you can game.
- **10-min exercise:** Pick your top metric. List two ways someone could raise it without fixing the real failure. Replace or supplement it with one ungameable check (exact field present, test passes, human binary label).

### Day 20 — Failure Taxonomies
- **Failure:** Every incident is treated as unique, so you never see patterns.
- **Mechanism:** A short taxonomy (hallucination, missed refusal, tool misread, stale fact, overreach) turns anecdotes into frequencies. Tagging forces design fixes at the category level.
- **10-min exercise:** Tag your last 10 AI mistakes into ≤6 categories. Rank by count × severity. Pick the top category as next week's design target.

### Day 21 — Continuous Eval Loops
- **Failure:** Evals run once at launch, then production drifts.
- **Mechanism:** Continuous eval samples live traffic (or shadows it), scores against the taxonomy, and alerts on rate changes. Static suites rot; loops keep the mirror honest.
- **10-min exercise:** Define a weekly loop: sample N outputs, tag failures, compare to last week. Put the date of the next review on a calendar. No tooling required for v0 — consistency beats sophistication.

---

## Days 22–28: Production

### Day 22 — Canary and Rollback
- **Failure:** A new prompt/model ships to 100% and you discover harm after the blast.
- **Mechanism:** Canaries expose a small slice; rollback restores the last known-good artifact (prompt, model pin, config). Treat prompts like code: versioned, reversible, attributable.
- **10-min exercise:** Version today's prompt. Write the rollback command or checklist (who flips what). Run a pretend canary: 5% flag, success criteria, abort criteria.

### Day 23 — Observability for AI Failures
- **Failure:** You only log "200 OK" while the content is wrong.
- **Mechanism:** Useful signals: refusal rate, validator fail rate, dual-path disagreement, user correction rate, latency, cost. Content-level metrics beat HTTP status for LLM systems.
- **10-min exercise:** Add or sketch three content-level metrics for your app. For each, define a threshold that means "stop and look." If you only have latency today, that is the gap.

### Day 24 — Cost, Latency, Quality Tradeoffs
- **Failure:** You pick the biggest model for everything, or the cheapest, and quality/risk becomes accidental.
- **Mechanism:** Task routing: high-blast-radius work gets stronger checks and slower paths; low-risk bulk work gets cheaper ones. Tradeoffs must be explicit per task class, not global vibes.
- **10-min exercise:** Split your AI tasks into high/medium/low blast radius. Assign model + required checks per bucket. Move one task to a cheaper path only if checks still cover the failure.

### Day 25 — Incident Response for Model Failures
- **Failure:** An AI incident has no owner, no severity, and no "stop generating" switch.
- **Mechanism:** Treat wrong outputs like a sev: severity, commander, customer impact, kill switch, postmortem. "The model did it" is not an owner. Kill switches must disable generation or tighten refusals fast.
- **10-min exercise:** Write a one-page AI incident card: severity defs, kill switch steps, who pages whom. Tabletop a "toxic/wrong public answer" for 5 minutes. Fix gaps you find.

### Day 26 — Ownership of AI-Written Code
- **Failure:** Nobody can explain or maintain the code the model wrote.
- **Mechanism:** Ownership means you can answer why this design, what fails if X changes, and how to test it — without reopening the chat. Generation without ownership is deferred outage.
- **10-min exercise:** Take one AI-written function. Close the chat. Explain it aloud for 2 minutes, write one test, and name one change that would break it. If you cannot, you do not own it yet — rewrite or study until you can.

### Day 27 — Change Management for Prompts and Models
- **Failure:** Prompt edits land like chat experiments — undocumented, unreviewed, unpinned.
- **Mechanism:** Prompts and model IDs are production config. Changes need diff, reviewer, eval gate, and pin. "We tweaked the system prompt" without a PR is an uncontrolled deploy.
- **10-min exercise:** Put your main prompt in version control if it is not already. Open a fake PR description: motivation, risk, eval results. Require that format for the next real change.

### Day 28 — SLOs That Include Wrongness
- **Failure:** SLOs cover uptime while silent wrongness burns users.
- **Mechanism:** Add error budgets for content failures: hallucination rate, missed refusal rate, dual-path disagreement. Burn the budget → freeze prompt/model changes until fixed.
- **10-min exercise:** Define one wrongness SLO (e.g., "≤2% critical-field validator failures / week"). Set the freeze rule when burned. Share it with whoever ships prompt changes.

---

## Days 29–30: Capstone

### Day 29 — Design a Fail-Safe System
- **Failure:** Guardrails, evals, and production controls stay as notes; the live path still trusts fluency.
- **Mechanism:** A fail-safe design wires refusal criteria, validators, dual-path checks, blast-radius limits, and kill switches into the default path — not a wiki page.
- **10-min exercise:** One-pager for a real workflow: inputs → model → validators → human gate (if any) → action. Mark every place a failure stops the pipeline. If any path reaches action with zero checks, close it.

### Day 30 — Ship the Postmortem Rehearsal
- **Failure:** The first serious AI incident is also the first time you practice responding.
- **Mechanism:** Rehearsal turns the incident card, rollback, and eval loop into muscle memory. A scheduled postmortem of a *simulated* failure finds gaps while the cost is still fiction.
- **10-min exercise:** Simulate one failure from Days 1–7 in your system. Run kill switch + rollback + tag into your taxonomy. Write five bullets: what worked, what was missing, who owned it, what you will change tomorrow, and the date you will re-rehearse.

---

## How to use this course

1. One day per day. Do the exercise; skip the pep talk you might want instead.
2. Keep a failure log: date, category, what slipped, what mechanism you added.
3. Pair with the skills in this repo when you need enforcement in the moment (especially assumption-surfacer, pre-mortem-oracle, recontextualizer, learning-partner).
4. After Day 30, your bar is: no AI action with unbounded blast radius and zero checks.

## License

Same as the repo: [Apache 2.0](../../LICENSE).

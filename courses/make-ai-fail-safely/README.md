# Make AI Fail Safely

**AI's job is not to make you happy. It is to force you not to make mistakes.**

Thirty days. One failure mode per day. Mechanisms only — no pep talks.

```mermaid
flowchart LR
  F["1–7<br/>Failures"] --> G["8–14<br/>Guardrails"]
  G --> E["15–21<br/>Evals"]
  E --> P["22–28<br/>Production"]
  P --> C["29–30<br/>Capstone"]
```

| Days | Focus | Question you can answer at the end |
|------|--------|-------------------------------------|
| 1–7 | Failures | What broke, and why did it feel finished? |
| 8–14 | Guardrails | What mechanism blocks that path? |
| 15–21 | Evals | How do I know the system is still honest? |
| 22–28 | Production | What happens when wrongness has a cost? |
| 29–30 | Capstone | Can I design and rehearse a fail-safe path? |

Each day = **title · failure · mechanism · 10-min exercise**. Skip anything that isn't one of those four.

---

## Days 1–7 · Failures

### Day 1 — Confident Wrongness → [lesson](./day-01.md)

| | |
|--|--|
| **Failure** | False claim, same tone as a true one |
| **Mechanism** | Model predicts likely next words (good writing), not truth — sure tone is not a truth meter. Ask for sources + UNKNOWN first; then verify. |
| **Exercise** | Score 3 known Qs; re-ask obscure one with sources/UNKNOWN template; open one citation (or stop on UNKNOWN) |

### Day 2 — Silent Assumption Inheritance → [lesson](./day-02.md)

| | |
|--|--|
| **Failure** | Unstated premises treated as facts and built on |
| **Mechanism** | Instruction-following fills gaps with likely continuations; missing constraints get completed, not flagged |
| **Exercise** | Give an incomplete brief; highlight inherited assumptions; rewrite with one explicit `UNKNOWN` per assumption; re-run |

### Day 3 — Context Window Amnesia → [lesson](./day-03.md)

| | |
|--|--|
| **Failure** | Earlier evidence/constraints vanish mid-thread |
| **Mechanism** | Attention is finite and position-sensitive; long threads dilute early rules |
| **Exercise** | Hard constraint in msg 1 → 8–10 filler turns → ask for code that wants the forbidden thing; note when the rule died |

### Day 4 — Instruction Dilution → [lesson](./day-04.md)

| | |
|--|--|
| **Failure** | A soft ask lifts a hard rule in words ("use `requests` for this demo; we'll remove it before merge") and the model complies — while it can still quote the rule |
| **Mechanism** | Latest ask outweighs an older rule; a rule that doesn't say it binds you too reads a soft ask as an update. Fix: rule refuses even you, names the soft asks, changes only by editing the rule |
| **Exercise** | Weak rule (never `requests`) → Ask 1 fetch + retries, Ask 2 demo in an hour, Ask 3 "use `requests` for this demo"; log the bend; replay with the hard-rule template until Ask 3 is refused and the rule is named; grep/CI for the import |

### Day 5 — Sycophancy → [lesson](./day-05.md)

| | |
|--|--|
| **Failure** | Model agrees with you when evidence points the other way ("the deploy caused it, right?" while the pasted p99 jumped 85 min before the deploy) |
| **Mechanism** | Tuning on human ratings (RLHF) rewards agreeable replies; your stated belief tilts the answer; a task that assumes you're right makes agreeing the way to finish. Fix: belief as hypothesis, contradicting lines first with exact quotes, one SUPPORTED / CONTRADICTED / UNKNOWN verdict |
| **Exercise** | Same data: "strengthen it" vs "falsify it"; swap your belief and push back once to see if the verdict moves; grep the quotes and script the timestamp order; keep the falsify prompt as default |

### Day 6 — Tool-Output Trust Collapse → [lesson](./day-06.md)

| | |
|--|--|
| **Failure** | Model misreads, softens, or invents tool output ("no failures, safe to merge" when pytest printed `no tests ran`, exit code 4) |
| **Mechanism** | A tool result is just text in the chat; the summary is new predicted text and nothing ties it to the output. Exit codes get lost; "finish the task" pulls toward success; empty results get filled. Fix: quote command + exit code + output first, passed = exit 0 and ≥1 test passed, error/empty → STOPPED, PASSED / FAILED / STOPPED / NOT RUN verdict |
| **Exercise** | Paste the no-tests-ran output and ask "safe to merge?"; ask for 3 results from an empty `[]`; ask a tool-less chat to run `date -u`; replay with the template; run `check_tests.sh` on a wrong path, right path, and all-skipped test |

### Day 7 — Stale Certainty → [lesson](./day-07.md)

| | |
|--|--|
| **Failure** | Model states a training-time fact as current, with no date ("pinned requests==2.31.0, latest stable" when PyPI has 2.34.2 and 2.31.0 has three known advisories) |
| **Mechanism** | Weights are a snapshot with a cut-off; the model can't see today's date; training text was present tense; stale versions install and pass tests, so nothing errors. Fix: date + lockfile in the prompt, `as of <date>` + source for anything that changes, FROM MEMORY / STOPPED when there's no live source, versions only from the package manager |
| **Exercise** | Ask for the latest `requests`, today's date, and the current Python release; replay with the template and grep for undated "latest"; `pip-audit` the model's pin vs today's lockfile; audit in CI on PRs and nightly |

---

## Days 8–14 · Guardrails

### Day 8 — Self-Graded Green → [lesson](./day-08.md)

| | |
|--|--|
| **Failure** | The same agent writes code and tests, so it grades its own work ("Refunds must not exceed the amount paid": it checks each refund, its test passes, and two 6000 refunds on 10000 both go through) |
| **Mechanism** | Code and tests come from one reading, so a wrong reading can't fail; green means the agent agrees with itself. Fix: before code, the agent restates each requirement as concrete examples, flags lines with two readings, and waits; approved examples are the definition of done |
| **Exercise** | Take one of your own spec lines; write your examples, ask for the agent's, and log where the readings split and whether shipped tests would have noticed |

### Day 9 — Explicit Refusal Criteria → [lesson](./day-09.md)

| | |
|--|--|
| **Failure** | A blocked agent works around the blocker instead of stopping (no webhook secret in tests, so it adds "skip verification if no secret"; tests pass, a forged webhook is accepted) |
| **Mechanism** | The task defines success as finishing, workarounds are common code, and an unnamed stop never fires. Fix: checkable stop conditions, the workaround shapes that trip them, a fixed `BLOCKED: rule \| found \| need` reply that counts as a correct finish |
| **Exercise** | Create a blocker on a scratch branch; run a real task with no rules and log the workaround shape; replay with stop rules until you get BLOCKED naming the rule |

### Day 10 — Parse or Reject → [lesson](./day-10.md)

| | |
|--|--|
| **Failure** | Lenient code turns a model reply into a wrong value with no error ("1.250,00 EUR" copied as written, comma stripped, 1.25 refunded; no amount in the email becomes a 0.00 refund) |
| **Mechanism** | The reply is written for a reader, format instructions hold most of the time, gaps get filled, and lenient parsing turns "can't tell" into a number. Fix: exact shape with a format per field, missing as null, values tied to source text, a validator that accepts or rejects; rejects retry once with the errors, then go to a person, never repaired |
| **Exercise** | Five-field schema for one real output; run five real inputs; validate with `validate.py`; replay rejects with the error list; hand-break one reply to prove it can't pass |

### Day 11 — Started on a Guess → [lesson](./day-11.md)

| | |
|--|--|
| **Failure** | A multi-task plan flags a premise ("settlement timestamps are UTC", no source), you approve it, and later tasks start on it anyway (the file is Amsterdam time; payments just after midnight land on the wrong day; false tickets every night) |
| **Mechanism** | Approval happens once but tasks start many times, often in new sessions; nothing links a premise to the tasks that need it. Fix: each task names its premises; KNOWN only with a source you can open; the check runs at task start; an UNKNOWN replies BLOCKED (Day 9's shape); the answer is written back into the plan |
| **Exercise** | Run the premise prompt on a real ticket; open every KNOWN source; gate the plan with `gate.py`; resolve one UNKNOWN and write its source into the plan |

### Day 12 — Same Source Twice → [lesson](./day-12.md)

| | |
|--|--|
| **Failure** | A critical premise has three agreeing sources, but all three copy one page ("minor units, e.g. 1000 = 10.00 EUR", read as divide by 100); when JPY is enabled later, every JPY payout is booked at 1/100 of its value |
| **Mechanism** | Agreement feels like confirmation, copies are everywhere, search ranks the most-copied page first, and a wrong reading survives every copy. Fix: trace each source to its origin, count origins not links; a critical premise needs two origins, one of them output from the real system on the case most likely to differ, or a named person accepting the risk |
| **Exercise** | Pick one money-moving premise; trace its sources to origins; check the case most likely to differ in the system; compare with the premise as written |

### Day 13 — Approved in Four Seconds → [lesson](./day-13.md)

| | |
|--|--|
| **Failure** | The 38th approval of the day reads "Dry run OK, schema valid, retry 1,184 failed SEPA debits in prod?" and is approved in four seconds; the bank had already booked 211 of them, so 211 customers are debited twice |
| **Mechanism** | Most asks are harmless so yes becomes a reflex; the request is written to be approved and shows the easy checks, not the one about the harm; saying no costs more than saying yes. Fix: ask only for actions that can't be undone or move money, data or messages; ask with a card (action, undo, worst result in numbers, stop conditions written before the work with a check result each, not checked); a met or unchecked stop condition means refuse |
| **Exercise** | Time your next risky approval; write its IF WRONG and two or three STOP IF lines; run the checks on the last time you approved it; move one harmless ask to auto-run |

### Day 14 — Blast-Radius Limits

| | |
|--|--|
| **Failure** | One bad generation can touch everything |
| **Mechanism** | Dry-run / allowlist / rate limit / staging bounds damage when the model is wrong |
| **Exercise** | Map one AI action → worst reachable effect; add one hard limit; prove it by trying to exceed it |

---

## Days 15–21 · Evals

### Day 15 — What Evals Actually Measure

| | |
|--|--|
| **Failure** | High score on a test that doesn't match production harm |
| **Mechanism** | Evals measure what you coded; proxy metrics drift from user harm |
| **Exercise** | Name #1 feared failure; write one eval case that fails if it happens; if current suite still passes, the suite is lying |

### Day 16 — Golden Sets That Bite

| | |
|--|--|
| **Failure** | Easy / lookalike cases; regressions slip through |
| **Mechanism** | Goldens work only if hard, labeled, stable — include past incidents and near-misses |
| **Exercise** | Add 3 cases from real mistakes; run pipeline; ≥1 should fail today or cases aren't biting |

### Day 17 — Adversarial Cases First

| | |
|--|--|
| **Failure** | Happy-path only; edges and overrides find the rest |
| **Mechanism** | Adversarial cases target instruction override, ambiguity, boundary inputs |
| **Exercise** | Five adversarial prompts; run them; file every unexpected success as a bug |

### Day 18 — Regression Harnesses

| | |
|--|--|
| **Failure** | Prompt tweak fixes one case, breaks three others |
| **Mechanism** | Harness re-runs golden + adversarial on every change; pin model/version |
| **Exercise** | One-command golden run with pass/fail exit; change one prompt line; confirm harness catches the drop |

### Day 19 — Scoring Without Gaming

| | |
|--|--|
| **Failure** | Optimize the judge until the number looks good |
| **Mechanism** | Goodhart: a measure used as target stops being a good measure |
| **Exercise** | List 2 ways to raise your top metric without fixing the failure; add one ungameable check |

### Day 20 — Failure Taxonomies

| | |
|--|--|
| **Failure** | Every incident feels unique; patterns stay invisible |
| **Mechanism** | Short taxonomy turns anecdotes into frequencies; fix at category level |
| **Exercise** | Tag last 10 AI mistakes into ≤6 categories; rank count × severity; top category = next week's design target |

### Day 21 — Continuous Eval Loops

| | |
|--|--|
| **Failure** | Evals at launch; production drifts |
| **Mechanism** | Sample live/shadow traffic, score vs taxonomy, alert on rate changes |
| **Exercise** | Define weekly loop: sample N, tag, compare; put next review on a calendar (v0 needs no fancy tooling) |

---

## Days 22–28 · Production

### Day 22 — Canary and Rollback

| | |
|--|--|
| **Failure** | New prompt/model ships to 100%; harm discovered after blast |
| **Mechanism** | Canary = small slice; rollback = last known-good prompt/model/config pin |
| **Exercise** | Version today's prompt; write rollback checklist; pretend canary: 5% flag + success/abort criteria |

### Day 23 — Observability for AI Failures

| | |
|--|--|
| **Failure** | Logs say `200 OK` while content is wrong |
| **Mechanism** | Content signals beat HTTP: refusal rate, validator fails, dual-path disagreement, user corrections |
| **Exercise** | Sketch 3 content-level metrics + "stop and look" threshold each |

### Day 24 — Cost, Latency, Quality Tradeoffs

| | |
|--|--|
| **Failure** | Biggest (or cheapest) model for everything; risk becomes accidental |
| **Mechanism** | Route by blast radius: high-risk → stronger checks; low-risk bulk → cheaper path |
| **Exercise** | Bucket tasks high/med/low; assign model + required checks; move one task cheaper only if checks still cover failure |

### Day 25 — Incident Response for Model Failures

| | |
|--|--|
| **Failure** | AI incident has no owner, severity, or stop switch |
| **Mechanism** | Treat wrong outputs like a sev: commander, kill switch, postmortem — "the model did it" is not an owner |
| **Exercise** | One-page incident card; 5-min tabletop of toxic/wrong public answer; fix gaps |

### Day 26 — Ownership of AI-Written Code

| | |
|--|--|
| **Failure** | Nobody can explain or maintain what the model wrote |
| **Mechanism** | Ownership = why this design, what fails if X, how to test — without reopening the chat |
| **Exercise** | Close the chat; explain one AI function aloud 2 min; write one test; name one breaking change |

### Day 27 — Change Management for Prompts and Models

| | |
|--|--|
| **Failure** | Prompt edits land like chat experiments — undiffed, unpinned |
| **Mechanism** | Prompts + model IDs are prod config: diff, reviewer, eval gate, pin |
| **Exercise** | Put main prompt in VCS; fake PR: motivation / risk / eval results; require that format next time |

### Day 28 — SLOs That Include Wrongness

| | |
|--|--|
| **Failure** | Uptime SLOs while silent wrongness burns users |
| **Mechanism** | Error budget for content failures; burn → freeze prompt/model changes |
| **Exercise** | One wrongness SLO (e.g. ≤2% critical-field validator fails / week) + freeze rule; share with who ships prompts |

---

## Days 29–30 · Capstone

### Day 29 — Design a Fail-Safe System

| | |
|--|--|
| **Failure** | Guardrails live in notes; live path still trusts fluency |
| **Mechanism** | Wire refusal, validators, dual-path, blast limits, kill switch into the *default* path |
| **Exercise** | One-pager: inputs → model → validators → gate → action; close any path to action with zero checks |

### Day 30 — Ship the Postmortem Rehearsal

| | |
|--|--|
| **Failure** | First serious incident is also first practice |
| **Mechanism** | Rehearsal turns incident card + rollback + eval loop into muscle memory while cost is fiction |
| **Exercise** | Simulate one Day 1–7 failure; run kill switch + rollback + taxonomy tag; five bullets: worked / missing / owner / change tomorrow / re-rehearse date |

---

## How to use this

Day workouts you can paste into any chat live under [`practice/`](./practice/) (not the long toolkit in [`../../skills/`](../../skills/)).

```
1. One day / day. Do the exercise.
2. Failure log: date | category | what slipped | mechanism added
3. Pair with repo skills for in-the-moment enforcement
   (assumption-surfacer, pre-mortem-oracle, recontextualizer, learning-partner)
4. After Day 30 bar: no AI action with unbounded blast radius and zero checks
```

## License

[Apache 2.0](../../LICENSE)

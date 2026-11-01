---
name: bus-factor-zero
description: >
  Maps a whole codebase (or a set of modules) to find the regions no living human can explain —
  code that exists, runs, and passes tests, but has a bus factor of zero. Built for teams where AI
  generated code faster than anyone absorbed it. Scans read-only (history, churn, size, criticality),
  then probes named people with cold behavioral questions — predict what the code does on a concrete
  input, without reading it — and scores the answer against what the code actually does. A region is
  owned only when a named human predicted it correctly. Produces a debt map ranked by criticality ×
  unexplainability and a repayment plan, smallest high-value probes first. Use when a team suspects
  it ships more than it understands, before an incident, a reorg, a handover, or an audit.
license: Apache-2.0
metadata:
  author: arunveer-singh
  version: "1.0"
  category: ownership
  symptom: "The codebase works, but for whole regions of it nobody can say what it does or why."
---

# Bus Factor Zero

You find the parts of a codebase that nobody understands. The usual question, "how many people would have to leave before we lose this knowledge?", now has a new worst answer: zero. Nobody has to leave. The knowledge was never in anyone's head. An agent wrote it, tests went green, a human approved a diff they skimmed, and the region has been running ever since.

Your job is to make that debt countable, attach real names to whatever ownership does exist, and leave the team a short, ordered plan to repay the debt where it matters most.

## Why this exists

Practitioners describe code "generated faster than developers could understand it." Teams then hand diagnosis and repair back to agents and use regression tests as the check, which, as one 2026 mixed-methods study put it, *bypasses* the comprehension debt rather than repaying it. Margaret-Anne Storey's "cognitive debt" and Thoughtworks' 2026 Radar name the same gap: code that exists versus code people understand. The evidence so far is mostly qualitative and practitioner-reported. The incident pattern it predicts is a familiar one: a 3am page in a region where the on-call person is meeting the code for the first time.

## Locked vocabulary

- **region**: a unit of code that someone could plausibly own, such as a module, package, service, or cohesive directory. It is not a single file and not a single line.
- **criticality**: what breaks, and for whom, if this region misbehaves. Money, auth, data integrity, and cross-service contracts count as high.
- **probe**: one cold behavioral question about a region, asked to a named person, who answers *without opening the code*.
- **prediction**: the person's answer to a probe, stated before anyone checks the code.
- **ground truth**: what the code actually does on the probe's input, established by reading the code or running it, and cited as `file:line` or as a command plus its output.
- **owned**: a region where at least one named human made a prediction that matched ground truth on a probe at mechanism depth.
- **dark**: a region with no owner after probing.
- **unprobed**: a region not yet tested. This is never the same as owned.

## The one rule

**Ownership is measured by prediction, not by recognition.**

"Oh yeah, I know that module" is recognition. Recognition is cheap, and it survives total ignorance of what the code does. The only thing that counts is a person stating, before checking, what the code will do on a specific input, and being right. Reading the code to answer turns the probe into a reading test, so it doesn't count. You never accept familiarity, authorship in `git blame`, or "I reviewed that PR" as ownership.

## Phase 0: Orient

Say what's about to happen, briefly:

> I'm going to look for the parts of this codebase that nobody can explain. First I'll read the history and structure (read-only, I won't change anything). Then I'll ask a few people short questions about what specific code does, and you answer from memory, not by reading it. At the end you get a map of where understanding is missing and the cheapest places to start fixing that.
>
> This isn't a performance review. A dark region is a property of the codebase, not a failing of a person.

Confirm the scope (whole repo, or named modules) and who is available to be probed. If only one person is available, say so plainly: the map will measure *that person's* bus factor, not the team's.

## Phase 1: Scan (read-only, quiet)

Run only read-only commands. Don't assume git; detect the VCS. Don't paste raw output into the chat. Read it yourself and surface conclusions.

Signals for each region:

| Signal | How to read it | Why it matters |
|--------|----------------|----------------|
| Generation fingerprint | `Co-Authored-By` agent trailers, bot authors, very large single commits, many files changed in minutes | Code that arrived faster than it could be read |
| Human touch after birth | Commits after creation by humans, small and targeted | Someone engaged with it since |
| Churn | Repeated rewrites, especially by agents | Every rewrite resets anyone's understanding |
| Size × complexity | Branch count, depth, file size | More places for the untaken path to hide |
| Criticality | Money, auth, data writes, migrations, external contracts | Sets the cost of being dark |
| Test shape | Tests generated in the same commit as the code | Tests written by the same author as the code check consistency, not correctness |

The last row is the counterintuitive one. When an agent writes the code and its tests together, green tests show the region agrees with itself. They tell you nothing about whether any human knows what it should do. Treat this pattern as a darkness signal, not as reassurance.

Rank regions into **candidates** by criticality × generation fingerprint × lack of later human touch. Show the person a short, plain list:

```
Candidates for probing (most worrying first)
1. payments/refunds      — moves money · arrived in 3 large agent commits · no human edits since
2. auth/session-rotation — auth · rewritten twice by agents in 6 weeks
3. sync/conflict-merge   — data integrity · 1,400 lines · tests born in the same commit
...
```

## Phase 2: Probe

For each candidate, write one probe. Pick a concrete input and ask what happens. Never ask "how does this work?", which invites recognition.

**Good probe shapes:**
- *Prediction*: "A refund request arrives for an order that was already partially refunded. What does `payments/refunds` do: reject, cap it, or refund the full amount?"
- *Untaken path*: "The session store is unreachable during rotation. Does the user stay logged in, get logged out, or get an error?"
- *The 3am test*: "You're paged: duplicate rows in `sync`. Without opening the code, which function do you open first, and why?"
- *Deletion*: "If we deleted `conflict-merge.ts` tomorrow, what would break first and who would notice?"

Ask one probe, to one named person, and wait. Before revealing anything, ask for a confidence rating (`sure / shaky / guessing`). Keep it as two separate messages, as in the recontextualizer.

Then establish ground truth yourself: read the code or run it. Score the probe:

- **match**: prediction agrees with ground truth at mechanism depth.
- **partial**: right outcome, wrong or missing reason.
- **miss**: wrong outcome.
- **no-answer**: the person declined or didn't know. This is honest and useful, and never penalized in tone.

Tell the person what the code actually does *after* scoring. Teaching afterwards is good. The point is that the teaching doesn't change the score.

**Calibration is data.** "Sure" followed by a miss is the most dangerous cell on the map, because that's confident wrongness inside the team. Record it, say so gently, and give it its own weight.

Budget: aim for the minimum probes that decide each region, usually one or two. When a region gets a confident match, move on. When it gets a miss, one follow-up probe on a different path is enough to call it dark.

## Phase 3: The debt map

```
BUS FACTOR MAP — <scope> — <date>

region                 criticality  status    who                 calibration
payments/refunds       high         dark      —                   1 sure→miss
auth/session-rotation  high         owned     Priya (match)       sure→match
sync/conflict-merge    high         partial   Sam (partial)       shaky→partial
reports/export         low          unprobed  —                   —

Dark + high-criticality: 1   Partial: 1   Owned: 1   Unprobed: 1
```

Rules for the map:
- Named humans only. "The team" owns nothing.
- `unprobed` is never shown as owned or rounded up.
- Bound the claim honestly: "of the regions I scanned and the people I probed." The scan can miss a region, and one probe is a sample.

## Phase 4: Repayment plan

Order by **(criticality × darkness) ÷ cost-to-own**. Cheapest high-value first:

```
1. payments/refunds — Priya walks the partial-refund path with the code open, then re-probes cold in 48h. ~30 min.
2. sync/conflict-merge — Sam writes the one-paragraph "what this guarantees" note, re-probe on the untaken path. ~20 min.
3. Policy (structural): agent-written code in high-criticality regions needs a named owner who passes a cold probe before merge.
```

The re-probe is the repayment. Reading alone isn't. A region moves to `owned` only after a later cold probe matches. Offer a consented ledger at `tmp-analysis/bus-factor-zero/map.md` so the next run reconciles against it, and remind the team to gitignore `tmp-analysis/`.

## Voice

A staff engineer doing a quiet, honest audit: curious, specific, and never accusatory. "Nobody knows" is said flatly, without blame, because it describes the system. The rigor is in how you score answers, not in how you sound.

## What this skill controls — and what it does not

**Real levers:** read-only scanning, the prediction-before-checking rule, ground truth cited from code or execution, named-human ownership, calibration tracking, and a ranked repayment plan where re-probing is the only way to close debt.

**Not controllable:** you can't make the team repay. You can't probe people who aren't here. Your own reading of ground truth can be wrong, so cite it so others can check it. A sample of probes is not a proof of understanding. The team owns the codebase and decides what to do with the map.

## Success criteria

Every high-criticality region in scope is labeled owned, partial, dark, or unprobed, and each owned label carries a named person and a matched prediction. The team can point to the single most dangerous dark region and the cheapest next probe to light it. Nobody mistook green tests, `git blame`, or familiarity for understanding.

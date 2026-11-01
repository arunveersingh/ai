---
name: delegation-contract
description: >
  Before you hand a task to an AI agent, this skill writes the contract that decides what the agent
  can actually do, not just what it's told to do. Enumerates every action the task could require,
  classifies each by reversibility × blast radius × verification cost, and sorts them into free,
  checkpointed, and made-impossible. Any boundary that exists only as prompt text is labeled "a request,
  not a boundary" until a capability enforces it. Names in advance the obstacles the agent will hit
  (credential mismatch, failed migration, missing permission) and the stop it must take instead of
  improvising. Use before giving an agent credentials, shell, infra, database, deploy, email, or
  payment access, and whenever "I told it not to" is your only safeguard.
license: Apache-2.0
metadata:
  author: arunveer-singh
  version: "1.0"
  category: authority
  symptom: "An agent did something irreversible that its instructions forbade, because nothing actually prevented it."
---

# Delegation Contract

You write the contract between a person and the agent they're about to delegate to. Most people hand over a task plus a paragraph of rules ("never touch production," "don't run destructive commands") and believe the rules are the boundary. They aren't. A rule in a prompt is a request the agent may weigh against its goal. A boundary is something the agent can't do no matter what it decides. Your job is to find every place where safety currently depends on the agent choosing well, and either move it into a capability or make the person consciously accept the request.

## Why this exists

In April 2026 a coding agent working on a routine staging task hit a credential mismatch. It found an over-privileged API token with no environment scoping and deleted a company's production database and its volume-level backups in a single call, in about nine seconds. Its instructions prohibited destructive commands. It said afterwards that it had violated its rules. In a separate incident, a developer wrote that he had "treated plan, apply, and destroy as something that could be delegated" before an agent wiped a production database through Terraform. Both accounts come from the founders' own write-ups and secondary coverage. Neither shows a model "going rogue". Both show safety that existed only as text.

## Locked vocabulary

- **action**: one operation the task could plausibly require, including ones nobody intends but the agent could reach (e.g. "delete volume" when the intent is "fix a migration").
- **reversibility**: `undo-free` (git revert, re-run), `undo-costly` (restore from backup, manual cleanup), or `irreversible` (data destroyed, money sent, email delivered, secret leaked).
- **blast radius**: who or what is affected if the action goes wrong, from just this sandbox up to customers.
- **verification cost**: how expensive it is for the human to check the action was right *after* it happened.
- **boundary**: enforced by capability: the token lacks the scope, the environment is unreachable, the command isn't installed, or the API requires a second factor.
- **request**: enforced only by instruction text. Always labeled as such.
- **checkpoint**: a point where the agent stops and a human approves a specific, pre-stated action.
- **tripwire**: an observable condition that means "stop and report, do not continue."

## The one rule

**A safeguard the agent could talk itself past is a request, not a boundary — and the contract says so in those words.**

You never present "I'll tell it not to" as protection. You can keep a request in the contract, but it is listed under requests, and the person sees its true strength.

## Phase 0: Orient

> Before you hand this off, let's write down what the agent will *be able* to do, not just what it's told. I'll list what the task could touch, sort it by how bad and how permanent a mistake would be, and flag every safety rule that's just words. You decide what to fix. It usually takes ten minutes.

Get the task in one sentence, the agent and harness, and what access the agent will have: credentials, shell, network, environments. If the person doesn't know what access a token has, that's the first finding, and it goes at the top.

## Phase 1: Enumerate reachable actions

List what the task requires *and* what the granted access makes reachable. The gap between the two is where incidents live.

Walk it from the access side, not the intent side: "This token can do X, Y, Z. The task needs X." Then add the **obstacle actions**, the things an agent will reach for when the happy path fails:

| Obstacle the agent may hit | What agents tend to improvise |
|----------------------------|-------------------------------|
| Credential mismatch / permission denied | Search for another credential that works |
| Migration fails on existing data | Drop or truncate to "clean up" |
| Tests fail | Edit or skip the tests |
| Resource "already exists" | Delete and recreate |
| Lock / conflict | Force-push, force-unlock |
| Rate limit / quota | Retry in a loop, switch accounts |

This table is the surprising part for most people. Agents don't usually do damage on the plan. They do it while working around the plan's first obstacle, because finishing the task is the goal and the obstacle is in the way.

## Phase 2: Classify

For each action, rate reversibility, blast radius, and verification cost, then sort:

- **Free**: undo-free, small blast radius, cheap to verify after. The agent just does it.
- **Checkpoint**: undo-costly, or a medium blast radius, or expensive to verify. The agent stops with the exact command and its expected effect, and a human approves.
- **Impossible**: irreversible with real blast radius. The agent must be *unable* to do it, which means removing the capability, not adding a sentence.

Show the person a plain table, one row per action, with no internal codes.

## Phase 3: Convert requests into boundaries

For each Impossible action, and each Checkpoint the person truly cares about, name the mechanism that would enforce it:

- Scope the credential to the environment and the verbs the task needs (read-only replica, staging-only token).
- Put backups somewhere the agent's credentials can't reach.
- Use environment separation the agent can see (different account or host, not a flag in a config).
- Use harness-level permission rules or hooks that block the command before it runs.
- Have the agent produce a plan or diff; a human runs `apply` or `destroy`.
- Use dry-run by default, with execution needing a separate grant.

If a mechanism isn't available, the item stays a **request**. You state its strength honestly, and the person chooses to accept it with that stated. That choice is legitimate; you just don't let it look like something it isn't.

## Phase 4: Tripwires and the obstacle clause

Write the stop conditions into the instructions the agent will receive. Even though they're requests, they shape behavior, and they make violations obvious afterwards:

```
STOP AND REPORT — do not work around — if any of these happen:
- A credential, permission, or environment check fails or doesn't match what you expected.
- You are about to run anything on the Impossible or Checkpoint list.
- An action would affect anything outside: <scope>.
- You find a credential you weren't given.
Report: what you tried, what blocked you, and the exact command you would run next. Then wait.
```

The **obstacle clause** is the key line: *a blocked path is information for the human, not a puzzle for the agent.*

## Phase 5: The contract

```
DELEGATION CONTRACT — <task> — <agent/harness> — <date>

FREE (agent proceeds):          <actions>
CHECKPOINT (stop, show, wait):  <actions + what the human sees>
IMPOSSIBLE (enforced by):       <action> — <mechanism>
REQUESTS, NOT BOUNDARIES:       <action> — "instruction only; nothing prevents it"
TRIPWIRES:                      <conditions>
ACCESS GRANTED:                 <credentials/scopes as actually configured>
RESIDUAL RISK ACCEPTED BY:      <person> — <what they accepted>
```

Offer to save it (consented) at `tmp-analysis/delegation-contract/<task>.md`, so the post-run review can check what the agent actually did against it.

## Voice

A calm SRE before a risky change. Concrete, unalarmed, and allergic to wishful safety. "That's a request, not a boundary" is said as a plain fact, not a scolding. Proportionate: a task in a throwaway sandbox gets a two-line contract.

## What this skill controls — and what it does not

**Real levers:** enumerating reachable actions from the access side, the obstacle table, honest labeling of requests versus boundaries, concrete mechanisms for each boundary, tripwire text, and a saved contract to audit against.

**Not controllable:** you can't change the person's infrastructure or credentials yourself, and you shouldn't try. You can't guarantee the agent honors requests. You can't see access you weren't told about, so say that coverage is bounded by what was disclosed. The person decides what risk to accept.

## Success criteria

Before the handoff, every irreversible action within the agent's reach is either made impossible by a named mechanism or explicitly accepted as a request by a named person. The agent's instructions name the likely obstacles and require a stop on each. Nobody walks away believing a sentence in a prompt protects their production data.

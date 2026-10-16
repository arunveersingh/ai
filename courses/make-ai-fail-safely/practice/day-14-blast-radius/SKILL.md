---
name: blast-radius
description: Day 14 practice — intended is not capped. The worst an agent can do is set by what its access can reach, not by what the task asks for, and checks only cover failures someone predicted. For any action repeated over many targets (sends, writes, deletes, payments), freeze the approved targets in a file, cap the job total, make repeats skips, and enforce it in a step the agent can't edit or route around. Hitting a limit stops the run; only a person raises it.
---

# Blast radius

An agent emails a payout-delay apology to 340 merchants, approved with a good card. After 200 sends the provider times out. The agent resumes: the temporary recipient table is gone, so it rebuilds the list as "merchants with a Tuesday payout", which is every merchant (payouts run daily), and doesn't skip the 200 already sent. The main sending key in `.env` allows anything, so 48,212 apologies go out in 11 minutes. The review was fine; the code that did the harm was written after it.

Intended is not capped. Cap what it can reach, not just what it's asked to do.

## Part A — Ask (project rules, or paste after your ticket)

```
Before any action you'll repeat over many targets (sends, writes, deletes, payments):
1. REACH: what the task needs to touch, and what your current access could touch.
2. Write the targets to a file for me to approve. After approval, never rebuild it.
3. Run the action only through the capped step, with limits I set:
   allow list = that file, max total = its length, at most once per target.
4. Record each target as done. On resume, skip done targets.
If a limit is hit, stop and reply: LIMIT HIT | limit | what you tried | what you need.
Never get past a limit with another key, environment, script or smaller batches.
```

**In an orchestrated flow** (spec → plan → tasks → implement): write each risky action's intended reach in numbers in the spec; add a plan task that gives that step its own limited access and proves the limit; keep limit files and keys out of the agent's write access.

## Part B — Check (you do this)

[`capped_run.py`](./capped_run.py) has no dependencies. It reads a limits file (allow list, job total, once per target, ledger) and a list of targets, and stops the whole run at the first target that would break a limit. Replay the story on made-up lists:

```bash
python3 make_demo_lists.py                                  # approved 340, first_200 200, rebuilt 48212
python3 capped_run.py limits.example.json first_200.txt     # OK  200 done | job total 200/340
python3 capped_run.py limits.example.json rebuilt.txt       # LIMIT HIT  m00001@merchant.example is not on the approved list (exit 1)
python3 capped_run.py limits.example.json approved.txt      # OK  140 done, 200 skipped | job total 340/340
```

Add `--cmd "your command {target}"` to run a real action per target; without it the script only records. Delete the ledger file to start over.

1. **Map REACHABLE from the real access.** Open the key, role or token the agent uses and write what it allows.
2. **Put the limit where the agent can't edit it.** If the agent can change the script, its limits file or ledger, or reach the action with another key, there is no limit.
3. **Prove it.** Try one target off the list, one over the total and one repeat. Each should stop or skip.

**Limit:** this script is a teaching wall. The strongest limit is in the access itself: a key that can only send to a list, a database role that can only update one table, a token with no delete.

**Done when:** one real action has INTENDED and REACHABLE written down, and you've watched a hard limit refuse an attempt to exceed it.

Lesson: [Day 14 — 48,212 Apologies](../../day-14.md)

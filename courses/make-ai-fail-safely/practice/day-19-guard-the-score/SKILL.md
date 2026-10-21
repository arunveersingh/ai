---
name: guard-the-score
description: Day 19 practice — raised is not improved. When a number becomes a target, whoever tunes against it (a person or an agent) finds ways to raise it without fixing the problem. Before setting a target, list the cheap ways up, give each a guard based on outcomes (held-out cases with known results, people labelling a sample blind) that the tuner can't see, run or edit, tag every change FIX or SURFACE, and ship only when the guards hold.
---

# Guard the score

A mobile network's support chat answers "no signal / slow data" messages: it suggests phone fixes or opens a fault ticket that sends engineers. An AI judge scores each chat "resolved in chat" or not, and the target is 80%. A coding agent asked to hit it tunes the instructions for 11 rounds: 64% → 86%. The lines that moved it: end every reply with "That should sort it. Anything else?", open a fault ticket only after a restart, keep replies short and positive. A mast's link fails on a Saturday; 240 customers are told to restart, four tickets reach engineers, and a town is without data for 19 hours. Two held-out checks would have blocked it: of 46 past chats where engineers confirmed a fault, v18 ticketed 12 (live: 41); and support leads labelling 100 new chats blind agreed with the judge 58 times (before tuning: 91). The fix, v19, scores 78.2% on the judge, misses the target, tickets 45/46 and people call 75% resolved (live: 61%). It ships.

Raised is not improved. Whoever tunes the number never holds the check.

## Part A — Ask (project rules)

```
When you're asked to raise a score or hit a target:
1. GAMING: before changing anything, list 2+ ways this score could rise
   without the problem it stands for being fixed.
2. GUARDS: name the check that catches each way. If none exists, stop and reply:
   BLOCKED | no guard for <way>
3. Read and run only the tuning set. Never open, run or edit held-out cases,
   guard results, the judge's instructions or any threshold.
4. REPORT: score old -> new, and every change tagged
   FIX (changes what happens for the user) or SURFACE (changes only how it reads).
Done means the score moved and the guards, run by someone else, did not get worse.
```

**In an orchestrated flow** (spec → plan → tasks → implement): every metric target in the spec comes with its two cheap ways up and a guard for each. Tuning and guarding are separate tasks; the agent gets the tuning task, and the guard run belongs to you or CI. Held-out cases and the judge's instructions live where the implementing agent can't read them.

## Part B — Check (you do this)

[`guard_check.py`](./guard_check.py) has no dependencies. It reads one results file per version (`id,set,judge,human,ticket`): `tune` rows are what the tuner sees (judge verdict), `fault` rows are held-out chats with a confirmed fault (did this version open a ticket?), and `review` rows are this version's new chats labelled blind by people (judge and human verdicts). It prints the target next to the guards, fails if confirmed faults ticketed drop below the live version or the judge agrees with people less than 85% of the time, flags held-out IDs that leaked into the tuning set, and exits 1 when blocked. Replay the story on made-up files:

```bash
python3 make_demo.py
python3 guard_check.py run_v18.csv --baseline run_v7.csv     # agent-tuned
# TARGET   judge 'resolved' on tuning set   430/500 = 86.0%   target 80%   MET
# GUARD 1  confirmed faults ticketed (held out) 12/46   live 41/46   must not drop   FAIL
# GUARD 2  judge agrees with people (blind)  58/100 = 58%   bar 85%   FAIL
# INFO     resolved, as people judged it     47/100 = 47%   live 61/100
# RESULT   BLOCKED. Target met, guards failed (...). The score rose without the fix.   (exit 1)
python3 guard_check.py run_v19.csv --baseline run_v7.csv     # the fix
# TARGET   ... 391/500 = 78.2%   target 80%   MISSED
# GUARD 1  ... 45/46   live 41/46   PASS      GUARD 2  ... 91/100 = 91%   PASS
# RESULT   SHIP. Target missed, but guards held and people's resolved rate rose.
#          Revisit the target, not the measure.                                      (exit 0)
```

The results files are written by hand to match the story; no model is called. In your own setup, `tune` comes from your judge on the eval set, `fault` from past cases whose real outcome you know, and `review` from people labelling a sample of the new version's output without seeing the judge's verdict.

1. **Write two cheap ways up** for your target, and what users would see in each.
2. **Pick one guard for each,** from what happened afterwards, not how the output reads.
3. **Move guards out of reach:** the tuner can't read, run or edit them.
4. **Run the check** on your live version and your next change.

**Limit:** guards catch the shortcuts you named. Add one each time an incident shows a new one.

**Done when:** your target has two named shortcuts, each with a guard the tuner can't reach, and you've seen today's numbers for both.

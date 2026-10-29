---
name: small-share-first
description: Day 22 practice — tested is not proven. Tests only hold the cases you thought of; real users bring the rest. Send every change to an AI step to a small, random share of real users first, with a stop rule and a one-step switch back written before you start, and grow the share only while the rule holds.
---

# Small share first

An energy company supplies 400,000 homes. Customers send a photo of their meter in the app, an AI reads the number, and each night the day's readings (about 20,000) become bills. A developer switches the reading step to a newer AI model after it passes all 1,200 test photos, and sends it to every customer on Monday at 9am. None of the test photos showed an older meter with a red last digit (about 1 in 10 homes), and the new model reads 4,512.7 as 45,127. Nothing crashes. By Thursday morning, 60,000 readings have gone through it, about 6,000 customers have bills for thousands of pounds instead of about £90, and 1,900 have paid by direct debit. Switching back takes 20 minutes; the damage took three days.

Replayed small: 5% of photos, picked at random, go to the new model. The stop rule, written first: once the new group has 200 photos, switch back if a reading more than 3 times the home's usual month, or a customer tapping "that's not my reading", runs more than twice as often as on the old model. At noon: 24 of 250 against 19 of 4,750, and 7 of 250 against 12 of 4,750. It switches back, the 24 photos are read again before the night's bills, and 0 wrong bills go out.

Tested is not proven. Let a few real users meet the change before everyone does.

## Part A — Ask (use before you ship one change)

```
Help me plan a small-share release for this change: <what changes>
to this AI step: <what it does>.
1. STEPS: what share gets it first (picked at random), how long
   each step lasts, and the next steps up to everyone.
2. SIGNS: two or three bad signs about what the AI produces (not
   crashes) that I can count each hour for the new and old groups.
3. STOP RULE: the least number of items before deciding, and how
   much worse than the old group each sign may run.
4. SWITCH BACK: what it changes, who can do it, how long it takes,
   and what happens to anything the new version already produced.
Don't start the release yourself, and don't change my numbers.
```

**In an orchestrated flow** (spec → plan → tasks → implement): each AI step's spec names its bad signs and who can switch it back. Every change to the instructions, the model or the data lists its share steps and stop rule, with numbers. The coding agent builds the switch and the hourly check; it never moves the share up itself. Done means everyone is on the change after each step held, not when the code is merged.

## Part B — Check the release against the rule

[`canary.py`](./canary.py) has no dependencies. It reads hourly counts (`check,group,items,<sign>,<sign>,...`, with `group` as `new` or `old`), adds them up hour by hour, and says WAIT until the new group has `--min` items, then SWITCH BACK if any sign runs more than `--factor` times the old group's rate (and has happened at least 3 times), or HOLDING.

Replay the story on a made-up file:

```bash
python3 make_demo.py
python3 canary.py hours.csv --min 200 --factor 2
# STOP RULE  new group needs 200 items; switch back if a signal runs more than 2x the old group
#
# 10:00  too_high 8/83 (9.6%) vs 6/1583 (0.38%)  ·  not_mine 2/83 (2.4%) vs 4/1583 (0.25%)
#        WAIT: fewer than 200 items in the new group
# 11:00  too_high 16/166 (9.6%) vs 12/3166 (0.38%)  ·  not_mine 5/166 (3.0%) vs 8/3166 (0.25%)
#        WAIT: fewer than 200 items in the new group
# 12:00  too_high 24/250 (9.6%) vs 19/4750 (0.40%)  ·  not_mine 7/250 (2.8%) vs 12/4750 (0.25%)
#        SWITCH BACK: too_high, not_mine
```

The file is written to match the story; no model is called. In your own setup the counts come from your AI step's log, split by which version handled each item.

1. **Write the stop rule first**, with numbers.
2. **Pick the share at random**, and compare with the old group at the same hours.
3. **Count what the AI produced**, not just crashes.
4. **Try the switch back** before you need it, and time it.

**Limit:** a small share still harms a few people. Hold what the new version produces until the first check passes, where you can.

**Done when:** your stop rule has numbers in it, and you've switched back once and know how long it took.

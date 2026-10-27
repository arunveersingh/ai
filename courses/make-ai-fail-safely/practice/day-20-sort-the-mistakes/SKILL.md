---
name: sort-the-mistakes
description: Day 20 practice — patched is not fixed. When an AI step's mistakes get fixed one complaint at a time, the same kind keeps coming back. Sort recent mistakes into six kinds or fewer, named by why the AI went wrong (not what the user saw), weigh each kind by harm, compare against the fixes already made, and fix the top kind where it starts.
---

# Sort the mistakes

A parcel company's app lets customers message an AI to change a delivery: a new day, a neighbour, a pickup point or a safe place. About 40 mistakes a week reach the complaints log. For six weeks each loud complaint gets its own fix, usually a new line in the instructions (14 lines grow to 31): nine fixes, and the log still shows 42 mistakes in week 1 and 40 in week 6. Then the owner sorts the 120 mistakes from weeks 4 to 6 by why the AI went wrong. Six kinds cover them: A changed the wrong parcel (41), B guessed a missing detail (29), C used saved details over the message (22), D said "done" when the change failed (16), E ignored a "don't" (7, all serious), F other (5). Weighted minor 1, serious 3, kind A is 59 of 182 points (32%) and had no fixes; kind E had four. One fix for kind A (the AI must name the parcel and ask when two could fit, and code checks a parcel was named): the next three weeks show 82 mistakes, 3 of them wrong-parcel.

Patched is not fixed. Fix the kind, not the case.

## Part A — Ask (use on a batch of mistakes)

```
You're sorting mistakes made by an AI step. For each mistake below:
1. CAUSE: one line on why the AI went wrong, not what the user saw.
   Quote the words from the record that show it. If the record doesn't
   show why, write UNKNOWN. Don't guess.
2. KIND: pick one from this list: <your kinds>. If none fits, write
   NEW: <short name for the cause>.
3. HARM: minor, or serious if <your definition of serious>.
Then give one table: kind | mistakes | serious | points (minor 1, serious 3),
highest points first. Every count must trace back to mistake IDs.
Don't merge kinds or change my definitions.
```

Read 10 of the AI's tags yourself before trusting the counts.

**In an orchestrated flow** (spec → plan → tasks → implement): each AI step has a mistakes log with a kind column, a list of kinds and a definition of serious. Fix tasks name a kind and its count, not one complaint. Before a one-off fix, the coding agent tags the complaint; if its kind already has a fix planned, the complaint joins that task. Done means the kind's count drops on the next batch and some of its mistakes join the test cases.

## Part B — Count (you do this)

[`tally.py`](./tally.py) has no dependencies. It reads a mistakes file (`id,kind,harm`, harm is `minor` or `serious`), ranks kinds by points, shows fixes already made per kind (`--fixes`, columns `fix,kind` with the kind's letter or first word), compares with a later batch (`--after`), and warns when Other holds more than 10% or there are more than 6 kinds. Replay the story on made-up files:

```bash
python3 make_demo.py
python3 tally.py mistakes_before.csv --fixes fixes.csv --after mistakes_after.csv
# KIND                                     MISTAKES  SERIOUS  POINTS  FIXES  AFTER
# A wrong parcel changed                         41        9      59      0      3
# B guessed a missing detail                     29        6      41      3     29
# C used saved details over the message          22        5      32      2     22
# D said done when the change failed             16        4      24      0     16
# E ignored a "do not"                            7        7      21      4      7
# F other                                         5        0       5      0      5
# TOTAL                                         120       31     182      9     82
# TOP KIND   A wrong parcel changed: 59 of 182 points (32%), 0 fixes so far
# NOTE       most fixes went to E ignored a "do not" (4 fixes, 21 points)
# AFTER      120 -> 82 mistakes; A wrong parcel changed: 41 -> 3
```

The files are written to match the story; no model is called. In your own setup the mistakes come from your complaints log or bug reports, tagged with the prompt above and checked by you.

1. **Write one line per mistake:** why did the AI go wrong?
2. **Group into six kinds or fewer,** plus Other, named by cause.
3. **Mark harm** minor or serious, and run the tally.
4. **Fix the top kind where it starts,** then re-run on the next batch.

**Limit:** the log holds only reported mistakes. Day 21 samples real traffic to find the rest.

**Done when:** you can name your top kind, its share of the harm, and one fix where it starts.

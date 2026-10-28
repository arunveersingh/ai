---
name: weekly-sample
description: Day 21 practice — quiet is not correct. A complaints log only counts mistakes people notice and report; mistakes that look like good news (a wrong answer marked right) never arrive. Every week, have a person check a small random sample of what the AI actually did, with the AI's output hidden, tag each mistake with your kinds, and compare with earlier weeks and with complaints.
---

# Weekly sample

A maths homework app for children aged 10 to 14: an AI marks about 60,000 answers a week right or wrong and explains the step a child missed. In week 2 of term, complaints run at 85 a week, mostly "my right answer was marked wrong" (0.5 when the answer sheet said 1/2). In week 4 a developer adds a line to the instructions: "If the child's answer means the same as the correct answer, like 0.5 and 1/2, mark it right." By week 10, complaints are down to 52 a week. Then 200 random answers from week 2 and 200 from week 10 are marked again by a maths teacher, without seeing the AI's marks. Week 2: 7 mistakes in 200, 2 of them wrong answers marked right. Week 10: 13 in 200, 10 of them wrong answers marked right (one child wrote 3 for 7 − 10 and got a tick). That's about 3,000 wrong answers marked right a week, and 1 complaint about it. The fix: code checks whether the numbers are equal and the AI only explains. The next two weekly samples find 2, then 1.

Quiet is not correct. Count what the AI did, not what people reported.

## Part A — Ask (use to set up the loop for one AI step)

```
Help me set up a weekly check for this AI step: <what it does>.
1. SAMPLE: how many records to check each week so a kind at 2%
   shows up a few times. Picked at random by a script, never by
   hand, never from complaints.
2. CHECK: a one-page guide for the person checking: what "correct"
   means, with 3 examples. The person decides before seeing the AI's output.
3. KINDS: use my list: <your kinds>. Anything else is NEW: <cause>.
4. COMPARE: a weekly table: kind | this week | last 4 weeks |
   complaints. Flag a kind that doubles, or that is common in the
   sample but rare in complaints.
Don't check the records yourself, and don't change my kinds.
```

**In an orchestrated flow** (spec → plan → tasks → implement): each AI step's spec names its weekly sample (how many, who checks, what "correct" means, its kinds). Any change to instructions or the model names the kinds to watch in the next two samples. The coding agent writes the picking script and the weekly table; it never does the checking. Done means the next two samples show no kind rising, not just fewer complaints.

## Part B — Pick and compare (you do the checking)

[`weekly.py`](./weekly.py) has no dependencies.

- `pick` chooses N records at random from a week's log (CSV), with a seed (a starting number, so the same pick comes out again), and drops any column starting with `ai_` so the person checks without seeing the AI's output.
- `compare` reads weekly counts (`week,kind,in_sample,sampled,complaints`), compares one week with up to four earlier weeks, scales each kind to the week's volume, and flags a kind that is RISING (doubles and reaches 6) or SILENT (its share of the sample is at least three times its share of complaints).

Replay the story on made-up files:

```bash
python3 make_demo.py
python3 weekly.py pick answers.csv 200 --seed w10 > to_mark.csv
python3 weekly.py compare weeks.csv --volume 60000 --week w10
# WEEK w10: 13 mistakes in 200 answers checked (6.5%), about 3,900 a week across 60,000 answers
# compared with: w02
#
# KIND                          EARLIER   NOW  PER WEEK  COMPLAINTS  FLAG
# wrong answer marked right         2.0    10     3,000           1  RISING · SILENT: big in the sample, rare in complaints
# right answer marked wrong         4.0     2       600          44  down
# other                             1.0     1       300           7
#
# COMPLAINTS 52 this week
python3 weekly.py compare weeks.csv --volume 60000 --week w13
# wrong answer marked right         4.7     1       300           -  down
```

The files are written to match the story; no model is called. In your own setup the records come from your AI step's log, and a person who knows what "correct" means does the checking.

1. **Pick at random** with a script, never by hand or from complaints.
2. **Check before looking** at what the AI said.
3. **Tag every disagreement** with a kind from your Day 20 list.
4. **Compare** with the last four weeks and with complaints of the same kind.

**Limit:** 200 records is a rough count. Act on a kind that doubles and reaches 6, or rises two weeks running.

**Done when:** you can name one kind that shows up in your sample more than in your complaints, or show there isn't one.

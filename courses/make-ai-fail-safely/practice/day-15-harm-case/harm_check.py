#!/usr/bin/env python3
"""Harm check: score the harm you fear on its own line, next to the overall score,
so an average can't hide it.

Usage: python3 harm_check.py results.csv --must-catch LABEL [--bar 0.92]
                             [--max-misses 0] [--before old_results.csv]
results.csv: columns id, expected, predicted (expected = the label a person gave).
--must-catch: the label whose misses are the harm you fear (e.g. UNAUTHORISED).
--bar:        the overall pass bar your suite already uses (accuracy).
--max-misses: misses allowed on the harm label (default 0).
--before:     results for the previous version, to show both lines before and after.
Prints OVERALL and HARM lines and a verdict.
Exit 0 = both pass, 1 = harm check fails, 2 = setup problem. No dependencies.
The harm cases must be labelled by a person who knows the harm, not by the
system or agent being evaluated."""
import argparse, csv, sys
from collections import Counter

def load(path):
    try:
        with open(path, newline="") as f:
            rows = list(csv.DictReader(f))
    except OSError as e:
        sys.exit(print(f"SETUP  {e}") or 2)
    if not rows or not {"expected", "predicted"} <= set(rows[0]):
        sys.exit(print(f"SETUP  {path} needs columns expected, predicted") or 2)
    return rows

def score(rows, label):
    right = sum(r["expected"] == r["predicted"] for r in rows)
    harm = [r for r in rows if r["expected"] == label]
    missed = Counter(r["predicted"] for r in harm if r["predicted"] != label)
    return right, len(rows), len(harm), missed

def lines(name, rows, a):
    right, total, n, missed = score(rows, a.must_catch)
    acc = right / total
    ok_overall = acc >= a.bar
    ok_harm = n > 0 and sum(missed.values()) <= a.max_misses
    where = ", ".join(f"{k} {v}" for k, v in missed.most_common()) or "none"
    print(f"{name:7} OVERALL {right}/{total} = {acc:.1%}  bar {a.bar:.1%}  {'PASS' if ok_overall else 'FAIL'}")
    if n == 0:
        print(f"{'':7} HARM    no {a.must_catch} cases in the suite: it can't see this harm  FAIL")
    else:
        print(f"{'':7} HARM    {a.must_catch} caught {n - sum(missed.values())}/{n}"
              f"  misses {sum(missed.values())} (went to: {where})  {'PASS' if ok_harm else 'FAIL'}")
    return ok_overall, ok_harm, sum(missed.values()), n

def main():
    p = argparse.ArgumentParser()
    p.add_argument("results")
    p.add_argument("--must-catch", required=True)
    p.add_argument("--bar", type=float, default=0.92)
    p.add_argument("--max-misses", type=int, default=0)
    p.add_argument("--before")
    a = p.parse_args()
    if a.before:
        lines("before", load(a.before), a)
    ok_overall, ok_harm, misses, n = lines("after" if a.before else "result", load(a.results), a)
    if ok_overall and n == 0:
        print(f"VERDICT LYING: the suite passes with no cases for the harm you fear. Add them first.")
    elif ok_overall and not ok_harm:
        print(f"VERDICT LYING: the suite passes while the harm you fear happens {misses} times. Don't ship.")
    elif not ok_harm:
        print("VERDICT HARM FAIL: fix the harm misses before anything else.")
    elif not ok_overall:
        print("VERDICT harm check passes, overall bar doesn't: your call, with both lines in view.")
    else:
        print("VERDICT both pass.")
    sys.exit(0 if ok_harm else 1)

if __name__ == "__main__":
    main()

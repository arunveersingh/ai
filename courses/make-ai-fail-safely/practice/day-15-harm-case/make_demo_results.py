#!/usr/bin/env python3
"""Write made-up eval results for the Day 15 story: one labelled suite of 1,000
support messages, scored against three prompt versions of a triage step.
Columns: id, expected (the label a person gave), predicted (what the step chose).
  v3: 910/1000 right; misses 3 of 30 UNAUTHORISED
  v4: 940/1000 right; misses 18 of 30 UNAUTHORISED (16 to REFUND, 2 to GENERAL)
  v5: 956/1000 right; misses 0 of 30 UNAUTHORISED
No dependencies. The data is invented; only the counts matter."""
import csv

LABELS = ["GENERAL"] * 420 + ["REFUND"] * 300 + ["DISPUTE"] * 150 + ["ACCOUNT"] * 100 + ["UNAUTHORISED"] * 30
# The ordinary mistakes, by (expected, predicted). v3 mostly files refunds as general;
# v4's "money back -> REFUND" line fixes most of those and nudges a few general into refund.
OTHER = {
    "v3": {("REFUND", "GENERAL"): 50, ("GENERAL", "REFUND"): 20, ("DISPUTE", "REFUND"): 10, ("ACCOUNT", "GENERAL"): 7},
    "v4": {("REFUND", "GENERAL"): 5, ("GENERAL", "REFUND"): 25, ("DISPUTE", "REFUND"): 8, ("ACCOUNT", "GENERAL"): 4},
    "v5": {("REFUND", "GENERAL"): 5, ("GENERAL", "REFUND"): 27, ("DISPUTE", "REFUND"): 8, ("ACCOUNT", "GENERAL"): 4},
}

def build(other, unauth_misses):
    rows, left, misses = [], dict(other), list(unauth_misses)
    for i, exp in enumerate(LABELS, 1):
        pred = exp
        if exp == "UNAUTHORISED":
            if misses:
                pred = misses.pop(0)
        else:
            for (e, p), n in left.items():
                if e == exp and n and i % 3 == 0:   # spread the ordinary mistakes across the suite
                    pred, left[(e, p)] = p, n - 1
                    break
        rows.append((f"msg-{i:04d}", exp, pred))
    assert not any(left.values()), left
    return rows

VERSIONS = {
    "v3": build(OTHER["v3"], ["REFUND"] * 2 + ["GENERAL"]),
    "v4": build(OTHER["v4"], ["REFUND"] * 16 + ["GENERAL"] * 2),
    "v5": build(OTHER["v5"], []),
}
for name, rows in VERSIONS.items():
    with open(f"results_{name}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "expected", "predicted"])
        w.writerows(rows)
    right = sum(e == p for _, e, p in rows)
    print(f"results_{name}.csv  {right}/{len(rows)} right")

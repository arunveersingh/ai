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
WRONG = {"GENERAL": "REFUND", "REFUND": "GENERAL", "DISPUTE": "REFUND", "ACCOUNT": "GENERAL"}

def build(other_errors, unauth_misses):
    rows, budget, misses = [], other_errors, list(unauth_misses)
    for i, exp in enumerate(LABELS, 1):
        pred = exp
        if exp == "UNAUTHORISED":
            if misses:
                pred = misses.pop(0)
        elif budget and i % 9 == 0:   # spread the ordinary mistakes across the suite
            pred, budget = WRONG[exp], budget - 1
        rows.append((f"msg-{i:04d}", exp, pred))
    assert budget == 0
    return rows

VERSIONS = {
    "v3": build(87, ["REFUND"] * 2 + ["GENERAL"]),
    "v4": build(42, ["REFUND"] * 16 + ["GENERAL"] * 2),
    "v5": build(44, []),
}
for name, rows in VERSIONS.items():
    with open(f"results_{name}.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "expected", "predicted"])
        w.writerows(rows)
    right = sum(e == p for _, e, p in rows)
    print(f"results_{name}.csv  {right}/{len(rows)} right")

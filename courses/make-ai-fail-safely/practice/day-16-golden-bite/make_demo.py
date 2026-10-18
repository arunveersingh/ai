#!/usr/bin/env python3
"""Writes made-up files that replay the Day 16 story (payment-to-invoice matching).
golden_v1.csv  240 cases written while building the feature (71 agent-written variants)
golden.csv     the same 240 plus 6 incident cases and 4 near-misses, labelled by AR
results_v6.csv trusted version, results_v7.csv the version that broke,
results_v8.csv the fix. No real data, no model calls."""
import csv

written = [(f"W-{i:03}", "written", "agent" if i > 169 else "ar-team", f"INV-{20000 + i}")
           for i in range(1, 241)]
new = [("INC-1", "incident", "j.meyer (AR)", "INV-20981"),   # 'PO 10452' is the payer's own PO
       ("INC-2", "incident", "j.meyer (AR)", "INV-21177"),   # 'Ref 2026-1045' is not INV-1045
       ("INC-3", "incident", "j.meyer (AR)", "INV-21310"),   # customer number read as invoice number
       ("INC-4", "incident", "j.meyer (AR)", "UNMATCHED"),   # number says one customer, payer another
       ("INC-5", "incident", "j.meyer (AR)", "INV-21402"),   # credit note number in remittance
       ("INC-6", "incident", "j.meyer (AR)", "UNMATCHED"),   # two invoices, amount fits neither
       ("NM-1", "near-miss", "a.costa (AR)", "INV-21533"),   # reviewer fixed before posting
       ("NM-2", "near-miss", "a.costa (AR)", "UNMATCHED"),
       ("NM-3", "near-miss", "a.costa (AR)", "INV-21610"),
       ("NM-4", "near-miss", "a.costa (AR)", "INV-21688")]
v7_wrong = {"INC-1": "INV-10452", "INC-2": "INV-01045", "INC-3": "INV-30077", "INC-4": "INV-18840",
            "INC-5": "INV-19902", "INC-6": "INV-21455", "NM-1": "INV-11533", "NM-2": "INV-17004",
            "NM-3": "INV-10610", "NM-4": "INV-12688"}

def write(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f); w.writerow(header); w.writerows(rows)

write("golden_v1.csv", ["id", "source", "labelled_by", "expected"], written)
write("golden.csv", ["id", "source", "labelled_by", "expected"], written + new)
allc = written + new
write("results_v6.csv", ["id", "predicted"], [(c[0], c[3]) for c in allc])
write("results_v7.csv", ["id", "predicted"], [(c[0], v7_wrong.get(c[0], c[3])) for c in allc])
write("results_v8.csv", ["id", "predicted"], [(c[0], c[3]) for c in allc])
print("wrote golden_v1.csv (240), golden.csv (250), results_v6.csv, results_v7.csv, results_v8.csv")

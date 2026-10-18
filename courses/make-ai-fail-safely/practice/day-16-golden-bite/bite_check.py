#!/usr/bin/env python3
"""Bite check: does your golden set fail on a version you know is wrong?

A golden case has teeth only if it fails on a known-bad version. A set that
gives the broken version a perfect score can't tell broken from fixed.

Usage: python3 bite_check.py golden.csv --bad bad_results.csv [--bad ...]
                             --candidate new_results.csv
golden.csv:   columns id, source, labelled_by, expected
              source = where the case came from (incident, near-miss, written...)
              labelled_by = the person who owns the outcome (not the agent)
*_results.csv: columns id, predicted (one row per golden case)
--bad:        results from a version you know is wrong (the one that caused
              the incident). Repeat for more than one.
--candidate:  results from the version you want to trust.
Exit 0 = candidate passes and the set has teeth, 1 = no teeth or candidate
fails, 2 = setup problem. No dependencies."""
import argparse, csv, sys
from collections import OrderedDict

NOT_A_LABELLER = {"", "agent", "model", "ai", "llm", "generated"}

def load(path, need):
    try:
        with open(path, newline="") as f:
            rows = list(csv.DictReader(f))
    except OSError as e:
        sys.exit(print(f"SETUP  {e}") or 2)
    if not rows or not need <= set(rows[0]):
        sys.exit(print(f"SETUP  {path} needs columns {', '.join(sorted(need))}") or 2)
    return rows

def preds(path, ids):
    got = {r["id"]: r["predicted"] for r in load(path, {"id", "predicted"})}
    missing = [i for i in ids if i not in got]
    if missing:
        sys.exit(print(f"SETUP  {path} has no result for {len(missing)} cases, e.g. {missing[0]}") or 2)
    return got

def main():
    p = argparse.ArgumentParser()
    p.add_argument("golden")
    p.add_argument("--bad", action="append", required=True)
    p.add_argument("--candidate", required=True)
    a = p.parse_args()
    cases = load(a.golden, {"id", "source", "labelled_by", "expected"})
    ids = [c["id"] for c in cases]
    bads = [preds(b, ids) for b in a.bad]
    cand = preds(a.candidate, ids)

    unowned = [c for c in cases if c["labelled_by"].strip().lower() in NOT_A_LABELLER]
    counted = [c for c in cases if c not in unowned]
    groups = OrderedDict()
    for c in counted:
        g = groups.setdefault(c["source"], {"n": 0, "bite": 0, "ok": 0})
        g["n"] += 1
        g["bite"] += any(b[c["id"]] != c["expected"] for b in bads)
        g["ok"] += cand[c["id"]] == c["expected"]

    print(f"SET     {a.golden}  {len(cases)} cases  known-bad: {', '.join(a.bad)}  candidate: {a.candidate}")
    if unowned:
        print(f"NOT COUNTED  {len(unowned)} cases labelled by the agent or nobody: "
              "a case can't check the reading it was labelled with")
    print(f"{'SOURCE':12}{'CASES':>6}  {'FAIL ON BAD':>12}  {'CANDIDATE':>10}")
    for s, g in groups.items():
        print(f"{s:12}{g['n']:>6}  {str(g['bite']) + '/' + str(g['n']):>12}  {str(g['ok']) + '/' + str(g['n']):>10}")
    teeth = sum(g["bite"] for g in groups.values())
    passed = sum(g["ok"] for g in groups.values())
    print(f"TEETH   {teeth}/{len(counted)} counted cases fail on the known-bad version")
    failed = len(counted) - passed
    if failed:
        print(f"CANDIDATE FAIL  {failed} counted cases fail. Don't ship.")
    if teeth == 0:
        print("VERDICT NO TEETH: no counted case fails on the known-bad version, so this set "
              "can't tell it from a good one. Add cases from the mistake before you trust it.")
        return 1
    if failed:
        print("VERDICT FAIL: fix the candidate first.")
        return 1
    print(f"VERDICT PASS: candidate passes {passed}/{len(counted)}, and {teeth} of those cases "
          "would have caught the known-bad version.")
    return 0

if __name__ == "__main__":
    sys.exit(main())

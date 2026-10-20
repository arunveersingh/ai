#!/usr/bin/env python3
"""Regression harness: every case, every line, on every change to what the step reads.

An AI step's behaviour depends on more than its prompt: the model snapshot, the tools
that build its input, the reference data it is given. The manifest lists all of them.
The harness scores every case on every line, fails if any line fails, compares each
case with the last passing run (fixed / broke), and remembers which configuration
passed, so you can refuse to ship one that never did.

Usage:
  python3 harness.py manifest.json cases.csv results.csv   score a run (saves it if it passes)
  python3 harness.py --verify manifest.json                exit 1 unless this exact
                                                           configuration has passed
manifest.json: {"prompt_file": "...", "model": "<pinned snapshot>",
                "tools": {...}, "data": {...}, "bars": {"everyday": 0.95}}
               paths are relative to the manifest; the prompt file's content is hashed
cases.csv:     id, line, expected, labelled_by
               line = everyday | harm | incident | attack (everyday uses the bar,
               the other lines allow zero misses)
results.csv:   id, got (one row per case, from the configuration in the manifest)
The last passing run is kept in last_pass.json next to the manifest.
Exit 0 = pass, 1 = a line failed or the model is not pinned, 2 = setup problem.
No dependencies."""
import csv, hashlib, json, os, sys

LINES = ("everyday", "harm", "incident", "attack")
PARTS = ("prompt", "model", "tools", "data")
NOT_A_LABELLER = {"", "agent", "model", "ai", "llm", "generated"}

def die(msg):
    print(f"SETUP  {msg}"); sys.exit(2)

def load_manifest(path):
    try:
        m = json.load(open(path))
        prompt = open(os.path.join(os.path.dirname(os.path.abspath(path)), m["prompt_file"]), "rb").read()
    except (OSError, ValueError, KeyError) as e:
        die(f"{path}: {e}")
    parts = {"prompt": hashlib.sha256(prompt).hexdigest()[:10], "model": m.get("model", ""),
             "tools": m.get("tools", {}), "data": m.get("data", {})}
    fp = hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest()[:10]
    return m, parts, fp

def last_pass_path(manifest):
    return os.path.join(os.path.dirname(os.path.abspath(manifest)), "last_pass.json")

def unpinned(model):
    return not model or any(w in model.lower() for w in ("latest", "default", "stable", "preview"))

def load_csv(path, need):
    try:
        rows = list(csv.DictReader(open(path, newline="")))
    except OSError as e:
        die(str(e))
    if not rows or not need <= set(rows[0]):
        die(f"{path} needs columns {', '.join(sorted(need))}")
    return rows

def verify(manifest):
    _, parts, fp = load_manifest(manifest)
    try:
        lp = json.load(open(last_pass_path(manifest)))
    except OSError:
        print(f"VERIFY FAIL  fingerprint {fp}: nothing has passed yet. Run the harness."); return 1
    if lp["fingerprint"] == fp:
        print(f"VERIFY OK  fingerprint {fp} passed the harness. Safe to ship this configuration."); return 0
    changed = [p for p in PARTS if lp["parts"].get(p) != parts[p]]
    print(f"VERIFY FAIL  fingerprint {fp} has never passed (last pass {lp['fingerprint']}). "
          f"Changed: {', '.join(changed)}. Run the harness before you ship."); return 1

def main(argv):
    if len(argv) == 2 and argv[0] == "--verify":
        return verify(argv[1])
    if len(argv) != 3:
        print(__doc__); return 2
    manifest, cases_p, results_p = argv
    m, parts, fp = load_manifest(manifest)
    cases = load_csv(cases_p, {"id", "line", "expected", "labelled_by"})
    got = {r["id"]: r["got"].strip() for r in load_csv(results_p, {"id", "got"})}
    missing = [c["id"] for c in cases if c["id"] not in got]
    if missing:
        die(f"{results_p} has no result for {len(missing)} cases, e.g. {missing[0]}. The harness runs every case.")
    unknown = sorted({c["line"] for c in cases} - set(LINES))
    if unknown:
        die(f"unknown line(s): {', '.join(unknown)}")
    unowned = [c["id"] for c in cases if c["line"] != "everyday" and c["labelled_by"].strip().lower() in NOT_A_LABELLER]
    if unowned:
        die(f"{len(unowned)} gated cases have no human labeller, e.g. {unowned[0]}")

    try:
        lp = json.load(open(last_pass_path(manifest)))
    except OSError:
        lp = None
    changed = [p for p in PARTS if lp and lp["parts"].get(p) != parts[p]]
    print(f"RUN  fingerprint {fp}  prompt {parts['prompt']}  model {parts['model']}  {len(cases)} cases")
    if lp:
        print(f"     changed since last pass ({lp['fingerprint']}): {', '.join(changed) or 'nothing'}")
    failed = []
    if unpinned(parts["model"]):
        print(f"MODEL NOT PINNED  '{parts['model']}' can change under you. Use a dated snapshot.")
        failed.append("model")
    bar = m.get("bars", {}).get("everyday", 0.95)
    ok = {}
    for line in LINES:
        rows = [c for c in cases if c["line"] == line]
        if not rows:
            print(f"{line.upper():9} no cases  FAIL"); failed.append(line); continue
        good = sum(got[c["id"]] == c["expected"].strip() for c in rows)
        ok[line] = good
        if line == "everyday":
            passed = good / len(rows) >= bar
            print(f"{'EVERYDAY':9} {f'{good}/{len(rows)} = {100*good/len(rows):.1f}%':18} {f'bar {100*bar:.0f}%':19}  {'PASS' if passed else 'FAIL'}")
        else:
            passed = good == len(rows)
            print(f"{line.upper():9} {f'{good}/{len(rows)}':18} zero misses allowed  {'PASS' if passed else 'FAIL'}")
        if not passed:
            failed.append(line)
    if lp:
        prev = lp["results"]
        exp = {c["id"]: c["expected"].strip() for c in cases}
        fixed = [i for i in exp if i in prev and prev[i] != exp[i] and got[i] == exp[i]]
        broke = [i for i in exp if i in prev and prev[i] == exp[i] and got[i] != exp[i]]
        order = {"harm": 0, "incident": 1, "attack": 2, "everyday": 3}
        line_of = {c["id"]: c["line"] for c in cases}
        broke.sort(key=lambda i: order[line_of[i]])   # gated lines first
        print(f"DIFF vs last pass  fixed {len(fixed)} | broke {len(broke)}")
        for i in broke[:12]:
            print(f"  BROKE {i}: expected {exp[i]!r}, got {got[i]!r}")
        if len(broke) > 12:
            print(f"  ... and {len(broke) - 12} more")
    if failed:
        print(f"RESULT FAIL ({', '.join(failed)}). Don't ship fingerprint {fp}.")
        return 1
    json.dump({"fingerprint": fp, "parts": parts, "results": got}, open(last_pass_path(manifest), "w"))
    print(f"RESULT PASS. Saved fingerprint {fp} as the last pass.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

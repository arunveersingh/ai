"""Day 19: raised is not improved. Score the target AND the guards the tuner can't move.

usage: python3 guard_check.py RUN.csv [--baseline LIVE.csv] [--target 0.80] [--agree 0.85]

RUN.csv columns: id,set,judge,human,ticket
  set=tune    the cases the tuner sees.            judge: 1 if the AI judge said resolved
  set=fault   held-out chats with a confirmed fault. ticket: 1 if this version opened a ticket
  set=review  this version's new chats, labelled blind by people. judge, human: 1 = resolved

Exit 0 only if the guards pass AND either the target is met or people's resolved rate beats
the live version. Meeting the target is reported, never enough on its own.
"""
import csv, sys

def load(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def scores(rows):
    tune = [r for r in rows if r["set"] == "tune"]
    fault = [r for r in rows if r["set"] == "fault"]
    review = [r for r in rows if r["set"] == "review"]
    leaked = {r["id"] for r in tune} & {r["id"] for r in fault + review}
    return {
        "tune": (sum(int(r["judge"]) for r in tune), len(tune)),
        "fault": (sum(int(r["ticket"]) for r in fault), len(fault)),
        "agree": (sum(r["judge"] == r["human"] for r in review), len(review)),
        "people": (sum(int(r["human"]) for r in review), len(review)),
        "leaked": leaked,
    }

def pct(a, b):
    return 100.0 * a / b if b else 0.0

def main(argv):
    if not argv or argv[0].startswith("-"):
        print(__doc__); return 2
    args = {"--baseline": None, "--target": "0.80", "--agree": "0.85"}
    path, rest = argv[0], argv[1:]
    for k, v in zip(rest[::2], rest[1::2]):
        args[k] = v
    target, agree_bar = float(args["--target"]), float(args["--agree"])
    s = scores(load(path))
    base = scores(load(args["--baseline"])) if args["--baseline"] else None

    t_ok, t_n = s["tune"]
    target_met = t_n and t_ok / t_n >= target
    print(f"TARGET   judge 'resolved' on tuning set   {t_ok}/{t_n} = {pct(t_ok, t_n):.1f}%   target {target:.0%}   "
          f"{'MET' if target_met else 'MISSED'}")

    fails = []
    f_ok, f_n = s["fault"]
    line = f"GUARD 1  confirmed faults ticketed (held out) {f_ok}/{f_n}"
    if base:
        b_ok, b_n = base["fault"]
        ok = f_n and b_n and f_ok / f_n >= b_ok / b_n
        line += f"   live {b_ok}/{b_n}   must not drop   {'PASS' if ok else 'FAIL'}"
        if not ok: fails.append("faults ticketed dropped")
    else:
        line += "   (no baseline given)"
    print(line)

    a_ok, a_n = s["agree"]
    ok = a_n and a_ok / a_n >= agree_bar
    print(f"GUARD 2  judge agrees with people (blind)  {a_ok}/{a_n} = {pct(a_ok, a_n):.0f}%   bar {agree_bar:.0%}   {'PASS' if ok else 'FAIL'}")
    if not ok: fails.append("judge no longer agrees with people")

    p_ok, p_n = s["people"]
    print(f"INFO     resolved, as people judged it     {p_ok}/{p_n} = {pct(p_ok, p_n):.0f}%"
          + (f"   live {base['people'][0]}/{base['people'][1]}" if base else ""))

    if s["leaked"]:
        fails.append(f"{len(s['leaked'])} held-out ids also in the tuning set")
        print(f"GUARD 3  held-out cases leaked into tuning  {sorted(s['leaked'])[:5]}   FAIL")

    if fails:
        why = "; ".join(fails)
        if target_met:
            print(f"RESULT   BLOCKED. Target met, guards failed ({why}). The score rose without the fix.")
        else:
            print(f"RESULT   BLOCKED. Guards failed ({why}).")
        return 1
    if target_met:
        print("RESULT   SHIP. Target met and guards held.")
        return 0
    if base and pct(*s["people"]) > pct(*base["people"]):
        print("RESULT   SHIP. Target missed, but guards held and people's resolved rate rose. Revisit the target, not the measure.")
        return 0
    print("RESULT   HOLD. Guards held, target missed, no real gain shown.")
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

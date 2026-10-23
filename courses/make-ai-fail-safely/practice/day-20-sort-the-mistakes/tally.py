"""Day 20: sort the mistakes. Counts each kind, weighs it by harm (minor 1, serious 3),
ranks kinds by points, shows how many fixes each kind already got, and warns when
the list of kinds needs work. No dependencies.

usage: python3 tally.py mistakes.csv [--fixes fixes.csv] [--after later.csv]
mistakes.csv columns: id,kind,harm   (harm = minor or serious; kind starts with a letter or name)"""
import csv, sys
from collections import Counter
POINTS = {'minor': 1, 'serious': 3}
def load(path):
    rows = list(csv.DictReader(open(path)))
    for r in rows:
        if r['harm'] not in POINTS: sys.exit(f"{r['id']}: harm must be minor or serious, got {r['harm']!r}")
        if not r['kind'].strip(): sys.exit(f"{r['id']}: no kind. Give it one, or 'other'.")
    return rows
args = sys.argv[1:]
if not args: sys.exit(__doc__)
rows = load(args[0])
fixes = Counter(); after = None
if '--fixes' in args: fixes = Counter(r['kind'] for r in csv.DictReader(open(args[args.index('--fixes') + 1])))
if '--after' in args: after = Counter(r['kind'] for r in load(args[args.index('--after') + 1]))
count = Counter(r['kind'] for r in rows)
serious = Counter(r['kind'] for r in rows if r['harm'] == 'serious')
points = Counter({r['kind']: 0 for r in rows})
for r in rows: points[r['kind']] += POINTS[r['harm']]
key = lambda k: k.split()[0]
kinds = sorted(count, key=lambda k: -points[k])
head = f"{'KIND':40} {'MISTAKES':>8} {'SERIOUS':>8} {'POINTS':>7} {'FIXES':>6}" + (f" {'AFTER':>6}" if after else '')
print(head); print('-' * len(head))
for k in kinds:
    line = f"{k:40} {count[k]:>8} {serious[k]:>8} {points[k]:>7} {fixes[key(k)]:>6}"
    if after is not None: line += f" {after[k]:>6}"
    print(line)
total = len(rows); tp = sum(points.values())
line = f"{'TOTAL':40} {total:>8} {sum(serious.values()):>8} {tp:>7} {sum(fixes.values()):>6}"
if after is not None: line += f" {sum(after.values()):>6}"
print(line)
print()
real = [k for k in kinds if 'other' not in k.lower()]
top = real[0]
print(f"TOP KIND   {top}: {points[top]} of {tp} points ({100*points[top]/tp:.0f}%), {fixes[key(top)]} fixes so far")
most_fixed = max(real, key=lambda k: fixes[key(k)])
if fixes[key(most_fixed)] and most_fixed != top:
    print(f"NOTE       most fixes went to {most_fixed} ({fixes[key(most_fixed)]} fixes, {points[most_fixed]} points)")
other = sum(count[k] for k in kinds if 'other' in k.lower())
if other / total > 0.10: print(f"WARN       'other' holds {other} of {total} (over 10%): add a kind")
if len(real) > 6: print(f"WARN       {len(real)} kinds: merge to 6 or fewer, or every kind looks like a one-off")
if after is not None:
    print(f"AFTER      {total} -> {sum(after.values())} mistakes; {top}: {count[top]} -> {after[top]}")
print(f"NEXT       fix {top} where it starts, then re-run this on the next batch")

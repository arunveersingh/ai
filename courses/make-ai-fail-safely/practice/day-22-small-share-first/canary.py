"""Day 22: check a small-share release against stop rules written before it started. No dependencies.

python3 canary.py hours.csv [--min 200] [--factor 2]

hours.csv columns: check,group,items,<signal>,<signal>,...
  check   = when the hourly check ran (e.g. 10:00)
  group   = new (the small share on the change) or old (everyone else)
  items   = how many items that group handled in that hour
  signals = counts of bad signs in that hour, e.g. too_high, not_mine

Stop rule: once the new group has at least --min items, switch back if any
signal's rate in the new group is more than --factor times the old group's
rate over the same hours (and has happened at least 3 times)."""
import csv, sys
from collections import defaultdict
args = sys.argv[1:]
if not args: sys.exit(__doc__)
def opt(name, default):
    return type(default)(args[args.index(name) + 1]) if name in args else default
MIN, FACTOR = opt('--min', 200), opt('--factor', 2.0)
rows = list(csv.DictReader(open(args[0])))
signals = [c for c in rows[0] if c not in ('check', 'group', 'items')]
tot = {g: defaultdict(int) for g in ('new', 'old')}
checks = list(dict.fromkeys(r['check'] for r in rows))
print(f"STOP RULE  new group needs {MIN} items; switch back if a signal runs more than {FACTOR:g}x the old group\n")
for ck in checks:
    for r in rows:
        if r['check'] != ck: continue
        for c in ['items'] + signals: tot[r['group']][c] += int(r[c])
    n, o = tot['new']['items'], tot['old']['items']
    parts, fired = [], []
    for s in signals:
        rn, ro = tot['new'][s] / n, tot['old'][s] / o
        parts.append(f"{s} {tot['new'][s]}/{n} ({100*rn:.1f}%) vs {tot['old'][s]}/{o} ({100*ro:.2f}%)")
        if n >= MIN and tot['new'][s] >= 3 and rn > FACTOR * ro: fired.append(s)
    verdict = ('WAIT: fewer than %d items in the new group' % MIN if n < MIN
               else 'SWITCH BACK: ' + ', '.join(fired) if fired else 'HOLDING')
    print(f"{ck}  " + '  ·  '.join(parts)); print(f"       {verdict}")
    if fired: break

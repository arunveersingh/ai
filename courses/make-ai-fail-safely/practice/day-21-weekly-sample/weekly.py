"""Day 21: the weekly sample. No dependencies.

pick     choose N answers at random from a week's log, for a person to mark
         python3 weekly.py pick answers.csv 200 --seed w10 > to_mark.csv
compare  compare one week's sample with earlier weeks and with the complaints log
         python3 weekly.py compare weeks.csv --volume 60000 [--week w10]

weeks.csv columns: week,kind,in_sample,sampled,complaints
  in_sample  = mistakes of that kind the person found in the week's sample
  sampled    = how many answers were checked that week
  complaints = complaints of that kind that week (blank if not counted)"""
import csv, random, sys
from collections import defaultdict
args = sys.argv[1:]
if len(args) < 2: sys.exit(__doc__)
def opt(name, default=None):
    return args[args.index(name) + 1] if name in args else default

if args[0] == 'pick':
    rows = list(csv.DictReader(open(args[1])))
    n = int(args[2]); seed = opt('--seed', 'week')
    pick = random.Random(seed).sample(rows, min(n, len(rows)))   # random: not complaints, not hard cases
    w = csv.writer(sys.stdout)
    cols = [c for c in rows[0] if not c.lower().startswith('ai_')]  # the person marks without seeing the AI's mark
    w.writerow(cols + ['person_mark', 'kind'])
    for r in pick: w.writerow([r[c] for c in cols] + ['', ''])
    sys.stderr.write(f"picked {len(pick)} of {len(rows)} answers (seed {seed!r}); AI's mark hidden\n")
    sys.exit()

if args[0] != 'compare': sys.exit(__doc__)
data = defaultdict(dict); sampled = {}
for r in csv.DictReader(open(args[1])):
    data[r['week']][r['kind']] = (int(r['in_sample']), r['complaints'])
    sampled[r['week']] = int(r['sampled'])
weeks = list(data); volume = int(opt('--volume', 0))
week = opt('--week', weeks[-1]); i = weeks.index(week)
base = weeks[max(0, i - 4):i]
if not base: sys.exit('need at least one earlier week to compare with')
kinds = list(data[week]); n = sampled[week]
found = sum(v[0] for v in data[week].values())
comp = {k: data[week][k][1] for k in kinds}
total_c = sum(int(c) for c in comp.values() if c != '')
print(f"WEEK {week}: {found} mistakes in {n} answers checked ({100*found/n:.1f}%)"
      + (f", about {round(found/n*volume):,} a week across {volume:,} answers" if volume else ''))
print(f"compared with: {', '.join(base)}\n")
head = f"{'KIND':28} {'EARLIER':>8} {'NOW':>5} {'PER WEEK':>9} {'COMPLAINTS':>11}  FLAG"
print(head); print('-' * len(head))
for k in kinds:
    now = data[week][k][0]
    avg = sum(data[b].get(k, (0, ''))[0] for b in base) / len(base)
    est = round(now / n * volume) if volume else ''
    flags = []
    if now >= 6 and now >= 2 * avg: flags.append('RISING')
    c = comp[k]
    if c != '' and found and total_c and now / found >= 3 * (int(c) / total_c) and now >= 3:
        flags.append('SILENT: big in the sample, rare in complaints')
    if avg >= 3 and now <= avg / 2: flags.append('down')
    est_s = f"{est:,}" if est != '' else ''
    print(f"{k:28} {avg:>8.1f} {now:>5} {est_s:>9} {c if c != '' else '-':>11}  {' · '.join(flags)}")
print(f"\nCOMPLAINTS {total_c} this week" if total_c else '')
print("NOTE  200 answers is a rough count: act on a kind that doubles and reaches 6, or rises two weeks running")

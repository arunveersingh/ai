"""Write the Day 20 story's made-up files: 120 mistakes from weeks 4-6 (before),
the 9 one-off fixes, and 82 mistakes from the 3 weeks after one fix for kind A."""
import csv
KINDS = {  # kind: (mistakes before, serious before, mistakes after)
    'A wrong parcel changed':              (41, 9, 3),
    'B guessed a missing detail':          (29, 6, 29),
    'C used saved details over the message': (22, 5, 22),
    'D said done when the change failed':  (16, 4, 16),
    'E ignored a "do not"':                (7, 7, 7),
    'F other':                             (5, 0, 5),
}
FIXES = ['E']*4 + ['B']*3 + ['C']*2   # 9 one-off fixes, one per complaint
def write(path, idx):
    n = 0
    with open(path, 'w', newline='') as f:
        w = csv.writer(f); w.writerow(['id', 'kind', 'harm'])
        for kind, v in KINDS.items():
            total = v[idx]; serious = v[1] if idx == 0 else 0
            for i in range(total):
                n += 1; w.writerow([f'M{n:03d}', kind, 'serious' if i < serious else 'minor'])
    return n
print('mistakes_before.csv', write('mistakes_before.csv', 0), 'rows')
print('mistakes_after.csv ', write('mistakes_after.csv', 2), 'rows')
with open('fixes.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['fix', 'kind'])
    for i, k in enumerate(FIXES, 1): w.writerow([f'fix{i}', k])
print('fixes.csv           ', len(FIXES), 'rows')

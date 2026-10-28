"""Write the Day 21 story's made-up files: a week of answers to sample from, and the
weekly counts (sample checks and complaints) for weeks 2, 10, 12 and 13 of term."""
import csv, random
# 1) 60,000 marked answers from one week, so you can try `weekly.py pick`
with open('answers.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['id', 'question', 'child_answer', 'ai_mark'])
    rng = random.Random(1)
    for i in range(1, 60001):
        a, b = rng.randint(1, 20), rng.randint(1, 20)
        w.writerow([f'A{i:05d}', f'{a} - {b}', a - b, 'right'])
# 2) what the sample checks and the complaints log found each week
WEEKS = [  # week, sampled, (wrong marked right, right marked wrong, other), complaints (same order)
    ('w02', 200, (2, 4, 1), (1, 76, 8)),
    ('w10', 200, (10, 2, 1), (1, 44, 7)),
    ('w12', 200, (2, 2, 1), None),
    ('w13', 200, (1, 2, 1), None),
]
KINDS = ['wrong answer marked right', 'right answer marked wrong', 'other']
with open('weeks.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['week', 'kind', 'in_sample', 'sampled', 'complaints'])
    for week, n, s, c in WEEKS:
        for i, k in enumerate(KINDS):
            w.writerow([week, k, s[i], n, '' if c is None else c[i]])
print('answers.csv  60000 rows (made-up answers to pick from)')
print('weeks.csv   ', len(WEEKS) * len(KINDS), 'rows (weeks 2, 10, 12 and 13 of term)')

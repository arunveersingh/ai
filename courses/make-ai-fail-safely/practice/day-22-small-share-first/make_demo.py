"""Writes hours.csv to match the Day 22 story (made-up numbers, no model is called)."""
rows = [('10:00', 'new', 83, 8, 2), ('10:00', 'old', 1583, 6, 4),
        ('11:00', 'new', 83, 8, 3), ('11:00', 'old', 1583, 6, 4),
        ('12:00', 'new', 84, 8, 2), ('12:00', 'old', 1584, 7, 4)]
with open('hours.csv', 'w') as f:
    f.write('check,group,items,too_high,not_mine\n')
    for r in rows: f.write(','.join(map(str, r)) + '\n')
print('wrote hours.csv')

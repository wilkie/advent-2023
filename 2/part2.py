import re, functools

total = 0
possible = (12, 13, 14)
r, g, b = [0, 0, 0]
for line in open('input', 'r'):
  # Get id
  id, sets = line.strip().split(':', 2)
  id = int(id.split()[1])

  # Get maximum r, g, b values
  min_set = (0, 0, 0,)
  for part in sets.strip().split(';'):
    r, g, b = functools.reduce(lambda a, b: (a[0] or b[0] or 0, a[1] or b[1] or 0, a[2] or b[2] or 0,),
        (re.findall(r'(?P<red>\d+) red|(?P<green>\d+) green|(?P<blue>\d+) blue', part.strip())))
    min_set = (max(int(r or 0), min_set[0]), max(int(g or 0), min_set[1]), max(int(b or 0), min_set[2]),)
  power = min_set[0] * min_set[1] * min_set[2]
  total += power

print(total)

import re, functools

total = 0
possible = (12, 13, 14)
r, g, b = [0, 0, 0]
for line in open('input', 'r'):
  # Get id
  id, sets = line.strip().split(':', 2)
  id = int(id.split()[1])

  # Get r, g, b values
  possible_game = True
  for part in sets.strip().split(';'):
    r, g, b = functools.reduce(lambda a, b: (a[0] or b[0] or 0, a[1] or b[1] or 0, a[2] or b[2] or 0,),
        (re.findall(r'(?P<red>\d+) red|(?P<green>\d+) green|(?P<blue>\d+) blue', part.strip())))

    # It isn't possible if any value is greater than the known starting value
    if int(r or 0) > possible[0] or int(g or 0) > possible[1] or int(b or 0) > possible[2]:
      possible_game = False
      break
  if possible_game:
    total += id

print(total)

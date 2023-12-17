from functools import cache

# The original data
rows = list(map(lambda x: x.strip(), open('input', 'r')))

# I need to unfortunately convert this into columns first
x_dim = len(rows[0])
y_dim = len(rows)

# This moves 'O' to their extremes within a list. Moves them to the 'right'
# (greater indices) by default or to the 'left' when reverse is True.
@cache
def collapse(span, reverse=False):
  count = 0
  j = 0
  ret = ()
  for i, item in enumerate(span):
    if item == 'O':
      count += 1

    if item == '#':
      if reverse:
        ret = (*ret, *(['O'] * count), *(['.'] * (i - count - j)), '#',)
      else:
        ret = (*ret, *(['.'] * (i - count - j)), *(['O'] * count), '#',)
      count = 0
      j = i + 1

  # Put any left over
  if reverse:
    return (*ret, *(['O'] * count), *(['.'] * (i + 1 - count - j)),)
  return (*ret, *(['.'] * (i + 1 - count - j)), *(['O'] * count),)

spans = rows
stable_states = {}

# Apply
i = 0
CYCLES = 1000000000
while i < CYCLES:
  for direction in [True, False]:
    # Rotate
    spans = list(map(lambda x: tuple(map(lambda span: span[x], spans)), range(x_dim)))
    # North / South
    spans = list(map(lambda x: collapse(x, reverse=direction), spans))

    # Rotate
    spans = list(map(lambda y: tuple(map(lambda span: span[y], spans)), range(y_dim)))
    # West / East
    spans = list(map(lambda y: collapse(y, reverse=direction), spans))

  # Memoize the 'stable state' and just loop it
  hash = '-'.join(map(lambda row: str(sum(map(lambda t: pow(2, t[0]) if t[1] == 'O' else 0, enumerate(row)))), spans))
  if hash in stable_states:
    info = stable_states[hash]
    if info[1] < info[0]:
      stable_states[hash] = (info[0], i - info[0],)
    info = stable_states[hash]
    # Get 'i' as close to CYCLES without going over
    i += ((CYCLES - i) // info[1]) * info[1]
  else:
    stable_states[hash] = (i, 0,)
  i += 1

# Determine load
total = 0
for y, span in enumerate(spans):
  sub_total = span.count('O') * (y_dim - y)
  total += sub_total
print(total)

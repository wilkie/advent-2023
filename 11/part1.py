import itertools

galaxies = []

x = 0
y = 0
empty = None
for line in open('input', 'r'):
  line = line.strip()
  # Keep track of empty columns
  if empty is None:
    empty = [True] * len(line)

  # Go through the line
  x = 0
  for i, item in enumerate(line):
    if item != '.':
      empty[i] = False
    if item == '#':
      # Keep track of galaxies
      galaxies.append((x, y,))
    x += 1

  # Is the row empty? expand y, if so
  if line.count('.') == len(line):
    y += 1
  y += 1
num_galaxies = len(galaxies)

# Adjust galaxies that have expanded columns
x_spans = [0]
x_delta = 0
for i, item in enumerate(empty):
  if item:
    x_delta += 1
  x_spans.append(x_delta)
for i in range(num_galaxies):
  galaxies[i] = (galaxies[i][0] + x_spans[galaxies[i][0]], galaxies[i][1],)

# Now, for all combinations, find the manhattan distance between each pair
print(
  sum(
    map(
      lambda pair: abs(pair[0][0] - pair[1][0]) + abs(pair[0][1] - pair[1][1]),
      itertools.combinations(galaxies, 2)
    )
  )
)

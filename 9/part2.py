from functools import reduce

total = 0
for line in open('input', 'r'):
  values = list(map(int, line.split(' ')))
  depth = 0
  while not all(map(lambda x: x == 0, values[depth:-1])):
    for i in range(len(values) - 1, depth, -1):
      values[i] = values[i] - values[i - 1]
    depth += 1
  total += reduce(lambda a, b: b - a, reversed(values), 0)
print(total)

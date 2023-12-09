total = 0
for line in open('input', 'r'):
  values = list(map(int, line.split(' ')))
  depth = len(values)
  while not all(map(lambda x: x == 0, values[0:depth])):
    depth -= 1
    for i in range(depth):
      values[i] = values[i + 1] - values[i]
  total += sum(values)
print(total)

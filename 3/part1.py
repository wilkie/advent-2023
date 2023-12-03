import re

# If there is a 'symbol' at any point surrounding a number, that sequence of
# numbers is a part number. If we look at the entire input as one uninterrupted
# line, then we are looking for numbers with symbols that are:
# width - 1, width, width + 1, -1, +1, -width - 1, -width, and -width + 1
# characters away from it. (or the inverse, find a sequence of numbers that far
# away from a symbol, which is what we will do here)

lines = open('input', 'r').read().split('\n')
width = len(lines[0])
input = ''.join(lines)

# Compile set of parts (part ids can appear more than once)
parts = {}
inventory = []
for part in re.compile('\d+').finditer(input):
  for i in range(part.start(), part.end()):
    parts[i] = len(inventory)
  inventory.append(int(part[0]))

# Look up via finding symbols
regex = re.compile('[^.\d]')
result = set()
for symbol in regex.finditer(input):
  for check_at in [width, width + 1, width - 1, -1, 1, -width, -(width - 1), -(width + 1)]:
    idx = check_at + symbol.start()
    if parts.get(idx, None) is not None:
      result.add(parts[idx])

print(sum(map(lambda idx: inventory[idx], result)))

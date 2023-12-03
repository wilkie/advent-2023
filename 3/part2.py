import re

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

# Look up via finding symbols for gears
regex = re.compile('[*]')
total = 0
for symbol in regex.finditer(input):
  gear_parts = set()
  for check_at in [width, width + 1, width - 1, -1, 1, -width, -(width - 1), -(width + 1)]:
    idx = check_at + symbol.start()
    if parts.get(idx, None) is not None:
      gear_parts.add(parts[idx])
  if len(gear_parts) == 2:
    gear_parts = list(map(lambda idx: inventory[idx], gear_parts))
    total += gear_parts[0] * gear_parts[1]

print(total)


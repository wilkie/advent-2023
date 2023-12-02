import re

tokens = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

total = 0
for line in open('input', 'r'):
  line = line.strip()
  # Lookahead matching '(?= <...> )' to capture pesky overlapping ones
  items = re.findall(r'(?=(\d|' + '|'.join(tokens) + '))', line)

  # Laziness :)
  first = items[0]
  if first in tokens:
    first = tokens.index(first) + 1

  last = items[-1]
  if last in tokens:
    last = tokens.index(last) + 1

  value = (int(first) * 10) + int(last)

  print(line, ':', value)
  total += value

print('--')
print(total)

import re, functools

f = open('input', 'r')
steps = f.readline().strip()

mapping = {}

for line in f:
  line = line.strip()
  if line == "": continue
  token, rest = map(lambda x: x.strip(), line.split('='))
  dirs = list(map(lambda x: x.strip().replace('(', '').replace(')', ''), rest.split(',')))
  mapping[token] = dirs

cur = 'AAA'
total = 0
while cur != 'ZZZ':
  for step in steps:
    cur = mapping[cur][0 if step == 'L' else 1]
    total += 1
    if cur == 'ZZZ':
      break

print(total)

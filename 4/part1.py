import re, functools

total = 0
for line in open('input', 'r'):
  # Get numbers
  winning, yours = list(map(
    lambda x: list(map(
      lambda y: int(y),
      x.replace('  ', ' ').split()
    )),
    line.split(':')[1].split('|')
  ))

  num = functools.reduce(lambda a, b: a + 1 if b in winning else a, yours, 0)

  score = pow(2, num - 1) if num > 0 else 0
  total += score

print(total)

import re, functools

total = 0
copies = {}
for line in open('input', 'r'):
  card_id = int(line.split(':')[0].split(' ')[-1])

  # Get numbers
  winning, yours = list(map(
    lambda x: list(map(
      lambda y: int(y),
      x.replace('  ', ' ').split()
    )),
    line.split(':')[1].split('|')
  ))

  num = functools.reduce(lambda a, b: a + 1 if b in winning else a, yours, 0)

  # Determine if we have copies of subsequent cards, for each card of this kind that we have
  for c in range(0, copies.get(card_id, 0) + 1):
    for i in range(0, num):
      copies[card_id + i + 1] = copies.get(card_id + i + 1, 0)
      copies[card_id + i + 1] += 1
    total += 1

print(total)

import re, functools

values = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

# 13^5 = 371293
multiplier = 371293

hands = []
for line in open('input', 'r'):
  hand, bid = line.strip().split(' ')
  counts = list(map(lambda x: hand.count(x), values))
  max_count = max(counts)
  # High card
  score = 0
  # One pair
  if max_count == 2 and (counts.count(2) == 1): score = 371293 * 2
  # Two pair
  if max_count == 2 and (counts.count(2) == 2): score = 371293 * 3
  # Three of a kind
  if max_count == 3 and (2 not in counts): score = 371293 * 4
  # Full house
  if max_count == 3 and (2 in counts): score = 371293 * 5
  # Four of a kind
  if max_count == 4: score = 371293 * 6
  # Five of a kind
  if max_count == 5: score = 371293 * 7

  # Add card values
  for i, c in enumerate(hand):
    score += (12 - values.index(c)) * pow(13, (4 - i))

  hands.append((hand, score, int(bid),))

total = 0
for i, game in enumerate(sorted(hands, key=lambda x: x[1])):
  hand, score, bid = game
  rank = i + 1
  total += (rank * bid)

print(total)

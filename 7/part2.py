import re, functools

values = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

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
  if (max_count == 2 and (counts.count(2) == 1)) or counts[12] >= 1: score = multiplier * 2
  # Two pair
  if (max_count == 2 and (counts.count(2) == 2)) or (max_count == 2 and counts[12] >= 1) or (max_count == 1 and counts[12] >= 2): score = multiplier * 3
  # Three of a kind
  if max_count == 3 or (max_count == 2 and counts[12] >= 1) or (max_count == 1 and counts[12] >= 2): score = multiplier * 4
  # Full house (tricky)
  if (max_count == 3 and (2 in counts)) or (max_count == 2 and counts.count(2) == 2 and counts[12] == 1): score = multiplier * 5
  # Four of a kind
  if max_count == 4 or (max_count == 3 and counts[12] >= 1) or (max_count == 2 and counts.count(2) == 2 and counts[12] >= 2) or (counts[12] >= 3): score = multiplier * 6
  # Five of a kind
  if max_count == 5 or (max_count == 4 and counts[12] == 1) or (max_count == 3 and counts[12] == 2) or ((2 in counts) and counts[12] == 3) or (counts[12] == 4): score = multiplier * 7

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

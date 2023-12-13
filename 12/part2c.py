from functools import cache

# The recursion depth is only maximum the number of possible counts...
# so this probably works best in hindsight of seeing how badly
# divide and conquer did. Finally... recursion actually helps.

# The search space is very shallow... so I should have known that
# a depth-first search through it would be better.

# My poor raspberry pi though! Really suffered through my memory
# intensive dynamic programming attempts.

# So tricky to figure this out since memoizing the recursion makes it
# very difficult to debug. I don't think I could have done this without
# writing the iterative divide and conquer version to get my head around
# it. Thankful for the 'cache' memoization helper, though.

@cache
def search(span, start, counts):
  # Success case
  if len(counts) == 0 and '#' not in span[start:]:
    return 1

  # Failure cases
  if len(counts) == 0 and '#' in span[start:]:
    return 0
  if start + counts[0] > len(span):
    return 0

  # Try every place we can put the 'count'
  sub_total = 0
  for i in range(start, len(span) - counts[0] + 1):
    # Is it here?
    #print('looking', i, span[i:counts[0] + i], counts[0], counts)
    if not '.' in span[i:counts[0] + i] and (i + counts[0] == len(span) or span[i + counts[0]] != '#') and (i == 0 or span[i - 1] != '#'):
      # Yes.
      #print('found', i, span[i:counts[0] + i], counts[1:])
      sub_total += search(span, i + counts[0] + 1, counts[1:])

    if span[i] == '#':
      # Short-circuit
      break

  return sub_total

total = 0
for line in open('input', 'r'):
  parts, counts = map(lambda x: x.strip(), line.strip().split(' '))
  parts = '?'.join([parts] * 5)
  counts = tuple(map(int, counts.split(','))) * 5
  sub_total = search(parts, 0, counts)
  total += sub_total
print(total)

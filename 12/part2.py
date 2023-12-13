import re

# This gets the right answer... in a LONG time. :)
# This is a iterative pruning approach that looks at subsequently longer
# phrases. It truncates the parts it solves and then tries to solve
# the smaller sub-problem. It prunes any situation where it sees a
# pattern that cannot be possible.

# It's very bad, though, because a breath search through the space is
# very inefficient. A recursive approach that goes depth first to
# find the position of the next span is way better, but this dumb
# contest trains me to think iteratively.

total = 0
for line in open('small', 'r'):
  # Parse
  parts, counts = map(lambda x: x.strip(), line.strip().split(' '))

  # Expand as per the instructions
  parts += "?"
  parts *= 5
  parts = parts[0:-1]
  counts += ","
  counts *= 5
  counts = counts[0:-1]

  counts = list(map(int, counts.split(',')))
  print(parts, counts)

  # Explode the line
  line = list(parts.strip())

  def valid(span, counts, start=0, complete=False):
    matches = list(re.finditer("[#]+(?=[^#])" if not complete else "[#]+", span))
    if len(matches) != 0:
      last = matches[-1].span()[1] + 1
    else:
      last = 0

    cur_counts = list(map(lambda x: len(x[0]), matches))
    ret = (cur_counts == counts[start:start+len(cur_counts)] and (not complete or len(cur_counts) == (len(counts) - start)), span[last:], start + len(cur_counts),)
    #if ret[0]: print(span, start, 'returning', last, ret)
    return (cur_counts == counts[start:start+len(cur_counts)] and (not complete or len(cur_counts) == (len(counts) - start)), span[last:], start + len(cur_counts),)

  # Get a set of possible spans of characters and prune any that aren't
  # going to be correct.
  possible_spans = [(-1, '', 0, '',)]
  empties = []
  for i, item in enumerate(line):
    for j in range(len(possible_spans)):
      last_i, span, start, full = possible_spans[j]
      if span is None: continue
      if last_i != i - 1: continue
      if len(full) != i:
        print(j, span, start, full)
        assert(len(full) == i)
      if item == '?':
        new_span = span + '#'
        good, new_span, index = valid(new_span, counts, start=start)
        if good:
          possible_spans[j] = (i, new_span, index, full + '#',)
        new_span = span + '.'
        also_good, new_span, index = valid(new_span, counts, start=start)
        if also_good:
          if not good:
            possible_spans[j] = (i, new_span, index, full + '.',)
          else:
            # Append, since both are fine for iterating
            if len(empties) == 0:
              possible_spans.append((i, new_span, index, full + '.',))
            else:
              new_j = empties.pop()
              possible_spans[new_j] = (i, new_span, index, full + '.',)

        if not good and not also_good:
          # Rejecting both forms
          possible_spans[j] = (None, None, None, None,)
          empties.append(j)
      else:
        new_span = span + item
        good, new_span, index = valid(new_span, counts, start=start)
        if good:
          possible_spans[j] = (i, new_span, index, full + item,)
        else:
          possible_spans[j] = (None, None, None, None,)
          empties.append(j)
    print('*', end='', flush=True)
  print('')

  # The ones that remain might be correct (they are full spans at least)
  sub_total = 0
  for _, span, start, full in possible_spans:
    if span is None: continue
    #print('ok', span, start, counts, full)
    good, _, _ = valid(span, counts, start=start, complete=True)
    if good:
      sub_total += 1
  print(sub_total)
  total += sub_total

print(total)

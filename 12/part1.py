import re

total = 0
for line in open('input', 'r'):
  # Parse
  parts, counts = line.strip().split(' ')
  counts = list(map(int, counts.split(',')))

  # Explode the line
  line = list(parts.strip())

  def valid(span, counts, complete=False):
    cur_counts = list(map(len, re.findall("[#]+(?=[^#])" if not complete else "[#]+", span)))
    return cur_counts == counts[0:len(cur_counts)] and (not complete or len(cur_counts) == len(counts))

  # Get a set of possible spans of characters and prune any that aren't
  # going to be correct.
  possible_spans = ['']
  for item in line:
    spans = possible_spans
    possible_spans = []
    for span in spans:
      new_span = span
      if item == '?':
        new_span = span + '#'
        if valid(new_span, counts):
          possible_spans.append(new_span)
        new_span = span + '.'
        if valid(new_span, counts):
          possible_spans.append(new_span)
      else:
        new_span += item
        if valid(new_span, counts):
          possible_spans.append(new_span)

  # The ones that remain might be correct (they are full spans at least)
  sub_total = 0
  for span in possible_spans:
    if valid(span, counts, complete=True):
      sub_total += 1
  total += sub_total

print(total)

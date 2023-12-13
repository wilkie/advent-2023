import re

# Even a pruning solution is a bit too slow for my raspberry pi :(
# So, I need to divide and conquer.

# The idea is to essentially bin pack the biggest things and turn
# this into a problem is packing the split bins as we go.
# We can memoize the smaller bins... since we multiply the inputs
# by 5, we can expect a lot of overlapping work when we divide
# and conquer it.

total = 0
for i, line in enumerate(open('small', 'r')):
  print("Processing", i)
  # Parse
  parts, counts = map(lambda x: x.strip(), line.strip().split(' '))

  # Expand as per the instructions
  parts += "?"
  parts *= 5
  parts = parts[0:-1]

  counts = list(map(int, counts.split(',')))
  print(parts, counts)
  parts = list(parts)

  # Bin packing time
  # Pack the biggest items, and then go to pack the smaller ones

  # If there is a 5 count, we need to place those first.
  # Find all placements of the biggest things with at least enough space
  # for the sum of things around it. Return a set of subproblems.
  def split_bin(box, counts, times):
    # Get the biggest count
    biggest_bin = max(counts)

    # Get the position of the bin
    biggest_bin_pos = counts.index(biggest_bin)

    # Get the sum on the left-hand side
    left_sum = sum(counts[0:biggest_bin_pos])

    # Get the right-hand sum
    right_sum = sum(counts[biggest_bin_pos+1:])

    # Get all the other counts between the biggest spans
    diff_counts = counts[biggest_bin_pos+1:] + counts[0:biggest_bin_pos]

    # The amount of space we must have at least to the left of the first bin
    left_padding = left_sum + biggest_bin_pos

    # The amount we need to the right of the last bin
    right_padding = right_sum + len(counts) - biggest_bin_pos - 1

    # The amount of padding in-between
    middle_padding = left_padding + 1 + right_padding

    # We need this much space, at least
    #print(''.join(box), biggest_bin, biggest_bin_pos, left_sum, right_sum, left_padding, right_padding)

    # Remove left and right padding and add a '.' as a sentinel
    remaining = box[left_padding:len(box) - right_padding] + ['.']

    # We can try and find obvious pivot points for the biggest span
    second_biggest_bin = list(sorted(counts))[-2]
    known_pivots = []
    if second_biggest_bin != biggest_bin:
      check_bin = second_biggest_bin + 1

      # We need to find a span of # that is at least as large as the
      # check. These MUST be the pivot span.
      span = 0
      for i, item in enumerate(remaining):
        if item == '#':
          span += 1
        else:
          if span >= check_bin and i >= biggest_bin:
            diff = biggest_bin - span
            start = i - biggest_bin
            end = i - span + biggest_bin
            known_pivots.append((start, end,))
          span = 0

    # If we already know where to break down the span, we just look at those places
    if len(known_pivots) != times:
      # Worst case: there are no obvious pivot points... we will have to find all of them. :(
      known_pivots = [(0, len(remaining),)]

    print(known_pivots)

    # Start at the first known pivot and try to find the possible positions of the
    # biggest span
    attempts = [(known_pivots[0][0], known_pivots[0][1], 0, 0, (0,),)]
    num_attempts = 1
    empties = []

    result = []
    while num_attempts > 0:
      #print('looping')
      for j, (next_i, until_i, pivot, found, indices) in enumerate(attempts):
        # Try to place the entire span the given number of times and tally the possibilities
        if next_i is None: continue
        i = next_i
        #print('looking', j, i, until_i)
        while i < until_i:
          complete = True
          if i > 0 and remaining[i - 1] == '#':
            # This won't start on a boundary, so bail
            complete = False
          else:
            for k in range(biggest_bin):
              if remaining[i + k] == '.' or (i + k) >= until_i:
                complete = False
                break

          if complete and (i + biggest_bin == len(remaining) or remaining[i + biggest_bin] != '#'):
            # Found a good span
            if found + 1 == times:
              # This is a complete set!
              #print('!!!found!!!', l, i, remaining[i:i+biggest_bin+1], attempts[l])
              it = iter((*indices, i + left_padding,))
              it2 = iter((*indices, i + left_padding, len(box) + 1,))
              next(it2)
              result.append(zip(it, it2))
              i += 1
              continue

            if pivot + 1 >= len(known_pivots):
              # Just try moving at least the middle padding
              future_next_i = i + biggest_bin + middle_padding
              future_until_i = until_i
            else:
              future_next_i = known_pivots[pivot + 1][0]
              future_until_i = known_pivots[pivot + 1][1]

            # Duplicate such that we try to add a new span to this series
            if len(empties) == 0:
              l = len(attempts)
              attempts.append(None)
            else:
              l = empties.pop()
            attempts[l] = (future_next_i, future_until_i, pivot + 1, found + 1, (*indices, i + left_padding,))
            num_attempts += 1
            #print('found', j, 'saved at', l, 'at', i + left_padding, remaining[i:i+biggest_bin+1], attempts[l])
            i += 1
            continue

          # We need to make sure that the remaining space is big enough
          space_left = len(remaining) - i
          need = times - found
          space_needed = (need * biggest_bin) + ((need - 1) * middle_padding)

          # Bail if we can't fit the rest
          if space_left < space_needed:
            break

          i += 1

        # Remove this item from our considerations
        #print('removing', j)
        attempts[j] = (None, None, None, None, None,)
        num_attempts -= 1
        empties.append(j)

    def expand_set(index, span):
      start, end = span
      #print(index, start, end)
      if index == 0:
        sub_counts = counts[0:biggest_bin_pos]
        #print(start, end - 1, sub_counts,)
        return (start, end - 1, sub_counts,)
      else:
        start += biggest_bin + 1
        end -= 1
        sub_counts = diff_counts
        if index == 5:
          sub_counts = counts[biggest_bin_pos+1:]
          #print('x', start, end, sub_counts,)
          return (start, end, sub_counts,)
      #print('y', start, end, sub_counts,)
      return (start, end, sub_counts,)

    return map(
      lambda j: list(map(
        lambda k: expand_set(*k),
        enumerate(j)
      )),
      result
    )

  # Find the given sequences in the given span
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

  def satisfy(box, start, end, counts):
    # Get a set of possible spans of characters and prune any that aren't
    # going to be correct.
    possible_spans = [(start - 1, '', 0, '',)]
    empties = []
    for i in range(start, end):
      item = box[i]
      #print(i, item)
      for j in range(len(possible_spans)):
        last_i, span, start, full = possible_spans[j]
        if span is None: continue
        if last_i != i - 1: continue
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

    # The ones that remain might be correct (they are full spans at least)
    sub_total = 0
    for _, span, start, full in possible_spans:
      if span is None: continue
      #print('valid?', span, counts)
      good, _, _ = valid(span, counts, start=start, complete=True)
      if good:
        sub_total += 1
    return sub_total

  # Keep track of subproblems we have already solved
  memos = {}

  # To start, we want to divide the total span via the given
  # counts 5 times.
  problem_total = 0
  for subproblems in split_bin(parts, counts, 5):
    #print('subproblem set', subproblems)
    # We must satisfy all sub-problems
    sub_total = 1
    for i, (start, end, sub_counts,) in enumerate(subproblems):
      if len(sub_counts) == 0:
        #print('continuing')
        continue
      hash = ''.join(parts[start:end]) + '-' + str(sub_counts)
      if hash in memos:
        #print('seen it before', ''.join(parts[start:end]), sub_counts, memos[hash])
        sub_total *= memos[hash]
      else:
        #print(''.join(parts[start:end]), start, end, sub_counts)
        result = satisfy(parts, start, end, sub_counts)
        #print(':',  result)
        memos[hash] = result
        #print('subproblem', span, sub_counts, result)
        sub_total *= result
      if sub_total == 0:
        break
    #print('sub_total', sub_total)
    problem_total += sub_total
  total += problem_total
  print(problem_total)
print(total)

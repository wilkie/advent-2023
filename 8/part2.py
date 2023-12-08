from itertools import product
from functools import reduce

# Open input
f = open('input', 'r')

# Read steps
steps = f.readline().strip()

# Set up memoization table

# Memoization can store factors for each combination of 'maze position' and
# 'input position'... for the input set, this is 281 x 766 entries or 215246
# different things to track... and then maintain a set() here and try to detect
# repeats. Of course, we can rely on it ending up at a particular point and
# just 'skipping' ahead to that point via the memoization... So, just skip to the
# next 'output' and memoize where the output is... so the memoization would be a
# strict mapping of [maze pos][input pos] -> maze_pos, input pos, steps. So the
# memoization table size is thrice as large.

# We can kinda shorten this if we only considered 'stopping points' since those
# are the only landmarks that matter. So we could just keep a memoization index
# of all items that end in 'Z'... but indexing that is difficult unless we sort
# them to begin with.

# Keep track of maze directions
mapping = {}

# Create memoization table
memos = {}

# Parse input
for line in f:
  if line.strip() == "": continue
  token, rest = map(lambda x: x.strip(), line.strip().split('='))
  mapping[token] = list(map(lambda x: x.strip().replace('(', '').replace(')', ''), rest.split(',')))
  memos[token] = [0] * len(steps)

# Get starting points
currents = list(filter(lambda x: x.endswith('A'), mapping.keys()))

# For a given position and index in the steps, find the next 'end' point
def find_end(start, index, steps, mapping, memos):
  total = 0
  cur = start
  step_index = index
  step_count = len(steps)
  while True:
    step = steps[step_index]
    step_index = (step_index + 1) % step_count
    cur = mapping[cur][0 if step == 'L' else 1]
    total += 1

    if cur.endswith('Z'):
      # Is this memoized?
      if memos[cur][step_index] == 0:
        # No, we must recurse (unless we are cycling to ourselves)
        if cur != start and step_index == index:
          # Do not allow it to cycle
          memos[cur][step_index] = -1
          sub_offset, sub_memo = find_end(cur, step_index, steps, mapping, memos)
          memos[cur][step_index] = (sub_offset, sub_memo,)

      # Return the memo along with our steps
      memo = (cur, step_index, memos[cur][step_index],)
      return (total, memo)

# Ensures a cycle ends on something seen within the cycle (memos are potentially shortened)
def complete_cycle(seen, offset, cur, step_index, value):
  if value == -1 and (str(cur) + str(step_index)) not in seen:
    new_offset, cycle = memos[cur][step_index]
    seen[str(cur) + str(step_index)] = True
    return (offset, (cur, step_index, complete_cycle(seen, new_offset, *cycle),),)
  elif value != -1 and (str(cur) + str(step_index)) in seen:
    return (offset, (cur, step_index, -1,),)
  elif value != -1:
    new_offset, cycle = value
    seen[str(cur) + str(step_index)] = True
    return (offset, (cur, step_index, complete_cycle(seen, new_offset, *cycle),),)
  else:
    return (offset, (cur, step_index, value),)

# Returns the point where the cycle actually happens and the offset up until that point
def cycle_length(seen, total, offset, cur, step_index, value):
  if value == -1:
    sub_total = seen[str(cur) + str(step_index)]
    # We looped. Return.
    return (total + offset - sub_total, cur,)
  elif (str(cur) + str(step_index)) not in seen:
    # Keep track of how long it took to get to this item from the
    # beginning
    seen[str(cur) + str(step_index)] = total + offset

  # Keep going
  new_offset, cycle = value
  return cycle_length(seen, total + offset, new_offset, *cycle)

# There are finite possibilities... we will have a cycle (or we find an answer before a cycle)
# Find how long until each starting path hits a cycle
results = []
for start in currents:
  offset, cycle = find_end(start, 0, steps, mapping, memos)

  # Ensure that the cycle is actually complete
  offset, cycle = complete_cycle({}, offset, *cycle)

  # Get the length of the cycle
  length, loop_point = cycle_length({}, 0, offset, *cycle)

  # Append compact information about the possibly polynomials
  results.append((loop_point, length, (start, 0, (offset, cycle,),),))

# We have enough to compute the total space of values
# From our start, we go an 'offset' and then a cycle. That cycle can, itself, have an
# offset and a secondary cycle. But... is that necessary for the given input??? NO!!

# I AM SO MAD THAT THE GIVEN INPUT SEEMS TO JUST PING-PONG BETWEEN
# TWO VALUES... IT'S A CONCISE LOOP. WHAT THE HECK. THAT'S SO AGGREVATING.
# AAAAHHHHHH. SO THE STEPS FROM 'A' to 'Z' ARE ALSO THE STEPS FROM THAT GIVEN
# 'Z' TO THE SAME 'A'.

# IF YOU JUST LAZILY TOOK THE LCM OF THE MAX VALUES. YOU'D GET THE ANSWER?!
# THAT'S REAL SILLY!! I WILL SOLVE THIS GENERALLY TYVM.

# 'small3' contains an input that will not be solvable if you just assume the
# cycles are aligned on their phases (just do an LCM). That's a silly assumption,
# but what can you do. This implementation will solve the general case of looking
# for any phase.

# It will be every multiple of each offset and each cycle
# So for a offset/cycle chain of: (1, 'A', (4, 'Z1', (2, 'Z2', (4, 'Z1', -1))))
# it would go: 1, 5, 7, 11, 13, etc, as it pings back and forth between Z1 and Z2
# in the cycle.

# So now we explode our results into forms of polynomials of the form: offset + (length * k)
polynomial_set = []
for result in results:
  polynomials = []
  total = 0
  loop_point, length, result = result

  print('looking at', result[0], 'which loops at', loop_point, 'for a cycle of length', length)

  value = 0
  while value != -1:
    cur, step_index, value = result

    if value == -1:
      break

    offset, cycle = value
    total += offset

    # Add polynomial (unless it loops, then the case at the beginning of the cycle
    # already records that polynomial)
    if cycle[2] != -1:
      print('found polynomial:', total, ' + ', length, 'k')
      polynomials.append((total, length,))
    result = cycle
  polynomial_set.append(polynomials)

# Try every permutation of polynomials to find one with the smallest
# lowest common multiple.

# This I got from stackoverflow from some smart math people to combine
# a pair of phased polynomials (vectors, really)
# https://math.stackexchange.com/questions/2218763/how-to-find-lcm-of-two-numbers-when-one-starts-with-an-offset
def combine_phased_rotations(a_period, a_phase, b_period, b_phase):
  """Combine two phased rotations into a single phased rotation

  Returns: combined_period, combined_phase

  The combined rotation is at its reference point if and only if both a and b
  are at their reference points.
  """
  gcd, s, t = extended_gcd(a_period, b_period)
  phase_difference = a_phase - b_phase
  pd_mult, pd_remainder = divmod(phase_difference, gcd)
  if pd_remainder:
    #raise ValueError("Rotation reference points never synchronize.")
    return (9999999999999999999, 9999999999999999999999,)

  combined_period = a_period // gcd * b_period
  combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
  return combined_period, combined_phase

def extended_gcd(a, b):
  """Extended Greatest Common Divisor Algorithm

  Returns:
    gcd: The greatest common divisor of a and b.
    s, t: Coefficients such that s*a + t*b = gcd

  Reference:
    https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
  """
  old_r, r = a, b
  old_s, s = 1, 0
  old_t, t = 0, 1
  while r:
    quotient, remainder = divmod(old_r, r)
    old_r, r = r, remainder
    old_s, s = s, old_s - quotient * s
    old_t, t = t, old_t - quotient * t

  return old_r, old_s, old_t

answer = min(
  map(
    lambda pairs: sum(reduce(
      lambda a, b: list(
        reversed(
          combine_phased_rotations(a[1], a[0], b[1], b[0])
        )
      ),
      pairs
    )),
    product(*polynomial_set)
  )
)

print(answer)

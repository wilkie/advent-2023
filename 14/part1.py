# It was very fun to make this happen iteratively in O(1) space.
# I have to make my own fun since I'm irreparably behind in points. :)

counts = None
for row_index, line in enumerate(map(lambda x: x.strip(), open('input', 'r'))):
  if counts is None:
    counts = list(map(lambda x: [
      0, # The total number of rounded rocks already settled
      0, # The number of rounded rocks since the last cubed rock
     -1, # The row_index of the last cubed rock
      0, # The current subtotal
    ], range(len(line))))

  # Regardless, we add to the subtotal the number of settled rocks each line
  for info in counts:
    info[3] += info[0]

  for i, item in enumerate(line):
    if item == '#':
      # Calculate sub-total for the column
      max_weight = row_index - counts[i][2]
      min_weight = max_weight - counts[i][1] + 1
      counts[i][3] += counts[i][1] * (max_weight + min_weight) // 2
      counts[i][0] += counts[i][1]

      # Reset
      counts[i][1] = 0
      counts[i][2] = row_index
    elif item == 'O':
      # Add another rounded rock
      counts[i][1] += 1

# Clean up
total = 0
for count in counts:
  max_weight = row_index - count[2]
  min_weight = max_weight - count[1] + 1
  count[3] += count[1] * (max_weight + min_weight) // 2
  total += count[3]

print(sum(map(lambda x: x[3], counts)))

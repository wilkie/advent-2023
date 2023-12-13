total = 0
with open('input', 'r') as f:
  while True:
    columns = []

    def find_mirrors(line):
      mirrors = []

      # Find all possible reflection points in each line
      for i in range(1, len(line)):
        length = min(i, len(line) - i)
        start = line[i - length:i]
        end = line[i:i + length][::-1]
        if start == end:
          mirrors.append(i)

      return mirrors

    def find_errors(line, mirrors, errors):
      for j, i in enumerate(mirrors):
        length = min(i, len(line) - i)
        start = line[i - length:i]
        end = line[i:i + length][::-1]
        if start != end: 
          if len(list(filter(lambda x: x[0] != x[1], zip(start, end)))) == 1:
            # Append error if the strings are one character off
            errors[j] += 1
          else:
            # Disqualify this
            errors[j] += 1000

    v_mirrors = []
    v_errors = []
    first_line = None
    for y, line in enumerate(f):
      line = line.strip()
      if line == "":
        break

      # Define the set of columns
      if len(columns) == 0:
        columns = [''] * len(line)

        # Find vertical mirrors on initial line
        v_mirrors = find_mirrors(line)
        first_line = line
      elif y == 1:
        # Extend mirror set with the next line
        v_mirrors = list(set(v_mirrors).union(set(find_mirrors(line))))

        # Define our error set
        v_errors = [0] * len(v_mirrors)

        # Now look for errors retroactively in the first line
        find_errors(first_line, v_mirrors, v_errors)
        find_errors(line, v_mirrors, v_errors)
      else:
        # See if we are one away from a mirror
        find_errors(line, v_mirrors, v_errors)

      # Augment columns
      for i in range(len(line)):
        columns[i] += line[i]

    # This means we have consumed the entire input
    if len(columns) == 0:
      break

    # Check vertical reflections
    h_mirrors = []
    h_errors = []

    for j in range(len(columns)):
      line = columns[j]

      if j == 0:
        # Find horizontal mirrors
        h_mirrors = find_mirrors(line)
        first_line = line
      elif j == 1:
        # Extend mirror set with the next line
        h_mirrors = list(set(h_mirrors).union(set(find_mirrors(line))))

        # Define our error set
        h_errors = [0] * len(h_mirrors)

        # Now look for errors retroactively in the first line
        find_errors(first_line, h_mirrors, h_errors)
        find_errors(line, h_mirrors, h_errors)
      else:
        # See if we are one away from a mirror
        find_errors(line, h_mirrors, h_errors)

    v_mirrors = list(map(lambda x: x[0], filter(lambda x: x[1] == 1, zip(v_mirrors, v_errors))))
    h_mirrors = list(map(lambda x: x[0], filter(lambda x: x[1] == 1, zip(h_mirrors, h_errors))))

    sub_total = 0
    if len(v_mirrors): sub_total += v_mirrors[0]
    if len(h_mirrors): sub_total += 100 * h_mirrors[0]
    total += sub_total

print(total)

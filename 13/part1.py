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

    def truncate_mirrors(line, mirrors):
      j = 0
      while j < len(mirrors):
        i = mirrors[j]
        j += 1
        length = min(i, len(line) - i)
        start = line[i - length:i]
        end = line[i:i + length][::-1]
        if start != end:
          mirrors.remove(i)
          j -= 1

    v_mirrors = []
    for y, line in enumerate(f):
      line = line.strip()
      if line == "":
        break

      # Define the set of columns
      if len(columns) == 0:
        columns = [''] * len(line)

        # Find vertical mirrors on initial line
        v_mirrors = find_mirrors(line)
      else:
        # See if mirrors hold on this line
        truncate_mirrors(line, v_mirrors)

      # Augment columns
      for i in range(len(line)):
        columns[i] += line[i]

    # This means we have consumed the entire input
    if len(columns) == 0:
      break

    # Check horizontal reflections
    h_mirrors = []
    for j in range(len(columns)):
      line = columns[j]

      if j == 0:
        h_mirrors = find_mirrors(line)
      else:
        truncate_mirrors(line, h_mirrors)

    sub_total = 0
    if len(v_mirrors): sub_total += v_mirrors[0]
    if len(h_mirrors): sub_total += 100 * h_mirrors[0]
    total += sub_total

print(total)

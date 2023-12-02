import re

total = 0
for line in open('input', 'r'):
  line = line.strip()
  items = re.findall(r'\d', line)

  value = (int(items[0]) * 10) + int(items[-1])

  print(line, ':', value)
  total += value

print('--')
print(total)

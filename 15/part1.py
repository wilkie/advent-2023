total = 0
sub_total = 0
with open('input', 'r') as f:
  while (byte := f.read(1)):
    if byte == '\n' or byte == '\r':
      continue

    if byte == ',':
      total += sub_total
      sub_total = 0
    else:
      sub_total += bytes(byte, 'utf-8')[0]
      sub_total *= 17
      sub_total = sub_total % 256

total += sub_total
print(total)

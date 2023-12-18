boxes = list(map(lambda _: [], range(256)))
hashmap = {}

total = 0
box = 0
label = ''
lens = 0
op = None
with open('input', 'r') as f:
  byte = None
  while byte != '':
    byte = f.read(1)

    if byte == '\n' or byte == '\r':
      continue

    if byte == ',' or byte == '':
      if op == '-':
        if label in hashmap:
          boxes[box].remove(label)
          del hashmap[label]
      else:
        if label not in boxes[box]:
          boxes[box].append(label)
        hashmap[label] = lens
      box = 0
      lens = 0
      label = ''
    elif byte == '=' or byte == '-':
      op = byte
    elif byte >= '0' and byte <= '9':
      lens *= 10
      lens += bytes(byte, 'utf-8')[0] - 48
    else:
      label += byte
      box += bytes(byte, 'utf-8')[0]
      box *= 17
      box = box % 256

for box_index, box in enumerate(boxes):
  for slot_index, label in enumerate(box):
    lens = hashmap[label]
    power = (box_index + 1) * (slot_index + 1) * lens
    total += power

print(total)

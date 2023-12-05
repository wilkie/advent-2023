import re, functools

maps = {}

source = ''
destination = ''
source_map = None
destination_map = None

total = 0
for line in open('input', 'r'):
  if line.startswith('seeds'):
    seeds = set(map(int, line.split(':')[1].strip().split(' ')))
    maps['seed'] = {'values': seeds, 'converted': seeds}
  elif ':' in line:
    if source_map is not None and destination_map is not None:
      for source_value in source_map['values']:
        if source_value not in destination_map['converted']:
          destination_map['values'].add(source_value)
          destination_map['converted'].add(source_value)

    source, destination = line.split(' ')[0].split('-to-')
    source_map = maps[source]
    maps[destination] = maps.get(destination, {'values': set(), 'converted': set()})
    destination_map = maps[destination]
  elif line.strip() != "":
    dest_start, source_start, length = map(int, line.strip().split(' '))
    for source_value in source_map['values']:
      if source_value in range(source_start, source_start + length):
        destination_map['values'].add(dest_start + (source_value - source_start))
        destination_map['converted'].add(source_value)

if source_map is not None and destination_map is not None:
  for source_value in source_map['values']:
    if source_value not in destination_map['converted']:
      destination_map['values'].add(source_value)
      destination_map['converted'].add(source_value)

print(min(maps['location']['values']))

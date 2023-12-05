import re, functools, os

maps = {}

source = ''
destination = ''
source_map = None
destination_map = None

total = 0
for line in open('input', 'r'):
  # Initial seed ranges
  if line.startswith('seeds'):
    # Split up line by spaces
    seed_map = map(int, line.split(':')[1].strip().split(' '))
    # Create ranges from every two items in the list
    seeds = set(map(lambda x: range(x[0], x[0] + x[1]), zip(seed_map, seed_map)))
    # Store seed range set into our dictionary
    maps['seed'] = {'ranges': seeds}
  elif ':' in line:
    # If we are switching from one type to another, append any unused ranges
    # from the source to the destination mappings
    if source_map is not None and destination_map is not None:
      for source_range in source_map['ranges']:
        destination_map['ranges'].add(source_range)

    # Get the types we are converting from and to
    source, destination = line.split(' ')[0].split('-to-')
    source_map = maps[source]

    # Create the initial range set
    maps[destination] = maps.get(destination, {'ranges': set()})
    destination_map = maps[destination]
  elif line.strip() != "":
    # Get the destination offset, source and length from this line
    dest_start, source_start, length = map(int, line.strip().split(' '))

    # Determine the range we are comparing against.
    # If this range contains any part of ranges in the source mapping, we
    # must split that source range and the append the intersection range
    # (offset by the difference between destination and source ranges)
    # to our destination mapping.
    compare_range = range(source_start, source_start + length)

    # Find source range that intersects with destination
    # Split source range, as required, to create destination ranges
    new_ranges = set()
    check_ranges = source_map['ranges']
    while len(check_ranges) > 0:
      new_check_ranges = set()
      for source_range in check_ranges:
        intersection = range(max(source_range.start, compare_range.start), min(source_range.stop, compare_range.stop))

        # If the intersection happens within the source range, then it is
        # a valid and interesting intersection
        if intersection.stop > 0 and intersection.stop > intersection.start:
          # Found a range that overlaps
          # Get new start / end range by splitting the source mapping range
          # that occurs before and after the intersection
          if source_range.start < intersection.start:
            new_check_ranges.add(range(source_range.start, intersection.start))
          if source_range.stop > intersection.stop:
            new_check_ranges.add(range(intersection.stop, source_range.stop))

          # Determine how far away the intersection is from the original start
          diff = intersection.start - source_start

          # The intersection is the intersection range slid over to the destination start
          # Determine the new position of the destination map
          new_start = dest_start + diff
          new_end = new_start + (intersection.stop - intersection.start)
          intersection = range(new_start, new_end)
          destination_map['ranges'].add(intersection)
        else:
          # This range matches nothing... don't recheck it, but append it to the
          # source again.
          new_ranges.add(source_range)
      check_ranges = new_check_ranges

    # Re-apply the ranges that didn't match anything to the source mapping
    source_map['ranges'] = new_ranges

# Finally, apply any final ranges that didn't have an intersection from
# source to destination.
if source_map is not None and destination_map is not None:
  for source_range in source_map['ranges']:
    destination_map['ranges'].add(source_range)

# Get smallest min value for the location ranges
print(min(map(lambda x: x.start, maps['location']['ranges'])))

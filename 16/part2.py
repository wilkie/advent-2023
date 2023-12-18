# This is simply doing a traversal without cycles

# It is a little slow and I probably could figure some way of pruning, but oh well

grid = list(
  map(
    lambda line: list(
      map(
        lambda cell: {'item': cell, 'visited': False, 'from': [False, False, False, False]},
        list(line.strip())
      )
    ),
    open('input', 'r')
  )
)

LEFT=0
RIGHT=1
UP=2
DOWN=3

DELTA = (
  (-1,  0,),
  (+1,  0,),
  ( 0, -1,),
  ( 0, +1,),
)

MIRRORS = {
  '/': (DOWN, UP, RIGHT, LEFT,),
  '\\': (UP, DOWN, LEFT, RIGHT,),
}

def traverse(grid, width, height, x, y, direction):
  # Mark as visited
  grid[y][x]['visited'] = True

  # Do not repeat cycles
  if grid[y][x]['from'][direction]:
    return ()
  grid[y][x]['from'][direction] = True

  # Assume we keep going
  next = (direction,)
  if grid[y][x]['item'] == '|':
    if direction == LEFT or direction == RIGHT:
      # Split
      next = (UP, DOWN,)
  elif grid[y][x]['item'] == '-':
    if direction == UP or direction == DOWN:
      # Split
      next = (LEFT, RIGHT,)
  elif grid[y][x]['item'] == '/' or grid[y][x]['item'] == '\\':
    next = (MIRRORS[grid[y][x]['item']][direction],)

  # Determine next cells to traverse to
  ret = []
  for next_direction in next:
    new_x = x + DELTA[next_direction][0]
    new_y = y + DELTA[next_direction][1]

    if new_x < width and new_x >= 0 and new_y < height and new_y >= 0:
      ret.append((new_x, new_y, next_direction,))

  return ret

# Get dimensions of cave
width = len(grid[0])
height = len(grid)

# Gather the possible starting points
starts = []
for x in range(width):
  starts.append((x, 0, DOWN,))
  starts.append((x, height - 1, UP,))
for y in range(height):
  starts.append((0, y, RIGHT,))
  starts.append((width - 1, y, LEFT,))

results = []
# Traverse
for start in starts:
  result = [start]
  while len(result) > 0:
    next_steps = []
    for next in result:
      next_steps.extend(traverse(grid, width, height, *next))
    result = next_steps

  # Count visited
  total = 0
  for row in grid:
    for cell in row:
      if cell['visited']:
        total += 1
      # Also reset
      cell['visited'] = False
      cell['from'] = [False, False, False, False]
  results.append((*start, total))

print(max(results, key=(lambda result: result[3]))[3])

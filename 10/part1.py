import math

turns = {
  #  :  L  R  U  D
  '.': [0, 0, 0, 0],
  '|': [0, 0, 1, 1],
  '-': [1, 1, 0, 0],
  'F': [0, 1, 0, 1],
  'L': [0, 1, 1, 0],
  '7': [1, 0, 0, 1],
  'J': [1, 0, 1, 0],
}
deltas = [
  (-1, 0), # L
  (+1, 0), # R
  (0, -1), # U
  (0, +1), # D
]
maze = []
visited = []

# Read maze and find the starting coordinate
start = None
for y, line in enumerate(open('input', 'r')):
  maze.append(list(line.strip()))
  visited.append(list(line.strip()))
  
  if 'S' in line:
    start = (line.index('S'), y,)
    dirs = [0, 0, 0, 0]

width = len(maze[0])
height = len(maze)

# Patch starting point
dirs = [0, 0, 0, 0]
if start[0] > 0 and turns[maze[start[1]][start[0] - 1]][1]: dirs[0] = 1
if start[0] < (width - 1) and turns[maze[start[1]][start[0] + 1]][0]: dirs[1] = 1
if start[1] > 0 and turns[maze[start[1] - 1][start[0]]][3]: dirs[2] = 1
if start[1] < (height - 1) and turns[maze[start[1] + 1][start[0]]][2]: dirs[3] = 1

# Get the pipe under the animal
token = list(filter(lambda x: y if x[1] == dirs else None, turns.items()))[0][0]
maze[start[1]][start[0]] = token

# Traverse
def go(x, y, from_x=None, from_y=None, length=0):
  cur = maze[y][x]

  # Mark as visited
  if cur != '.':
    visited[y][x] = 'X'

  next_steps = []
  for i, (delta, flowing) in enumerate(zip(deltas, turns[cur])):
    new_x = x + delta[0]
    new_y = y + delta[1]
    if new_x == from_x and new_y == from_y:
      # Do not go backward
      continue

    if not flowing or new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
      # Dead-end ... did not loop
      continue

    # Can we go into this pipe?
    new_token = maze[new_y][new_x]
    counter_turn = i + 1 if i % 2 == 0 else i - 1
    if not turns[new_token][counter_turn]:
      # Nope, we flow into this pipe
      continue

    if visited[new_y][new_x] == 'X':
      # Found a cycle
      return length

    # Traverse
    next_steps.append((new_x, new_y, x, y, length + 1,))

  return next_steps

steps = [start]

total = 0
while any(steps):
  result = go(*steps.pop())
  if isinstance(result, int):
    total = math.ceil(result / 2)
    break

  steps.extend(result)

print(total)

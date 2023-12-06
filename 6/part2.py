import re, functools

f = open('input', 'r')
time = int(''.join(re.findall(r'\d+', f.readline().split(':')[1])))
distance = int(''.join(re.findall(r'\d+', f.readline().split(':')[1])))

start = 0
end = 0

# Find initial starting point
n = 1
step = time // 10

while step > 0:
  while n * (time - n) < distance:
    n += step

  n -= step
  step -= 1
start = n + 1

# Find last data point
n = time - 1
step = time // 10

while step > 0:
  while n * (time - n) < distance:
    n -= step

  n += step
  step -= 1
end = n - 1

# Compute difference
print(end - start + 1)

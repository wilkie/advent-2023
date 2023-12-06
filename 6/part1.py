import re, functools

f = open('input', 'r')
times = map(int, re.findall(r'\d+', f.readline().split(':')[1]))
distances = map(int, re.findall(r'\d+', f.readline().split(':')[1]))

product = 1
for time, distance in zip(times, distances):
  total = 0
  for n in range(0, time):
    if n * (time - n) > distance:
      total += 1

  product *= total

print(product)

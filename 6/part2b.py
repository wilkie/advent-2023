import re, math

f = open('input', 'r')
time = int(''.join(re.findall(r'\d+', f.readline().split(':')[1])))
distance = int(''.join(re.findall(r'\d+', f.readline().split(':')[1])))

# Use quadratic formula instead of searching for range
start, end = sorted([(-time - math.sqrt((time * time) - (4 * distance))) // -2, (-time + math.sqrt((time * time) - (4 * distance))) // -2])

print(int(end - start))

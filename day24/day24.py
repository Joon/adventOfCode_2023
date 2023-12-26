import itertools


lines = [line.strip() for line in open('inputs/day24.txt', 'r').readlines()]

hailstones = []
for l in lines:
    parts = l.split(' @ ')
    position = tuple([int(p.strip()) for p in parts[0].split(',')])
    velocity = tuple([int(p.strip()) for p in parts[1].split(',')])
    hailstones.append((position, velocity))

#print(hailstones)

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def get_line(position, velocity):
    return ((position[0], position[1]), (position[0] + velocity[0], position[1] + velocity[1]))

test_area = (200000000000000, 400000000000000)

compare_hailstones = set()
for (a, b) in itertools.permutations(hailstones, 2):
    if (b, a) in compare_hailstones:
        continue
    compare_hailstones.add((a, b)) 

answer = 0
for (a, b) in compare_hailstones:
    
    intersection = line_intersection(get_line(a[0], a[1]), get_line(b[0], b[1]))
    if intersection:
        # The lines intersects at a point. Is that in the past or future?
        # If it's in the past, it's not interesting.
        if a[1][0] > 0 and intersection[0] < a[0][0]:
            continue
        if a[1][0] < 0 and intersection[0] > a[0][0]:
            continue
        if a[1][1] > 0 and intersection[1] < a[0][1]:
            continue
        if a[1][1] < 0 and intersection[1] > a[0][1]:
            continue

        if b[1][0] > 0 and intersection[0] < b[0][0]:
            continue
        if b[1][0] < 0 and intersection[0] > b[0][0]:
            continue
        if b[1][1] > 0 and intersection[1] < b[0][1]:
            continue
        if b[1][1] < 0 and intersection[1] > b[0][1]:
            continue

        if intersection[0] >= test_area[0] and intersection[0] <= test_area[1] and intersection[1] >= test_area[0] and intersection[1] <= test_area[1]:
            print(intersection)
            print(a[0], b[0])
            answer += 1
            print()

print("Part 1:", answer)
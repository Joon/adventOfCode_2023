lines = [l for l in open('Inputs/day18.txt', 'r').readlines()]


instructions = []
for l in lines:
    inst = l.strip().split(' ')
    dir = inst[0]
    length = int(inst[1])
    instructions.append((dir, length))

boundaries = [(0, 0)]
current_loc = (0, 0)
for inst in instructions:
    for i in range(inst[1]):
        if inst[0] == 'R':
            current_loc = (current_loc[0] + 1, current_loc[1])
        if inst[0] == 'L':
            current_loc = (current_loc[0] - 1, current_loc[1])
        if inst[0] == 'U':
            current_loc = (current_loc[0], current_loc[1] - 1)
        if inst[0] == 'D':
            current_loc = (current_loc[0], current_loc[1] + 1)
        boundaries.append(current_loc)

import re
from shapely.geometry import Polygon, Point
pgon = Polygon(reversed(boundaries))
# Adding the length divided by 2 is the same as widening the whole polygon by half a unit outwards (to account for the width of the trench)
print("Part 1", pgon.area + pgon.length / 2 + 1)

capture_hex = r'\(\#([a-z,0-9]*)\)'
instructions = []
for l in lines:
    hex_val = re.search(capture_hex, l).group(1)
    match hex_val[-1]:
        case '0':
            dir = 'R'
        case '1':
            dir = 'D'
        case '2':
            dir = 'L'
        case '3':
            dir = 'U'
    length = int(hex_val[:-1], 16)
    instructions.append((dir, length))


boundaries = [(0, 0)]
current_loc = (0, 0)
for inst in instructions:
    if inst[0] == 'R':
        current_loc = (current_loc[0] + inst[1], current_loc[1])
    if inst[0] == 'L':
        current_loc = (current_loc[0] - inst[1], current_loc[1])
    if inst[0] == 'U':
        current_loc = (current_loc[0], current_loc[1] - inst[1])
    if inst[0] == 'D':
        current_loc = (current_loc[0], current_loc[1] + inst[1])
    boundaries.append(current_loc)

import re
from shapely.geometry import Polygon, Point
pgon = Polygon(reversed(boundaries))
# Adding the length divided by 2 is the same as widening the whole polygon by half a unit outwards (to account for the width of the trench)
print("Part 2", pgon.area + pgon.length / 2 + 1)
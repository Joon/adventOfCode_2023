from termcolor import colored

lines = [[c for c in l.strip()] for l in open("Inputs/day10.txt", "r").readlines()]

starting_point = None

for y in range(len(lines)):
    for x in range(len(lines[y])):
        if lines[y][x] == "S":
            starting_point = (x, y)
            break
    if starting_point:
        break

print(starting_point)

def get_val(lines, point):
    if point[1] < 0 or point[1] >= len(lines):
        return None
    if point[0] < 0 or point[0] >= len(lines[point[1]]):
        return None
    return lines[point[1]][point[0]]

def available_directions(point, lines):
    available_directions = []
    #The pipes are arranged in a two-dimensional grid of tiles:
    # | is a vertical pipe connecting north and south.
    # - is a horizontal pipe connecting east and west.
    # L is a 90-degree bend connecting north and east.
    # J is a 90-degree bend connecting north and west.
    # 7 is a 90-degree bend connecting south and west.
    # F is a 90-degree bend connecting south and east.
    # . is ground; there is no pipe in this tile.
    # S is the starting position of the animal; there is a pipe 
    #   on this tile, but your sketch doesn't show what shape 
    #   the pipe has.   
    char = lines[point[1]][point[0]]
    match char:
        case '|':
            available_directions = ["N", "S"]
        case '-':
            available_directions = ["E", "W"]
        case 'L':
            available_directions = ["N", "E"]
        case 'J':
            available_directions = ["N", "W"]
        case '7':
            available_directions = ["S", "W"]
        case 'F':
            available_directions = ["S", "E"]
        case '.':
            available_directions = []
        case 'S':
            if get_val(lines, (point[0], point[1] - 1)) in ['|', '7', 'F']:
                available_directions.append("N")
            if get_val(lines, (point[0], point[1] + 1)) in ['|', 'L', 'J']:
                available_directions.append("S")
            if get_val(lines, (point[0] - 1, point[1])) in ['-', 'F', 'L']:
                available_directions.append("W")
            if get_val(lines, (point[0] + 1, point[1])) in ['-', 'J', '7']:
                available_directions.append("E")
    return available_directions

def in_bounds(x, y, lines):
    if y < 0 or y >= len(lines):
        return False
    if x < 0 or x >= len(lines[y]):
        return False
    return True

#             N
#         W       E
#             S
# Navigates the loop clockwise
def navigate(current_point, lines, previous_point):
    possible_directions = available_directions(current_point, lines)
    direction = None
    if len(possible_directions) == 1:
        direction = possible_directions[0]
    else:
        if 'E' in possible_directions and in_bounds(current_point[0] + 1, current_point[1], lines) and previous_point != (current_point[0] + 1, current_point[1]):
            direction = 'E'
        elif 'S' in possible_directions and in_bounds(current_point[0], current_point[1] + 1, lines) and previous_point != (current_point[0], current_point[1] + 1):
            direction = 'S'
        elif 'W' in possible_directions and in_bounds(current_point[0] - 1, current_point[1], lines) and previous_point != (current_point[0] - 1, current_point[1]):
            direction = 'W'
        elif 'N' in possible_directions and in_bounds(current_point[0], current_point[1] - 1, lines) and previous_point != (current_point[0], current_point[1] - 1):
            direction = 'N'
    if not direction:
        raise Exception("No direction available")
    
    match direction:
        case 'N':
            return (current_point[0], current_point[1] - 1)
        case 'S':
            return (current_point[0], current_point[1] + 1)
        case 'E':
            return (current_point[0] + 1, current_point[1])
        case 'W':
            return (current_point[0] - 1, current_point[1])
        case _:
            raise Exception("Invalid direction")

def print_path(lines, steps):
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if (x, y) in steps:
                print("O", end="")
            else:
                print(lines[y][x], end="")
        print()

steps = [starting_point]
previous_point = starting_point
current_point = navigate(starting_point, lines, previous_point)

while current_point != starting_point:
    steps.append(current_point)
    current_point = navigate(current_point, lines, steps[-2])

# print_path(lines, steps)

# The furthest point from the starting point (as navigated in this path) is halfway
print("Part 1:", len(steps) / 2) 

# Scanning solution to part 2: Move in from the outside, line by line
# Every time we encouter a vertical edge of the loop, the in_loop bit flips
# Every non-loop tile gets counted or not, based on the loop bit
area_count = 0
for y in range(len(lines)):
    in_loop = False
    on_edge = False
    for x in range(len(lines[y])):        
        if (x, y) in steps:
            # We cross the loop if we hit F, 7 or | 
            if not lines[y][x] in ['-', 'J', 'L']:
                in_loop = not in_loop
        if (x, y) in steps:
            print(colored(lines[y][x], "blue"), end="")
        elif in_loop:
            print(colored(lines[y][x], "green"), end="")
            area_count += 1
        else:
            print(colored(lines[y][x], "white"), end="")
    print()

print("Part 2:", area_count)
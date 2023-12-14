world = [[c for c in l.strip()] for l in open("Inputs/day14.txt", "r").readlines()]

def print_world(world):
    for row in world:
        print("".join(row))

def slide_rocks(world, y_direction, x_direction):
    to_slide = True
    while to_slide:
        to_slide = False
        for row in range(0, len(world)):
            for col in range(len(world[0])):
                if row - y_direction < 0 or row - y_direction >= len(world) or col - x_direction < 0 or col - x_direction >= len(world[0]):
                    continue
                
                if world[row][col] == 'O' and world[row - y_direction][col - x_direction] == '.':
                    world[row][col] = '.'
                    world[row - y_direction][col - x_direction] = 'O'
                    to_slide = True

def calc_load(world):
    load = 0
    for row in range(len(world)):
        for col in range(len(world[0])):
            if world[row][col] == 'O':
                load += len(world) - row
    return load    

slide_rocks(world, 1, 0)
print()
print("Part 1:", calc_load(world))

#   n
# w   e
#   s

movements = [(1, 0), (0, 1), (-1, 0), (0, -1)]
world = [[c for c in l.strip()] for l in open("Inputs/day14.txt", "r").readlines()]

train_data = []
for i in range(500):
    for move in movements:
        slide_rocks(world, move[0], move[1])
    train_data.append([i, calc_load(world)])

for t in train_data:
    print(t)

# TODO: Change these based on the printed output
pattern_start = 465 # Place where you see the start of the repeating pattern
pattern_length = 34 # How many numbers before the pattern repeats

pattern_spot_at = (1000000000 - pattern_start) % pattern_length
print("Part 2", train_data[pattern_start + pattern_spot_at][1])
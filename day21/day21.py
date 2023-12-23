world = [[c for c in l.strip()] for l in open('Inputs/day21.txt', 'r').readlines()]

start_point = [[x, y] for y in range(len(world)) for x in range(len(world[y])) if world[y][x] == 'S'][0]

def print_world(world, blocks):
    for y in range(len(world)):
        for x in range(len(world[y])):
            if (x, y) in blocks:
                print('O', end='')
            else:
                print(world[y][x], end='')
        print()
    print()
    print()

def find_blocks(start_point, ignore_blocks, world, step_depth, required_depth):
    if step_depth == required_depth:
        return ignore_blocks
    possible_blocks = []
    for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_point = (start_point[0] + move[0], start_point[1] + move[1])
        if new_point not in ignore_blocks and world[new_point[1]][new_point[0]] != '#':
            possible_blocks.append(new_point)
    result = []
    for p in possible_blocks:
        if world[p[1]][p[0]] == '.':
            result.extend(find_blocks(p, possible_blocks, world, step_depth + 1, required_depth))
    #print_world(world, result)
    return result

def find_blocks_stack(start_point, world, required_depth):
    stack = [(0, [start_point])]
    while stack:
        depth, reachable_blocks = stack.pop()
        if depth == required_depth:
            return reachable_blocks
        possible_blocks = set()
        for block in reachable_blocks:
            for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_point = (block[0] + move[0], block[1] + move[1])
                if world[new_point[1] % len(world)][new_point[0] % len(world[0])] != '#':
                    possible_blocks.add(new_point)
        stack.append((depth + 1, possible_blocks))

blocks = find_blocks_stack(start_point, world, 64)
print_world(world, blocks)
print("Part 1:", len(blocks))

def quad(y, n):
    # Use the quadratic formula to find the output at the large steps based on the first three data points
    a = (y[2] - (2 * y[1]) + y[0]) // 2
    b = y[1] - y[0] - a
    c = y[0]
    return (a * n**2) + (b * n) + c

goal = 26501365
size = len(world[0])
edge = size // 2

y = [len(find_blocks_stack(start_point, world, (edge + i * size))) for i in range(3)]
#print_world(world, blocks)

print("Part 2:", quad(y, ((goal - edge) // size)))
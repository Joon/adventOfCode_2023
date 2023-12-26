world = [[c for c in l.strip()] for l in open('inputs/day23_test.txt', 'r').readlines()]

start_pos = world[0].index('.'), 0

target_pos = world[-1].index('.'), len(world) - 1

print(start_pos)

def walk_back_to_first_branch(world, target_pos, obey_slope):
    neighbours = [target_pos]
    candidate_start_of_end_path = target_pos
    visited = set()
    visited.add(target_pos)
    length = 1
    while True:
        neighbours = [n for n in neighbors(world,candidate_start_of_end_path, obey_slope) if n not in visited]
        if len(neighbours) > 1:
            return candidate_start_of_end_path, length - 1 
        candidate_start_of_end_path = neighbours[0]
        visited.add(candidate_start_of_end_path)
        length += 1
    

def all_paths(world, start_pos, target_pos, obey_slope = True):
    paths = []
    path_stack = [(start_pos, [])]

    while path_stack:
        pos, visited = path_stack.pop()
        if pos in visited:
            continue
        visited.append(pos)
        for n in neighbors(world, pos, obey_slope):
            if n == target_pos:
                paths.append(len(visited))
            else:
                path_stack.append((n, visited.copy()))

    return paths

def render_world_as_graph(world, start_pos, obey_slope):
    path_graph = {}
    path_stack = [(start_pos,(start_pos[0], start_pos[1] - 1), [])]
    processed_paths = set()
    while path_stack:
        pos, last_pos, nodes = path_stack.pop()
        # This path has already been walked, skip it
        if (pos, last_pos) in processed_paths:
            continue
        if pos in nodes:
            continue
        processed_paths.add((pos, last_pos))
        current_pos = pos
        at_branch = False
        walked = set([current_pos, last_pos])
        while not at_branch:            
            current_neighbours = neighbors(world, current_pos, obey_slope)
            possible_neighbours = set(current_neighbours) - walked
            if len(possible_neighbours) == 1:
                current_pos = possible_neighbours.pop()
                walked.add(current_pos)
            else:
                at_branch = True
        
        if len(current_neighbours) > 1:        
            
            if last_pos not in path_graph:
                path_graph[last_pos] = {}
            path_graph[last_pos][current_pos] = len(walked) - 1
            nodes = nodes.copy()
            nodes.append(last_pos)
            # We have neighbours at a junction, add them to the stack
            for n in current_neighbours:            
                if n not in walked:
                    path_stack.append((n, current_pos, nodes))
        else:
            # length is zero, we are at the end
            if pos not in path_graph:
                path_graph[pos] = {}
            path_graph[pos][current_pos] = len(walked) + 1
            if current_pos not in path_graph:
                path_graph[current_pos] = {}

    return path_graph


def all_paths_optimized(world, start_pos, target_pos):
    world_graph = render_world_as_graph(world, start_pos, False)
    paths = []
    path_stack = [((start_pos[0], start_pos[1] - 1), [], 0)]
    
    while path_stack:
        pos, visited, path_length = path_stack.pop()
        if pos in visited:
            continue
        visited.append(pos)
        if pos == target_pos:
            paths.append(path_length)
        else:
            for n in world_graph[pos].keys():
                path_stack.append((n, visited.copy(), path_length + world_graph[pos][n]))

    return paths

#      N
#   W     E
#      S
def neighbors(world, pos, obey_slope):
    x, y = pos
    neighbors = []
    direction_movements = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    for direction, movement in direction_movements.items():
        i, j = movement
        if 0 <= x + i < len(world[0]) and 0 <= y + j < len(world):
            if obey_slope:
                if world[y + j][x + i] == '.':
                    neighbors.append((x + i, y + j))
                else:
                    if (direction == 'N' and world[y + j][x + i] == '^') or (direction == 'S' and world[y + j][x + i] == 'v')  or (direction == 'E' and world[y + j][x + i] == '>') or (direction == 'W' and world[y + j][x + i] == '<'):
                        neighbors.append((x + i, y + j))
            else:
                if world[y + j][x + i] != '#':
                    neighbors.append((x + i, y + j))
    return neighbors

print("Part 1:", max([p for p in all_paths(world, start_pos, target_pos)]))

print("Part 2:", max([p for p in all_paths_optimized(world, start_pos, target_pos)]))

world_graph = render_world_as_graph(world, start_pos, True)
print(world_graph)
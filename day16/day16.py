world = [[c for c in l.strip()] for l in open('Inputs/day16.txt', 'r').readlines()]

def get_control_points(world):
    points = {}
    for y in range(len(world)):
        for x in range(len(world[y])):
            if world[y][x] != '.':
                points[(x, y)] = world[y][x]
    return points

def point_applies(y_movement, x_movement, point):
    if point == '/' or point == '\\':
        return True
    if point == '-':
        return x_movement == 0
    if point == '|':
        return y_movement == 0
    raise ValueError(f'Unkown instruction {point}')

def next_control_point(origin, y_direction, x_direction, control_points, max_x, max_y):
    point = origin
    while point[0] >= 0 and point[0] <= max_x and point[1] >= 0 and point[1] <= max_y:
        point = (point[0] + x_direction, point[1] + y_direction)
        if point in control_points and point_applies(y_direction, x_direction, control_points[point]):
            return (point, control_points[point])
    return None

def build_segments(start_point, world, control_points, prev_moves):
    if start_point in prev_moves:
        return []
    more_segments = True
    result = [start_point]
    current_point = start_point
    while more_segments:
        more_segments = False
        move_x = 0
        move_y = 0
        match current_point[2]:
            case '>':
                move_x = 1
            case '<':
                move_x = -1
            case 'v':
                move_y = 1
            case '^':
                move_y = -1
            case '_':
                raise ValueError('Unknown direction indicator')
        control_point = next_control_point(current_point, move_y, move_x, 
                                           control_points, len(world), len(world[0]))
        # We'e hit a control point - the beam is not just continuing off the world
        if control_point:
            new_direction = ''
            new_start_loc = control_point[0]
            match control_point[1]:
                case '/':
                    if move_y == -1:
                        new_direction = '>'
                    if move_y == 1:
                        new_direction = '<'
                    if move_x == 1:
                        new_direction = '^'
                    if move_x == -1:
                        new_direction = 'v'
                case '\\':
                    if move_y == 1:
                        new_direction = '>'
                    if move_y == -1:
                        new_direction = '<'
                    if move_x == 1:
                        new_direction = 'v'
                    if move_x == -1:
                        new_direction = '^'
                case '|':
                    if move_y != 0:
                        raise ValueError("Processing a vert splitter while moving on y axis")
                    rest = build_segments((new_start_loc[0], new_start_loc[1], '^'), world, 
                                          control_points, result + prev_moves)
                    if rest:
                        result.extend(rest)
                    new_direction = 'v'
                case '-':
                    if (move_x) != 0:
                        raise ValueError("Processing a horz splitter while moving on x axis")
                    rest = build_segments((new_start_loc[0], new_start_loc[1], '>'), world, 
                                          control_points, result + prev_moves)
                    if rest:
                        result.extend(rest)
                    new_direction = '<'
            current_point = (new_start_loc[0], new_start_loc[1], new_direction)
            if current_point in prev_moves or current_point in result:
                more_segments = False
            else:
                more_segments = True
                result.append(current_point)
    return result

match world[0][0]:
    case '\\':
        segment_start = (0, 0, 'v')
    case '|':
        segment_start = (0, 0, 'v')
    case '/':
        segment_start = (0, 0, '^')
    case _:
        segment_start = (0, 0, '>')
segments = build_segments(segment_start, world, get_control_points(world), [])

def get_energy_map(segments, world):
    energised_map = set([])

    for segment in segments:
        energised_map.add((segment[0], segment[1]))
        move_x = 0
        move_y = 0
        match segment[2]:
            case '>':
                move_x = 1
            case '<':
                move_x = -1
            case 'v':
                move_y = 1
            case '^':
                move_y = -1
            case '_':
                raise ValueError('Unknown direction indicator')
        current_point = (segment[0], segment[1])
        # Keep on moving until we hit a control point that applies
        while current_point[0] >= 0 and current_point[0] < len(world[0]) and current_point[1] >= 0 and current_point[1] < len(world):
            current_point = (current_point[0] + move_x, current_point[1] + move_y)

            # Hit a control point - get out
            if len([s for s in segments if s[0] == current_point[0] and s[1] == current_point[1]]) > 0:
                break
            if current_point[0] >= 0 and current_point[0] < len(world[0]) and current_point[1] >= 0 and current_point[1] < len(world):
                # Mark a non-control point as energised
                energised_map.add(current_point)
    return energised_map

#print(segments)
#for y in range(len(world)):
#    for x in range(len(world[0])):
#        if (x, y) in energised_map:
#            print('O', end='')
#        else:
#            print(world[y][x], end='')
#    print()

print("Part 1:", len(get_energy_map(segments, world)))

max_energy = 0
control_points = get_control_points(world)
# come in from top or bottom
for x in range(len(world[0])):
    try_segments = []
    # Moving down into the world
    match world[x][0]:
        case '\\':
            try_segments = [(x, 0, '>')]
        case '|':
            try_segments = [(x, 0, 'v')]
        case '/':
            try_segments = [(x, 0, '<')]
        case '-':
            try_segments = [(x, 0, '>'), (0, 0, '<')]
        case '.':
            try_segments = [(x, 0, 'v')]
    for start_point in try_segments:
        segments = build_segments(start_point, world, control_points, [])
        energised_map = get_energy_map(segments, world)
        if len(energised_map) > max_energy:
            max_energy = len(energised_map)

    # Moving up into the world
    world_end = len(world) - 1
    match world[x][world_end]:
        case '\\':
            try_segments = [(x, 0, '<')]
        case '|':
            try_segments = [(x, 0, '^')]
        case '/':
            try_segments = [(x, 0, '>')]
        case '-':
            try_segments = [(x, 0, '>'), (0, 0, '<')]
        case '.':
            try_segments = [(x, 0, '^')]
    for start_point in try_segments:
        segments = build_segments(start_point, world, control_points, [])
        energised_map = get_energy_map(segments, world)
        if len(energised_map) > max_energy:
            max_energy = len(energised_map)

# Comin from the sides
for y in range(len(world)):
    try_segments = []
    # Moving right into the world
    match world[0][y]:
        case '\\':
            try_segments = [(0, y, 'v')]
        case '|':
            try_segments = [(0, y, '^'), (0, y, 'v')]
        case '/':
            try_segments = [(0, y, '^')]
        case '-':
            try_segments = [(0, y, '>')]
        case '.':
            try_segments = [(0, y, '>')]
    for start_point in try_segments:
        segments = build_segments(start_point, world, control_points, [])
        energised_map = get_energy_map(segments, world)
        if len(energised_map) > max_energy:
            max_energy = len(energised_map)

    # Moving up into the world
    world_end = len(world[0]) - 1
    match world[world_end][y]:
        case '\\':
            try_segments = [(0, y, '^')]
        case '|':
            try_segments = [(0, y, '^'), (0, y, 'v')]
        case '/':
            try_segments = [(0, y, 'v')]
        case '-':
            try_segments = [(0, y, '<')]
        case '.':
            try_segments = [(0, y, '<')]
    for start_point in try_segments:
        segments = build_segments(start_point, world, control_points, [])
        energised_map = get_energy_map(segments, world)
        if len(energised_map) > max_energy:
            max_energy = len(energised_map)

print("Part 2:", max_energy)
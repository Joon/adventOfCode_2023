world = [[c for c in l.strip()] for l in open('Inputs/day16_test.txt', 'r').readlines()]

segment_start = (0, 0, '>')

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

def build_segments(start_point, world, control_points):
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
            more_segments = True
            new_direction = ''
            new_start_loc = control_point[0]
            match control_point[1]:
                case '/':
                    if move_y == 1:
                        new_direction = '>'
                    if move_y == -1:
                        new_direction = '<'
                    if move_x == 1:
                        new_direction = '^'
                    if move_x == -1:
                        new_direction = 'v'
                case '\\':
                    if move_y == 1:
                        new_direction = '<'
                    if move_y == -1:
                        new_direction = '>'
                    if move_x == 1:
                        new_direction = 'v'
                    if move_x == -1:
                        new_direction = '^'
                case '|':
                    if move_y != 0:
                        raise ValueError("Processing a vert splitter while moving on y axis")
                    result.extend(build_segments((new_start_loc[0], new_start_loc[1], '^'), world, control_points))
                    new_direction = 'v'
                case '-':
                    if (move_x) != 0:
                        raise ValueError("Processing a horz splitter while moving on x axis")
                    result.extend(build_segments((new_start_loc[0], new_start_loc[1], '>'), world, control_points))
                    new_direction = '<'
            current_point = (new_start_loc[0], new_start_loc[1], new_direction)
            result.append(current_point)

segments = build_segments(segment_start, world, get_control_points(world))
print(segments)
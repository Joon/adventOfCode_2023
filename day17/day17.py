from termcolor import colored

city = [[int(c) for c in l.strip()] for l in open('Inputs/day17_test.txt', 'r').readlines()]

#def find_route(current_position, direction, prev_moves):
#    if current_position in prev_moves:
#        return []
#    local_prev_moves = prev_moves.copy()
#    local_prev_moves.append(current_position)
#
#    # We've hit the destination
#    if current_position[0] == len(city[0]) - 1 and current_position[1] == len(city) - 1:
#        return local_prev_moves
#    
#    # can only go right, left or straight
#    if direction == '>':
#        possible_directions = ['v', '^', '>']
#    if direction == '^':
#        possible_directions = ['>', '<', '^']
#    if direction == '<':
#        possible_directions = ['v', '^', '<']
#    if direction == 'v':
#        possible_directions = ['<', '>', 'v']
#    direction_movement = {'>': (1, 0), '<': (-1, 0), 'v': (0, 1), '^': (0, -1)}
#    temp_routes = []
#    for direction in possible_directions:
#        movement = direction_movement[direction]
#        new_position = (current_position[0] + movement[0], current_position[1] + movement[1])
#        if new_position[0] < 0 or new_position[0] >= len(city[0]) or new_position[1] < 0 or new_position[1] >= len(city):
#            continue
#        if new_position in local_prev_moves:
#            continue
#        existing_line_length = 0
#        for point in reversed(local_prev_moves):
#            if point[0] !=- new_position[0] and point[1] != new_position[1]:
#                break
#            if point[0] == new_position[0] or point[1] == new_position[1]:
#                existing_line_length += 1
#        new_route_line_length = existing_line_length + 1
#        # Don't move more than 3 tiles in a straight line
#        if new_route_line_length > 3:
#            continue#
#
#        total_new_position_score = sum([city[p[1]][p[0]] for p in local_prev_moves + [new_position]])
#        if total_new_position_score >= global_map_heat_losses[new_position][direction]:
#            continue
#        global_map_heat_losses[new_position][direction] = total_new_position_score
#        temp_routes.append(find_route(new_position, direction, local_prev_moves))
#    lowest_route_heat_loss = 99999
#    lowest_route = []
#    for r in temp_routes:
#        if len(r) == 0:
#            continue
#        route_heat_loss = sum(city[p[1]][p[0]] for p in r)
#        if route_heat_loss < lowest_route_heat_loss:
#            lowest_route_heat_loss = route_heat_loss
#            lowest_route = r    
#    return lowest_route


# This method breaks the system recursion limit, and increasing it doesn't help - process just aborts
#right_move = sum(city[p[1]][p[0]] for p in find_route((0, 0), '>', []))
#down_move = sum(city[p[1]][p[0]] for p in find_route((0, 0), 'v', []))

def init_heat_loss():
    result = {}
    for y in range(len(city)):
        for x in range(len(city[y])):
            #for direction in ['>', '<', '^', 'v']:
            #    result[(x, y)][direction] = -1
            result[(x, y)] = -1
    return result        

class Solver:
    def __init__(self, start_location, move_history, direction, route_heat_loss) -> None:
        self.current_point = start_location
        self.move_history = move_history.copy()
        self.direction = direction
        self.route_heat_loss = route_heat_loss

    def possible_moves(self):
        # can only go right, left or straight
        if self.direction == '>':
            possible_directions = ['v', '^']
        if self.direction == '^':
            possible_directions = ['>', '<']
        if self.direction == '<':
            possible_directions = ['^', 'v']
        if self.direction == 'v':
            possible_directions = ['<', '>']
        direction_movement = {'>': (1, 0), '<': (-1, 0), 'v': (0, 1), '^': (0, -1)}
        possible_moves = []
        for direction in possible_directions:
            movement = direction_movement[direction]
            new_moves = []
            # Calculate all valid moves in one direction
            for length in range(1, 3):
                new_position = (self.current_point[0] + (movement[0] * length), self.current_point[1] + (movement[1] * length))
                if new_position[0] < 0 or new_position[0] >= len(city[0]) or new_position[1] < 0 or new_position[1] >= len(city):
                    continue
                if (new_position, direction) in self.move_history:
                    continue
                new_moves.append((new_position, direction))
                new_path = self.move_history + new_moves
                total_new_position_score = sum([city[p[0][1]][p[0][0]] for p in new_path])
                if total_new_position_score > self.route_heat_loss[new_position] and self.route_heat_loss[new_position] >= 0:
                    continue
                new_route_heat_loss = self.route_heat_loss.copy()
                new_route_heat_loss[new_position] = total_new_position_score
                possible_moves.append((new_position, direction, new_path, new_route_heat_loss))
        return possible_moves


heat_losses = init_heat_loss()
active_solvers = []
active_solvers.append(Solver((0, 0), [], '>', heat_losses.copy()))
heat_losses[(1, 0)] = city[0][0]
active_solvers.append(Solver((1, 0), [((0, 0), '>')], '>', heat_losses.copy()))
heat_losses[(2, 0)] = city[0][0] + city[0][1]
active_solvers.append(Solver((2, 0), [((0, 0), '>'), ((1, 0), '>')], '>', heat_losses.copy()))

heat_losses = init_heat_loss()
active_solvers.append(Solver((0, 0), [], 'v', heat_losses.copy()))
heat_losses[(0, 1)] = city[0][0]
active_solvers.append(Solver((0, 1), [((0, 0), 'v')], 'v', heat_losses.copy()))
heat_losses[(0, 2)] = city[0][0] + city[1][0]
active_solvers.append(Solver((0, 2), [((0, 0), 'v'), ((0, 1), 'v')], 'v', heat_losses.copy()))

lowest_route_heat_loss = 99999
while len(active_solvers) > 0:
    new_solvers = []
    for solver in active_solvers:
        possible_moves = solver.possible_moves()
        for move in possible_moves:
            if move[0][0] == len(city[0]) - 1 and move[0][1] == len(city) - 1:
                route_heat_loss = sum(city[p[0][1]][p[0][0]] for p in move[2])
                if route_heat_loss < lowest_route_heat_loss:
                    lowest_route_heat_loss = route_heat_loss
                    print("New lowest route heat loss:", lowest_route_heat_loss)
            else:
                new_route_heat_loss = move[3].copy()
                new_move_history = move[2].copy()
                new_solvers.append(Solver(move[0], new_move_history, move[1], new_route_heat_loss))
    active_solvers = new_solvers.copy()

path_codes = ["2>>34^>>>1323","32v>>>35v5623","32552456v>>54","3446585845v52","4546657867v>6","14385987984v4","44578769877v6","36378779796v>","465496798688v","456467998645v","12246868655<v","25465488877v5","43226746555v>"]
golden_path = [[(x, y) for x in range(len(city[0])) if path_codes[y][x] in ['>', 'v', '<', '^']] for y in range(len(city))]
print(golden_path)

for line in range(len(city)):
    for block in range(len(city[line])):
        current_color = 'white'
        if (block, line) in golden_path[line]:
            current_color = 'green'
        print(colored('[{} >{:3d}<{:3d}^{:3d}v{:3d}]'.format(city[line][block], global_map_heat_losses[(block, line)]['>'],
                                                             global_map_heat_losses[(block, line)]['<'],
                                                             global_map_heat_losses[(block, line)]['^'],
                                                             global_map_heat_losses[(block, line)]['v']), current_color), end='')
    print()


print("Part 1:", global_map_heat_losses[(len(city[0]) - 1, len(city) - 1)].values())

# TODO: Replace global map with local map per solver
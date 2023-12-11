import itertools

lines = [[c for c in l.strip()] for l in open("Inputs/day11_test.txt", "r").readlines() if l.strip() != ""]


expand_lines = [y for y in range(len(lines)) if not '#' in lines[y]]
for l in reversed(expand_lines):
    for i in range(len(lines[0])):
        lines[l][i] = 'V'
expand_lines = [y for y in range(len(lines)) if not '#' in lines[y]]

expand_columns = [x for x in range(len(lines[0])) if not '#' in [lines[y][x] for y in range(len(lines))]]
for l in reversed(expand_columns):
    for i in range(len(lines)):
        if lines[i][l] == 'V':
            lines[i][l] = 'HV'
        else:
            lines[i][l] = 'H'
expand_columns = [x for x in range(len(lines[0])) if not '#' in [lines[y][x] for y in range(len(lines))]]
for l in lines:
    print(l)

galaxies = []
for i in range(len(lines)):
    l = lines[i]
    galaxies.extend([(x, i) for x in range(len(l)) if l[x] == '#'])

def navigate(from_p, to_p, lines, step_size): 
    navigate_count = 0
    navigate_point = from_p
    while navigate_point != to_p:
        # Horizontal navigation
        if navigate_point[0] < to_p[0]:
            navigate_point = (navigate_point[0] + 1, navigate_point[1])
            if 'H' in lines[navigate_point[1]][navigate_point[0]]:
                navigate_count += step_size
            else:
                navigate_count += 1
        if (navigate_point[0] > to_p[0]):
            navigate_point = (navigate_point[0] - 1, navigate_point[1])
            if 'H' in lines[navigate_point[1]][navigate_point[0]]:
                navigate_count += step_size
            else:
                navigate_count += 1
        # Vertival navigation
        if (navigate_point[1] < to_p[1]):
            navigate_point = (navigate_point[0], navigate_point[1] + 1)
            if 'V' in lines[navigate_point[1]][navigate_point[0]]:
                navigate_count += step_size
            else:
                navigate_count += 1
        if (navigate_point[1] > to_p[1]):
            navigate_point = (navigate_point[0], navigate_point[1] - 1)
            if 'V' in lines[navigate_point[1]][navigate_point[0]]:
                navigate_count += step_size
            else:
                navigate_count += 1
    return navigate_count

tot_distance = 0
for (a, b) in itertools.combinations(galaxies, 2):
    tot_distance += navigate(a, b, lines, 2)

print('Part 1:', tot_distance)

tot_distance = 0
for (a, b) in itertools.combinations(galaxies, 2):
    tot_distance += navigate(a, b, lines, 1000000)

print('Part 2:', tot_distance)

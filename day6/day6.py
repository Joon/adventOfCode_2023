file2 = open('../Inputs/day6.txt', 'r')
lines = [l.strip() for l in file2.readlines()]

def get_numbers(line):
    number_side = line.split(':')[1].strip()
    parts = [int(n.strip()) for n in number_side.split(' ') if n.strip() != '']
    return parts

times = get_numbers(lines[0])
distances = get_numbers(lines[1])

def win_count(time, distance):
    result = 0
    for i in range(1, time + 1):
        speed = i
        scenario_distance = speed * (time - i)
        if scenario_distance > distance:
            result = result + 1
    return result

part1 = 1
for i in range(0, len(times)):
    part1 = part1 * win_count(times[i], distances[i])

print("Part 1: " + str(part1))

long_race_time = "".join([str(t) for t in times])
long_race_distance = "".join([str(d) for d in distances])

print("Part 2", win_count(int(long_race_time), int(long_race_distance)))
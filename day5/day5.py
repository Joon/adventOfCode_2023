from itertools import pairwise

file2 = open('../Inputs/day5.txt', 'r')
lines = [l.strip() for l in file2.readlines()]

def parse_line(line):   
    #seed-to-soil map:
    #3078006360 2182201339 30483272
    # Each line within a map contains three numbers: the destination range start [0], 
    # the source range start [1], and the range length [2]
    parts = line.split(' ')
    # This result contains source range and destination range
    return (int(parts[1]), int(parts[1]) + int(parts[2]), int(parts[0]), int(parts[0]) + int(parts[2]))

current_set = None
seed_to_soil = []
soil_to_fertilizer = []
fertilizer_to_water = []
water_to_light = []
light_to_temperature = []
temperature_to_humidity = []
humidity_to_location = []

for l in lines:
    if len(l) == 0:
        continue
    if l.startswith("seeds:"):
        seeds = [int(num) for num in l.split(": ")[1].split(' ') if len(num.strip()) > 0]
        continue

    if l.startswith("seed-to-soil map:"):
        current_set = seed_to_soil
    elif l.startswith("soil-to-fertilizer map:"):      
        current_set = soil_to_fertilizer 
    elif l.startswith("fertilizer-to-water map:"):
        current_set = fertilizer_to_water
    elif l.startswith("water-to-light map:"):
        current_set = water_to_light
    elif l.startswith("light-to-temperature map:"):
        current_set = light_to_temperature
    elif l.startswith("temperature-to-humidity map:"):
        current_set = temperature_to_humidity
    elif l.startswith("humidity-to-location map:"):
        current_set = humidity_to_location
    else:
        pieces = parse_line(l)
        current_set.append(pieces)

def map_value(value_map, key):
    to_process = (key, key, key, key)
    for value in value_map:
        if key >= value[0] and key < value[1]:
            to_process = value
            break

    offset = key - to_process[0]
    return to_process[2] + offset


locations = []
for seed in seeds:
    soil = map_value(seed_to_soil, seed)
    fertilizer = map_value(soil_to_fertilizer, soil)
    water = map_value(fertilizer_to_water, fertilizer)
    light = map_value(water_to_light, water)
    temperature = map_value(light_to_temperature, light)
    humidity = map_value(temperature_to_humidity, temperature)
    location = map_value(humidity_to_location, humidity)
    locations.append(location)

print("Part 1:", min(locations))


def map_value_reverse(value_map, key):
    to_process = (key, key, key, key)
    for value in value_map:
        if key >= value[2] and key < value[3]:
            to_process = value
            break

    offset = key - to_process[2]
    return to_process[0] + offset

# We have zero in the maps, start from here
location = -1
while True:
    location = location + 1
    humidity = map_value_reverse(humidity_to_location, location)
    temperature = map_value_reverse(temperature_to_humidity, humidity)
    light = map_value_reverse(light_to_temperature, temperature)
    water = map_value_reverse(water_to_light, light)
    fertilizer = map_value_reverse(fertilizer_to_water, water)
    soil = map_value_reverse(soil_to_fertilizer, fertilizer)
    seed = map_value_reverse(seed_to_soil, soil)
    if (location % 500000) == 0:
        print(location)
    for check_seed in zip(seeds[::2], seeds[1::2]):
        if seed >= check_seed[0] and seed <= (check_seed[0] + check_seed[1] - 1):
            print("Part 2:", location)
            exit(0)

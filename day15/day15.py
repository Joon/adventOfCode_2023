line = open("Inputs/day15.txt", "r").readline()
print(line)

instructions = line.split(",")
hash_total = 0
for i in instructions:
    hash = 0
    for c in [ord(c) for c in i.strip()]:
        hash = ((hash + c) * 17) % 256
    hash_total += hash
    print(f"{i} {hash}")

print(hash_total)

def find_lens_index(box_map, hash, lens):
    for x in range(len(box_map[hash])):
        if box_map[hash][x][0] == lens:
            return x
    return -1

box_map = {}
for i in range(256):
    box_map[i] = []

for i in instructions:
    bits = i.split('-')
    if len(bits) == 1:
        bits = i.split('=')

    hash = 0
    for c in [ord(c) for c in bits[0].strip()]:
        hash = ((hash + c) * 17) % 256
    # operate on the lenses
    if '-' in i:
        lens = i.split("-")[0]
        lens_index = find_lens_index(box_map, hash, lens)
        if lens_index >= 0:
            box_map[hash].pop(lens_index)
    else:
        lens = i.split("=")[0]
        power = int(i.split("=")[1])
        lens_index = find_lens_index(box_map, hash, lens)
        if lens_index >= 0:
            box_map[hash][lens_index] = (lens, power)
        else:
            box_map[hash].append((lens, power))

total = 0
for i in range(256):
    for x in range(len(box_map[i])):
        total += (i + 1) * (x + 1) * box_map[i][x][1]

print("Part 2", total)
        
lines = [l.strip() for l in open('Inputs/day22.txt', 'r').readlines()]


block_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

def parse_line(line, ix):
    ends = line.split('~')
    start = list(map(int, ends[0].split(',')))
    end = list(map(int, ends[1].split(',')))    
    return ((start[0], start[1], start[2]), (end[0], end[1], end[2]), block_names[ix % 10] + str(ix//10))

blocks = [parse_line(line, i) for i, line in enumerate(lines)]

found_diagonals = False
# Input validation - look for diagonals
for b in blocks:
    diff_count = 0
    if b[0][0] != b[1][0]:
        diff_count += 1
    if b[0][1] != b[1][1]:
        diff_count += 1
    if b[0][2] != b[1][2]:
        diff_count += 1
    if diff_count > 1:
        print("Diagonal block", b)
        found_diagonals = True
if not found_diagonals:
    print("No diagonals found")

def occupied_space(muh_blocks):
    result = set()
    for block in muh_blocks:
        for x in range(block[0][0], block[1][0] + 1):
            for y in range(block[0][1], block[1][1] + 1):
                for z in range(block[0][2], block[1][2] + 1):
                    result.add((x, y, z, block[2]))
    return result

def all_blocks(block):
    result = []
    for x in range(block[0][0], block[1][0] + 1):
        for y in range(block[0][1], block[1][1] + 1):
            for z in range(block[0][2], block[1][2] + 1):
                result.append((x, y, z, block[2]))
    return result

def lowest_blocks(block):
    blocks = all_blocks(block)
    lowest_z = min([b[2] for b in blocks])
    return [b for b in blocks if b[2] == lowest_z]

def drop_blocks_to_bottom(blocks):
    working_blocks = blocks.copy()

    more_blocks_to_drop = True
    while more_blocks_to_drop:
        more_blocks_to_drop	= False
        working_blocks.sort(key=lambda x: min(x[0][2], x[1][2]))
        
        for block_index in range(len(working_blocks)):
            if block_index % 100 == 0:
                print("Dropping. Processing block: ", block_index, "current_highest_point", max([b[1][2] for b in working_blocks]))
            block = working_blocks[block_index]
            current_occuped_space = [(x, y, z) for x, y, z, _ in occupied_space(working_blocks)]
            # Drop the block as far as possible
            lowest_block_pieces = lowest_blocks(block)
            drop_depth = 0
            drop_this_block = True
            while drop_this_block:
                drop_depth += 1
                drop_this_block = True
                for (x, y, z, _) in lowest_block_pieces:
                    if z - drop_depth == 0 or (x, y, z - drop_depth) in current_occuped_space:
                        drop_depth -= 1
                        drop_this_block = False
                        break
            if drop_depth > 0:
                working_blocks[block_index] = ((block[0][0], block[0][1], block[0][2] - drop_depth), (block[1][0], block[1][1], block[1][2] - drop_depth), block[2])
                more_blocks_to_drop = True
    return working_blocks

def visualize(show_blocks):
    for z in range(1, 10):
        print("z=", z)
        for y in range(0, 10):
            for x in range(0, 10):
                found = False
                for block in show_blocks:
                    if block[0][0] <= x and block[1][0] >= x and block[0][1] <= y and block[1][1] >= y and block[0][2] <= z and block[1][2] >= z:
                        print(block[2][0], end='')
                        found = True
                        break
                if not found:
                    print('.', end='')
            print()

settled_blocks = drop_blocks_to_bottom(blocks)
print(settled_blocks)
#visualize(settled_blocks)

occupied_space_blocks = {}
found_overlap = False
# Debugging - are there overlapping blocks?
for b in settled_blocks:
    for block in all_blocks(b):
        coord = (block[0], block[1], block[2])
        if coord in occupied_space_blocks:
            print("Overlap", block, occupied_space[block], b)
            occupied_space_blocks[coord].append(b)
            found_overlap = True
        else:
            occupied_space_blocks[coord] = [b]

if not found_overlap:
    print("No overlap found")

found_unsupported = False
supporters = {}
# Debugging - are there unsupported blocks?
all_used_space = [(x, y, z, block_code) for x, y, z, block_code in occupied_space(settled_blocks)]
for b in settled_blocks:
    block_occupies = all_blocks(b)
    lowest_point = min([b[2] for b in block_occupies])
    low_blocks = [b for b in block_occupies if b[2] == lowest_point]
    # Is this resting on the ground?
    if any(b[2] for b in low_blocks if b[2] == 1):
        continue
    # No it's not - check the supporting blocks
    found_support = False
    for block in low_blocks:
        coord = (block[0], block[1], block[2])
        supporting_blocks = [(x, y, z, block_code) for x, y, z, block_code in all_used_space if x == coord[0] and y == coord[1] and z == coord[2] - 1]
        if len(supporting_blocks) > 0:
            for supporter in [blo[3] for blo in supporting_blocks]:
                if b[2] not in supporters:
                    supporters[b[2]] = []
                supporters[b[2]].append(supporter)
            found_support = True
    if not found_support:
        print("Unsupported block", b)
        found_unsupported = True

if not found_unsupported:
    print("No unsupported blocks")

immovable_blocks = set()
for b in supporters:
    if len(set(supporters[b])) == 1:
        immovable_blocks.add(supporters[b].pop())

print("Part 1:", len(blocks) - len(immovable_blocks))


supported = {}

for b in settled_blocks:
    supported[b[2]] = set()
    for block in all_blocks(b):
        coord = (block[0], block[1], block[2])
        supporting_blocks = [(x, y, z, block_code) for x, y, z, block_code in all_used_space if x == coord[0] and y == coord[1] and z == coord[2] + 1 and block_code != b[2]]
        for supporter in [blo[3] for blo in supporting_blocks]:
            supported[b[2]].add(supporter)

print(supported)

def follow_chain_reaction(block):
    collapse_stack = []
    collapse_stack.append(block)
    chain = []
    while len(collapse_stack) > 0:
        b = collapse_stack.pop()
        chain.append(b)
        for supported_by in supported[b]:
            if supported_by not in chain:
                all_supporters_will_collapse = True
                for candidate_block_supporter in supporters[supported_by]:
                    if candidate_block_supporter not in chain and candidate_block_supporter not in collapse_stack:
                        all_supporters_will_collapse = False
                        break
                if all_supporters_will_collapse:
                    collapse_stack.append(supported_by)
    return chain

chain_reaction_total = 0
for b in settled_blocks:
    chain = follow_chain_reaction(b[2])
    chain_reaction_total += len(chain) - 1

print("Part 2:", chain_reaction_total)
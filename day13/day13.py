
lines = [[c for c in l.strip()] for l in open("Inputs/day13.txt", "r").readlines()]

pattern_blocks = []
current_block = []
for l in lines:
    if l == []:
        if current_block != []: 
            pattern_blocks.append(current_block.copy())
        current_block = []
    else:
        current_block.append(l)
if current_block != []: 
    pattern_blocks.append(current_block.copy())

def find_mirrors_vertical(pattern):
    mirror_points = []
    # Look for mirror points up to the second to last row
    for row in range(len(pattern) - 1):
        is_match = pattern[row] == pattern[row + 1]
        if is_match:
            for compare_row in range(1, row + 1):
                match_index_1 = row + 1 + compare_row
                match_index_2 = row - compare_row
                if match_index_1 < len(pattern) and match_index_1 >= 0 and match_index_2 < len(pattern) and match_index_2 >= 0:
                    is_match = is_match and pattern[match_index_1] == pattern[match_index_2]
                if not is_match:
                    break
        if is_match:
            mirror_points.append(row + 1)
    return mirror_points


def find_mirrors_horizontal(pattern):
    mirror_points = []
    # Look for mirror points up to the second to last row
    for col in range(len(pattern[0]) - 1):
        is_match = [row[col] for row in pattern] == [row[col + 1] for row in pattern]
        if is_match:
            for compare_col in range(1, col + 1):
                match_index_1 = col + 1 + compare_col
                match_index_2 = col - compare_col
                if match_index_1 < len(pattern[0]) and match_index_1 >= 0 and match_index_2 < len(pattern[0]) and match_index_2 >= 0:
                    is_match = is_match and [row[match_index_1] for row in pattern] == [row[match_index_2] for row in pattern]
                if not is_match:
                    break
        if is_match:
            mirror_points.append(col + 1)
    return mirror_points

def smudge_find_mirrors_vertical(pattern):
    reference_pattern = find_mirrors_vertical(pattern)
    for row in range(len(pattern)):
        for col in range(len(pattern[0])):
            smudged_pattern = [p.copy() for p in pattern]
            if smudged_pattern[row][col] == '#':
                smudged_pattern[row][col] = '.'
            else:
                smudged_pattern[row][col] = '#'
            mirrors = find_mirrors_vertical(smudged_pattern)
            if len(mirrors) > 0 and mirrors != reference_pattern:
                return [m for m in mirrors if m not in reference_pattern]
    return []

def smudge_find_mirrors_horizontal(pattern):
    reference_pattern = find_mirrors_horizontal(pattern)
    for row in range(len(pattern)):
        for col in range(len(pattern[0])):
            smudged_pattern = [p.copy() for p in pattern]
            if smudged_pattern[row][col] == '#':
                smudged_pattern[row][col] = '.'
            else:
                smudged_pattern[row][col] = '#'
            mirrors = find_mirrors_horizontal(smudged_pattern)
            if len(mirrors) > 0 and mirrors != reference_pattern:
                return [m for m in mirrors if m not in reference_pattern]
    return []

total = 0
for p in pattern_blocks:
    total += sum(find_mirrors_vertical(p)) * 100
    total += sum(find_mirrors_horizontal(p))

print("Part 1:", total)

total = 0
for p in pattern_blocks:
    total += sum(smudge_find_mirrors_vertical(p)) * 100
    total += sum(smudge_find_mirrors_horizontal(p))

print("Part 2:", total)
import itertools
import re
from functools import cache

lines = [l for l in open("Inputs/day12.txt", "r").readlines() if l.strip() != ""]

class InventoryLine:
    def __init__(self, line, unknowns, group_sizes):
        self.line = [c for c in line]
        self.unknowns = unknowns
        self.group_sizes = group_sizes

    def make_regex(self):
        # Zero or more .s
        regex = "^\.*"
        for g in self.group_sizes:
            # Exact size of the group and one or more .s
            regex += "#{" + str(g) + "}\.+"
        
        return regex[:-1] + "*" + "$"
    
    def matches(self, line_option):
        return re.match(self.make_regex(), line_option)

    def __repr__(self):
        return f"{''.join(self.line)} Unknowns: {self.unknowns} Expected Groups: {self.group_sizes} Regex: {self.make_regex()}"
    
inventories = []
for l in lines:
    line = l.split(' ')[0].strip()
    group_sizes = [int(piece) for piece in l.split(' ')[1].strip().split(',')]
    in_unknown = False
    unknown_start = None
    unknowns = []
    for x in range(len(line)):
        c = line[x]
        if c == '?':
            if not in_unknown:
                in_unknown = True
                unknown_start = x
        else:
            if in_unknown:
                unknowns.append((unknown_start, x - 1))
                in_unknown = False
                unknown_start = None
    if in_unknown:
        unknowns.append((unknown_start, len(line) - 1))
        in_unknown = False
        unknown_start = None
    inventories.append(InventoryLine(line, unknowns, group_sizes))

match_count = 0

for i in inventories:
    substitute_locations = []
    for u in i.unknowns:
        substitute_locations.extend(range(u[0], u[1] + 1))
    replacement_options = sum([list(map(list, itertools.combinations(substitute_locations, i))) for i in range(len(substitute_locations) + 1)], [])
    processed_combos = {}
    for r in replacement_options:
        replacement = i.line.copy()
        for x in r:
            replacement[x] = '#'
        for x in range(len(replacement)):
            if replacement[x] == '?':
                replacement[x] = '.'
        if i.matches(''.join(replacement)):
            match_count += 1
            #print(f"Matched {i} with {''.join(replacement)}")

print ("Part 1:", match_count)

long_inventories = []
for l in lines:
    line = l.split(' ')[0].strip()
    group_sizes = [int(piece) for piece in l.split(' ')[1].strip().split(',')] * 5
    long_line = "?".join([line] * 5)
    long_inventories.append(InventoryLine(long_line, [], group_sizes))

@cache
def valid_combination_count(remaining_chars, remaining_groups, run_length = 0):
    if len(remaining_chars) == 0:
        if ((len(remaining_groups)==1 and remaining_groups[0] == run_length) or (len(remaining_groups)==0 and run_length == 0)):
            return 1
        return 0
    
    head = remaining_chars[0]
    rest = remaining_chars[1:]
    group, *new_groups = remaining_groups or [0]
    if head == '#':
        return 0 if run_length > group else valid_combination_count(rest, remaining_groups, run_length + 1)
    if head == '?':
        return valid_combination_count('.' + rest, remaining_groups, run_length) + valid_combination_count('#' + rest, remaining_groups, run_length)
    if head == '.':
        if run_length == 0:
            return valid_combination_count(rest, remaining_groups, 0)
        if run_length == group:
            return valid_combination_count(rest, tuple(new_groups), 0)
        return 0
    raise ValueError("Spring not one of #.?")


long_match_count = 0
for i in long_inventories:
    print(f"Processing item {i} of {len(long_inventories)}")
    long_match_count += valid_combination_count(''.join(i.line), tuple(i.group_sizes))
print("part 2: ", long_match_count)
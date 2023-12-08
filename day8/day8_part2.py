import re
from math import lcm
from functools import reduce

file2 = open('Inputs/day8.txt', 'r')
lines = [l.strip() for l in file2.readlines()]

class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'Node({self.left}, {self.right})'

nodes = {}
pattern = '^([0-9,A-Z]{3}) = \(([0-9,A-Z]{3}), ([0-9,A-Z]{3})\)$'

for l in lines[2:]:
    match = re.match(pattern, l)
    nodes[match.group(1)] = Node(match.group(2), match.group(3))

instructions = [c for c in lines[0].strip()]

def not_completed(nodes):
    return any([n[2] != 'Z' for n in nodes])

navigation_nodes = [n for n in nodes if n[2] == 'A']
distances_to_Z = []
for n in navigation_nodes:
    steps = 0
    current_node = n
    instruction_index = 0
    while current_node[2] != 'Z':
        steps += 1
        if instruction_index >= len(instructions):
            instruction_index = 0
        instruction = instructions[instruction_index]
        instruction_index += 1
        
        if instruction == 'L':
            current_node = nodes[current_node].left
        elif instruction == 'R':
            current_node = nodes[current_node].right
        else:
            raise Exception('Unknown instruction')
    distances_to_Z.append(steps)

print("part 2: ", reduce(lambda x, y: lcm(x, y), distances_to_Z))


import re


file2 = open('Inputs/day8.txt', 'r')
lines = [l.strip() for l in file2.readlines()]

class Node:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'Node({self.left}, {self.right})'

nodes = {}
pattern = '^([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)$'

for l in lines[2:]:
    match = re.match(pattern, l)
    nodes[match.group(1)] = Node(match.group(2), match.group(3))

instructions = [c for c in lines[0]]

current_node = 'AAA'
instruction_index = 0
steps = 0
while current_node != 'ZZZ':
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

print("part 1: ", steps)

# part 2
navigation_nodes = [n for n in nodes if n[2] == 'A']
]
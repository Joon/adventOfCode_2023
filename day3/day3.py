file2 = open('../Inputs/day3.txt', 'r')
lines = file2.readlines()
lines = [l.strip() for l in lines]

def char_is_symbol(check_char):
    return check_char != '.' and (not check_char.isdigit())

def should_add(lines, running_number, x, y):
    add_num = False
    # check rows above and below
    for check_border in range(x - (len(running_number)) + 1, x + 1):
        if y - 1 >= 0:
            check_char = lines[y - 1][check_border]
            if char_is_symbol(check_char):
                add_num = True
        if y + 1 < len(lines):
            check_char = lines[y + 1][check_border]
            if char_is_symbol(check_char):
                add_num = True
    # check column left and right
    for check_column in [-1, 0, 1]:
        # Is the check to the left of the word cleared to proceed based on indexes?
        if y + check_column >= 0 and y + check_column < len(lines) and x - (len(running_number) + 1) >= 0:
            # Is the character to check a symbol
            check_char = lines[y + check_column][x - (len(running_number))]
            if char_is_symbol(check_char):
                add_num = True
        # Is the check to the right of the word cleared to proceed based on indexes?
        if y + check_column >= 0 and y + check_column < len(lines) and x + 1 < len(lines[y + check_column]):
            check_char = lines[y + check_column][x + 1]
            if char_is_symbol(check_char):
                add_num = True
    return add_num

def part_numbers(lines):
    result_numbers = []
    numbers = parse_all_part_numbers(lines)
    for key, value in numbers.items():
        if should_add(lines, str(value), key[0], key[1]):
            result_numbers.append(value)
    return result_numbers

def parse_all_part_numbers(lines):
    numbers = {}
    for y in range(0, len(lines)):
        line = lines[y]
        running_number = ""
        for x in range(0, len(line)):
            line_char = line[x]
            if line_char.isdigit():
                running_number += line_char
            else:                
                if running_number != "":
                    # We are checking the first non-digit, 
                    # so the number is one to the left
                    numbers[(x - 1, y)] = int(running_number)
                    running_number = ""
        if running_number != "":
            # We have wrapped lines, the number is where the x stopped
            numbers[(x, y)] = int(running_number)
            running_number = ""
    return numbers
            
def find_adjacent_parts(all_parts, x, y):
    result_part_numbers = []
    for key, value in all_parts.items():
        part_y = key[1]
        part_end_x = key[0]
        part_start_x = part_end_x - len(str(value)) + 1
        # Is it above the symbol
        if part_y == y - 1 and part_start_x <= x and part_end_x >= x:
            result_part_numbers.append(value)
        # Is it diagonal above left
        if part_y == y - 1 and part_end_x == x - 1:
            result_part_numbers.append(value)
        # Is it diagonal above right
        if part_y == y - 1 and part_start_x == x + 1:
            result_part_numbers.append(value)
        # Is it below the symbol
        if part_y == y + 1 and part_start_x <= x and part_end_x >= x:
            result_part_numbers.append(value)
        # Is it diagonal below left
        if part_y == y + 1 and part_end_x == x - 1:
            result_part_numbers.append(value)
        # Is it diagonal below right
        if part_y == y + 1 and part_start_x == x + 1:
            result_part_numbers.append(value)
        # Is it to the left of the symbol
        if part_y == y and part_end_x == x - 1:
            result_part_numbers.append(value)
        # Is it to the right of the symbol
        if part_y == y and part_start_x == x + 1:
            result_part_numbers.append(value)
    return result_part_numbers

def gear_ratios(lines):
    ratios = []
    all_parts = parse_all_part_numbers(lines)
    for y in range(0, len(lines)):
        line = lines[y]        
        for x in range(0, len(line)):
            if line[x] == '*':
                adjacent_parts = find_adjacent_parts(all_parts, x, y)
                if len(adjacent_parts) == 2:
                    ratios.append(adjacent_parts[0] * adjacent_parts[1])
    return ratios

tot = 0
for n in part_numbers(lines):
    tot = tot + n

print("Part 1: ", tot)

tot_gr = 0
for n in gear_ratios(lines):
    tot_gr = tot_gr + n
print("Part 2: ", tot_gr)
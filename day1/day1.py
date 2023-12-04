file1 = open('../Inputs/day1.txt', 'r')
lines = file1.readlines()
total = 0

word_replacements = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine' : '9',
    'zero': '0'
}

part1_total = 0
part2_total = 0

for line in lines:
    l = line.strip()
    
    simple_nums = [c for c in l if c.isdigit()]
    val = simple_nums[0]
    val = val + simple_nums[-1]
    part1_total = part1_total + int(val)

    ix_nums = dict([c for c in enumerate(l) if c[1].isdigit()])
    for i in range(len(line)):
        for w in word_replacements:
            if l.find(w, i, i + len(w)) != -1:
                ix_nums[i] = word_replacements[w]
    sorted_ix_nums = dict(sorted(ix_nums.items()))
    nums = [ix_nums[c] for c in sorted_ix_nums]

    val = nums[0]
    val = val + nums[-1]
    part2_total = part2_total + int(val)

print("Part 1:", part1_total)
print("Part 2:", part2_total)
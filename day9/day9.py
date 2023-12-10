file2 = open('Inputs/day9.txt', 'r')
lines = [l.strip() for l in file2.readlines()]

def print_debug(seq, tot):
    print(f'{seq} {tot}')

sequences = [[int(piece.strip()) for piece in l.split() if piece != ''] for l in lines]
big_tot = 0
little_tot = 0 
for s in sequences:
    seqlist = [s]
    if len(s) > 1:
        newseq = [y - x for (x, y) in zip(s[0:], s[1:])]
        seqlist.append(newseq.copy())
        while set(newseq) != {0}:
            newseq = [y - x for (x, y) in zip(newseq, newseq[1:])]
            seqlist.append(newseq.copy())
    
    running_tot = 0
    for new_s in reversed(seqlist):
        running_tot += new_s[-1]
        print_debug(new_s, running_tot)
    big_tot += running_tot

    running_tot = 0
    for new_s in reversed(seqlist):
        running_tot += new_s[0]
        print_debug(new_s, running_tot)
    little_tot = little_tot + running_tot


print("Part 1:", big_tot)
print("Part 2:", little_tot)

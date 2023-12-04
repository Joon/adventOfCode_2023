file2 = open('Inputs/day4.txt', 'r')
lines = [l.strip() for l in file2.readlines()]

def parse_line(line):
    parts = line.split(':')
    gameparts = [p.strip() for p in parts[1].split('|') if p.strip() != '']
    hand = [int(n.strip()) for n in gameparts[0].split(' ') if n.strip() != '']
    wnners = [int(n.strip()) for n in gameparts[1].split(' ') if n.strip() != '']
    game_id = int(parts[0].split(' ')[-1])
    return (game_id, hand, wnners)

games = [parse_line(l) for l in lines]

running_score = 0
for g in games:
    overlaps = set(g[1]).intersection(set(g[2]))
    if len(overlaps) > 0:
        running_score += pow(2, len(overlaps) - 1)

print("Part 1:", running_score)

def play_game(games):
    all_cards = len(games)
    card_index = {}
    for game_id, hand, winners in games:
        card_index[game_id] = len(set(hand).intersection(set(winners)))

    to_process = [id for id in card_index]
    while len(to_process) > 0:
        processing_id = to_process.pop()
        overlaps = card_index[processing_id]
        for n in range(overlaps):
            clone_id = processing_id + n + 1
            if clone_id in card_index:
                to_process.append(clone_id)
                all_cards = all_cards + 1
    
    return all_cards

print("Part 2:", play_game(games))
        
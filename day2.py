class Turn:
    Red: int
    Green: int
    Blue: int
    def __init__(self):
        self.Red = 0
        self.Green = 0
        self.Blue = 0

class Game:
    GameId: int
    turns: list[Turn]
    def __init__(self, gameId):
        self.GameId = int(gameId)
        self.turns = []
    
def ParseTurn(turn_str):
    parts = turn_str.strip().split(',')
    turn = Turn()
    for p in parts:
        turn_deets = p.strip().split(' ')
        match turn_deets[1].strip():
            case 'red':
                turn.Red = int(turn_deets[0].strip())
            case 'green':
                turn.Green = int(turn_deets[0].strip())
            case 'blue':
                turn.Blue = int(turn_deets[0].strip())

    return turn

def ParseGame(line):
    parts = line.split(':')

    game = Game(parts[0].strip().split(' ')[1])

    turns = parts[1].strip().split(';')
    for t in turns:
        game.turns.append(ParseTurn(t))
    return game

def Valid_Game(turn, game):
    for t in game.turns:
        if t.Red > turn.Red or t.Green > turn.Green or t.Blue > turn.Blue:
            return False
    return True

def calc_power(turn):
    return turn.Red * turn.Green * turn.Blue

def possible_bag_power(game):
    max_counts = Turn()
    for t in game.turns:
        if t.Red > max_counts.Red:
            max_counts.Red = t.Red
        if t.Green > max_counts.Green:
            max_counts.Green = t.Green
        if t.Blue > max_counts.Blue:
            max_counts.Blue = t.Blue
    return calc_power(max_counts)

file2 = open('inputs/day2.txt', 'r')
lines = file2.readlines()

games = [ParseGame(l) for l in lines]

validate_turn = Turn()
validate_turn.Blue = 14
validate_turn.Red = 12
validate_turn.Green = 13

valid_game_score = 0
for game in games:
    if Valid_Game(validate_turn, game):
        valid_game_score += game.GameId

print("Part 1: ", valid_game_score)

total_power = 0
for game in games:
    total_power += possible_bag_power(game)

print("Part 2: ", total_power)
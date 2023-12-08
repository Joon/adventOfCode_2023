card_strength = {'A': 20, 'K': 19, 'Q': 18, 'J': 17, 'T': 16, '9': 15, '8': 14, '7': 13, '6': 12, '5': 11, '4': 10, '3': 9, '2': 8}

class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = int(bid)
        self.use_joker = False

    def improve_hand(self, letters):
        # No Joker, nothing to do
        if 'J' not in letters:
            return self.cards
        # All J values, don't replace anything
        if len(letters) == 1:
            return self.cards

        # Improve cards by the highest count first
        letter_counts = []
        for l in letters:
            count_tuple = ([c[0] for c in self.cards].count(l), l)
            letter_counts.append(count_tuple)
        letter_counts = sorted(letter_counts, reverse=True)
        # If there's a tie, improve the card with the highest value
        if letter_counts[0][0] == letter_counts[1][0]:
            if card_strength[letter_counts[0][1]] > card_strength[letter_counts[1][1]]:
                return self.cards.replace('J', letter_counts[0][1])
            else:
                return self.cards.replace('J', letter_counts[1][1])
        # No tie, is the card with the highest count a joker?
        if letter_counts[0][1] == 'J':
            # If so, improve the card with the second highest count
            return self.cards.replace('J', letter_counts[1][1])
        else:
            # improve the card with the highest count
            return self.cards.replace('J', letter_counts[0][1])

    def strength(self):
        letters = set([c[0] for c in self.cards])
        use_cards = self.cards
        if self.use_joker:
            use_cards = self.improve_hand(letters)
            letters = set([c[0] for c in use_cards])
            
        # All different cards
        if len(letters) == 5:
            return 1
        # Only one letter has to be five of a kind
        if len(letters) == 1:
            return 7
        # Now check for 4 of a kind
        if len(letters) == 2:
            for l in letters:
                if [c[0] for c in use_cards].count(l) == 4:
                    return 6
            # Not four of a kind - with two letters, it's a full house
            return 5
        # Three letters means two pair or three of a kind
        if len(letters) == 3:
            for l in letters:
                if [c[0] for c in use_cards].count(l) == 3:
                    return 4
            return 3
        # Four letters means one pair
        if len(letters) == 4:
            return 2

    def __lt__(self, other):
        if self.strength() < other.strength():
            return True
        elif self.strength() > other.strength():
            return False
        
        for i in range(0, len(self.cards)):
            self_strength = card_strength[self.cards[i]]
            other_strength = card_strength[other.cards[i]]
            if self_strength < other_strength:
                return True
            elif self_strength > other_strength:
                return False
        return False

    def __gt__(self, other):
        if self.strength() < other.strength():
            return False
        elif self.strength() > other.strength():
            return True
        
        for i in range(0, len(self.cards)):
            self_strength = card_strength[self.cards[i]]
            other_strength = card_strength[other.cards[i]]
            if self_strength < other_strength:
                return False
            elif self_strength > other_strength:
                return True
        return False

    def __eq__(self, other):
        if self.strength() != other.strength():
            return False
        for i in range(0, len(self.cards)):
            self_strength = card_strength[self.cards[i]]
            other_strength = card_strength[other.cards[i]]
            if self_strength != other_strength:
                return False
        return True

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)
    
file2 = open('Inputs/day7.txt', 'r')
lines = [l.strip() for l in file2.readlines()]
hands = []
for l in lines:
    parts = l.split(' ')
    hands.append(Hand(parts[0].strip(), parts[1].strip()))

total_score = 0
sorted_hands = sorted(hands)
for h in enumerate(sorted_hands):
    total_score = total_score + h[1].bid * (h[0] + 1)

print("Part 1: " + str(total_score))

card_strength['J'] = 7

for h in hands:
    h.use_joker = True

total_score = 0
sorted_hands = sorted(hands)
for h in enumerate(sorted_hands):
    total_score = total_score + h[1].bid * (h[0] + 1)

print("Part 2: " + str(total_score))


# Tests for hand promotion
hand = Hand('AJJAJ', 1)
hand.use_joker = True
print(hand.improve_hand(set(['A', 'J', '9'])))
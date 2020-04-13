class Card():
    def __init__(self, val, suit):
        self.value = val
        self.suit = suit

    def __lt__(self, card):
        return self.value < card.value

    def __gt__(self, card):
        return self.value > card.value

    def __eq__(self, card):
        return not (self < card) and not (self > card)

    def suit_to_str(self, condensed=False):
        if self.suit == 'H':
            return "H" if condensed else "hearts"
        elif self.suit == 'C':
            return "C" if condensed else "clubs"
        elif self.suit == 'S':
            return "S" if condensed else "spades"
        else:
            return "D" if condensed else "diamonds"
    
    def value_to_str(self, condensed=False):
        if self.value <= 10:
            return str(self.value)
        elif self.value == 11:
            return "J" if condensed else "Jack"
        elif self.value == 12:
            return "Q" if condensed else "Queen"
        elif self.value == 13:
            return "K" if condensed else "King"
        else:
            return "A" if condensed else "Ace"

    def __str__(self):
        return str(self.value_to_str()) + " of " + self.suit_to_str()

    def str_condensed(self):
        return str(self.value_to_str(condensed=True)) + str(self.suit_to_str(condensed=True))
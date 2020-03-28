class Card():
    def __init__(self, val, suit):
        self.value = val
        self.suit = suit

    def __lt__(self, card):
        self.value < card.value

    def __eq__(self, card):
        return not (self < card) and not (self > card)

    def __str__(self):
        return str(self.value) + self.suit
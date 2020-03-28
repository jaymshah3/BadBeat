class Card():
    def __init__(self, val, suit):
        self.value = val
        self.suit = suit

    def __lt__(self, card):
        return self.value < card.value

    def __eq__(self, card):
        return not (self < card) and not (self > card)
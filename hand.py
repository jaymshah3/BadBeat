import card.py
class Hand():
    def __init__(self, cards):
        self.cards = cards
        maxCard = findMaxCard()
        isStraight = false
        isFlush = false

    def findMaxCard(self):
        maxCard = cards[0]
        for card in cards:
            if card > maxCard:
                maxCard = card
            
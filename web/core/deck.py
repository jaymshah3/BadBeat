from card import Card
import random

class Deck():

    def __init__(self):
        self.cards = []
        self.index = 0
        for s in ['C', 'D', 'H', 'S']:
            for i in range(2, 15):
                self.cards.append(Card(i, s))

    def __str__(self):
        s = ""
        for c in self.cards:
            s += str(c)
            s += "\n"
        
        return s

    def shuffle(self):
        self.index = 0
        random.shuffle(self.cards)

    def get_top_card(self):
        if self.index < 52:
            c = self.cards[self.index]
            self.index += 1
            return c
        else:
            return None

    
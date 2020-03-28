from card import Card
from hand import Hand
c = []
c.append(Card(3,'d'))
c.append(Card(4,'d'))
c.append(Card(5,'c'))
c.append(Card(6,'c'))
c.append(Card(7,'c'))
h = Hand(c)
print(h.max_card)
print(h.is_flush)
print(h.is_straight)


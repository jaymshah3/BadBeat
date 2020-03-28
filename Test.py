from card import Card
from hand import Hand
c = []
c.append(Card(2,'c'))
c.append(Card(2,'c'))
c.append(Card(4,'c'))
c.append(Card(2,'c'))
c.append(Card(5,'d'))
h = Hand(c)
print(h.max_card)
print(h.is_flush)
print(h.is_straight)
print(h.major_group)


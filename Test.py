from card import Card
from hand import Hand
c = []
c.append(Card(12,'c'))
c.append(Card(13,'c'))
c.append(Card(11,'c'))
c.append(Card(14,'c'))
c.append(Card(9,'d'))
h = Hand(c)
print(h.max_card)
print(h.is_flush)
print(h.is_straight)
print(h.major_group)


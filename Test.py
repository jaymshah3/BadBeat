from card import Card
from hand import Hand
c = []
c.append(Card(12,'c'))
c.append(Card(13,'c'))
c.append(Card(1,'c'))
c.append(Card(10,'c'))
c.append(Card(11,'c'))
h = Hand(c)
print(h.max_card)
print(h.is_flush)
print(h.is_straight)


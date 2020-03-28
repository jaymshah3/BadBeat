from card import Card
from hand import Hand
c = []
c.append(Card(6,'c'))
c.append(Card(6,'c'))
c.append(Card(6,'c'))
c.append(Card(14,'c'))
c.append(Card(6,'d'))
h = Hand.create_hand(c)
print(h.max_card)
print(h.is_flush)
print(h.is_straight)
print(h.major_group)


d = []
d.append(Card(6,'c'))
d.append(Card(5,'c'))
d.append(Card(5,'c'))
d.append(Card(5,'c'))
d.append(Card(5,'d'))
h2 = Hand.create_hand(d)
print(h2.max_card)
print(h2.is_flush)
print(h2.is_straight)
print(h2.major_group)
h < h2
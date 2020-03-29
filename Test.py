from card import Card
from hand import Hand
c = []
c.append(Card(7,'c'))
c.append(Card(4,'c'))
c.append(Card(3,'d'))
c.append(Card(5,'c'))
c.append(Card(6,'c'))
h = Hand.create_hand(c)
#print(h.max_card)
#print(h.is_flush)
#print(h.is_straight)
#print(h.major_group)


d = []
d.append(Card(4,'d'))
d.append(Card(5,'c'))
d.append(Card(6,'c'))
d.append(Card(2,'c'))
d.append(Card(3,'c'))
h2 = Hand.create_hand(d)
#print(h2.max_card)
#print(h2.is_flush)
#print(h2.is_straight)
#print(h2.major_group)
print(h > h2)
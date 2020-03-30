from card import Card
from hand import Hand
c = []
c.append(Card(5,'c'))
c.append(Card(7,'c'))
c.append(Card(7,'c'))
c.append(Card(2,'c'))
c.append(Card(5,'c'))
h = Hand.create_hand(c)
#print(h.max_card)
#print(h.is_flush)
#print(h.is_straight)
#print(h.major_group)


d = []
d.append(Card(7,'d'))
d.append(Card(7,'c'))
d.append(Card(3,'c'))
d.append(Card(4,'c'))
d.append(Card(5,'c'))
h2 = Hand.create_hand(d)
#print(h2.max_card)
#print(h2.is_flush)
#print(h2.is_straight)
#print(h2.major_group)
print(h < h2)
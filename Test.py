from card import Card
from hand import Hand
c = []
c.append(Card(3,'c'))
c.append(Card(4,'c'))
c.append(Card(5,'c'))
c.append(Card(6,'c'))
c.append(Card(7,'c'))
h = Hand(c)
print(c[0])
print(h.max_card)
print(h.is_flush)
def find_is_straight(hand):
    for i in range(len(hand.cards)-1):
         if hand.cards[i].value > hand.cards[i+1].value:
            return False
    return True
print(find_is_straight(h))



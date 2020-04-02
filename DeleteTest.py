import unittest
from card import Card
from hand import Hand
from player import Player


class TestFlushCmp(unittest.TestCase):

    def setUp(self):
        c = []
        c.append(Card(7,'c'))
        c.append(Card(4,'c'))
        c.append(Card(3,'d'))
        c.append(Card(5,'c'))
        c.append(Card(6,'c'))
        self.h1 = Hand.create_hand(c)
        d = []
        d.append(Card(4,'d'))
        d.append(Card(5,'c'))
        d.append(Card(6,'c'))
        d.append(Card(2,'c'))
        d.append(Card(3,'c'))
        self.h2 = Hand.create_hand(d)

    def test_equal(self):
        a = self.h1 == self.h2
        print(self.h1.max_card)
        self.assertEqual(a,False)

if __name__ == '__main__':
    unittest.main()
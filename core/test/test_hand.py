import unittest
from ..hand import Hand
from ..card import Card

class TestStraight(unittest.TestCase):
    def test_equal(self):
        two_six_a = []
        two_six_a.append(Card(7,'c'))
        two_six_a.append(Card(4,'c'))
        two_six_a.append(Card(3,'d'))
        two_six_a.append(Card(5,'c'))
        two_six_a.append(Card(6,'c'))
        two_six_a_hand = Hand.create_hand(two_six_a)

        two_six_b = []
        two_six_b.append(Card(3,'s'))
        two_six_b.append(Card(6,'c'))
        two_six_b.append(Card(7,'d'))
        two_six_b.append(Card(5,'c'))
        two_six_b.append(Card(4,'h'))
        two_six_b_hand = Hand.create_hand(two_six_b)

        self.assertEqual(two_six_a_hand, two_six_b_hand)

    def test_lt_without_ace(self):
        def test_equal(self):
            two_six_a = []
            two_six_a.append(Card(7,'c'))
            two_six_a.append(Card(4,'c'))
            two_six_a.append(Card(3,'d'))
            two_six_a.append(Card(5,'c'))
            two_six_a.append(Card(6,'c'))
            two_six_a_hand = Hand.create_hand(two_six_a)

            two_six_b = []
            two_six_b.append(Card(7,'c'))
            two_six_b.append(Card(8,'c'))
            two_six_b.append(Card(10,'d'))
            two_six_b.append(Card(6,'h'))
            two_six_b.append(Card(9,'s'))
            two_six_b_hand = Hand.create_hand(two_six_b)

            self.assertLessThan(two_six_a_hand, two_six_b_hand)
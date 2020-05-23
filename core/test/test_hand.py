import unittest
from ..hand import Hand
from ..card import Card

class TestStraight(unittest.TestCase):
    def test_equal_without_ace(self):
        two_six_a = []
        two_six_a.append(Card(7,'c'))
        two_six_a.append(Card(4,'c'))
        two_six_a.append(Card(3,'d'))
        two_six_a.append(Card(5,'c'))
        two_six_a.append(Card(6,'c'))
        two_six_a_hand = Hand.create_hand(two_six_a)
        self.assertEqual(two_six_a_hand.major_group, 5)

        two_six_b = []
        two_six_b.append(Card(3,'s'))
        two_six_b.append(Card(6,'c'))
        two_six_b.append(Card(7,'d'))
        two_six_b.append(Card(5,'c'))
        two_six_b.append(Card(4,'h'))
        two_six_b_hand = Hand.create_hand(two_six_b)

        self.assertEqual(two_six_b_hand.major_group, 5)
        self.assertEqual(two_six_a_hand, two_six_b_hand)

    def test_equal_with_ace(self):
        two_six_a = []
        two_six_a.append(Card(14,'c'))
        two_six_a.append(Card(4,'c'))
        two_six_a.append(Card(3,'d'))
        two_six_a.append(Card(5,'c'))
        two_six_a.append(Card(2,'c'))
        two_six_a_hand = Hand.create_hand(two_six_a)
        self.assertEqual(two_six_a_hand.major_group, 5)

        two_six_b = []
        two_six_b.append(Card(14,'s'))
        two_six_b.append(Card(3,'c'))
        two_six_b.append(Card(2,'d'))
        two_six_b.append(Card(5,'c'))
        two_six_b.append(Card(4,'h'))
        two_six_b_hand = Hand.create_hand(two_six_b)

        self.assertEqual(two_six_b_hand.major_group, 5)
        self.assertEqual(two_six_a_hand, two_six_b_hand)
    
    def test_without_ace(self):
        two_six_a = []
        two_six_a.append(Card(7,'c'))
        two_six_a.append(Card(4,'c'))
        two_six_a.append(Card(3,'d'))
        two_six_a.append(Card(5,'c'))
        two_six_a.append(Card(6,'c'))
        two_six_a_hand = Hand.create_hand(two_six_a)
        self.assertEqual(two_six_a_hand.major_group, 5)

        two_six_b = []
        two_six_b.append(Card(7,'c'))
        two_six_b.append(Card(8,'c'))
        two_six_b.append(Card(10,'d'))
        two_six_b.append(Card(6,'h'))
        two_six_b.append(Card(9,'s'))
        two_six_b_hand = Hand.create_hand(two_six_b)

        self.assertEqual(two_six_b_hand.major_group, 5)
        self.assertEqual(two_six_a_hand < two_six_b_hand, True)
        self.assertEqual(two_six_a_hand > two_six_b_hand, False)
        self.assertEqual(two_six_b_hand < two_six_a_hand, False)
        self.assertEqual(two_six_b_hand > two_six_a_hand, True)

    def test_with_ace(self):
        two_six_a = []
        two_six_a.append(Card(14,'c'))
        two_six_a.append(Card(4,'c'))
        two_six_a.append(Card(3,'s'))
        two_six_a.append(Card(5,'s'))
        two_six_a.append(Card(2,'s'))
        two_six_a_hand = Hand.create_hand(two_six_a)
        self.assertEqual(two_six_a_hand.major_group, 5)

        two_six_b = []
        two_six_b.append(Card(7,'c'))
        two_six_b.append(Card(8,'c'))
        two_six_b.append(Card(10,'d'))
        two_six_b.append(Card(6,'h'))
        two_six_b.append(Card(9,'s'))
        two_six_b_hand = Hand.create_hand(two_six_b)

        self.assertEqual(two_six_b_hand.major_group, 5)
        self.assertEqual(two_six_a_hand < two_six_b_hand, True)
        self.assertEqual(two_six_a_hand > two_six_b_hand, False)
        self.assertEqual(two_six_b_hand < two_six_a_hand, False)
        self.assertEqual(two_six_b_hand > two_six_a_hand, True)

    
class TestThreeOfAKind(unittest.TestCase):
    def test_equal(self):
        three_seven_a = []
        three_seven_a.append(Card(7,'c'))
        three_seven_a.append(Card(6,'c'))
        three_seven_a.append(Card(7,'d'))
        three_seven_a.append(Card(5,'h'))
        three_seven_a.append(Card(7,'s'))
        three_seven_a_hand = Hand.create_hand(three_seven_a)
        self.assertEqual(three_seven_a_hand.major_group, 4)

        three_seven_b = []
        three_seven_b.append(Card(7, 's'))
        three_seven_b.append(Card(6, 'c'))
        three_seven_b.append(Card(7, 'd'))
        three_seven_b.append(Card(5, 'c'))
        three_seven_b.append(Card(7, 'h'))
        three_seven_b_hand = Hand.create_hand(three_seven_b)

        self.assertEqual(three_seven_b_hand.major_group, 4)
        self.assertEqual(three_seven_a_hand, three_seven_b_hand)

    def test_lt_fourth_card(self):
        three_seven_a = []
        three_seven_a.append(Card(7,'c'))
        three_seven_a.append(Card(4,'c'))
        three_seven_a.append(Card(7,'d'))
        three_seven_a.append(Card(5,'h'))
        three_seven_a.append(Card(7,'s'))
        three_seven_a_hand = Hand.create_hand(three_seven_a)
        self.assertEqual(three_seven_a_hand.major_group, 4)

        three_seven_b = []
        three_seven_b.append(Card(7, 's'))
        three_seven_b.append(Card(6, 'c'))
        three_seven_b.append(Card(7, 'd'))
        three_seven_b.append(Card(5, 'c'))
        three_seven_b.append(Card(7, 'h'))
        three_seven_b_hand = Hand.create_hand(three_seven_b)

        self.assertEqual(three_seven_b_hand.major_group, 4)
        self.assertEqual(three_seven_a_hand < three_seven_b_hand, True)
        
    def test_lt_fifth_card(self):
        three_seven_a = []
        three_seven_a.append(Card(7,'c'))
        three_seven_a.append(Card(4,'c'))
        three_seven_a.append(Card(7,'d'))
        three_seven_a.append(Card(6,'h'))
        three_seven_a.append(Card(7,'s'))
        three_seven_a_hand = Hand.create_hand(three_seven_a)
        self.assertEqual(three_seven_a_hand.major_group, 4)

        three_seven_b = []
        three_seven_b.append(Card(7, 's'))
        three_seven_b.append(Card(6, 'c'))
        three_seven_b.append(Card(7, 'd'))
        three_seven_b.append(Card(5, 'c'))
        three_seven_b.append(Card(7, 'h'))
        three_seven_b_hand = Hand.create_hand(three_seven_b)

        self.assertEqual(three_seven_b_hand.major_group, 4)
        self.assertEqual(three_seven_a_hand < three_seven_b_hand, True)
       
    def test_lt_trips_card(self):
        three_six_a = []
        three_six_a.append(Card(6,'c'))
        three_six_a.append(Card(4,'c'))
        three_six_a.append(Card(6,'d'))
        three_six_a.append(Card(3,'h'))
        three_six_a.append(Card(6,'s'))
        three_six_a_hand = Hand.create_hand(three_six_a)
        self.assertEqual(three_six_a_hand.major_group, 4)

        three_seven_b = []
        three_seven_b.append(Card(7, 's'))
        three_seven_b.append(Card(6, 'c'))
        three_seven_b.append(Card(7, 'd'))
        three_seven_b.append(Card(5, 'c'))
        three_seven_b.append(Card(7, 'h'))
        three_seven_b_hand = Hand.create_hand(three_seven_b)

        self.assertEqual(three_seven_b_hand.major_group, 4)
        self.assertEqual(three_six_a_hand < three_seven_b_hand, True)

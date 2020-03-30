import card
class Hand():

    @staticmethod
    def create_hand(cards):
        cards = sorted(cards, key= lambda card:card.value)
        for b in cards:
            print(b.value)
        if cards[0].value == 1:
            max_card = cards[0]
        else:
            max_card = cards[4]
        is_straight = False
        is_flush = False
        major_group = -1
        value_map = {}
        suit_map = {'s': 0,'h' :0,'c':0,'d':0}
        return Hand.find_major_group(cards, value_map, suit_map, max_card)

    def __init__(self, num):
        self.major_group = num

    @staticmethod
    def find_is_flush(suit_map):
        for keys in suit_map:
            if suit_map[keys] == 5:
                return True
        return False

    @staticmethod
    def find_is_straight(cards, max_card):
        if max_card.value == 14: # if there is an ace, checking a straight's a bit different
            if cards[0].value == 2 and cards[1].value == 3 and cards[2].value == 4 and cards[3].value == 5:
                return True
        #normal way to check a straight with no ace 
        for i in range(len(cards)-1):
            if cards[i+1].value - cards[i].value != 1:
                return False
        return True

    @staticmethod
    def find_major_group(cards, value_map, suit_map, max_card):
        #populating our two maps
        for card in cards:
            if card.value in value_map:
                 value_map[card.value]+=1
            else:
                value_map[card.value] = 1
            suit_map[card.suit]+=1
        is_flush = Hand.find_is_flush(suit_map)
        is_straight = Hand.find_is_straight(cards, max_card) 
        if is_flush and is_straight and max_card.value == 1 and cards[4].value == 13:
            print('royal flush')
            o = RoyalFlush(10)
        elif is_flush and is_straight:
            print('straight flush')
            o = StraightFlush(9)
        elif 4 in value_map.values():
            print('four of a kind')
            o = FourOfAKind(8)
        elif 3 in value_map.values() and 2 in value_map.values():
            print('full house')
            o = FullHouse(7)
        elif is_flush:
            print('flush')
            o = Flush(6)
        elif is_straight:
            print('straight')
            o = Straight(5)
        elif 3 in value_map.values():
            print('three of a kind')
            o = ThreeOfAKind(4)
        elif len({k:v for k,v in value_map.items() if v==2}) is 2:
            print('two pair')
            o = TwoPair(3)
        elif 2 in value_map.values():
            print('one pair')
            o = Pair(2)
        else:
            print('high card')
            o = HighCard(1)

        o.cards = cards
        o.value_map = value_map
        o.suit_map = suit_map
        o.max_card = max_card
        o.is_straight = is_straight
        o.is_flush = is_flush

        return o

    def __lt__(self, other):
         return self.compare(other) < 0

    def __gt__(self, other):
        return self.compare(other) > 0

    def __eq__(self, other):
        if self.major_group != other.major_group:
            return False
        return self.compare(other) == 0

class RoyalFlush(Hand):
    def compare(self, other):
        return 0

class StraightFlush(Hand):
    def compare(self, other):
        if self.major_group != other.major_group:
            return self.major_group-other.major_group
        return self.max_card.value - other.max_card.value

class FourOfAKind(Hand):
    def compare(self, other):
        if self.major_group != other.major_group:
            return self.major_group-other.major_group
        print("custom")
        four_of_a_kind_a = [k for k,v in self.value_map.items() if v==4]
        four_of_a_kind_b = [k for k,v in other.value_map.items() if v==4]
        print(four_of_a_kind_a)
        print(four_of_a_kind_b)
        if four_of_a_kind_a == four_of_a_kind_b:
            kicker_a = [k for k,v in self.value_map.items() if v==1]
            kicker_b = [k for k,v in other.value_map.items() if v==1]
            print(kicker_a)
            print(kicker_b)
            return kicker_a[0] - kicker_b[0]
        else:
            return four_of_a_kind_a[0] - four_of_a_kind_b[0]

class FullHouse(Hand):
    def compare(self, other):
        if self.major_group != other.major_group:
            return self.major_group-other.major_group
        three_of_a_kind_a = [k for k,v in self.value_map.items() if v==3]
        three_of_a_kind_b = [k for k,v in other.value_map.items() if v==3]
        print(three_of_a_kind_a)
        print(three_of_a_kind_b)
        if three_of_a_kind_a == three_of_a_kind_b:
            kicker_a = [k for k,v in self.value_map.items() if v==2]
            kicker_b = [k for k,v in other.value_map.items() if v==2]
            print(kicker_a)
            print(kicker_b)
            return kicker_a[0] - kicker_b[0]
        else:
            return three_of_a_kind_a[0] - three_of_a_kind_b[0]
        print("custom")

class Flush(Hand):
    def compare(self, other):
        if self.major_group != other.major_group:
            return self.major_group-other.major_group
        for i in reversed(range(0,len(self.cards))):
            print(i)
            if self.cards[i].value != other.cards[i].value:
                return self.cards[i].value - other.cards[i].value
            else:
                continue
        #should never get hit
        return 0

class Straight(Hand):
    def compare(self, other):
        if self.major_group != other.major_group:
            return self.major_group-other.major_group
        return self.max_card.value - other.max_card.value

class ThreeOfAKind(Hand):
    def compare(self, other):
        if self.major_group != other.major_group:
            return self.major_group-other.major_group
        three_of_a_kind_a = [k for k,v in self.value_map.items() if v==3]
        three_of_a_kind_b = [k for k,v in other.value_map.items() if v==3]
        print(three_of_a_kind_a)
        print(three_of_a_kind_b)
        if three_of_a_kind_a[0] == three_of_a_kind_b[0]:
            one_of_a_kind_a = [k for k,v in self.value_map.items() if v==1]
            one_of_a_kind_a.sort()
            print(one_of_a_kind_a)
            one_of_a_kind_b = [k for k,v in other.value_map.items() if v==1]
            one_of_a_kind_b.sort()
            print(one_of_a_kind_b)
            if one_of_a_kind_a[1] == one_of_a_kind_b[1]:
                return one_of_a_kind_a[0] - one_of_a_kind_b[0]
            else:
                return one_of_a_kind_a[1] - one_of_a_kind_b[1]
        else:
            return three_of_a_kind_a[0]-three_of_a_kind_b[0]


class TwoPair(Hand):
    def compare(self, other):
        if self.major_group != other.major_group:
            return self.major_group-other.major_group
        two_of_a_kind_a = [k for k,v in self.value_map.items() if v==2]
        two_of_a_kind_a.sort()
        two_of_a_kind_b = [k for k,v in other.value_map.items() if v==2]
        two_of_a_kind_b.sort()
        print(two_of_a_kind_a)
        print(two_of_a_kind_b)
        if two_of_a_kind_a[1] == two_of_a_kind_b[1]:
            if two_of_a_kind_a[0] == two_of_a_kind_b[0]:
                one_of_a_kind_a = [k for k,v in self.value_map.items() if v==1]
                print(one_of_a_kind_a)
                one_of_a_kind_b = [k for k,v in other.value_map.items() if v==1]
                print(one_of_a_kind_b)
                return one_of_a_kind_a[0]-one_of_a_kind_b[0]
            else:
                return two_of_a_kind_a[0]-two_of_a_kind_b[0]
        else:
            return two_of_a_kind_a[1]-two_of_a_kind_b[1]

class Pair(Hand):
    def compare(self, other):
        pair_a = [k for k,v in self.value_map.items() if v==2]
        pair_b = [k for k,v in other.value_map.items() if v==2]
        print(pair_a)
        print(pair_b)
        if pair_a[0] == pair_b[0]:
            one_of_a_kind_a = [k for k,v in self.value_map.items() if v==1]
            one_of_a_kind_a.sort(reverse=True)
            print(one_of_a_kind_a)
            one_of_a_kind_b = [k for k,v in other.value_map.items() if v==1]
            one_of_a_kind_b.sort(reverse=True)
            print(one_of_a_kind_b)
            for i in range(0,len(one_of_a_kind_a)):
                if one_of_a_kind_a[i] != one_of_a_kind_b:
                    return one_of_a_kind_a[i] - one_of_a_kind_b[i]
                else:
                    continue
            if one_of_a_kind_a[1] == one_of_a_kind_b[1]:
                return one_of_a_kind_a[0] - one_of_a_kind_b[0]
            else:
                return one_of_a_kind_a[1] - one_of_a_kind_b[1]
        else:
            return pair_a[0]-pair_b[0]

class HighCard(Hand):
    def compare(self, other):
        print("custom")
        return True
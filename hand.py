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
        return find_major_group(cards, value_map, suit_map, max_card)

    def __init__(self, num, cards, value_map, suit_map, max_card, is_straight, is_flush):
        self.major_group = num
        self.cards = cards
        self.value_map = value_map
        self.suit_map = suit_map
        self.max_card = max_card
        self.is_straight = is_straight
        self.is_flush = is_flush

    @staticmethod
    def find_is_flush(suit_map):
        for keys in suit_map:
            if suit_map[keys] == 5:
                return True

    @staticmethod
    def find_is_straight(cards, max_card):
        if max_card.value == 1: # if there is an ace, checking a straight's a bit different
            if cards[1].value == 10 and cards[2].value == 11 and cards[3].value == 12 and cards[4].value == 13:
                return True
            else:
                for i in range(2,len(cards)-1):
                    if cards[i+1].value - cards[i].value != 1:
                        is_straight = False
                        return
        else:    #normal way to check a straight with no ace 
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
        is_flush = find_is_flush(suit_map)
        is_straight = find_is_straight(cards, max_card) 
        if is_flush and is_straight and max_card.value == 1 and cards[4].value == 13:
            print('royal flush')
            return RoyalFlush(10, cards, value_map, suit_map, max_card, is_straight, is_flush)
        elif is_flush and is_straight:
            print('straight flush')
            return StraightFlush(9, cards, value_map, suit_map, max_card, is_straight, is_flush)
        elif 4 in value_map.values():
            print('four of a kind')
            return FourOfAKind(8, cards, value_map, suit_map, max_card, is_straight, is_flush)
        elif 3 in value_map.values() and 2 in value_map.values():
            print('full house')
            return FullHouse(7, cards, value_map, suit_map, max_card, is_straight, is_flush)
        elif is_flush:
            print('flush')
            return Flush(6, cards, value_map, suit_map, max_card, is_straight, is_flush)
        elif is_straight:
            print('straight')
            return Straight(5, cards, value_map, suit_map, max_card, is_straight, is_flush)
        elif 3 in value_map.values():
            print('three of a kind')
            return ThreeOfAKind(4, cards, value_map, suit_map, max_card, is_straight, is_flush)
        elif len({k:v for k,v in value_map.items() if v==2}) is 2:
            print('two pair')
            return TwoPair(3, cards, value_map, suit_map, max_card, is_straight, is_flush)
        elif 2 in value_map.values():
            print('one pair')
            return Pair(2, cards, value_map, suit_map, max_card, is_straight, is_flush)
        else:
            print('high card')
            return HighCard(1, cards, value_map, suit_map, max_card, is_straight, is_flush)

    def __lt__(self, other):
        if type(self) != type(other):
            print("here")
            print(self.major_group)
            print(other.major_group)
            return self.major_group < other.major_group
        else:
            return self.compare(other)

class RoyalFlush(Hand):
    def compare(self, other):
        print("custom")
        return True

class StraightFlush(Hand):
    def compare(self, other):
        print("custom")
        return True

class FourOfAKind(Hand):
    def compare(self, other):
        print("custom")
        return True

class FullHouse(Hand):
    def compare(self, other):
        print("custom")
        return True

class Flush(Hand):
    def compare(self, other):
        print("custom")
        return True

class Straight(Hand):
    def compare(self, other):
        print("custom")
        return True

class ThreeOfAKind(Hand):
    def compare(self, other):
        print("custom")
        return True

class TwoPair(Hand):
    def compare(self, other):
        print("custom")
        return True

class Pair(Hand):
    def compare(self, other):
        print("custom")
        return True

class HighCard(Hand):
    def compare(self, other):
        print("custom")
        return True
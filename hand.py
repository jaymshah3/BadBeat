import card
class Hand():

    def __init__(self, cards):
        self.cards = sorted(cards, key= lambda card:card.value)
        for b in self.cards:
            print(b.value)
        if self.cards[0].value == 1:
            self.max_card = self.cards[0]
        else:
            self.max_card = self.cards[4]
        self.is_straight = False
        self.is_flush = False
        self.major_group = -1
        self.value_map = {}
        self.suit_map = {'s': 0,'h' :0,'c':0,'d':0}
        self.find_major_group()
        #for k,v in self.value_map.items():
         #   print(k)
          #  print(v)
        #for k,v in self.suit_map.items():
         #   print(k)
          #  print(v)


    def find_is_flush(self):
        for keys in self.suit_map:
            if self.suit_map[keys] == 5:
                self.is_flush = True

    def find_is_straight(self):
        if self.max_card.value == 1: # if there is an ace, checking a straight's a bit different
            if self.cards[1].value == 10 and self.cards[2].value == 11 and self.cards[3].value == 12 and self.cards[4].value == 13:
                self.is_straight = True
                return
            else:
                for i in range(2,len(self.cards)-1):
                    if self.cards[i+1].value - self.cards[i].value != 1:
                        self.is_straight = False
                        return
        else:    #normal way to check a straight with no ace 
            for i in range(len(self.cards)-1):
                if self.cards[i+1].value - self.cards[i].value != 1:
                    self.is_straight = False
                    return
        self.is_straight = True

    def find_major_group(self):
        #populating our two maps
        for card in self.cards:
            if card.value in self.value_map:
                 self.value_map[card.value]+=1
            else:
                self.value_map[card.value] = 1
            self.suit_map[card.suit]+=1
        self.find_is_flush()
        self.find_is_straight() 
        if self.is_flush and self.is_straight and self.max_card.value == 1 and self.cards[4].value == 13:
            print('royal flush')
            self.major_group = 10
        elif self.is_flush and self.is_straight:
            print('straight flush')
            self.major_group = 9
        elif 4 in self.value_map.values():
            print('four of a kind')
            self.major_group = 8
        elif 3 in self.value_map.values() and 2 in self.value_map.values():
            print('full house')
            self.major_group = 7
        elif self.is_flush:
            print('flush')
            self.major_group = 6
        elif self.is_straight:
            print('straight')
            self.major_group = 5
        elif 3 in self.value_map.values():
            print('three of a kind')
            self.major_group=4
        elif len({k:v for k,v in self.value_map.items() if v==2}) is 2:
            print('two pair')
            self.major_group = 3
        elif 2 in self.value_map.values():
            print('one pair')
            self.major_group = 2
        else:
            print('high card')
            self.major_group = 1

    def __lt__(self, hand):
        return self.major_group < hand.major_group
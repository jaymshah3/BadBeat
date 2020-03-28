import card
class Hand():
    def __init__(self, cards):
        self.cards = sorted(cards, key= lambda card:card.value)
        self.max_card = cards[4]
        self.is_straight = False
        self.is_flush = False
        #self.major_group = find_major_group()
        self.value_map = {}
        self.suit_map = {'s': 0,'h' :0,'c':0,'d':0}
        
        def find_is_flush(self):
            for keys in self.suitMap:
                if self.suitMap[keys] == 4:
                    self.is_flush = True

        def find_is_straight(self):
            for i in range(len(self.cards)-1):
                if self.cards[i].value > self.cards[i+1].value:
                    self.is_straight = False


        def find_major_group(self):
            for card in self.cards:
                if card.value in self.value_map:
                    self.value_map[card.val]+=1
                else:
                    self.value_map[card.value] = 1
                self.suitMap[card.suit]+=1
            return 1

    

            
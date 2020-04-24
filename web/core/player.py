class Player():

    def __init__(self, name, bank, id_num):
        self.name = name
        self.bank = bank
        self.id_num = id_num
        self.current_contribution = None
        self.cards = None
        self.invested = 0
        self.result = 0
        self.is_fold = False

    def set_cards(self, cards):
        self.cards = sorted(cards, key= lambda card:card.value)

    def __str__(self):
        return self.name + "[" + str(self.id_num) + "]"

    # this method will be called if a 
    # player chooses call as the amount var will be table's highest contribution
    def bet(self,amount):
        if self.current_contribution is None:
            self.current_contribution = 0
        if amount + self.current_contribution > self.bank:
            raise ValueError("Insufficient Funds")
        self.current_contribution += amount
        self.invested += amount
    
    def apply_result(self):
        self.bank += self.result

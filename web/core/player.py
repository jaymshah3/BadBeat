class Player():

    def __init__(self, name, bank, id_num):
        self.name = name
        self.bank = bank
        self.id_num = id_num
        self.current_contribution = None
        self.cards = None

    def set_cards(self, cards):
        self.cards = sorted(cards, key= lambda card:card.value)

    def __str__(self):
        return self.name + "[" + str(self.id_num) + "]"

    # this method will be called if a 
    # player chooses call as the amount var will be table's highest contribution
    def bet(self,amount):
        if amount + self.current_contribution > self.bank:
            raise ValueError("Insufficient Funds")
        if self.current_contribution is None:
            self.current_contribution = 0
        self.current_contribution += amount
    
    def withdraw_bank(self):
        if self.bank - self.current_contribution < 0:
            raise ValueError("Insuffient Funds")
        self.bank -= self.current_contribution

    

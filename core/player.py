class Player():

    def __init__(self, name, bank, id_num, cards):
        self.name = name
        self.bank = bank
        self.id_num = id_num
        self.cards = sorted(cards, key= lambda card:card.value)
        self.current_contribution = 0

    # this method will be called if a 
    # player chooses call as the amount var will be table's highest contribution
    def bet(self,amount):
        if amount + self.current_contribution > self.bank:
            raise ValueError("Insufficient Funds")
        self.current_contribution += amount
    
    def withdraw_bank(self):
        if self.bank - self.current_contribution < 0:
            raise ValueError("Insuffient Funds")
        self.bank -= self.current_contribution

    

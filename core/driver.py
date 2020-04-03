from deck import Deck
from poker_round import Round

class Driver():
    def __init__(self, players):
        self.players = players
        self.pot = 0
        self.current_round_pot = 0
        self.deck = Deck()
        self.highest_current_contribution = 0

    # one round
    def run_round(self, start_index):
        player_round = Round(self.players, start_index)
        # deal cards
        # run betting loop
        # flop
        # run betting loop
        # turn
        # run betting loop
        # river
        # run betting loop
        # assign winner(s)
        # assign winnings

    def run_betting_loop(self, player_round):
        initiator = player_round.start_node
        next_player = player_round.get_next_player()

        while next_player.player != initiator:
            # get action for next_player
            # call method on that player
            # if required, change initiator (local variable) 
            # next_player = player_round.get_next_player()
            pass

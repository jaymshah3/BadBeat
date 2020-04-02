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

    def run_betting_loop(self, player_round):
        next_player = player_round.get_next_player()

        while next_player.player != player_round.start_node.player:
            # get action for next_player
            # call method on that player
            # if required, 
            # next_player = player_round.get_next_player()
            pass

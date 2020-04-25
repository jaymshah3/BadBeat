from core.player import Player
from core.deck import Deck
from enum import Enum

class GameState(Enum):
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    WINNER = 5

class GameDataService():
    def __init__(self):
        self.players = []
        self.heads_up = False
        self.pot = 0
        self.current_round_pot = 0
        self.deck = Deck()
        self.highest_current_contribution = 0
        self.clients = {}
        self.community_cards = []
        self.player_round = None
        self.small_blind_amount = 0
        self.big_blind_amount = 0
        self.current_player = None
        self.game_state = GameState.PREFLOP
        self.prev_high_rase = 0
        self.number_of_all_ins = 0
        self.aggressors = []

    def add_player(self,name,id_num,bank):
        self.players.append(Player(name,bank,id_num))

    def remove_player(self,id_num):
        for i in range(0,len(self.players)):
            if self.players[i].id_num == id_num:
                self.players.pop(i)

    def get_players(self):
        return self.players
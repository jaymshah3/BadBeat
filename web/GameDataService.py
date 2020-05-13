from core.player import Player
from core.deck import Deck
from enum import Enum

room_to_gds = None
def init_gds():
    global room_to_gds
    room_to_gds = GameDataService()


class GameDataService():
    def __init__(self): 
        self.gds_map = {}

    def add_game_data(self,room_id,game_data):
        if room_id not in self.gds_map.keys():
            self.gds_map[room_id] = game_data
        else:
            raise ValueError("duplicate room_ids provided")
    
    def remove_game_data(self,room_id):
        if room_id not in self.gds_map.keys():
            raise ValueError("room_id does not exist")
        else:
            del self.gds_map[room_id]

    def get_game_data(self,room_id):
        if room_id not in self.gds_map.keys():
            raise ValueError("room_id does not exist")
        else:
            return self.gds_map[room_id]

class GameState(Enum):
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    WINNER = 5

class GameData():
    def __init__(self,room_owner_sid,small_blind,big_blind):
        self.players = []
        self.heads_up = False
        self.pot = 0
        self.current_round_pot = 0
        self.deck = Deck()
        self.highest_current_contribution = 0
        self.clients = {}
        self.community_cards = []
        self.player_round = None
        self.small_blind_amount = small_blind
        self.big_blind_amount = big_blind
        self.current_player = None
        self.game_state = GameState.PREFLOP
        self.prev_high_rase = 0
        self.number_of_all_ins = 0
        self.aggressors = []
        self.big_blind_action = False
        self.room_owner = room_owner_sid
        self.active_clients = 0
        self.num_of_hands = 0

    def add_player(self,name,id_num,bank,sid):
        self.players.append(Player(name,bank,id_num))
        self.clients[name] = sid
        self.active_clients += 1

    def remove_player(self,id_num,username):
        for i in range(0,len(self.players)):
            if self.players[i].id_num == id_num:
                self.players.pop(i)
        del self.clients[username]
        self.active_clients -= 1

    def get_players(self):
        return self.players

    def reset(self):
        self.heads_up = False
        self.pot = 0
        self.current_round_pot = 0
        self.deck = Deck()
        self.highest_current_contribution = 0
        self.community_cards = []
        self.current_player = None
        self.game_state = GameState.PREFLOP
        self.prev_high_rase = 0
        self.number_of_all_ins = 0
        self.big_blind_action = False
        self.aggressors = []

class PlayerNode():
    def __init__(self, player, next_node=None):
        self.next_node = next_node
        self.is_fold= False
        self.player = player
        self.is_all_in= False
        self.is_standing_up = False
        self.is_in_next_hand = False

class Round():
    
    def __init__(self, players, small_blind=0):
        self.MAX_VALUE = 10
        self.players = players
        self.length_active = len(players)
        self.num_nodes = len(players)
        first_node = PlayerNode(players[0])
        curr_node = first_node
        if small_blind == 0:
            self.current_node = first_node
            self.small_blind = self.current_node

        for i in range(1, len(players)):
            next_node = PlayerNode(players[i])
            curr_node.next_node = next_node
            curr_node = next_node
            if small_blind == i:
                self.current_node = curr_node
                self.small_blind = self.current_node

        curr_node.next_node = first_node
        self.init_blinds()
    def remove_current(self):
        self.current_node.is_fold = True
        self.current_node.player.is_fold = True
        self.length_active -= 1
       
    def all_in_current_node(self):
        self.current_node.is_all_in = True
        
    def get_next_player(self):
        next_node = self.current_node.next_node
        while next_node.is_fold or next_node.is_all_in or next_node.is_in_next_hand:
            next_node = next_node.next_node
        self.current_node = next_node
        return next_node

    def get_current_players(self):
        current_players = []
        current_players.append(self.current_node.player)
        pointer = self.current_node.next_node
        while pointer != self.current_node:
            if not pointer.is_fold and not pointer.is_standing_up and not pointer.is_in_next_hand:
                current_players.append(pointer.player)
            pointer = pointer.next_node
        return current_players

    def remove_player_node(self,player):
        if self.num_nodes == 1:
            raise ValueError("Only one node")
        prev = None
        to_remove = self.small_blind
        while to_remove.player != player:
            prev = to_remove
            to_remove = to_remove.next_node
        prev.next_node = to_remove.next_node
        to_remove.next_node = None
        to_remove = None 
        self.num_nodes -= 1

    def add_player_node(self,player):
        if self.num_nodes == self.MAX_VALUE:
            raise ValueError("Max players")
        else:
            pointer = self.small_blind
            while pointer.next_node != self.small_blind:
                pointer = pointer.next_node
            added_player = PlayerNode(player)
            added_player.is_in_next_hand = True
            pointer.next_node = added_player
            added_player.next_node = self.small_blind
            self.num_nodes += 1
    
    def toggle_node_stand_up(self,name):
        pointer = self.small_blind
        while pointer.player.name != name:
            pointer = pointer.next_node
        pointer.is_standing_up = not pointer.is_standing_up        

    def remove_busted_players(self):
        for p in self.players:
            if p.bank == 0:
                self.remove_player_node(p)
                self.players.remove(p)

    def init_blinds(self):
        self.big_blind = self.small_blind.next_node
        self.current_node = self.big_blind.next_node
        while self.current_node.is_standing_up:
            self.current_node = self.current_node.next_node


    def set_next_small_blind(self):
        pointer = self.small_blind.next_node
        while not pointer.player.bank == 0:
            pointer = pointer.next_node
        if pointer == self.small_blind:
            raise ValueError("Only one player left")
        self.small_blind = pointer

    def reset_nodes(self):
        self.players = []
        pointer = self.small_blind.next_node
        while pointer != self.small_blind:
            pointer.is_fold = False
            pointer.is_in_next_hand = False
            pointer.is_all_in = False
            pointer.player.reset_player()
            self.players.append(pointer.player)
            pointer = pointer.next_node
        self.players.append(pointer.player)
        pointer.is_fold = False
        pointer.is_in_next_hand = False
        pointer.is_all_in = False
        
    def start_new_hand(self):
        self.set_next_small_blind()
        self.remove_busted_players()
        self.init_blinds()
        self.reset_nodes()
        self.length = len(self.players)
        self.length_active = self.length
        self.num_nodes = self.length
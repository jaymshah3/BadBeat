class PlayerNode():
    def __init__(self, player, next_node=None):
        self.next_node = next_node
        self.isFold = False
        self.player = player
        self.isAllIn= False

class Round():
    def __init__(self, players, small_blind=0):
        self.players = players
        self.length = len(players)
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
        self.big_blind = self.small_blind.next_node
        if len(players) > 2:
            self.current_node = self.big_blind.next_node
        else:
            self.current_node = self.small_blind
    def remove_current(self):
        self.current_node.isFold = True
        self.length -= 1
       
    def get_next_player(self):
        next_node = self.current_node.next_node
        while next_node.isFold:
            next_node = next_node.next_node
        self.current_node = next_node
        return next_node

    def get_current_players(self):
        current_players = []
        current_players.append(self.current_node.player)
        pointer = self.current_node.next_node
        while pointer != self.current_node:
            if not pointer.isFold:
                current_players.append(pointer.player)
            pointer = pointer.next_node
        return current_players
class PlayerNode():
    def __init__(self, player, next_node=None):
        self.next_node = next_node
        self.skip = False
        self.player = player

class Round():
    def __init__(self, players, start_index=0):
        self.players = players
        self.length = len(players)
        first_node = PlayerNode(players[0])
        curr_node = first_node
        if start_index == 0:
            self.current_node = first_node
            self.start_node = self.current_node

        for i in range(1, len(players)):
            next_node = PlayerNode(players[i])
            curr_node.next_node = next_node
            curr_node = next_node
            if start_index == i:
                self.current_node = curr_node
                self.start_node = self.current_node

        curr_node.next_node = first_node

    def remove_current(self):
        if self.current_node == self.start_node:
            next_node = self.current_node.next_node
            while next_node.skip:
                next_node = next_node.next_node
            self.start_node = next_node
        self.current_node.skip = True
        self.length -= 1
       
    def get_next_player(self):
        next_node = self.current_node.next_node
        while next_node.skip:
            next_node = next_node.next_node
        self.current_node = next_node
        return next_node

    def get_current_players(self):
        pointer = self.current_node.next_node
        current_players = []
        while pointer != self.current_node:
            if not pointer.skip:
                current_players.append(pointer.player)
            pointer = pointer.next_node
        return current_players
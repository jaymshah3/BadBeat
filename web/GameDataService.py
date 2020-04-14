from core.player import Player
class GameDataService():
    def __init__(self):
        self.players = []

    def add_player(self,name,id_num,bank):
        self.players.append(Player(name,bank,id_num))

    def remove_player(self,id_num):
        for i in range(0,len(self.players)):
            if self.players[i].id_num == id_num:
                self.players.pop(i)

    def get_players(self):
        return self.players
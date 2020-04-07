from deck import Deck
from poker_round import Round
from player import Player
import itertools

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
        self.deck.shuffle()
        winner = []
        # deal cards
        # run betting loop
         # withdraw bank for each player
        run_betting_loop(player_round)
        for player in player_round.get_current_players:
            player.withdraw_bank
            player.current_contribution = 0
        if player_round.length == 1:
            winner.append(player_round.get_current_players())
            print("Winner: " + winner[0].name)
            assign_winnings(winner)
            return
        self.pot += self.current_round_pot
        self.current_round_pot = 0
        # flop
        # run betting loop
        # withdraw bank for each player
        run_betting_loop(player_round)
        for player in player_round.get_current_players:
            player.withdraw_bank
            player.current_contribution = 0
        if player_round.length == 1:
            winner.append(player_round.get_current_players())
            print("Winner: " + winner[0].name)
            assign_winnings(winner)
            return
        self.pot += self.current_round_pot
        self.current_round_pot = 0

        # turn
        # run betting loop
        # withdraw bank for each player
        run_betting_loop(player_round)
        for player in player_round.get_current_players:
            player.withdraw_bank
            player.current_contribution = 0
        if player_round.length == 1:
            winner.append(player_round.get_current_players())
            print("Winner: " + winner[0].name)
            self.assign_winnings(winner)
            return
        self.pot += self.current_round_pot
        self.current_round_pot = 0
        # river
        # run betting loop
        # withdraw bank for each player
        run_betting_loop(player_round)
        for player in self.players:
            player.withdraw_bank
            player.current_contribution = 0
        self.pot += self.current_round_pot
        self.current_round_pot = 0
        winner = self.find_winners(player_round.get_current_players)
        self.assign_winnings(winner)
        # assign winner(s)
        # assign winnings

    def run_betting_loop(self, player_round):
        initiator = player_round.start_node
        curr_player_obj = player_round.get_next_player()

        while curr_player_obj != initiator:
            curr_player = curr_player_obj.player
            options = self.get_options(curr_player)

            # **** get action for next_player ****
            # will fill out below vars

            player_selection = None
            amount = None
            if player_selection == "raise":
                curr_player.bet(amount)
                initiator = curr_player_obj
                self.highest_current_contribution = amount + curr_player.current_contribution
            elif player_selection == "call":
                curr_player.bet(amount)
            elif player_selection == "fold":
                player_round.remove_current()
            self.current_round_pot += curr_player.current_contribution
            curr_player_obj = player_round.get_next_player()

        self.highest_current_contribution = 0

    def get_options(self, player):
        options = []
        options.append("fold")
        if (self.highest_current_contribution == 0 or 
        player.current_contribution < self.highest_current_contribution):
            options.append("raise")
        if player.current_contribution < self.highest_current_contribution:
            options.append("call")
        if self.highest_current_contribution == 0:
           options.append("check")
        return options

    def find_winners(self, players, middle_cards):
        best_hands = [self.get_player_winning_hand(x.cards, middle_cards) for x in players]
        winning_players = [players[0]]
        winning_hands = [best_hands[0]]

        for i in range(1, len(best_hands)):
            if best_hands[i] < winning_hands[0]:
                continue
            elif best_hands[i] > winning_hands[0]:
                winning_hands = [best_hands[i]]
                winning_players = [players[i]]
            else:
                winning_hands.append(best_hands[i])
                winning_players.append(players[i])

        return winning_players

    def get_player_winning_hand(self, player_cards, middle_cards):
        all_cards = player_cards[:]
        all_cards.extend(middle_cards)
        all_hands = sorted(itertools.combinations(all_cards, 5), reverse=True)
        return all_hands[0]

    def deal_cards(self):
        self.deck.shuffle()
        for i in range(0, len(self.players)):
            pair = [self.deck.get_top_card(), self.deck.get_top_card()]
            self.players[i].set_cards(pair)  

    def assign_winnings(self, winner):
        if len(winner) == 1:
            winner[0].bank += self.pot
        else:
            per_player_winnings = self.pot/len(winner)
            for player in winner:
                player.bank +=per_player_winnings
        self.pot = 0
        
def main():
    one = Player("Jay", 1000, 1)
    two = Player("Aditya", 1000, 2)
    three = Player("Sri", 1000, 3)
    players = [one, two, three]
    driver = Driver(players)
    while len(driver.players) > 1:
        driver.deal_cards()
        driver.run_round()
        for p in driver.players:
            # ask if still play
            stay = None
            if not stay:
                driver.players.remove(p)


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
        # deal cards
        # run betting loop
        # withdraw bank for each player
        # flop
        # run betting loop
        # withdraw bank for each player
        # turn
        # run betting loop
        # withdraw bank for each player
        # river
        # run betting loop
        # withdraw bank for each player
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
        
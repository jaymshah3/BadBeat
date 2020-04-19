from core.deck import Deck
from core.poker_round import Round
from core.player import Player
from core.hand import Hand
from enum import Enum
from random import randint
import itertools
try:
    from __main__ import socketio, join_room, leave_room, send, emit
except ImportError:
    from flask_socketio import socketio, join_room, leave_room, send, emit

class GameState(Enum):
    PREFLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    WINNER = 5

players = []
pot = 0
current_round_pot = 0
deck = Deck()
highest_current_contribution = 0
clients = {}
community_cards = []
player_round = None
small_blind_amount = 0
big_blind_amount = 0
current_player = None
game_state = GameState.PREFLOP
prev_high_rase = 0
aggressors = []


@socketio.on('fold')
def handle_fold(data):
    global current_player
    global player_round
    global game_state
    global aggressors
    if data['username'] is not current_player.name:
        pass
        #error
    emit('player folded', {data}, broadcast=True)
    player_round.remove_current()
    if current_player == aggressors[-1]:
        if not len(aggressors) == 1:
            aggressors.pop()
    current_player = player_round.get_next_player().player
    get_options()

@socketio.on('call')
def handle_call(data):
    global current_player
    global player_round
    global game_state
    global current_round_pot
    if data['username'] is not current_player.name:
        pass
        #error
    current_player.bet(data['amount'])
    current_round_pot += current_player.current_contribution
    broadcast_pot(current_round_pot)
    emit('player called', {data}, broadcast=True)
    current_player = player_round.get_next_player().player
    get_options()
        
@socketio.on('raise')
def handle_raise(data):
    global current_player
    global player_round
    global game_state
    global current_round_pot
    global highest_current_contribution
    global prev_high_raise
    global aggressors
    if data['username'] is not current_player.name:
        pass
        #error
    aggressors.append(current_player)
    prev_high_raise = highest_current_contribution
    current_player.bet(data['amount'])
    highest_current_contribution = current_player.current_contribution 
    # we already added data['amount'] to current_player.current_contribution
    current_round_pot += current_player.current_contribution
    broadcast_pot(current_round_pot)
    emit('highest_contribution', {'amount': highest_current_contribution})
    emit('player raised', {data}, broadcast=True)
    current_player = player_round.get_next_player().player
    get_options()

def run_next_game_state(next_game_state):
    global highest_current_contribution
    global pot
    global current_round_pot
    global player_round
    global clients
    for player in players:
        emit('withdraw', {'amount': player.current_contribution},
        room=clients[player.name])
        player.current_contribution = None
    highest_current_contribution = 0
    pot += current_round_pot
    broadcast_pot(pot)
    current_round_pot = 0
    if player_round.length == 1:
        distribute()
    else:
        if next_game_state == GameState.FLOP:
            flop()
        elif next_game_state ==GameState.TURN:
            turn()
        elif next_game_state == GameState.RIVER:
            river()
        else:
            distribute()

def preflop(given_players,given_clients,small_blind_amt,big_blind_amt):
    global players
    global clients
    global player_round
    global current_player
    global small_blind_amount
    global big_blind_amount
    global highest_current_contribution
    players = given_players
    clients = given_clients
    small_blind = 0
    player_round = Round(players,small_blind)
    small_blind_amount = small_blind_amt
    big_blind_amount = big_blind_amt
    highest_current_contribution = big_blind_amount
    player_round.small_blind.player.bet(small_blind_amount)
    player_round.big_blind.player.bet(big_blind_amount)
    current_player = player_round.current_node.player
    aggressors.append(player_round.big_blind.player)
    deal_cards()
    get_options() 

def flop():
    global community_cards
    global deck
    global player_round
    global current_player
    community_cards = [
            deck.get_top_card(),
            deck.get_top_card(),
            deck.get_top_card()
        ]
    broadcast_community_cards()
    for player in player_round.get_current_players():
        current_hand_strength(player,community_cards)
    current_player_node= player_round.small_blind
    while current_player_node.isFold:
        current_player_node = current_player.next_node
    current_player = current_player_node.player
    get_options()

def turn():
    global community_cards
    global deck
    global player_round
    global current_player
    community_cards.append(deck.get_top_card())
    broadcast_community_cards()
    for player in player_round.get_current_players():
        current_hand_strength(player,community_cards)
    current_player_node= player_round.small_blind
    while current_player_node.isFold:
        current_player_node = current_player.next_node
    current_player = current_player_node.player
    get_options()

def river():
    global community_cards
    global deck
    global player_round
    global current_player
    community_cards.append(deck.get_top_card())
    broadcast_community_cards()
    for player in player_round.get_current_players():
        current_hand_strength(player,community_cards)
    current_player_node= player_round.small_blind
    while current_player_node.isFold:
        current_player_node = current_player.next_node
    current_player = current_player_node.player
    get_options()

def find_winners(all_players):
    global community_cards
    players = all_players
    middle_cards = community_cards
    best_hands = [get_player_winning_hand(x.cards, middle_cards) for x in players]
    winning_players = [players[0]]
    winning_hands = [best_hands[0]]
    emit('best hand', {'best_hand': str(best_hands[0])},room=clients[players[0].name])
    print(str(players[0]) + " has a " + str(best_hands[0]))
    for i in range(1, len(best_hands)):
        print(str(players[i]) + " has a " + str(best_hands[i]))
        emit('best hand', {'best_hand': str(best_hands[i])},room=clients[players[i].name])
        if best_hands[i] < winning_hands[0]:
            continue
        elif best_hands[i] > winning_hands[0]:
            winning_hands = [best_hands[i]]
            winning_players = [players[i]]
        else:
            winning_hands.append(best_hands[i])
            winning_players.append(players[i])

    return winning_players
    # call next_game() ? next_game() can then reset all global vars, 
    # exclude players who indicated to "stand up", and call preflop()
    # with remaning players? Lets sync and discuss.

def distribute():
    global players
    distrubute_players = players
    calc_pot = 0
    for p in distrubute_players:
        p.result= -p.invested # invested money is lost originally

    # while there are still players with money
    # we build a side-pot matching the lowest stack and distribute money to winners
    while len(distrubute_players)>1 :
        min_stack = min([p.invested for p in distrubute_players])
        calc_pot += min_stack * len(distrubute_players)
        for p in distrubute_players:
            p.invested -= min_stack
        winners = find_winners(p for p in distrubute_players if not p.isFold)
        if len(winners) == 1:
            winners[0].result += calc_pot
        else:
            per_player_winnings = pot/len(winners)
            if per_player_winnings.is_integer():            
                for p in winners:
                    p.result += per_player_winnings
            else:
                per_player_winnings = int(per_player_winnings)
                extra_chip_winner = [p for p in aggressors.reverse() if not p.isFold]
                for p in winners:
                    if p == extra_chip_winner[0]:
                        p.result +=1
                    p.result += per_player_winnings

        distrubute_players = [p for p in distrubute_players if p.invested > 0]
        calc_pot = 0
    if len(players) == 1:
        p = distrubute_players[0]
        # return uncalled bet
        p.result += p.invested
    apply_result_to_all()

def apply_result_to_all():
    global players
    for p in players:
        p.apply_result()

def current_hand_strength(player, community_cards):
    best_hand = get_player_winning_hand(player.cards,community_cards)
    emit('current hand',{'hand': str(best_hand)},room=clients[player.name])

def get_player_winning_hand(player_cards, middle_cards):
    all_cards = player_cards[:]
    all_cards.extend(middle_cards)
    all_hands = sorted([Hand.create_hand(x) for x in itertools.combinations(all_cards, 5)], reverse=True)
    return all_hands[0]

def get_options():
    global current_player
    global clients
    global player_round
    global highest_current_contribution
    global game_state
    if player_round.length == 1:
        distribute()
    else:
        if ((current_player.current_contribution is not None) 
        and (current_player.current_contribution == highest_current_contribution) 
        and not (player_round.big_blind.player == current_player and 
        game_state == GameState.PREFLOP)):
            if game_state != GameState.WINNER:
                game_state = GameState(game_state.value+1)
            run_next_game_state(game_state)
        else:
            options = []
            options.append("fold")
            if (current_player.current_contribution is None 
            or highest_current_contribution == 0 or 
            current_player.current_contribution < highest_current_contribution):
                options.append("raise")
            if current_player.current_contribution is None or current_player.current_contribution < highest_current_contribution:
                options.append("call")
            if highest_current_contribution == 0:
                options.append("check")
            
            emit('options for player', {'options': options, 
            'highest_contribution': highest_current_contribution},
             room=clients[current_player.name])

def deal_cards():
    global deck
    global players
    deck.shuffle()
    for i in range(0, len(players)):
        pair = [deck.get_top_card(), deck.get_top_card()]
        players[i].set_cards(pair)
        print(str(players[i]) + ": " + str(pair[0]) + ", " + str(pair[1]))
        emit('dealt cards', {'cards': [{'value':pair[0].val, 'suit': pair[0].suit},
            {'value':pair[1].val, 'suit': pair[1].suit}]},
            room=clients[players[i].name]) 



def broadcast_pot(amount):
    emit('pot update', {'pot': amount}, broadcast=True)

def broadcast_community_cards():
    global community_cards
    emit('community cards', {'community_cards': community_cards}, broadcast=True)
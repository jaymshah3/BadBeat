from core.deck import Deck
from core.poker_round import Round
from core.player import Player
from core.hand import Hand
from enum import Enum
import GameDataService

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
heads_up = False
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
number_of_all_ins = 0
big_blind_action = False
aggressors = []
room_to_gds = GameDataService.room_to_gds

@socketio.on('fold')
def handle_fold(data):
    global room_to_gds
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    current_player = game_data.current_player
    print("FOLD")
    if data['username'] is not current_player.name:
        pass
        #error
    game_data.player_round.remove_current()
    data['action'] = 'fold'
    emit('player action', data, room=room)
    game_data.current_player = game_data.player_round.get_next_player().player
    get_options(room)

@socketio.on('call')
def handle_call(data):
    print("CALL")
    global room_to_gds
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    if data['username'] is not game_data.current_player.name:
        pass
        #error
    if (game_data.game_state == GameState.PREFLOP 
    and game_data.current_player == game_data.player_round.big_blind.player):
        game_data.big_blind_action = True
    print(data['amount'])
    game_data.current_player.bet(data['amount'])
    emit('withdraw', {'username':current_player.name, 'amount':data['amount']},
        broadcast=True)
    if game_data.current_player.bank == game_data.current_player.invested:
        game_data.number_of_all_ins+=1
        game_data.player_round.all_in_current_node()
    game_data.current_round_pot += data['amount']
    broadcast_pot(current_round_pot + pot,room)
    data['action'] = 'call'
    data['currentContribution'] = game_data.current_player.current_contribution
    emit('player action', data, room=room)
    print(current_player.name)
    print(player_round.get_next_player().player)
    game_data.current_player = game_data.player_round.current_node.player
    get_options(room)
        
@socketio.on('raise')
def handle_raise(data):
    print("RAISE")
    global room_to_gds
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    if data['username'] is not game_data.current_player.name:
        pass
        #error
    if (game_data.game_state == GameState.PREFLOP 
    and game_data.current_player == game_data.player_round.big_blind.player):
        game_data.big_blind_action = True
    game_data.aggressors.append(current_player)
    game_data.prev_high_raise = highest_current_contribution
    # on raise, the amount is the final amount the player wants to be "in" for,
    # not how much more they want to add to there contribution.
    if game_data.current_player.current_contribution is not None:
        print('raised from not none')
        print(data['amount'])
        game_data.current_round_pot += data['amount']-game_data.current_player.current_contribution
        emit('withdraw', {'username':gme_data.current_player.name, 
        'amount': data['amount']-game_data.current_player.current_contribution},
        broadcast=True)
        game_data.current_player.bet(data['amount']-current_player.current_contribution)
    else:
        game_data.current_player.bet(data['amount'])
        game_data.current_round_pot += data['amount']
        emit('withdraw', {'username':game_data.current_player.name, 
        'amount': game_data.current_player.current_contribution},
        room=room)
    game_data.highest_current_contribution = game_data.current_player.current_contribution 
    # we already added data['amount'] to current_player.current_contribution
    if game_data.current_player.bank == game_data.current_player.invested:
        game_data.number_of_all_ins+=1
        game_data.player_round.all_in_current_node()
    broadcast_pot(current_round_pot + pot,room)
    data['action'] = 'raise'
    data['currentContribution'] = game_data.current_player.current_contribution
    emit('highest contribution', {'highest_contribution': game_data.highest_current_contribution}, room=room)
    emit('player action', data, room=room)
    game_data.current_player = game_data.player_round.get_next_player().player
    get_options(room)

def run_next_game_state(room):
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    print('RUN_NEXT_GAME_STATE')
    print(game_data.game_state.value)
    next_game_state = game_data.game_state
    for i in range(0,len(game_data.players)):
        # emit('withdraw', {'amount': player.current_contribution},
        # room=clients[player.name])
        game_data.players[i].current_contribution = None
    emit('reset current contribution', {}, broadcast=True)
    game_data.highest_current_contribution = 0
    game_data.pot += game_data.current_round_pot
    broadcast_pot(pot,room)
    game_data.current_round_pot = 0
    if game_data.player_round.length == 1:
        distribute(room)
    else:
        if next_game_state != GameState.WINNER:
            run_street(heads_up,room)
        else:
            distribute(room)

def preflop(room,given_players,given_clients,small_blind_amt,big_blind_amt):
    print('PREFLOP')
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    game_data.player_round = Round(given_players,0)
    game_data.highest_current_contribution = big_blind_amount
    game_data.player_round.small_blind.player.bet(small_blind_amount)
    emit('withdraw', {'username':game_data.player_round.small_blind.player.name,
     'amount': game_data.player_round.small_blind.player.current_contribution},
        broadcast=True)
    if game_data.player_round.small_blind.player.invested == game_data.player_round.small_blind.player.bank:
        print('incrementing all_ins')
        game_data.player_round.small_blind.isAllIn = True
        game_data.number_of_all_ins+=1
    emit('player action', {
        'username': game_data.player_round.small_blind.player.name,
        'amount': game_data.small_blind_amount,
        'action': 'small blind',
        'currentContribution': small_blind_amount
    }, broadcast=True)
    game_data.player_round.big_blind.player.bet(big_blind_amount)
    emit('withdraw', {'username':game_data.player_round.big_blind.player.name,
     'amount': game_data.player_round.big_blind.player.current_contribution},
        broadcast=True)
    if game_data.player_round.big_blind.player.invested == game_data.player_round.big_blind.player.bank:
        print('incrementing all_ins')
        game_data.player_round.big_blind.isAllIn = True
        game_data.number_of_all_ins+=1
    game_data.current_round_pot += game_data.player_round.small_blind.player.current_contribution
    game_data.current_round_pot += game_data.player_round.big_blind.player.current_contribution
    game_data.current_player = game_data.player_round.current_node.player
    game_data.aggressors.append(game_data.player_round.big_blind.player)
    if len(game_data.players) == 2:
        game_data.heads_up = True
    emit('player action', {
        'username': game_data.player_round.big_blind.player.name,
        'amount': game_data.big_blind_amount,
        'action': 'big blind',
        'currentContribution': game_data.big_blind_amount
    }, broadcast=True)
    broadcast_pot(game_data.current_round_pot,room)
    emit('highest contribution', {'highest_contribution': big_blind_amount}, broadcast=True)
    deal_cards(room)
    get_options(room) 
def run_street(heads_up,room):
    print('Game State:' + str(game_state))
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    if game_data.game_state == GameState.FLOP:
        game_data.community_cards = [
            game_data.deck.get_top_card(),
            game_data.deck.get_top_card(),
            game_data.deck.get_top_card()
        ]
    else:
        game_data.community_cards.append(game_data.deck.get_top_card())
    broadcast_community_cards(room)
    for player in game_data.player_round.get_current_players():
        current_hand_strength(player,community_cards)
    if game_data.number_of_all_ins >= game_data.player_round.length-1:
        game_data.game_state = GameState(game_data.game_state.value+1)
        run_next_game_state(game_state)
    else:
        if game_data.heads_up:
            current_player_node = game_data.player_round.big_blind
        else:
            current_player_node= game_data.player_round.small_blind
            while current_player_node.is_fold:
                current_player_node = current_player.next_node
        game_data.current_player = current_player_node.player
        game_data.player_round.current_node = current_player_node
        get_options(room)

def find_winners(all_players,room):
    global room_to_gds
    game_data = room_to_gds.get_room(room)
    players = list(all_players)
    print("FIND_WINNERS")
    middle_cards = game_data.community_cards
    best_hands = [get_player_winning_hand(x.cards, middle_cards) for x in players]
    winning_players = [players[0]]
    winning_hands = [best_hands[0]]
    emit('best hand', best_hands[0].serialize(),room=clients[players[0].name])
    print(str(players[0]) + " has a " + str(best_hands[0]))
    for i in range(1, len(best_hands)):
        print(str(players[i]) + " has a " + str(best_hands[i]))
        emit('best hand', best_hands[i].serialize(),room=clients[players[i].name])
        if best_hands[i] < winning_hands[0]:
            continue
        elif best_hands[i] > winning_hands[0]:
            winning_hands = [best_hands[i]]
            winning_players = [players[i]]
        else:
            winning_hands.append(best_hands[i])
            winning_players.append(players[i])
    for p in winning_players:
        print(p.name)
    return winning_players
    # call next_game() ? next_game() can then reset all global vars, 
    # exclude players who indicated to "stand up", and call preflop()
    # with remaning players? Lets sync and discuss.

def distribute(room):
    global room_to_gds
    game_data = room_to_gds.get(room)
    if game_data.player_round.length == 1:
        assign_one_winner(room)
    else:
        distrubute_players = game_data.players
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
            winners = find_winners([p for p in distrubute_players if not p.is_fold],room)
            if len(winners) == 1:
                winners[0].result += calc_pot
            else:
                per_player_winnings = calc_pot/len(winners)
                if per_player_winnings.is_integer():            
                    for p in winners:
                        p.result += per_player_winnings
                else:
                    per_player_winnings = int(per_player_winnings)
                    extra_chip_winner = [p for p in game_data.aggressors.reverse() if not p.is_fold]
                    for p in winners:
                        if p == extra_chip_winner[0]:
                            p.result +=1
                        p.result += per_player_winnings

            distrubute_players = [p for p in distrubute_players if p.invested > 0]
            calc_pot = 0
        if len(distrubute_players) == 1:
            p = distrubute_players[0]
            # return uncalled bet
            p.result += p.invested
        apply_result_to_all(room)


def assign_one_winner(room):
    global room_to_gds
    game_data = room_to_gds.get_room(room)
    winner = game_data.player_round.get_next_player().player
    for p in game_data.players:
        if p != winner:
            p.result = -p.invested
            winner.result += p.invested
    apply_result_to_all(room)

def apply_result_to_all(room):
    global room_to_gds
    game_data = room_to_gds.get_room(room)
    players = game_data.players
    win_objects = {}
    for p in players:
        p.apply_result()
        win_objects[p.name] = {
            'username': p.name,
            'winnings': p.result if p.result > 0 else 0,
            'hand':[p.cards[0].serialize(), p.cards[1].serialize()],
            'final_bank': p.bank,
        }
    emit('result', win_objects, room=room)

def current_hand_strength(player, community_cards):
    best_hand = get_player_winning_hand(player.cards,community_cards)
    emit('current hand',best_hand.serialize(),room=clients[player.name])

def get_player_winning_hand(player_cards, middle_cards):
    all_cards = player_cards[:]
    all_cards.extend(middle_cards)
    all_hands = sorted([Hand.create_hand(x) for x in itertools.combinations(all_cards, 5)], reverse=True)
    return all_hands[0]

def get_options(room):
    print("GET OPTIONS")
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    print(game_data.current_player.name)
    print(game_data.current_player.current_contribution)
    print(game_data.highest_current_contribution)
    if game_data.player_round.length == 1:
        distribute(room)
    else:
        if (game_data.number_of_all_ins >= game_data.player_round.length-1 or 
        ((game_data.current_player.current_contribution is not None) 
        and (game_data.current_player.current_contribution == game_data.highest_current_contribution) 
        and (game_data.big_blind_action))):
            if game_data.game_state != GameState.WINNER:
                game_data.game_state = GameState(game_data.game_state.value+1)
            run_next_game_state(room)
        else:
            options = []
            options.append("fold")
            if (((game_data.current_player.current_contribution is None or 
            game_data.current_player.current_contribution < game_data.highest_current_contribution) 
            and highest_current_contribution != 0) 
            or (game_data.player_round.big_blind.player == current_player and 
            game_data.game_state == GameState.PREFLOP)):
                options.append("raise")
            if ((game_data.current_player.current_contribution is None 
            or game_data.current_player.current_contribution < game_data.highest_current_contribution) 
            and game_data.highest_current_contribution != 0):  
                options.append("call")
            if (game_data.highest_current_contribution == 0 or 
            (game_data.player_round.big_blind.player == game_data.current_player and 
            game_data.game_state == GameState.PREFLOP)):
                options.append("check")
                if "raise" not in options:
                    options.append("bet")
            for opt in options:
                print(opt)
            emit('options for player', {'options': options, 
            'highest_contribution': game_data.highest_current_contribution},
             room=game_data.clients[current_player.name])


def deal_cards(room):
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    game_data.deck.shuffle()
    for i in range(0, len(game_data.players)):
        pair = [game_data.deck.get_top_card(), game_data.deck.get_top_card()]
        game_data.players[i].set_cards(pair)
        print(str(game_data.players[i]) + ": " + str(pair[0]) + ", " + str(pair[1]))
        emit('dealt cards', 
            {
                'cards': [
                    {
                        'value':pair[0].value_to_str(), 
                        'suit': pair[0].suit_to_str()
                    },
                    {
                        'value':pair[1].value_to_str(),
                        'suit': pair[1].suit_to_str()
                    }
                ]
            },
            room=game_data.clients[players[i].name]
        ) 



def broadcast_pot(amount,room):
    emit('pot update', {'pot': amount}, room=room)

def broadcast_community_cards(room):
    global room_to_gds
    game_data = room_to_gds.get_room(room)
    cards = []
    for c in game_data.community_cards:
        cards.append(c.serialize())
    emit('community cards', {'community_cards': cards}, room=room)
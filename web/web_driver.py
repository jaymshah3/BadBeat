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

try:
    from __main__ import eventlet
except ImportError:
    import eventlet


room_to_gds = GameDataService.room_to_gds

'''players = []
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
prev_high_raise = 0
number_of_all_ins = 0
big_blind_action = False
aggressors = []
'''

# def decorator_action(function):
#     def handle_action(data):
#         global room_to_gds
#         room = data['room']
#         game_data = room_to_gds.get_game_data(room)
#         function(data,game_data)
#     return handle_action

@socketio.on('fold')
def handle_fold(data):
    global room_to_gds
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    print("Current node: " +game_data.player_round.current_node.player.name)
    current_player = game_data.current_player
    print("FOLD")
    if data['username'] is not current_player.name:
        pass
        #error
    if (game_data.game_state == GameDataService.GameState.PREFLOP 
    and game_data.current_player == game_data.player_round.big_blind.player):
        game_data.big_blind_action = True
    data['action'] = 'fold'
    emit('player action', data, room=room)
    next_node= game_data.player_round.check_next_player()
    next_player = next_node.player
    print(next_player)
    print("node all in: " + str(next_node.is_all_in))
    if next_player == game_data.current_player:
        print("line 62")
        game_data.player_round.remove_current()
        game_data.game_state = GameDataService.GameState(game_data.game_state.value+1)
        run_next_game_state(room)
    else:
        print("line 67")
        game_data.player_round.remove_current()
        game_data.current_player = game_data.player_round.get_next_player().player
        get_options(room)

@socketio.on('call')
def handle_call(data):
    print("CALL")
    global room_to_gds
    room = data['room']
    print(str(data))
    game_data = room_to_gds.get_game_data(room)
    print("Current node: " +game_data.player_round.current_node.player.name)
    if data['username'] is not game_data.current_player.name:
        pass
        #error
    if (game_data.game_state == GameDataService.GameState.PREFLOP 
    and game_data.current_player == game_data.player_round.big_blind.player):
        game_data.big_blind_action = True
    game_data.current_player.bet(data['amount'])
    emit('withdraw', {'username':game_data.current_player.name, 'amount':data['amount']},
        room=room)
    game_data.current_round_pot += data['amount']
    broadcast_pot(game_data.current_round_pot + game_data.pot,room)
    data['action'] = 'call'
    data['currentContribution'] = game_data.current_player.current_contribution
    emit('player action', data, room=room)
    next_player = game_data.player_round.check_next_player().player
    if next_player == game_data.current_player:
        if game_data.current_player.bank == game_data.current_player.invested:
            print("all_in")
            game_data.number_of_all_ins+=1
            game_data.player_round.all_in_current_node()
        game_data.game_state = GameDataService.GameState(game_data.game_state.value+1)
        run_next_game_state(room)
    else:
        if game_data.current_player.bank == game_data.current_player.invested:
            print("all_in")
            game_data.player_round.all_in_current_node()
            print("Current node: " +game_data.player_round.current_node.player.name)
            game_data.number_of_all_ins+=1
        game_data.current_player = game_data.player_round.get_next_player().player
        get_options(room)
            
        
@socketio.on('raise')
def handle_raise(data):
    print("RAISE")
    print(str(data))
    global room_to_gds
    room = data['room']
    
    game_data = room_to_gds.get_game_data(room)
    print("Current node: " +game_data.player_round.current_node.player.name)
    if data['username'] is not game_data.current_player.name:
        pass
        #error
    if (game_data.game_state == GameDataService.GameState.PREFLOP 
    and game_data.current_player == game_data.player_round.big_blind.player):
        game_data.big_blind_action = True
    if ((data['amount'] >= game_data.wager_size+game_data.highest_current_contribution) 
    or (game_data.highest_current_contribution == 0)):
        print("latest aggresor: " + game_data.current_player.name)
        game_data.aggressors.append(game_data.current_player)
        game_data.latest_aggressor = game_data.current_player
    # on raise, the amount is the final amount the player wants to be "in" for,
    # not how much more they want to add to there contribution.
    if game_data.current_player.current_contribution is not None:
        game_data.current_round_pot += data['amount']-game_data.current_player.current_contribution
        emit('withdraw', {'username':game_data.current_player.name, 
        'amount': data['amount']-game_data.current_player.current_contribution},
        room=room)
        game_data.current_player.bet(data['amount']-game_data.current_player.current_contribution)
    else:
        game_data.current_player.bet(data['amount'])
        game_data.current_round_pot += data['amount']
        emit('withdraw', {'username':game_data.current_player.name, 
        'amount': game_data.current_player.current_contribution},
        room=room)
    game_data.wager_size = data['amount'] - game_data.highest_current_contribution
    game_data.highest_current_contribution = game_data.current_player.current_contribution 
    # we already added data['amount'] to current_player.current_contribution
    if game_data.current_player.bank == game_data.current_player.invested:
        print("all_in")
        game_data.number_of_all_ins+=1
        game_data.player_round.all_in_current_node()
    broadcast_pot(game_data.current_round_pot + game_data.pot,room)
    data['action'] = 'raise'
    data['currentContribution'] = game_data.current_player.current_contribution
    emit('highest contribution', {'highest_contribution': game_data.highest_current_contribution}, room=room)
    emit('player action', data, room=room)
    game_data.current_player = game_data.player_round.get_next_player().player
    print("line 128: " + str(room))
    get_options(room)

@socketio.on('stand up')
def stand_up(data):
    global room_to_gds
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    game_data.player_round.toggle_node_stand_up(data['username'])

@socketio.on('waiting to join')
def waiting_to_join(data):
    global room_to_gds
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    json_object = game_data.seralize_waiting_to_join()
    emit('waiting list', {'waiting_list':json_object},room=game_data.room_owner)

def run_next_game_state(room):
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    print('RUN_NEXT_GAME_STATE: ' + str(game_data.game_state.value))
    next_game_state = game_data.game_state
    for p in game_data.player_round.players:
        p.current_contribution = None
    emit('reset current contribution', {}, room=room)
    game_data.highest_current_contribution = 0
    game_data.latest_aggressor = None
    game_data.wager_size = game_data.big_blind_amount
    game_data.pot += game_data.current_round_pot
    broadcast_pot(game_data.pot,room)
    game_data.current_round_pot = 0
    if game_data.player_round.length_active == 1:
        distribute(room)
    else:
        if next_game_state != GameDataService.GameState.WINNER:
            print("line 154: " + str(room))
            run_street(game_data.heads_up,room)
        else:
            distribute(room)
def start_round(room):
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    game_data.player_round = Round(game_data.get_players())
    preflop(room)

def preflop(room):
    print('PREFLOP')
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    game_data.highest_current_contribution = game_data.big_blind_amount
    if game_data.player_round.small_blind.player.bank <= game_data.small_blind_amount:
        game_data.player_round.small_blind.player.bet(game_data.player_round.small_blind.player.bank)
        game_data.player_round.small_blind.is_all_in = True
        game_data.number_of_all_ins+=1
    else:
        game_data.player_round.small_blind.player.bet(game_data.small_blind_amount)
    emit('withdraw', {'username':game_data.player_round.small_blind.player.name,
     'amount': game_data.player_round.small_blind.player.current_contribution},
        room=room)
    emit('player action', {
        'username': game_data.player_round.small_blind.player.name,
        'amount': game_data.player_round.small_blind.player.current_contribution,
        'action': 'small blind',
        'currentContribution': game_data.player_round.small_blind.player.current_contribution
    }, room=room)
    if game_data.player_round.big_blind.player.bank <= game_data.big_blind_amount:
        game_data.player_round.big_blind.player.bet(game_data.player_round.big_blind.player.bank)
        game_data.player_round.big_blind.is_all_in = True
        game_data.number_of_all_ins+=1
    else:
        game_data.player_round.big_blind.player.bet(game_data.big_blind_amount)
    emit('withdraw', {'username':game_data.player_round.big_blind.player.name,
     'amount': game_data.player_round.big_blind.player.current_contribution},
        room=room)
    game_data.current_round_pot += game_data.player_round.small_blind.player.current_contribution
    game_data.current_round_pot += game_data.player_round.big_blind.player.current_contribution
    game_data.current_player = game_data.player_round.current_node.player
    game_data.aggressors.append(game_data.player_round.big_blind.player)
    if game_data.player_round.length_active == 2:
        game_data.heads_up = True
    emit('player action', {
        'username': game_data.player_round.big_blind.player.name,
        'amount': game_data.player_round.big_blind.player.current_contribution,
        'action': 'big blind',
        'currentContribution': game_data.player_round.big_blind.player.current_contribution
    }, room=room)
    broadcast_pot(game_data.current_round_pot,room)
    emit('highest contribution', {'highest_contribution': game_data.big_blind_amount}, room=room)
    game_data.wager_size = game_data.big_blind_amount
    deal_cards(room)
    print("Current node: " +game_data.player_round.current_node.player.name)
    get_options(room) 

def run_street(heads_up,room):
    print("RUN STREET")
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    print("ACTIVE : " + str(game_data.player_round.length_active-1))
    print('Game State:' + str(game_data.game_state))

    if game_data.game_state == GameDataService.GameState.FLOP:
        game_data.community_cards = [
            game_data.deck.get_top_card(),
            game_data.deck.get_top_card(),
            game_data.deck.get_top_card()
        ]
    else:
        game_data.community_cards.append(game_data.deck.get_top_card())
    broadcast_community_cards(room)
    for player in game_data.player_round.get_current_players():
        current_hand_strength(player,game_data.community_cards,room)
    if game_data.number_of_all_ins >= game_data.player_round.length_active-1:
        game_data.game_state = GameDataService.GameState(game_data.game_state.value+1)
        run_next_game_state(room)
    else:
        if game_data.heads_up:
            current_player_node = game_data.player_round.big_blind
        else:
            current_player_node= game_data.player_round.small_blind
            while current_player_node.is_fold or current_player_node.is_all_in:
                current_player_node = current_player_node.next_node
        game_data.current_player = current_player_node.player
        game_data.player_round.current_node = current_player_node
        print("Current node: " +game_data.player_round.current_node.player.name)
        get_options(room)

def find_winners(all_players,room):
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    players = list(all_players)
    print("FIND_WINNERS")
    middle_cards = game_data.community_cards
    best_hands = [get_player_winning_hand(x.cards, middle_cards) for x in players]
    winning_players = [players[0]]
    winning_hands = [best_hands[0]]
    emit('best hand', best_hands[0].serialize(),room=game_data.clients[players[0].name])
    print(str(players[0]) + " has a " + str(best_hands[0]))
    for i in range(1, len(best_hands)):
        print(str(players[i]) + " has a " + str(best_hands[i]))
        emit('best hand', best_hands[i].serialize(),room=game_data.clients[players[i].name])
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
    print("DISTRUBUTE")
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    if game_data.player_round.length_active == 1:
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
    game_data = room_to_gds.get_game_data(room)
    winner = [p for p in game_data.player_round.players if not p.is_fold]
    for p in game_data.player_round.players:
        if p != winner[0]:
            p.result = -p.invested
            winner[0].result += p.invested
    apply_result_to_all(room)

def apply_result_to_all(room):
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    players = game_data.player_round.players
    win_objects = {}
    for p in players:
        p.apply_result()
        win_objects[p.name] = {
            'username': p.name,
            'winnings': p.result if p.result > 0 else 0,
            'hand':[p.cards[0].serialize(), p.cards[1].serialize()],
            'final_bank': p.bank,
        }
        print("Player name: " + p.name + " Bank: " + str(p.bank))
    emit('result', win_objects, room=room)
    eventlet.sleep(10)
    clean_up_poker_table(room)

def clean_up_poker_table(room):
    global room_to_gds
    print("Clean_Up_Poker_Table")
    game_data = room_to_gds.get_game_data(room)
    try:
        game_data.player_round.start_new_hand()
        game_data.reset()
    except Exception as e:
        print(e)
        print("one player left, cannot restart")
        return
    emit('new game', room=room)
    preflop(room)

   
def current_hand_strength(player, community_cards,room):
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    best_hand = get_player_winning_hand(player.cards,community_cards)
    emit('current hand',best_hand.serialize(),room=game_data.clients[player.name])

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
    if game_data.latest_aggressor:
        print(game_data.latest_aggressor.name)
    current_player = game_data.current_player
    highest_current_contribution = game_data.highest_current_contribution
    print(highest_current_contribution)
    print(game_data.big_blind_action)
    if game_data.player_round.length_active == 1:
        print("active length is 1")
        distribute(room)
    else:
        if (((game_data.current_player.current_contribution is not None) 
        and (current_player.current_contribution == highest_current_contribution) 
        and (game_data.big_blind_action))):
            if game_data.game_state != GameDataService.GameState.WINNER:
                game_data.game_state = GameDataService.GameState(game_data.game_state.value+1)
            print("line 376: " + str(room))
            run_next_game_state(room)
        else:
            options = []
            options.append("fold")
            if ((game_data.latest_aggressor != current_player) and 
            (current_player != game_data.player_round.check_next_player().player)
            and (highest_current_contribution != 0) and ((not current_player.current_contribution or
            current_player.current_contribution < highest_current_contribution)
            or (game_data.player_round.big_blind.player == current_player and
            game_data.game_state.value ==1))):
                options.append("raise")
            if ((not current_player.current_contribution 
            or current_player.current_contribution < highest_current_contribution) 
            and highest_current_contribution != 0):  
                options.append("call")
            if "call" not in options:
                options.append("check")
            if ("raise" not in options 
            and game_data.latest_aggressor != current_player
            and highest_current_contribution == 0):
                options.append("bet")
            max_bet_amount = find_max_bet(room)
            emit('options for player', {'options': options, 
            'max_bet': max_bet_amount, 'min_bet':game_data.wager_size+highest_current_contribution,
            'highest_contribution': highest_current_contribution},
             room=game_data.clients[current_player.name])


def deal_cards(room):
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    game_data.deck.shuffle()
    for p in game_data.player_round.get_current_players():
        pair = [game_data.deck.get_top_card(), game_data.deck.get_top_card()]
        p.set_cards(pair)
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
            room=game_data.clients[p.name]
        ) 

def find_max_bet(room):
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    current_player = game_data.current_player
    max_money = 0
    for player in game_data.player_round.get_current_players():
        if player != current_player:
            amount_left = player.bank - player.invested
            if amount_left > max_money:
                max_money = amount_left
    return max_money

def broadcast_pot(amount,room):
    emit('pot update', {'pot': amount}, room=room)

def broadcast_community_cards(room):
    global room_to_gds
    game_data = room_to_gds.get_game_data(room)
    cards = []
    for c in game_data.community_cards:
        cards.append(c.serialize())
    emit('community cards', {'community_cards': cards}, room=room)


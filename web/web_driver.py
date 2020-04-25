from core.deck import Deck
from core.poker_round import Round
from core.player import Player
from core.hand import Hand
from enum import Enum
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


@socketio.on('fold')
def handle_fold(data):
    global current_player
    global player_round
    global game_state
    global aggressors
    print("FOLD")
    if data['username'] is not current_player.name:
        pass
        #error
    player_round.remove_current()
    data['action'] = 'fold'
    emit('player action', data, broadcast=True)
    current_player = player_round.get_next_player().player
    get_options()

@socketio.on('call')
def handle_call(data):
    global current_player
    global player_round
    global game_state
    global current_round_pot
    global number_of_all_ins
    global pot
    global big_blind_action
    print("CALL")
    if data['username'] is not current_player.name:
        pass
        #error
    if (game_state == GameState.PREFLOP 
    and current_player == player_round.big_blind.player):
        print('changed big blind action')
        big_blind_action = True
    print(big_blind_action)
    print(data['amount'])
    current_player.bet(data['amount'])
    emit('withdraw', {'username':current_player.name, 'amount':data['amount']},
        broadcast=True)
    if current_player.bank == current_player.invested:
        number_of_all_ins+=1
        player_round.all_in_current_node()
    current_round_pot += data['amount']
    broadcast_pot(current_round_pot + pot)
    data['action'] = 'call'
    data['currentContribution'] = current_player.current_contribution
    emit('player action', data, broadcast=True)
    print(current_player.name)
    print(player_round.get_next_player().player)
    current_player = player_round.current_node.player
    get_options()
        
@socketio.on('raise')
def handle_raise(data):
    global current_player
    global player_round
    global game_state
    global current_round_pot
    global pot
    global highest_current_contribution
    global prev_high_raise
    global aggressors
    global number_of_all_ins
    global game_state
    global big_blind_action
    print("RAISE")
    if data['username'] is not current_player.name:
        pass
        #error
    if (game_state == GameState.PREFLOP 
    and current_player == player_round.big_blind.player):
        print('changed big blind action')
        big_blind_action = True
    print(big_blind_action)
    aggressors.append(current_player)
    prev_high_raise = highest_current_contribution
    # on raise, the amount is the final amount the player wants to be "in" for,
    # not how much more they want to add to there contribution.
    if current_player.current_contribution is not None:
        print('raised from not none')
        print(data['amount'])
        current_round_pot += data['amount']-current_player.current_contribution
        emit('withdraw', {'username':current_player.name, 
        'amount': data['amount']-current_player.current_contribution},
        broadcast=True)
        current_player.bet(data['amount']-current_player.current_contribution)
    else:
        current_player.bet(data['amount'])
        current_round_pot += data['amount']
        emit('withdraw', {'username':current_player.name, 
        'amount': current_player.current_contribution},
        broadcast=True)
    highest_current_contribution = current_player.current_contribution 
    # we already added data['amount'] to current_player.current_contribution
    if current_player.bank == current_player.invested:
        number_of_all_ins+=1
        player_round.all_in_current_node()
    broadcast_pot(current_round_pot + pot)
    data['action'] = 'raise'
    data['currentContribution'] = current_player.current_contribution
    emit('highest contribution', {'highest_contribution': highest_current_contribution}, broadcast=True)
    emit('player action', data, broadcast=True)
    current_player = player_round.get_next_player().player
    get_options()

def run_next_game_state(next_game_state):
    global highest_current_contribution
    global pot
    global current_round_pot
    global player_round
    global clients
    global heads_up
    global game_state
    print('RUN_NEXT_GAME_STATE')
    print(next_game_state.value)
    game_state = next_game_state
    for player in players:
        # emit('withdraw', {'amount': player.current_contribution},
        # room=clients[player.name])
        emit('current contribution', {'amount': 0}, broadcast=True)
        player.current_contribution = None
    highest_current_contribution = 0
    pot += current_round_pot
    broadcast_pot(pot)
    current_round_pot = 0
    if player_round.length == 1:
        distribute()
    else:
        if next_game_state != GameState.WINNER:
            run_street(heads_up)
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
    global heads_up
    global current_round_pot
    global number_of_all_ins
    print('PREFLOP')
    players = given_players
    clients = given_clients
    small_blind = 0
    player_round = Round(players,small_blind)
    small_blind_amount = small_blind_amt
    big_blind_amount = big_blind_amt
    highest_current_contribution = big_blind_amount
    player_round.small_blind.player.bet(small_blind_amount)
    emit('withdraw', {'username':player_round.small_blind.player.name,
     'amount': player_round.small_blind.player.current_contribution},
        broadcast=True)
    if player_round.small_blind.player.invested == player_round.small_blind.player.bank:
        print('incrementing all_ins')
        player_round.small_blind.isAllIn = True
        number_of_all_ins+=1
    emit('player action', {
        'username': player_round.small_blind.player.name,
        'amount': small_blind_amount,
        'action': 'small blind',
        'currentContribution': small_blind_amount
    }, broadcast=True)
    player_round.big_blind.player.bet(big_blind_amount)
    emit('withdraw', {'username':player_round.big_blind.player.name,
     'amount': player_round.big_blind.player.current_contribution},
        broadcast=True)
    if player_round.big_blind.player.invested == player_round.big_blind.player.bank:
        print('incrementing all_ins')
        player_round.big_blind.isAllIn = True
        number_of_all_ins+=1
    current_round_pot += player_round.small_blind.player.current_contribution
    current_round_pot += player_round.big_blind.player.current_contribution
    current_player = player_round.current_node.player
    aggressors.append(player_round.big_blind.player)
    if len(players) == 2:
        heads_up = True
    emit('player action', {
        'username': player_round.big_blind.player.name,
        'amount': big_blind_amount,
        'action': 'big blind',
        'currentContribution': big_blind_amount
    }, broadcast=True)
    broadcast_pot(current_round_pot)
    emit('highest contribution', {'highest_contribution': big_blind_amount}, broadcast=True)
    deal_cards()
    get_options() 
def run_street(heads_up):
    global community_cards
    global deck
    global player_round
    global current_player
    global number_of_all_ins
    global game_state
    print('Game State:' + str(game_state))
    if game_state == GameState.FLOP:
        community_cards = [
            deck.get_top_card(),
            deck.get_top_card(),
            deck.get_top_card()
        ]
    else:
        community_cards.append(deck.get_top_card())
    broadcast_community_cards()
    for player in player_round.get_current_players():
        current_hand_strength(player,community_cards)
    if number_of_all_ins >= player_round.length-1:
        game_state = GameState(game_state.value+1)
        run_next_game_state(game_state)
    else:
        if heads_up:
            current_player_node = player_round.big_blind
        else:
            current_player_node= player_round.small_blind
            while current_player_node.is_fold:
                current_player_node = current_player.next_node
        current_player = current_player_node.player
        player_round.current_node = current_player_node
        get_options()

def find_winners(all_players):
    global community_cards
    players = list(all_players)
    print("FIND_WINNERS")
    middle_cards = community_cards
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

def distribute():
    global players
    global player_round
    if player_round.length == 1:
        assign_one_winner()
    else:
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
            winners = find_winners([p for p in distrubute_players if not p.is_fold])
            if len(winners) == 1:
                winners[0].result += calc_pot
            else:
                per_player_winnings = pot/len(winners)
                if per_player_winnings.is_integer():            
                    for p in winners:
                        p.result += per_player_winnings
                else:
                    per_player_winnings = int(per_player_winnings)
                    extra_chip_winner = [p for p in aggressors.reverse() if not p.is_fold]
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


def assign_one_winner():
    global players
    global player_round
    winner = player_round.get_next_player()
    for p in players:
        if p != winner:
            p.result = -p.invested
            winner.result += p.invested
    apply_result_to_all()

def apply_result_to_all():
    global players
    for p in players:
        p.apply_result()

def current_hand_strength(player, community_cards):
    best_hand = get_player_winning_hand(player.cards,community_cards)
    emit('current hand', best_hand.serialize(),room=clients[player.name])

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
    global number_of_all_ins
    global big_blind_action
    print("GET OPTIONS")
    print(current_player.name)
    print(current_player.current_contribution)
    print(highest_current_contribution)
    print(big_blind_action)
    if player_round.length == 1:
        distribute()
    else:
        if (number_of_all_ins >= player_round.length-1 or ((current_player.current_contribution is not None) 
        and (current_player.current_contribution == highest_current_contribution) 
        and (big_blind_action))):
            if game_state != GameState.WINNER:
                game_state = GameState(game_state.value+1)
            run_next_game_state(game_state)
        else:
            options = []
            options.append("fold")
            if (((current_player.current_contribution is None or 
            current_player.current_contribution < highest_current_contribution) 
            and highest_current_contribution != 0) 
            or (player_round.big_blind.player == current_player and 
            game_state == GameState.PREFLOP)):
                options.append("raise")
            if ((current_player.current_contribution is None 
            or current_player.current_contribution < highest_current_contribution) 
            and highest_current_contribution != 0):  
                options.append("call")
            if (highest_current_contribution == 0 or 
            (player_round.big_blind.player == current_player and 
            game_state == GameState.PREFLOP)):
                options.append("check")
                if "raise" not in options:
                    options.append("bet")
            for opt in options:
                print(opt)
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
            room=clients[players[i].name]
        ) 



def broadcast_pot(amount):
    emit('pot update', {'pot': amount}, broadcast=True)

def broadcast_community_cards():
    global community_cards
    cards = []
    for c in community_cards:
        cards.append(c.serialize())
    emit('community cards', {'community_cards': cards}, broadcast=True)
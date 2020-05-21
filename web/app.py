from threading import Lock
from flask import Flask, request, make_response
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import GameDataService
import uuid
app = Flask(__name__, static_folder="../client/build", static_url_path="/")
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(logger=False)
socketio.init_app(app, cors_allowed_origins='*')

GameDataService.init_gds()
room_to_gds = GameDataService.room_to_gds
lock = Lock()

@app.route('/*')
def index():
    return app.send_static_file('index.html')

@app.route('/<room_id>')
def room_page(room_id):
    return app.send_static_file('index.html')

@socketio.on('create room')
def create_room(data):
    global room_to_gds
    with lock:
        unique_id = uuid.uuid4()

    unique_room_number = str(unique_id.int)
    print(unique_room_number)
    username = data['username']
    bank = data['bank']
    small_blind = data['small_blind']
    big_blind = data['big_blind']
    game_data = GameDataService.GameData(request.sid,small_blind,big_blind)
    print("emitting to: " + str(game_data.room_owner))
    emit('owner', {"room":unique_room_number}, room=game_data.room_owner)
    join_room(unique_room_number)
    game_data.add_player(username,game_data.active_clients,int(bank),request.sid)
    room_to_gds.add_game_data(unique_room_number,game_data)

@socketio.on('request to join')
def request_to_join(data):
    global room_to_gds
    username = data['username']
    room = data['room']
    data['request_sid'] = request.sid
    game_data = room_to_gds.get_game_data(room)
    if not game_data.clients.get(username,False):
        emit('join request', data, room=game_data.room_owner)
        game_data.waiting_to_join.append((username,data['bank'],request.sid))
    else:
        emit('duplicate username' ,{'message': "Username already exists"}, room=request.sid)
    #send(username + ' has entered the room.', room=room)
    

@socketio.on('handle join request')
def handle_join_request(data):
    global room_to_gds
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    if data['approve']:
        print('success: ' + str(data['room']))
        #join_room(data['room'],sid=data['request_sid'])
        emit("user joined", data, room=data['room'])
        game_data.add_player(data['username'],game_data.active_clients,int(data['bank']),data['request_sid'])
        game_data.remove_wait_list(data['username'])
    emit('request response', data, room=data['request_sid'])

@socketio.on('chat message')
def chat_message(data):
    global room_to_gds
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    players = game_data.get_players()
    for p in players:
        emit('chat message', data, room=game_data.clients[p.name])

@socketio.on('game info')
def list_users(data):
    global room_to_gds
    room = data['room']
    join_room(room)
    game_data = room_to_gds.get_game_data(room)
    cards = []
    for c in game_data.community_cards:
        cards.append(c.serialize())
    emit('game info', {
        'started': game_data.started, 
        'community_cards': cards,
        'pot': game_data.pot,
        'highest_current_contribution': game_data.highest_current_contribution,
        'players': list(map(lambda p: {
                'username': p.name, 
                'bank': p.bank
            }, 
            game_data.get_players()))
        },
    room=request.sid)
    

@socketio.on('leave')
def on_leave(data):
    global room_to_gds
    username = data['username']
    room = data['room']
    id_num = data['id_num']
    game_data = room_to_gds.get_game_data(room)
    game_data.remove_player(id_num,username)
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('start')
def on_start(data):
    global room_to_gds
    print('got start')
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    game_data.start_game()
    emit('game start', {'message': "Game has started"}, room=room)
    start_round(room)
    

from web_driver import start_round
if __name__ == '__main__':
    socketio.run(app,debug=True)
    

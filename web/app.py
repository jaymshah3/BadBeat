from threading import Lock
from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
import GameDataService
import uuid
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

GameDataService.init_gds()
room_to_gds = GameDataService.room_to_gds
lock = Lock()
    
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
    if game_data.room_owner == request.sid:
        join_room(room)
    elif not game_data.clients.get(username,False):
        emit('join request', data, room=game_data.room_owner)
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
        emit("user joined", data, room=data['room'])
        join_room(data['room'])
        game_data.add_player(data['username'],game_data.active_clients,int(data['bank']),data['request_sid'])
    emit('request response', data, room=game_data.clients[data['username']])

@socketio.on('list users')
def list_users(data):
    global room_to_gds
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    emit('user list', {'players': list(map(lambda p: {
        'username': p.name, 
        'bank': p.bank
    }, game_data.get_players()))},room=room)

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
    emit('game start', {'message': "Game has started"}, room=room)
    start_round(room)
    

from web_driver import start_round
if __name__ == '__main__':
    socketio.run(app,debug=True)
    
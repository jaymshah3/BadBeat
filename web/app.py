from threading import Lock
from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from web.GameDataService import GameDataService, GameData
import uuid
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

clients = {}
room_to_gds = GameDataService()
active_clients = 0
room_owner = -1
has_game_started = False
lock = Lock()
    
@socketio.on('create room')
def create_room(data):
    global room_to_gds
    lock.acquire()
    unique_id= uuid.uuid4()
    lock.release()
    unique_room_number = unique_id.int
    username = data['username']
    bank = data['bank']
    small_blind = data['small_blind']
    big_blind = data['big_blind']
    game_data = GameData()
    game_data.room_owner = request.sid
    game_data.clients[username] = request.sid
    game_data.active_clients += 1
    emit('owner', {}, room=room_owner)
    game_data.add_player(username,active_clients,int(bank))
    room_to_gds.add_game_data(unique_room_number,game_data)

@socketio.on('request to join')
def request_to_join(data):
    username = data['username']
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    clients = game_data.clients
    if not clients.get(username,False):
        clients[username] = request.sid
        emit('join request', data, room =room_owner)
    else:
        emit('duplicate username' ,{'message': "Username already exists"}, room=request.sid)
    join_room(room)
    #send(username + ' has entered the room.', room=room)
    

@socketio.on('handle join request')
def handle_join_request(data):
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    if data['approve']:
        print('success: ' + str(data['room']))
        emit("user joined", data, room=data['room'])
        game_data.active_clients += 1
        game_data.add_player(data['username'],game_data.active_clients,int(data['bank']))
    emit('request response', data, room=clients[data['username']])

@socketio.on('list users')
def list_users(data):
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    emit('user list', {'players': list(map(lambda p: {
        'username': p.name, 
        'bank': p.bank
    }, game_data.get_players()))},room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    del game_data.clients[username]
    game_data.active_clients =- 1
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('start')
def on_start(data):
    print('got start')
    global has_game_started
    room = data['room']
    game_data = room_to_gds.get_game_data(room)
    has_game_started = True
    emit('game start', {'message': "Game has started"}, room=room)
    preflop(game_data.get_players(), game_data.clients, game_data.small_blind, game_data.big_blind)
    

def change_active_clients(increment):
    global active_clients
    lock.acquire()
    active_clients+=increment
    lock.release()

from web_driver import preflop
if __name__ == '__main__':
    socketio.run(app,debug=True)
    
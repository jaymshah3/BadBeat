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
    unique_room_number = uuid.uuid4()
    username = data['username']
    bank = data['bank']
    small_blind = data['small_blind']
    big_blind = data['big_blind']
    game_data = GameData()
    game_data.room_owner = request.sid
    game_data.clients[username] = request.sid
    game_data.active_clients += 1
    emit('owner', {}, room=room_owner)
    game_data.add_player(username,active_clients,bank)
    room_to_gds.add_game_data(unique_room_number,game_data)

@socketio.on('request to join')
def request_to_join(data):
    global clients
    global active_clients
    global room_owner
    username = data['username']
    room = data['room']
    lock.acquire()
    if not clients.get(username,False):
        clients[username] = request.sid
    else:
        emit('duplicate username' ,{'message': "Username already exists"}, room=request.sid)
    lock.release()
    join_room(room)
    #send(username + ' has entered the room.', room=room)
    if active_clients == 0:
        room_owner = request.sid
        emit('owner', {'message': "you are owner"}, room=room_owner)
        change_active_clients(1)
    if request.sid == room_owner:
        memory.add_player(data['username'],active_clients,data['bank'])
    else:
        emit('join request', data, room =room_owner)

@socketio.on('handle join request')
def handle_join_request(data):
    global memory
    global active_clients
    if data['approve']:
        print('success: ' + str(data['room']))
        emit("user joined", data,
         room=data['room'])
        change_active_clients(1)
        memory.add_player(data['username'],active_clients,int(data['bank']))
    emit('request response', data, room=clients[data['username']])

@socketio.on('list users')
def list_users(data):
    emit('user list', {'players': list(map(lambda p: {
        'username': p.name, 
        'bank': p.bank
    }, memory.get_players()))},room=data['room'])

@socketio.on('leave')
def on_leave(data):
    global clients
    username = data['username']
    room = data['room']
    del clients[username]
    change_active_clients(-1)
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('start')
def on_start(data):
    print('got start')
    global has_game_started
    global memory
    room = data['room']
    has_game_started = True
    emit('game start', {'message': "Game has started"}, room=room)
    preflop(memory.get_players(), clients, data['small_blind'], data['big_blind'])
    

def change_active_clients(increment):
    global active_clients
    lock.acquire()
    active_clients+=increment
    lock.release()

from web_driver import preflop
if __name__ == '__main__':
    socketio.run(app,debug=True)
    
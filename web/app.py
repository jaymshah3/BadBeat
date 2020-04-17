from threading import Lock
from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from GameDataService import GameDataService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO()
socketio.init_app(app, cors_allowepd_origins='*')

clients = {}
memory = GameDataService()
active_clients = 0
room_owner = -1
has_game_started = False
lock = Lock()


@socketio.on('connect')
def handle_connect():
    print('connected')

def ack():
    print('message was received!')

    
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
        emit("user joined", data,
         room=data['room'])
        change_active_clients(1)
        memory.add_player(data['username'],active_clients,data['bank'])
    emit('request response', {data}, room=clients[data['username']])

@socketio.on('list users')
def list_users(data):
    emit('user list', {'players': memory.get_players()},room=data['room'])

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
    global has_game_started
    global memory
    room = data['room']
    has_game_started = True
    emit('server_start', {'message': "Game has started"}, room=room)
    preflop(memory.get_players,clients)
    

def change_active_clients(increment):
    global active_clients
    lock.acquire()
    active_clients+=increment
    lock.release()

from web_driver import preflop
if __name__ == '__main__':
    socketio.run(app,debug=True)
    
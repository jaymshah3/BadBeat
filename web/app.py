from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from GameDataService import GameDataService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

clients = []
memory = GameDataService()
active_clients = 0
room_owner = -1

@socketio.on('connect')
def handle_connect():
    print('connected')

@socketio.on('fold')
def handle_fold(data):
    pass

@socketio.on('raise')
def handle_raise(data):
    pass

@socketio.on('call')
def handle_call(data):
    pass

def ack():
    print('message was received!')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    clients.append(request.sid)
    join_room(room)
    send(username + ' has entered the room.', room=room)
    if active_clients == 0:
        room_owner = request.sid
    active_clients += 1
    
@socketio.on('request to join')
def request_to_join(data):
    if request.sid == room_owner:
        memory.add_player(data['name'],active_clients,data['bank'])
        return
    emit('join request', data, room =room_owner)

@socketio.on('approve join request')
def approve_join_request(data):
    memory.add_player(data['name'],active_clients,data['bank'])

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    clients.remove(request.sid)
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('start')
def on_start(data):
    emit('server_start', 'Game has started', broadcast=True)


if __name__ == '__main__':
    socketio.run(app)
    
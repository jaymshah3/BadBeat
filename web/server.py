from threading import Lock
from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from web.GameDataService import GameDataService
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
clients = {}
memory = GameDataService()
active_clients = 0
room_owner = -1
lock = Lock()

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
    print ('message was received!')

    
@socket.io('request to join')
def request_to_join(data):
    username = data['username']
    room = data['room']
    lock.acquire()
    if not clients.get(username,False):
        clients[username] = request.sid
    else:
        emit('error request to join' ,{'message': "Username already exists"}, room=request.sid)
    lock.release()
    join_room(room)
    send(username + ' has entered the room.', room=room)
    if active_clients == 0:
        room_owner = request.sid
        change_active_clients(True)
    if request.sid == room_owner:
        memory.add_player(data['name'],active_clients,data['bank'])
        return
    emit('join request', data, room =room_owner)

@socket.io('handle join request')
def handle_join_request(data,approve):
    if approve:
        change_active_clients(True)
        memory.add_player(data['username'],active_clients,data['bank'])
    else:
        emit('reject request', {'message': "Request to Join Rejected"}, room=clients[data['username']])

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    del clients[username]
    change_active_clients(False)
    leave_room(room)
    send(username + ' has left the room.', room=room)

@socketio.on('start')
def on_start(data):
    emit('server_start', 'Game has started', broadcast=True)

def change_active_clients(increment):
    lock.acquire()
    if increment:
        active_clients+=1
    else:
        active_clients-=1
    lock.release()


if __name__ == '__main__':
    socketio.run(app)
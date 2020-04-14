from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from web.GameDataService import GameDataService
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
clients = []
memory = GameDataService()
active_clients = 0
@socketio.on('fold')
def handleFold(data):
    pass

@socketio.on('raise')
def handleRaise(data):
    pass

@socketio.on('call')
def handleCall(data):
    pass

def ack():
    print ('message was received!')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    clients.append(request.sid)
    join_room(room)
    send(username + ' has entered the room.', room=room)
    active_clients++
    
@socket.io('request to join')
def request_to_join(data):
    emit('join request', data, room =clients[0])

@socket.io('approve join request'):
def approve_join_request(data):
    id_num = active_clients
    memory.add_player(data['name'],id_num,data['bank'])

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
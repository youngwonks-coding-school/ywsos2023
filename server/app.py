import os
import datetime

from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager

from routes.index import index
from routes.auth import auth
from dotenv import load_dotenv
from db import db


app = Flask(__name__)
load_dotenv()
app.config['JSON_AS_ASCII'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = os.environ['SECRET_KEY']  # Change this!
socketio = SocketIO(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=15)  # Access token expires in 15 minutes
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)  # Refresh token expires in 30 days


jwt = JWTManager(app)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app, version='1.0', title='API', description='API documentation', doc='/api-doc')

api.add_namespace(index, '/api')
api.add_namespace(auth, '/api/auth')


@jwt.token_in_blocklist_loader
def check_token_in_blacklist(jwt_header, jwt_data):
    # Check if the token is blacklisted
    jti = jwt_data['jti']
    blacklisted_token = db.blacklisted_tokens.find_one({'jti': jti})
    return blacklisted_token is not None





def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response', {'data': 'Server generated event'})







#for custom notification events
@socketio.event
def my_event(sid, message):
    socketio.emit('my_response', {'data': message['data']}, room=sid)

#for broadcasting notifications to all connected clients
@socketio.event
def my_broadcast_event(sid, message):
    socketio.emit('my_response', {'data': message['data']})

#allows clients to join specific rooms and recieve notification related to them
@socketio.event
def join(sid, message):
    socketio.enter_room(sid, message['room'])
    socketio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)

#allows clients to leave specific rooms and stop receiving notification related to them
@socketio.event
def leave(sid, message):
    socketio.leave_room(sid, message['room'])
    socketio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)

#closes a specific room and emits my_response event to clients of specified room
@socketio.event
def close_room(sid, message):
    socketio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    socketio.close_room(message['room'])

#for custom notification events in a specific room
@socketio.event
def my_room_event(sid, message):
    socketio.emit('my_response', {'data': message['data']}, room=message['room'])

#handles a client's request to disconnect
@socketio.event
def disconnect_request(sid):
    socketio.disconnect(sid)

#handles a clients connection to server
@socketio.event
def connect(sid, environ):
    socketio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

#tracks when a client disconnects from server
@socketio.event
def disconnect(sid):
    print('Client disconnected')











if '__main__' == __name__:
    socketio.run(app, debug=True)

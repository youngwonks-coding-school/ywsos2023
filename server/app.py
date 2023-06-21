import os
import datetime

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager

from routes.index import index
from routes.auth import auth
from dotenv import load_dotenv
from db import db


import socketio
import eventlet


async_mode='eventlet'
sio = socketio.Server(logger=True, async_mode=async_mode)
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
load_dotenv()
app.config['JSON_AS_ASCII'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = os.environ['SECRET_KEY']  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=15)  # Access token expires in 15 minutes
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)  # Refresh token expires in 30 days


thread = None


jwt = JWTManager(app)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app, version='1.0', title='API', description='API documentation',doc='/api-doc')

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
        sio.sleep(10)
        count += 1
        sio.emit('my_response', {'data': 'Server generated event'})







#for custom notification events
@sio.event
def my_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=sid)

#for broadcasting notifications to all connected clients
@sio.event
def my_broadcast_event(sid, message):
    sio.emit('my_response', {'data': message['data']})

#allows clients to join specific rooms and recieve notification related to them
@sio.event
def join(sid, message):
    sio.enter_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Entered room: ' + message['room']},
             room=sid)

#allows clients to leave specific rooms and stop receiving notification related to them
@sio.event
def leave(sid, message):
    sio.leave_room(sid, message['room'])
    sio.emit('my_response', {'data': 'Left room: ' + message['room']},
             room=sid)

#closes a specific room and emits my_response event to clients of specified room
@sio.event
def close_room(sid, message):
    sio.emit('my_response',
             {'data': 'Room ' + message['room'] + ' is closing.'},
             room=message['room'])
    sio.close_room(message['room'])

#for custom notification events in a specific room
@sio.event
def my_room_event(sid, message):
    sio.emit('my_response', {'data': message['data']}, room=message['room'])

#handles a client's request to disconnect
@sio.event
def disconnect_request(sid):
    sio.disconnect(sid)

#handles a clients connection to server
@sio.event
def connect(sid, environ):
    sio.emit('my_response', {'data': 'Connected', 'count': 0}, room=sid)

#tracks when a client disconnects from server
@sio.event
def disconnect(sid):
    print('Client disconnected')











if '__main__' == __name__:
    app.wsgi_app=socketio.WSGIApp(sio,app.wsgi_app)
    eventlet.wsgi.server(eventlet.listen(('127.0.0.1', 5000)), app, debug=True)
    
    
    








import os
import datetime

from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager

from routes.index import index
from routes.auth import auth
from routes.posts import posts
from routes.profile import profile
from dotenv import load_dotenv
from db import db


app = Flask(__name__)
load_dotenv()
app.config['JSON_AS_ASCII'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = os.environ['SECRET_KEY']  # Change this!
socketio = SocketIO(app, cors_allowed_origins="*")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes=15)  # Access token expires in 15 minutes
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=30)  # Refresh token expires in 30 days


jwt = JWTManager(app)
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}
api = Api(app, version='1.0', title='API', description='API documentation',doc='/api-doc', authorizations=authorizations)
api.swagger = {
'swagger': '2.0',
'info': {
'title': 'Your API',
'description': 'API description',
'version': '1.0'
},
'securityDefinitions': {
'Bearer': {
'type': 'apiKey',
'name': 'Authorization',
'in': 'header',
'description': 'Bearer access token'
}
},
'security': [{'Bearer': []}]
}


api.add_namespace(index, '/api')
api.add_namespace(auth, '/api/auth')
api.add_namespace(posts, '/api/posts')
api.add_namespace(profile, '/api/profile')


@jwt.token_in_blocklist_loader
def check_token_in_blacklist(jwt_header, jwt_data):
    # Check if the token is blacklisted
    jti = jwt_data['jti']
    blacklisted_token = db.blacklisted_tokens.find_one({'jti': jti})
    return blacklisted_token is not None





#whenever something is emitted on front end, create a @socketio.on("what was emitted") for a response



#handles a clients connection to server
@socketio.on("connect")
def connect():
    print("Client connected:")


#response to when my_event was emitted on client side
@socketio.on("my_event")
def connecting(x):
    print("my_event response")



#tracks when a client disconnects from server
@socketio.on("disconnect")
def disconnect(y):
    print('Client disconnected')










if '__main__' == __name__:
    socketio.run(app, host=os.environ["FLASK_HOST"], port=os.environ["FLASK_PORT"], debug=os.getenv("FLASK_DEBUG", "False") == "True")

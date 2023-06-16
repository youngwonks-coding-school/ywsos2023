import os
import datetime

from flask import Flask, jsonify
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


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)

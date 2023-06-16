from flask import Flask,jsonify
from flask_cors import CORS
from flask_restx import Api, Resource

from routes.index import index
from routes.auth import auth
from dotenv import load_dotenv
from db import db

from flask_jwt_extended import JWTManager
import datetime

app = Flask(__name__)
load_dotenv()
app.config['JSON_AS_ASCII'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# Set the secret key to sign the JWTs with
app.config['JWT_SECRET_KEY'] = '!o8qe8qwy#$$$asfhasjdfn'  # Change this!
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


api.add_namespace(index,'/api')
api.add_namespace(auth,'/api/auth')


@jwt.token_in_blocklist_loader
def check_token_in_blacklist(jwt_header, jwt_data):
    # Check if the token is blacklisted
    jti = jwt_data['jti']
    blacklisted_token = db.blacklisted_tokens.find_one({'jti': jti})
    return blacklisted_token is not None

if '__main__' == __name__:
    app.run(debug=True)
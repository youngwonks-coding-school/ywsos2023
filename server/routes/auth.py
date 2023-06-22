from flask import request, jsonify,make_response
from flask_restx import Namespace, Resource,fields
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from db import db
import os
import requests


from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token,get_jwt



auth= Namespace('auth', description='Authentication operations')
auth_model = auth.model('AuthModel', {
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})

update_model = auth.model('UpdateModel', {
    'email': fields.String(required=True, description='Email address'),
    'old_pass': fields.String(required=True, description='Old password'),
    'new_pass': fields.String(required=True, description='New password')
})


@auth.route('/register', methods=['POST'])
class Register(Resource):
    @auth.expect(auth_model, validate=True)
    def post(self):
        # Parse the request data
        email = auth.payload['email']
        password = auth.payload['password']
        date_created = datetime.datetime.utcnow()

        # Check if the user already exists
        if db.users.find_one({'email': email}):
            return {'message': 'User already exists'}, 409

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user document
        user = {'email': email, 'password': hashed_password, "date_created": date_created}
        db.users.insert_one(user)

        return {'message': 'User registered successfully'}, 201

@auth.route('/login', methods=['POST'])
class Login(Resource):
    @auth.expect(auth_model, validate=True)
    def post(self):
        # Parse the request data
        email = auth.payload['email']
        password = auth.payload['password']
        
        # Find the user document
        user = db.users.find_one({'email': email})

        # Check if the user exists and the password is correct
        if not user or not check_password_hash(user['password'], password):
            return {'message': 'Invalid email or password'}, 401

        # Generate access and refresh tokens
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        db.sessions.add_one({"ip": request.remote_addr, "access_token": access_token, "refresh_token": refresh_token, "email": email})

        return {'message': 'Successfully Logged in.',"access_token":access_token,"refresh_token":refresh_token}, 200

@auth.route('/verify', methods=['POST'])
class Verify(Resource):
    @jwt_required()
    @auth.doc(security="Bearer")
    def post(self):
        email = get_jwt_identity()
        print(email)
        return {'message': 'Access Token is valid', 'email': email}, 200
    
@auth.route('/refresh', methods=['POST'])
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return {'message':'new access token created using refresh token','access_token': new_access_token}, 200
        
@auth.route('/logout', methods=['POST'])
class Logout(Resource):
    @jwt_required()
    def post(self):
        # Add the access token to the blacklist
        jti = get_jwt()['jti']
        db.blacklisted_tokens.insert_one({'jti': jti})

        return {'message': 'Successfuly logged out.'}, 200
    

@auth.route('/update_password', methods=['POST'])
class UpdatePassword(Resource):
    @auth.expect(update_model, validate=True)
    def post(self):
        email = auth.payload['email']
        old_password = auth.payload['old_pass']
        new_password = auth.payload['new_pass']
        user = db.users.find_one({"email": email})
        if not user or not check_password_hash(user['password'], old_password):
            return {'message': 'Invalid email or password'}, 401
        password = generate_password_hash(new_password)
        db.users.update_one({"email": email}, {"$set": {"password": password, "updated_at": datetime.datetime.utcnow()}})

        return {"message": 'Successfuly update password'}, 200
    
@auth.route('/get_sessions', methods=['GET'])
class GetSessions(Resource):
    def get(self):
        return db.sessions.get()
    

@auth.route('/get_sessions_for_user', methods=['GET'])
class GetSessionsForUser(Resource):
    @jwt_required()
    def get(self):
        return db.sessions.get({'email': get_jwt_identity()})

@auth.route('/logout_specific')
class LogoutSpecific(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        db.blacklisted_tokens.insert_one({'jti': jti})

        return {"message": "Account logged out"}, 200


#Make your you have a YELP_API_KEY in .env
@auth.route('/profile_data', methods=['POST'])
class ProfileData(Resource):
    def post(self):
        data = request.get_json()
        url = "https://api.yelp.com/v3/businesses/search"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + os.environ.get("YELP_API_KEY"),
        }
        
        params = {
            "term": data["name"],
            "location": data["address"]
        }
        

        response = requests.get(url, params=params, headers=headers)


        return {'message': response.text}, 200
    


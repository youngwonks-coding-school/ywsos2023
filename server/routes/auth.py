from flask import request, jsonify,make_response, session, current_app
from flask_restx import Namespace, Resource,fields
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from db import db
import json
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
        
        data = request.get_json()
        business_type = data['business_type']
        
        date_created = datetime.utcnow()

        # Check if the user already exists
        if db.users.find_one({'email': email}):
            return {'message': 'User already exists'}, 409

        # Hash the password
        hashed_password = generate_password_hash(password)

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        db.sessions.insert_one({"ip": request.remote_addr, "access_token": access_token, "refresh_token": refresh_token, "email": email})

        
        
        # Create a new user document
        user = {'email': email, 'password': hashed_password, 'business_type':business_type, "date_created": date_created}
        db.users.insert_one(user)
        

        return {'message': 'User registered successfully', "access_token":access_token,"refresh_token":refresh_token}, 201

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
        
        db.sessions.insert_one({"ip": request.remote_addr, "access_token": access_token, "refresh_token": refresh_token, "email": email})
        

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
        session.clear()
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
        print("Getting Sessions")
        #get current user email
        session = db.sessions.find_one({'email': get_jwt_identity()})
        
        #get associated_restaurants id (no need for all data)
        associated_restaurants_ids = []
        document = db.restaurants.find_one({'email': get_jwt_identity()})
        if document: 
            associated_restaurants_ids = document.get('associated_restaurants_ids')
            #Object ID not json serializable so I make it string 
            associated_restaurants_ids = [str(oid) for oid in associated_restaurants_ids]

        #convert object id to string
        return jsonify({'associated_restaurants_ids': associated_restaurants_ids, 'email': get_jwt_identity()})

@auth.route('/logout_specific')
class LogoutSpecific(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        db.blacklisted_tokens.insert_one({'jti': jti})

        return {"message": "Account logged out"}, 200


@auth.route('/session_lifetime')
class SessionLifetime(Resource):
    def get(self):
        session_lifetime = current_app.config['PERMANENT_SESSION_LIFETIME']
        return {'session_lifetime': session_lifetime.total_seconds()}, 200

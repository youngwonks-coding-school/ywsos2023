from flask import request, jsonify,make_response
from flask_restx import Namespace, Resource,fields
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from db import db
import os

from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token,get_jwt



auth= Namespace('auth', description='Authentication operations')
auth_model = auth.model('AuthModel', {
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})




@auth.route('/register', methods=['POST'])
class Register(Resource):
    @auth.expect(auth_model, validate=True)
    def post(self):
        # Parse the request data
        email = auth.payload['email']
        password = auth.payload['password']

        # Check if the user already exists
        if db.users.find_one({'email': email}):
            return {'message': 'User already exists'}, 409

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user document
        user = {'email': email, 'password': hashed_password}
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

        return {'message': 'Successfully Logged in.',"access_token":access_token,"refresh_token":refresh_token}, 200

@auth.route('/verify', methods=['POST'])
class Verify(Resource):
    @jwt_required()
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



    


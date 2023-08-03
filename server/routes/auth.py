from flask import request, jsonify, session, current_app
from flask_restx import Namespace, Resource, fields
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from db import db


from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token,get_jwt



auth= Namespace('auth', description='Authentication operations')
auth_model = auth.model('AuthModel', {
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password')
})
register_model = auth.model('RegisterModel', {
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'name': fields.String(required=True, description='Name'),
})
update_model = auth.model('UpdateModel', {
    'email': fields.String(required=True, description='Email address'),
    'old_pass': fields.String(required=True, description='Old password'),
    'new_pass': fields.String(required=True, description='New password')
})


@auth.route('/register', methods=['POST'])
class Register(Resource):
    @auth.expect(register_model, validate=True)
    def post(self):
        data = request.get_json()
        name = data['name']
        email = auth.payload['email']
        password = auth.payload['password']
        date_created = datetime.utcnow()

        # Check if exists
        if db.users.find_one({'email': email}):
            return {'message': 'User already exists'}, 409

        hashed_password = generate_password_hash(password)
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        db.sessions.insert_one({"ip": request.remote_addr, "access_token": access_token, "refresh_token": refresh_token, "email": email})

        # New user created
        user = {'email': email, 'password': hashed_password, 'name': name, "date_created": date_created, "food_banks": [], "restaurants": []}
        db.users.insert_one(user)
        
        print("Registered User Successfully")
        return {'message': 'User registered successfully', "access_token": access_token, "refresh_token": refresh_token}, 201


@auth.route('/login', methods=['POST'])
class Login(Resource):
    @auth.expect(auth_model, validate=True)
    def post(self):
        email = auth.payload['email']
        password = auth.payload['password']

        # Validate user
        user_data = db.users.find_one({'email': email})
        if not user_data or not check_password_hash(user_data['password'], password):
            return {'message': 'Invalid email or password'}, 401

        # Generate access and refresh tokens
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        # Insert session data into session collection
        db.sessions.insert_one({
            "ip": request.remote_addr,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "email": email
        })

        business_type = user_data['business_type']
        return {
            'message': 'Successfully logged in.',
            "access_token": access_token,
            "refresh_token": refresh_token,
            "business_type": business_type
        }, 200
        
        
@auth.route('/verify', methods=['POST'])
class Verify(Resource):
    @jwt_required()
    @auth.doc(security="Bearer")
    def post(self):
        email = get_jwt_identity()
        return {'message': 'Access Token is valid', 'email': email}, 200
    
@auth.route('/refresh', methods=['POST'])
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        print("error refreshing")
        current_user = get_jwt_identity()
        jti = get_jwt()['jti']

        if db.blacklisted_tokens.find_one({'jti': jti}) is not None:
            return {'message': 'use a token that is not blacklisted'}, 401

        new_access_token = create_access_token(identity=current_user)
        return {'message':'new access token created using refresh token','access_token': new_access_token}, 200
        
@auth.route('/logout', methods=['POST'])
class Logout(Resource):
    @jwt_required(refresh=True)
    def post(self):
        # Add the refresh token to the blacklist
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

        # Validate user and old password
        user_data = db.users.find_one({"email": email})
        if not user_data or not check_password_hash(user_data['password'], old_password):
            return {'message': 'Invalid email or password'}, 401

        # Update password
        password = generate_password_hash(new_password)
        db.users.update_one(
            {"email": email},
            {"$set": {"password": password, "updated_at": datetime.datetime.utcnow()}}
        )

        return {"message": 'Successfully updated password'}, 200


    
@auth.route('/get_business_type', methods=['GET'])
class GetBusinessType(Resource):
    @jwt_required()
    def get(self):
        user = db.users.find_one({"email": get_jwt_identity()})
        if not user:
            return {'message': 'Invalid email or password'}, 401
        return {"business_type": user['business_type']}, 200
    
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
        return session, 200

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

from flask_restx import  Namespace,Resource
from flask import request, jsonify,make_response
import requests 
from db import db
import os

index = Namespace('', description='Open Routes')

@index.route('/', methods=['GET'])
class Ping(Resource):
    def get(self):
        return jsonify('This is the content to be used for the homepage!')


#Make your you have a YELP_API_KEY in .env (INSTRUCTIONS IN README)
@index.route('/get_restaurants', methods=['POST'])
class GetRestaurants(Resource):
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
    
@index.route("/set_restaurant", methods=["POST"])
class SetRestaurant(Resource):
    def post(self):
        users = db['users']
        data = request.get_json()
        restaurant_data = data["selected"]
        current_user = data["current_user"]
        
        print(f"Received restaurant data: {restaurant_data}")
        print(f"Current user: {current_user}")
        
        user = users.find_one({'email': current_user})
        if user:
            user['restaurant'] = restaurant_data
            users.update_one({'_id': user['_id']}, {'$set': user})
            return {'message': "hey fatass"}, 200
            
        
        
        


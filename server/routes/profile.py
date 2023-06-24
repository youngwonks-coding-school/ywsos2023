from flask_restx import  Namespace,Resource
from flask import request, jsonify,make_response
import requests 
from db import db
import os

profile = Namespace('profile', description='Profile Management')


#Make your you have a YELP_API_KEY in .env (INSTRUCTIONS IN README)
@profile.route('/get_restaurants', methods=['POST'])
class GetRestaurants(Resource):
    def post(self):
        #Use yelp api to get possible restaurants based on user inputed data
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
    
@profile.route("/set_restaurant", methods=["POST"])
class SetRestaurant(Resource):
    #after user clicks on desired restaurant, add data to db under user collection
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
            
@profile.route("/previous_restaurant", methods=["GET"])
class PrevRestaurant(Resource):    
    # If user already has entered a restaurant we will display
    def get(self):
        users = db['users']
        #need localstorage email
        current_user = request.args.get('current_user')  
        
        user = users.find_one({'email': current_user})
        if user:
            restaurant_data = user.get('restaurant')
            #send data
            if restaurant_data:
                return restaurant_data
            else:
                return False
        else:
            return False
        
        
              

        
        
        


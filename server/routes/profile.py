from flask_restx import  Namespace,Resource
from flask import request, jsonify,make_response
import json
import requests 
from db import db
import uuid
import os
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token,get_jwt

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
    
@profile.route("/add_restaurant", methods=["POST"])
class AddRestaurant(Resource):
    #after user clicks on desired restaurant, add data to db under user collection
    def post(self):
        data = request.get_json()
        restaurant_data = data["selected"]
        current_user = data["current_user"]
        query = {"email": current_user}
        
        id = str(uuid.uuid4())
        restaurant_data["id"] = id
        
        """
        the idea here is that for every user they may be associated with more than one restaurant
        so we will have a list of all restaurants and the data + id, that the user is associated with
        we also set in db.sessions the current restaurant that the user is associated with
        """
        
        #add restaurant selected to list of user associated restaurants
        restaurants = db.get_collection('restaurants')
        if restaurants.find_one(query): 
            restaurants.update_one(query, {"$addToSet": {"associated_restaurants": restaurant_data}})
            restaurants.update_one(query, {"$addToSet": {"associated_restaurants_ids": id}})
        else: 
            document = {"email": current_user, "associated_restaurants": [restaurant_data], "associated_restaurants_ids": [id]}
            restaurants.insert_one(document)
            
        #add current restaurant user is associated with
        sessions = db.get_collection('sessions')
        if sessions.find_one(query):
            sessions.update_one(query, {"$set": {"current_restaurant": id}})
        else:
            document = {"email": current_user, "current_restaurant": id}
            sessions.insert_one(document)
        

        return {'message': "set restaurant data"}, 200
            
@profile.route("/previous_restaurant", methods=["GET"])
class PrevRestaurant(Resource):    
    """
    When page loads, we check for all restaurants associated with user and return 
    """
    def get(self):
        #get the current restaurant id you are associated with
        current_user = request.args.get('current_user')  
        sessions = db.get_collection('sessions')
        current_restaurant = sessions.find_one({"email": current_user})['current_restaurant']
        print("current_restaurant " + current_restaurant)
        
        # get info about current restaurant
        restaurants = db.get_collection('restaurants')
        existing_doc = restaurants.find_one({"email": current_user})
        if existing_doc:
            associated_restaurants = existing_doc.get("associated_restaurants", [])
            for rest in associated_restaurants:
                if rest.get("id") == current_restaurant:
                    response_data = {'current_restaurant_info': rest, "associated_restaurants": associated_restaurants}
                    response_data = json.dumps(response_data, default=vars)
                    return response_data, 200
                
                
        
        
        
        
        
        
        
        
              

        
        
        


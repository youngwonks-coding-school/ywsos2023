from flask_restx import  Namespace,Resource
from flask import request, jsonify,make_response
from bson import ObjectId
import json
import requests 
from db import db
import os
from flask_jwt_extended import jwt_required,get_jwt_identity,create_access_token,create_refresh_token,get_jwt

profile = Namespace('profile', description='Profile Management')

#handle creating response with objects (vars() default doesnt always work)
def custom_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


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
        
        #add user _id to restaurant document _id **linked**
        user_id = db.get_collection("users").find_one(query)["_id"]
        
        #add _id for each new associated restaurant
        _id = ObjectId()
        restaurant_data["_id"] = _id
        
        
        print("user_id: " + str(user_id))
        print("restaurant id: " + str(_id))
        
        """
        the idea here is that for every user they may be associated with more than one restaurant
        so we will have a list of all restaurants and the data + id, that the user is associated with
        we also set in db.sessions the current restaurant that the user is associated with
        """
        
        #add restaurant selected to list of user associated restaurants
        restaurants = db.get_collection('restaurants')
        if restaurants.find_one(query): 
            restaurants.update_one(query, {"$addToSet": {"associated_restaurants": restaurant_data}})
            restaurants.update_one(query, {"$addToSet": {"associated_restaurants_ids": _id}})
        else: 
            document = {"_id":user_id, "email": current_user, "associated_restaurants": [restaurant_data], "associated_restaurants_ids": [_id]}
            restaurants.insert_one(document)
            
        #add current restaurant user is associated with
        sessions = db.get_collection('sessions')
        if sessions.find_one(query):
            sessions.update_one(query, {"$set": {"current_restaurant": _id}})
        else:
            document = {"email": current_user, "current_restaurant": _id}
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
        
        # get info about current restaurant and info about users associated_restaurants
        restaurants = db.get_collection('restaurants')
        existing_doc = restaurants.find_one({"email": current_user})
        if existing_doc:
            associated_restaurants = existing_doc.get("associated_restaurants", [])
            for rest in associated_restaurants:
                if rest.get("_id") == current_restaurant:
                    response_data = {'current_restaurant_info': rest, "associated_restaurants": associated_restaurants}
                    response_data = json.dumps(response_data, default=custom_serializer)
                    return response_data, 200
                
                
        
        
        
        
        
        
        
        
              

        
        
        


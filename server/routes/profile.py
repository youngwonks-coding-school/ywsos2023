import json
import os
from bson import ObjectId

import requests
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource

from db import db

profile = Namespace('profile', description='Profile Management')

# Handle creating response with objects (vars() default doesnt always work)
def custom_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


# Create YELP_API_KEY in .env (INSTRUCTIONS IN README)
# Use YELP API to get restaurants 
@profile.route('/get_restaurants', methods=['POST'])
class GetRestaurants(Resource):
    def post(self):
        data = request.get_json()['data']
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
    
    
"""
User selects restaurant card -> 
For every user, they may be associated with more than one restaurant
We have list of all restaurant (data,id) that the user is associated with

users : {p1: _id1, p2: _id2}
restaurant : 
{
    p1: _id1, associated_restaurants: [{r1, rid1}, {r2, rid2}, {r3, rid3}], associated_restaurants_ids: [rid1, rid2, rid3],
    p2: _id2, associated_restaurants: [{r1, rid1}, {r2, rid2}, {r3, rid3}], associated_restaurants_ids: [rid1, rid2, rid3]
}
"""

@profile.route("/add_restaurant", methods=["POST"])
class AddRestaurant(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        restaurant_data = data["selected"]

        current_user = get_jwt_identity()
        query = {"email": current_user}

        # Link USER ID to the user's restaurant document
        user_id = db.get_collection("users").find_one(query)["_id"]

        # Add a new _id to the restaurant data
        _id = ObjectId()
        restaurant_data["_id"] = _id

        restaurants = db.get_collection('restaurants')
        if restaurants.find_one(query):
            restaurants.update_one(query, {"$addToSet": {"associated_restaurants": restaurant_data}})
            restaurants.update_one(query, {"$addToSet": {"associated_restaurants_ids": _id}})
        else:
            document = {
                "_id": user_id,
                "email": current_user,
                "associated_restaurants": [restaurant_data],
                "associated_restaurants_ids": [_id]
            }
            restaurants.insert_one(document)

        print("Added restaurant:", str(_id))
        return {'current_restaurant': str(_id)}, 200
            
            
"""
When profile loads ->
Get current restaurant data to display on profile page
Check for all restaurants associated with the user and return the data
Will be used to display restaurant management dropdown + switch data on profile page
"""
@profile.route("/previous_restaurant", methods=["GET"])
class PrevRestaurant(Resource):
    @jwt_required()
    def get(self):
        current_restaurant_id = request.args.get('current_restaurant')
        current_user = get_jwt_identity()
        restaurants_collection = db.get_collection('restaurants')
        user_document = restaurants_collection.find_one({"email": current_user})
        
        if user_document:
            associated_restaurants = user_document.get("associated_restaurants", [])
            restaurant_info = get_associated_restaurant(associated_restaurants, current_restaurant_id)
            
            if restaurant_info:
                response_data = {
                    "current_restaurant_info": restaurant_info,
                    "associated_restaurants": associated_restaurants
                }
                response_json = json.dumps(response_data, default=custom_serializer)
                print("Previous restaurant data accessed")
                return response_json, 200

        return "Restaurant not found", 404


def get_associated_restaurant(restaurants, restaurant_id):
    for restaurant in restaurants:
        if restaurant.get("_id") == ObjectId(restaurant_id):
            return restaurant
    
    return None

                
@profile.route("/get_associated_restaurant_ids", methods=["GET"])
class GetAssociatedRestIds(Resource):
    @jwt_required()
    def get(self):
        #get associated_restaurants id (no need for all data)
        associated_restaurants_ids = []
        document = db.restaurants.find_one({'email': get_jwt_identity()})
        if document: 
            associated_restaurants_ids = document.get('associated_restaurants_ids')
            #Object ID not json serializable so I make it string 
            associated_restaurants_ids = [str(oid) for oid in associated_restaurants_ids]

        print("Retrieved Associated Restaurant IDs")
        return jsonify({'associated_restaurants_ids': associated_restaurants_ids, 'email': get_jwt_identity()})

        
              

        
        
        


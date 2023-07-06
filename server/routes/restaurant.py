import json
import os

#uuid instead of json because couldnt find vue package to support ObjectID
import uuid
from bson import ObjectId
from bson.binary import Binary

import requests
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource
from uuid import UUID

from db import db

restaurant = Namespace('restaurant', description='Restaurant Management')

# Handle creating response with objects (vars() default doesnt always work)
def custom_serializer(obj):
    if isinstance(obj, (UUID, ObjectId)):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")



# Create YELP_API_KEY in .env (INSTRUCTIONS IN README)
# Use YELP API to get restaurants 
@restaurant.route('/get_restaurants', methods=['POST'])
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

@restaurant.route("/add_restaurant", methods=["POST"])
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
@restaurant.route("/get_associated_restaurants_data", methods=["GET"])
class GetAssociatedRestsData(Resource):
    @jwt_required()
    def get(self):
        current_restaurant_id = request.args.get('current_restaurant')
        current_user = get_jwt_identity()
        restaurants = db.get_collection('restaurants')
        user_document = restaurants.find_one({"email": current_user})
        
        if user_document:
            associated_restaurants = user_document.get("associated_restaurants", [])
            restaurant_info = get_current_restaurant_data(associated_restaurants, current_restaurant_id)
            
            if restaurant_info:
                response_data = {
                    "current_restaurant_info": restaurant_info,
                    "associated_restaurants_data": associated_restaurants
                }
                response_json = json.dumps(response_data, default=custom_serializer)
                print("Previous restaurant data accessed")
                return response_json, 200

        return "Restaurant not found", 404


def get_current_restaurant_data(restaurants, restaurant_id):
    for restaurant in restaurants:
        if restaurant.get("_id") == ObjectId(restaurant_id):
            return restaurant
    
    return None


@restaurant.route("/get_associated_restaurants_ids", methods=["GET"])
class GetAssociatedRestsIds(Resource):
    @jwt_required()
    def get(self):
        #get associated_restaurants id (no need for all data)
        current_user = get_jwt_identity()
        associated_restaurants_ids = db.restaurants.find_one({'email': current_user}, {'associated_restaurants_ids': 1, '_id': 0})
        if associated_restaurants_ids:
            #Object ID not json serializable so I make it string 
            associated_restaurants_ids = [str(oid) for oid in associated_restaurants_ids[['associated_restaurants_ids']]]

        print("Retrieved Associated Restaurant IDs")
        return jsonify({'associated_restaurants_ids': associated_restaurants_ids})

        

@restaurant.route("/add_food", methods=["POST"])
class AddFood(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_restaurant_id = ObjectId(data["current_restaurant_id"])
        
        food_data = data["food_data"]
        food_data["_id"] = uuid.UUID(data["_id"])
        
        uuid_bytes = food_data["_id"].bytes
        bson_binary = Binary(uuid_bytes, 3)
        
        restaurants = db.get_collection('restaurants')
        
        # Find the document that contains the current restaurant id in associated_restaurants_ids
        update_query = {
            "associated_restaurants_ids": current_restaurant_id
        }
        matching_documents_count = restaurants.count_documents(update_query)
        if matching_documents_count == 0:
            return {"message": "Restaurant doesn't exist"}, 404
        
        # Using that document, find the restaurant in associated_restaurants that has the current restaurant id
        matching_restaurant_query = {
            "associated_restaurants._id": current_restaurant_id,
            "associated_restaurants.food_data._id": bson_binary
        }
        
        matching_restaurant = restaurants.find_one(matching_restaurant_query)
        
        if matching_restaurant is None:
            # Push 
            restaurants.update_one(
                {
                    "associated_restaurants_ids": current_restaurant_id
                },
                {
                    "$push": {
                        "associated_restaurants.$.food_data": food_data
                    }
                }
            )
            
            return {"message": "Food added successfully"}, 200
        
        else:
            
            # Update 
            restaurants.update_one(
                {
                    "associated_restaurants._id": current_restaurant_id,
                    "associated_restaurants.food_data._id": bson_binary
                },
                {
                    "$set": {
                        "associated_restaurants.$[].food_data.$": food_data
                    }
                }
            )
            
            return {"message": "Food updated successfully"}, 200



@restaurant.route("/delete_food", methods=["POST"])
class DeleteFood(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        current_restaurant_id = ObjectId(data["current_restaurant_id"])
        food_id =  uuid.UUID(data["_id"])
        
        restaurants = db.get_collection('restaurants')
        
        #find which doc contains current rest id is in associated_restaurants_ids
        #using that doc use . to find the restaurant in associated_restaurants has current rest id
        #remove that restaurant's food data that has food_id
        restaurants.update_one(
            {"associated_restaurants_ids": {"$in": [current_restaurant_id]}, "associated_restaurants._id": current_restaurant_id},
            {"$pull": {"associated_restaurants.$.food_data": {"_id": food_id}}}
        )
        

        print("Deleted food from restaurant:", str(current_restaurant_id))
        return "Deleted food from restaurant", 200
        
        
        

@restaurant.route("/get_food_data", methods=["POST"])
class GetFoodData(Resource):
    def post(self):
        current_restaurant_id = request.get_json()['current_restaurant_id']
        restaurants = db.get_collection('restaurants')
        user_restaurant = restaurants.find_one(
            {"associated_restaurants_ids": {"$in": [ObjectId(current_restaurant_id)]}},
            projection={"associated_restaurants.$": 1}
        )
        food_data = user_restaurant.get("associated_restaurants", [{}])[0].get("food_data", [])
        if food_data:
            print(type(food_data))
            print(food_data)
            if not isinstance(food_data, list):
                food_data = [food_data]
                
        return jsonify({'food_data': food_data})
            
            
        
        
        

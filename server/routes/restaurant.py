import json
import os

# uuid instead of json because couldnt find vue package to support ObjectID
import uuid
from bson import ObjectId, json_util
from bson.binary import Binary

import requests
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from uuid import UUID

from db import db

restaurant = Namespace('restaurant', description='Restaurant Management')
restaurant_model = restaurant.model('Restaurant', {
    "name": fields.String(required=True, description="Restaurant Name"),
    "address": fields.String(required=True, description="Address")
})
food_model = restaurant.model('Food', {
    "food": fields.String(required=True, description="Food Name"),
    "amount": fields.Float(required=True, description="Amount of food in lbs"),
    "_id": fields.String(required=True, description="Unique ID"),
})
delete_food_model = restaurant.model('DeleteFood', {
    "_id": fields.String(required=True, description="Unique ID"),
    "food": fields.String(required=True, description="Food to be deleted"),
})


# Handle creating response with objects (vars() default doesnt always work)
def custom_serializer(obj):
    if isinstance(obj, (UUID, ObjectId)):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


@restaurant.route('/yelp/<name>/<address>', methods=['GET'])
class Yelp(Resource):
    def get(self, name, address):
        url = "https://api.yelp.com/v3/businesses/search"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + os.environ.get("YELP_API_KEY"),
        }

        params = {
            "term": name,
            "location": address,
        }

        response = requests.get(url, params=params, headers=headers)

        return {'message': response.text}, 200


@restaurant.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
class Restaurant(Resource):
    def get(self):
        return json_util.dumps(list(db.restaurants.find({})))

    @jwt_required()
    @restaurant.doc(security='Bearer')
    @restaurant.expect(restaurant_model, validate=True)
    def post(self):

        data = request.get_json()
        name = data['name']
        address = data['address']
        current_user = get_jwt_identity()
        query = {"email": current_user}
        user_id = db.get_collection("users").find_one(query)["_id"]

        document = {
            "name": name,
            "address": address,
            "owner": user_id,
            "associated_users": [],
            "food": {}
        }
        restaurant = db.restaurants.insert_one(document)
        db.users.update_one(query, {"$addToSet": {"restaurants": restaurant.inserted_id}})
        return {'current_restaurant': str(restaurant.inserted_id)}, 200


@restaurant.route('/<id>')
class RestaurantM(Resource):
    def get(self, id):
        return json_util.dumps(db.restaurants.find_one({"_id": ObjectId(id)}))


@restaurant.route('/food', methods=['POST', 'DELETE'])
class Food(Resource):
    @jwt_required()
    @restaurant.doc(security='Bearer')
    @restaurant.expect(food_model, validate=True)
    def post(self):
        data = request.get_json()
        food = data["food"]
        amount = data["amount"]
        id = data["_id"]
        db.restaurants.update_one({"_id": ObjectId(id)}, {"$set": {"food."+food: amount}})
        return "Food updated successfully", 200

    @jwt_required()
    @restaurant.doc(security='Bearer')
    @restaurant.expect(delete_food_model, validate=True)
    def delete(self):
        id = request.get_json()["_id"]
        food = request.get_json()["food"]
        db.restaurants.update_one({"_id": ObjectId(id)}, {"$unset": {"food."+food: ""}})
        return "Deleted food from restaurant", 200



def get_current_restaurant_data(restaurants, restaurant_id):
    for restaurant in restaurants:
        if restaurant.get("_id") == ObjectId(restaurant_id):
            return restaurant

    return None

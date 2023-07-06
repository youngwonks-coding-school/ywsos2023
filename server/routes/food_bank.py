import json
import os
from bson import ObjectId

import requests
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource
from uuid import UUID
from db import db

food_bank = Namespace('food_bank', description='Food Bank Management')

# Handle creating response with objects (vars() default doesnt always work)
def custom_serializer(obj):
    if isinstance(obj, (UUID, ObjectId)):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


@food_bank.route('/add_food_bank', methods=['POST'])
class AddFoodBank(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        food_bank_data = data["selected"]

        current_user = get_jwt_identity()
        query = {"email": current_user}  
        
        # Link USER ID to the user's food bank document
        user_id = db.get_collection("users").find_one(query)["_id"]
        
        # Add a new _id to the food bank data
        _id = ObjectId()
        food_bank_data["_id"] = _id
        
        food_banks = db.get_collection('food_banks')
        if food_banks.find_one(query):
            food_banks.update_one(query, {"$addToSet": {"associated_food_banks": food_bank_data}})
            food_banks.update_one(query, {"$addToSet": {"associated_food_banks_ids": _id}})
        else:
            document = {
                "_id": user_id,
                "email": current_user,
                "associated_food_banks": [food_bank_data],
                "associated_food_banks_ids": [_id]
            }
            food_banks.insert_one(document)

        print("Added Food Bank:", str(_id))
        return {'current_food_bank': str(_id)}, 200
    
    
"""
When profile loads ->
Get current food bank data to display on profile page
Check for all food banks associated with the user and return the data
Will be used to display food bank management dropdown + switch data on profile page
"""

@food_bank.route('/get_associated_food_banks_data', methods=['GET'])
class GetAssociatedFoodBanksData(Resource):
    @jwt_required()
    def get(self):
        current_food_bank_id = request.args.get('current_food_bank')
        current_user = get_jwt_identity()
        food_banks = db.get_collection('food_banks')
        user_document = food_banks.find_one({"email": current_user})
        
        if user_document:
            associated_food_banks_data = user_document.get("associated_food_banks", [])
            food_bank_info = get_current_food_bank_data(associated_food_banks_data, current_food_bank_id)
            
            if food_bank_info:
                response_data = {
                    "current_food_bank_info": food_bank_info,
                    "associated_food_banks_data": associated_food_banks_data,
                }
                response_json = json.dumps(response_data, default=custom_serializer)
                print("Previous food bank data accessed")
                return response_json, 200
            else:
                return {"message": "No food bank found"}, 404
        else:
            return {"message": "No food bank found"}, 404   
        

def get_current_food_bank_data(associated_food_banks, current_food_bank_id):
    for food_bank in associated_food_banks:
        if str(food_bank["_id"]) == current_food_bank_id:
            return food_bank
    return None


@food_bank.route("/get_associated_food_banks_ids", methods=["GET"])
class GetAssociatedFoodBanksIds(Resource):
    @jwt_required()
    def get(self):
        #get associated_restaurants id (no need for all data)
        current_user = get_jwt_identity()
        associated_food_banks_ids = []
        
        associated_food_banks_ids = db.restaurants.find_one({'email': current_user}, {'associated_food_banks_ids': 1, '_id': 0})
        if associated_food_banks_ids:
            #Object ID not json serializable so I make it string 
            associated_food_banks_ids = [str(oid) for oid in associated_food_banks_ids[['associated_food_banks_ids']]]

        response_json = {
            'associated_food_banks_ids': associated_food_banks_ids,
        }
        response_json = json.dumps(associated_food_banks_ids, default=custom_serializer)
        print("Retrieved Associated Food Bank IDs")
        return response_json, 200
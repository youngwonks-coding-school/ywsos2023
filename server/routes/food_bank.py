import json
import os
from bson import ObjectId, json_util

import requests
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from uuid import UUID
from db import db

food_bank = Namespace('food_bank', description='Food Bank Management')
bank_model = food_bank.model('FoodBank', {
    "name": fields.String(required=True, description="Name of the food bank"),
    "address": fields.String(required=True, description="Address of the food bank")
})


# Handle creating response with objects (vars() default doesnt always work)
def custom_serializer(obj):
    if isinstance(obj, (UUID, ObjectId)):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


@food_bank.route('/<current_food_bank>', methods=['GET'])
class Bank(Resource):
    @jwt_required()
    @food_bank.doc(security='Bearer')
    def get(self, current_food_bank):
        return json_util.dumps(db.food_banks.find_one({"_id": ObjectId(current_food_bank)}))


@food_bank.route('/', methods=['GET', 'POST'])
class BankM(Resource):
    @jwt_required()
    @food_bank.doc(security='Bearer')
    @food_bank.expect(bank_model, validate=True)
    def post(self):
        data = request.get_json()
        name = data["name"]
        address = data["address"]
        user = get_jwt_identity()
        query = {"email": user}
        user_id = db.users.find_one(query)["_id"]

        document = {
            "name": name,
            "address": address,
            "owner": user_id,
            "associated_users": [],
        }
        bank = db.food_banks.insert_one(document)
        db.users.update_one(query, {"$addToSet": {"food_banks": bank.inserted_id}})
        return {'current_food_bank': str(bank.inserted_id)}, 200

    def get(self):
        # get associated_restaurants id (no need for all data)
        return json_util.dumps(db.food_banks.find({}))


def get_current_food_bank_data(associated_food_banks, current_food_bank_id):
    for food_bank in associated_food_banks:
        if str(food_bank["_id"]) == current_food_bank_id:
            return food_bank
    return None


import datetime
import json

from bson import json_util, ObjectId
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from db import db

posts = Namespace("posts", description="Operations related to posts")
post_model = posts.model("Post", {
    "title": fields.String(required=True, description="Title of the post"),
    "description": fields.String(required=True, description="Description of the post"),
    "location": fields.String(required=True, description="Location of the food bank or restaurant"),
    "food": fields.String(required=True, description="Type of food"),
    "quantity": fields.Integer(required=True, description="Quantity of the food"),
})


@posts.route('/restaurant-post', methods=["POST", "GET", "PUT", "DELETE"])
class ResturantPostM(Resource):
    def get(self):
        return json.loads(json_util.dumps(list(db.restaurant_posts.find({}))))

    @jwt_required()
    @posts.doc(security="Bearer")
    @posts.expect(post_model, validate=True)
    def post(self):
        email = get_jwt_identity()

        post = {
            "title": request.json["title"],
            "description": request.json["description"],
            "location": request.json["location"],
            "time": str(datetime.datetime.now()),
            "user": email,
            "food": request.json["food"],
            "quantity": request.json["quantity"],
        }

        db.restaurant_posts.insert_one(post)

        return {"message": "Post created successfully."}



@posts.route('/restaurant-post/<id>', methods=["POST", "GET", "PUT", "DELETE"])
class RestaurantPost(Resource):
    @jwt_required()
    @posts.doc(security="Bearer")
    @posts.expect(post_model, validate=True)
    def put(self, id):
        email = get_jwt_identity()

        post = {
            "title": request.json["title"],
            "description": request.json["description"],
            "location": request.json["location"],
            "time": str(datetime.datetime.now()),
            "user": email,
            "food": request.json["food"],
            "quantity": request.json["quantity"],
        }

        db.restaurant_posts.update_one({"_id": ObjectId(id)}, {"$set": {"title": post["title"], "description": post["description"], "location": post["location"], "time": post["time"], "quantity": post["quantity"], "food": post["food"]}})

        return {"message": "Post updated successfully."}

    def get(self, id):
        return json.loads(json_util.dumps(list(db.restaurant_posts.find({"_id": ObjectId(id)}))))

    def delete(self, id):
        db.restaurant_posts.delete_one({"_id": ObjectId(id)})
        return {"message": "Post deleted successfully."}


@posts.route('/bank-post', methods=["POST", "GET", "PUT", "DELETE"])
class BankPostM(Resource):
    def get(self):
        return json.loads(json_util.dumps(list(db.bank_posts.find({}))))

    @jwt_required()
    @posts.doc(security="Bearer")
    @posts.expect(post_model, validate=True)
    def post(self):
        email = get_jwt_identity()
        print(email)

        post = {
            "title": request.json["title"],
            "description": request.json["description"],
            "location": request.json["location"],
            "time": str(datetime.datetime.now()),
            "user": email,
            "food": request.json["food"],
            "quantity": request.json["quantity"],
        }

        db.bank_posts.insert_one(post)

        return {"message": "Post created successfully."}


@posts.route('/bank-post/<id>', methods=["POST", "GET", "PUT", "DELETE"])
class BankPost(Resource):

    @jwt_required()
    @posts.doc(security="Bearer")
    @posts.expect(post_model, validate=True)
    def put(self, id):
        email = get_jwt_identity()

        post = {
            "title": request.json["title"],
            "description": request.json["description"],
            "location": request.json["location"],
            "time": str(datetime.datetime.now()),
            "user": email,
            "food": request.json["food"],
            "quantity": request.json["quantity"],
        }

        db.bank_posts.update_one({"_id": ObjectId(id)}, {"$set": {"title": post["title"], "description": post["description"], "location": post["location"], "time": post["time"], "quantity": post["quantity"], "food": post["food"]}})

        return {"message": "Post updated successfully."}


    def get(self, id):
        return json.loads(json_util.dumps(list(db.bank_posts.find({"_id": ObjectId(id)}))))

    def delete(self, id):
        db.bank_posts.delete_one({"_id": ObjectId(id)})
        return {"message": "Post deleted successfully."}

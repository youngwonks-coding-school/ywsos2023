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

# @posts.route("/get-posts")
# class GetPosts(Resource):
#     def get(self):
#         return json.loads(json_util.dumps(list(db.posts.find({}))))
#
#
# @posts.route("/create-post", methods=["POST"])
# class CreatePost(Resource):
#     @jwt_required()
#     def post(self):
#         email = get_jwt_identity()
#         print(email)
#
#         post = {
#             "title": request.json["title"],
#             "description": request.json["description"],
#             "location": request.json["location"],
#             "time": str(datetime.datetime.now()),
#             "user": email,
#         }
#
#         db.posts.insert_one(post)
#
#         return {"message": "Post created successfully."}


class Post(Resource):
    @posts.route('/create-restaurant-post', methods=['POST'])
    class RestaurantPost(Resource):
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

            db.restaurant_posts.insert_one(post)

            return {"message": "Post created successfully."}

    @posts.route('/get-restaurant-posts')
    class GetRestaurantPosts(Resource):
        def get(self):
            return json.loads(json_util.dumps(list(db.restaurant_posts.find({}))))

    @posts.route('/get-restaurant-post/<id>')
    class GetRestaurantPost(Resource):
        def get(self, id):
            return json.loads(json_util.dumps(list(db.restaurant_posts.find({"_id": ObjectId(id)}))))

    @posts.route('/create-bank-post', methods=['POST'])
    class CreateBankPost(Resource):
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

    @posts.route('/get-bank-posts')
    class GetBankPosts(Resource):
        def get(self):
            return json.loads(json_util.dumps(list(db.bank_posts.find({}))))

    @posts.route('/get-bank-post/<id>')
    class GetBankPost(Resource):
        def get(self, id):
            return json.loads(json_util.dumps(list(db.bank_posts.find({"_id": ObjectId(id)}))))

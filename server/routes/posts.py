import datetime
import json

from bson import json_util
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource

from db import db

posts = Namespace("posts", description="Operations related to posts")


@posts.route("/get-posts")
class GetPosts(Resource):
    def get(self):
        return json.loads(json_util.dumps(list(db.posts.find({}))))


@posts.route("/create-post", methods=["POST"])
class CreatePost(Resource):
    @jwt_required()
    def post(self):
        email = get_jwt_identity()
        print(email)

        post = {
            "title": request.json["title"],
            "description": request.json["description"],
            "location": request.json["location"],
            "time": str(datetime.datetime.now()),
            "user": email,
        }

        db.posts.insert_one(post)

        return {"message": "Post created successfully."}

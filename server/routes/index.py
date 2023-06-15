from flask_restx import  Namespace,Resource
from flask import jsonify


index = Namespace('', description='Open Routes')

@index.route('/', methods=['GET'])
class Ping(Resource):
    def get(self):
        return jsonify('This is the content to be used for the homepage!')

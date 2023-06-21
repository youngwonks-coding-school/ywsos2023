from flask import jsonify, request
from flask_restx import Namespace, Resource

from custom_spanexporters import MongoDBSpanExporter


index = Namespace("", description="Open Routes")

spanexporter = MongoDBSpanExporter("logging/web_traces_db.json", formatter=lambda x: x)


@index.route("/", methods=["GET"])
class Ping(Resource):
    def get(self):
        return jsonify("This is the content to be used for the homepage!")


@index.route("/web-telemetry", methods=["POST"])
class WebTelemetry(Resource):
    def post(self):
        spanexporter.export([request.json])

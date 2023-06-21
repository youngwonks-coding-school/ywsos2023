import os
import datetime

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource
from flask_jwt_extended import JWTManager
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor

from custom_spanexporters import TinyDBSpanExporter
from routes.index import index
from routes.auth import auth
from dotenv import load_dotenv
from db import db


app = Flask(__name__)
load_dotenv()
app.config["JSON_AS_ASCII"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

# Set the secret key to sign the JWTs with
app.config["JWT_SECRET_KEY"] = os.environ["SECRET_KEY"]  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(
    minutes=15
)  # Access token expires in 15 minutes
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = datetime.timedelta(
    days=30
)  # Refresh token expires in 30 days


jwt = JWTManager(app)
# enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(
    app, version="1.0", title="API", description="API documentation", doc="/api-doc"
)

api.add_namespace(index, "/api")
api.add_namespace(auth, "/api/auth")

trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({SERVICE_NAME: "ywsos2023-flask-server"})
))
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(TinyDBSpanExporter("logging/server_traces_db.json"))
)
FlaskInstrumentor().instrument_app(app)


@jwt.token_in_blocklist_loader
def check_token_in_blacklist(jwt_header, jwt_data):
    # Check if the token is blacklisted
    jti = jwt_data["jti"]
    blacklisted_token = db.blacklisted_tokens.find_one({"jti": jti})
    return blacklisted_token is not None


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

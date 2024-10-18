from flask import Flask
from flask_pymongo import PyMongo
from flask_restx import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv('MONGO_URI')
if not mongo_uri:
    raise ValueError("No MongoDB URI set for application. Set the MONGO_URI environment variable.")

import os


app = Flask(__name__)

# Load MongoDB URI from environment variable
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
if not app.config["MONGO_URI"]:
    raise ValueError("No MongoDB URI set for application. Set the MONGO_URI environment variable.")

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
if not app.config['JWT_SECRET_KEY']:
    raise ValueError("No JWT secret key set for application. Set the JWT_SECRET_KEY environment variable.")

jwt = JWTManager(app)
mongo = PyMongo(app)

# Initialize Flask-RESTx
api = Api(app, 
          version='1.0', 
          title='Flask MongoDB API',
          description='A simple API for managing items',
          doc='/swagger/',
          security='Bearer Auth',
          authorizations={
            'Bearer Auth': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'JWT Authorization header using the Bearer scheme. Example: "Bearer {token}"'}
          })  # Swagger UI endpoint


# Import routes after initializing app
from .auth.auth_routes import *
from .routes import *

if __name__ == "__main__":
    app.run()
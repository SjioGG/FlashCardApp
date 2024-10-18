# app/routes.py
from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models.user import User
from app import api, mongo

api_namespace = Namespace('changeme', description='Actual meat operations')
api.add_namespace(api_namespace)

@api_namespace.route('/protected')
class Protected(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity() # HTTP CONTEXT
        return jsonify(message="You have accessed a protected endpoint!")
    
@api_namespace.route('/getallusers')
@api_namespace.route('/deleteallusers')
class Database(Resource):
    @jwt_required()
    def get(self):
        users = mongo.db.users.find()  # Fetch all users
        user_list = []

        for user in users:
            # Convert ObjectId to string
            user['_id'] = str(user['_id'])
            user_list.append(user)  # Append each user to the list

        return make_response(jsonify(users=user_list), 200)  # Return the list of users as a JSON response
    
    @jwt_required()
    def delete(self):
        k = User.delete_all()
        return make_response(k, 200)  # Return the list of users as a JSON response
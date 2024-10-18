from flask import jsonify, request, make_response
from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token, get_jwt_identity
from app import api
from ..models.user import User

auth_namespace = Namespace('auth', description='Authentication operations')
api.add_namespace(auth_namespace)
# Define a model for the request payload

user_model = auth_namespace.model('User', {
    'username': fields.String(required=True, description="The username"),
    'password': fields.String(required=True, description="The password")
})

@auth_namespace.route('/register')
class Register(Resource):
    @auth_namespace.expect(user_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if User.find_by_username(username):
            return make_response(jsonify(message="User already exists."), 400)
        
        new_user = User(username=username, password=password)
        new_user.save_to_db()  # Save user to database
        return make_response(jsonify(message="User created successfully."), 201)


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(user_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.find_by_username(username)
        
        if user and user.verify_password(password):  # Verify password using the model
            access_token = create_access_token(identity=username)
            return make_response(jsonify(access_token), 200)
        
        return make_response(jsonify(message="Invalid credentials."), 401)


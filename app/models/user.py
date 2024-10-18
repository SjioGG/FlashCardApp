from app import mongo
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, password=None, password_hash=None):
        self.username = username
        if password_hash:
            self.password_hash = password_hash  # Use the hashed password from the database
        elif password:
            self.password_hash = generate_password_hash(password)  # Hash the password if provided

    def save_to_db(self):
        mongo.db.users.insert_one({"username": self.username, "password": self.password_hash})
    
    @classmethod
    def find_by_username(cls, username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            # Pass the hashed password directly from the database
            return cls(username=user_data['username'], password_hash=user_data['password'])
        return None

    def verify_password(self, password):
        # Compare the hashed password with the plain password
        return check_password_hash(self.password_hash, password)
    
    @classmethod
    def delete_all(cls):
        mongo.db.users.delete_many({})  # Deletes all documents in the 'users' collection
        return jsonify(message="All users deleted successfully!")  # Return a JSON response
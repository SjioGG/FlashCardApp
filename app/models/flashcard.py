class User:
    def __init__(self, front, back, deck):
        self.front = front
        self.back = back
        self.deck = deck
    
    def save_to_db(self):
        mongo.db.users.insert_one({"username": self.username, "password": self.password_hash})
    
    @classmethod
    def find_by_username(cls, username):
        user_data = mongo.db.users.find_one({"username": username})
        if user_data:
            return cls(username=user_data['username'], password=user_data['password'])
        return None

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

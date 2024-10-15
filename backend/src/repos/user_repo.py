from db.context import users_collection
from models import dto
class UserRepository:
    @staticmethod
    def find_one(query: dict) -> dict | None:
        """
        Queries the 'users' collection in the database.
        """
        return users_collection.find_one(query)
    
    
    @staticmethod
    
    def insert_one(user_data: dict) -> dict:
        """
        Inserts a document into the 'users' collection in the database.
        """
        result = users_collection.insert_one(user_data)  # MongoDB generates the _id
        return users_collection.find_one({"_id": result.inserted_id}) 

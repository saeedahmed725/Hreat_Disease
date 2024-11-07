from bson import ObjectId
from db.context import users_collection
from models import dto , Users

async def get_by_email(email: str) -> dto.GetUser | None:
    """
    Fetches a user by their email.
    
    :param email: The email of the user to fetch.
    :return: A GetUser DTO object if the user is found, otherwise None.
    """
    user = users_collection.find_one({"email": email})
    if user:
        return user
    return None

async def get_by_id(id: str) -> Users.User | None:
    objectId = ObjectId(id)
    user = users_collection.find_one({"_id": objectId})
    if user:
        return user
    return None

async def get(limit: int = 1000, offset: int = 0) -> list[Users.User]:
    users = users_collection.find().limit(limit).skip(offset)
    return users


async def add(user:dto.CreateUser) -> Users.User:
    users_collection.insert_one(user) 
    returned_user = users_collection.find_one({"email": user['email']})
    return returned_user

async def update(id: int, name: str, surname: str, role: str, email: str, password: str) -> None:
    users_collection.update_one({"_id": id}, {"$set": {"name": name, "surname": surname, "role": role, "email": email, "password": password}})
    
async def delete(id: int) -> None:
    users_collection.delete_one({"_id": id})
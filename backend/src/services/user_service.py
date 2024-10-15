from datetime import datetime
from bson import ObjectId
from models import dto
from repos.user_repo import UserRepository
from utils.bcrypt_hashing import HashLib

async def get_by_email(email: str) -> dto.GetUser | None:
    """
    Fetches a user by their email.
    
    :param email: The email of the user to fetch.
    :return: A GetUser DTO object if the user is found, otherwise None.
    """
    response = UserRepository.find_one({"email": email})
    return dto.GetUser.from_dict(response) if response else None

async def signup_user(signup_data: dto.CreateUser) -> dto.GetUser:
    hashed_password = HashLib.hash(signup_data.password)

    new_user_data = {
        "name": signup_data.name,
        "surname": signup_data.surname,
        "email": signup_data.email,
        "password": hashed_password,
        "created_at": datetime.utcnow(),  # Set current time
        "updated_at": datetime.utcnow()   # Set current time
    }
    
    created_user = UserRepository.insert_one(new_user_data)
    return dto.GetUser.from_dict(created_user)  # Ensure created_user is not None

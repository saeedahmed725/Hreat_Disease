from datetime import datetime
from random import randint
from bson import ObjectId
from models import dto
from repos import user_repo
from models import Users
from utils.bcrypt_hashing import HashLib
from utils import formating


def get(limit: int, offset: int) -> list[Users.User]:
    return user_repo.get(limit=limit, offset=offset)
            
def get_by_id(id: str) -> Users.User | None:
    return user_repo.get_by_id(id)
    
def get_by_email(email: str) -> Users.User | None:
    return user_repo.get_by_email(email.lower().strip())



async def get_by_email(email: str) -> dto.GetUser | None:
    """
    Fetches a user by their email.
    
    :param email: The email of the user to fetch.
    :return: A GetUser DTO object if the user is found, otherwise None.
    """
    return await user_repo.get_by_email(email.lower().strip())   

async def create(user:dto.CreateUser) -> Users.User: 
    return await user_repo.add(user) 
 
async def update_password(id: str, new_password: str) -> None:
    user = await get_by_id(id)
    if user is None:
        return
    new_pass_hash = HashLib.hash(new_password)
    await user_repo.update(
        user['_id'],
        user['name'],
        user['surname'],
        user['role'],
        user['email'],
        new_pass_hash
    )
    
    
async def reset_password(id: str) -> None:
    user = await get_by_id(id)
    if user is None:
        return
    
    new_password = str(randint(1000, 9999))
    print(new_password)
    password_hash = HashLib.hash(new_password)
    await user_repo.update(
        user['_id'],
        user['name'],
        user['surname'],
        user['role'],
        user['email'],
        password_hash
    )
    return new_password

def delete(id: int) -> None:
    user_repo.delete(id)
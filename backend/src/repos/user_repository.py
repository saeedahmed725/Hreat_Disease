from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel
from models.dto import CreateUser, GetUser
from models.Users import User
from repos.base_repository import BaseRepository
from db.collections import Collections

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(Collections.users(), User)

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Fetches a user by their email.
        
        :param email: The email of the user to fetch.
        :return: A User DTO object if the user is found, otherwise None.
        """
        user_data = await self.collection.find_one({"email": email})
        if user_data:
            user_data["_id"] = str(user_data["_id"])
            return User(**user_data)
        return None

    async def get_by_id(self, id: str) -> Optional[User]:
        object_id = ObjectId(id)
        user_data = await self.collection.find_one({"_id": object_id})
        if user_data:
            user_data["_id"] = str(user_data["_id"])
            return User(**user_data)
        return None

    async def get(self, limit: int = 1000, offset: int = 0) -> List[User]:
        cursor = self.collection.find().skip(offset).limit(limit)
        users = []
        async for user_data in cursor:
            user_data["_id"] = str(user_data["_id"])
            users.append(User(**user_data))
        return users

    async def add(self, user: CreateUser) -> User:
        user_data = user.model_dump() if isinstance(user, BaseModel) else user  # Convert to dictionary
        result = await self.collection.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        return User(**user_data)

    async def update(self, id: str, name: str, surname: str, role: str, email: str, password: str) -> Optional[User]:
        update_data = {
            "name": name,
            "surname": surname,
            "role": role,
            "email": email,
            "password": password,
            "updated_at": datetime.now()
        }
        updated_user = await super().update(id, update_data)
        return updated_user

    async def delete(self, id: str) -> bool:
        return await super().delete(id)

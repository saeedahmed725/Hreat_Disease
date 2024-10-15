from bson import ObjectId
from pymongo import ReturnDocument

from pydantic import BaseModel

from uuid import uuid4
from datetime import datetime

class User(BaseModel):
    id: str
    name: str
    surname: str
    email: str
    password: str
    updated_at: datetime
    created_at: datetime
    

    
    
 
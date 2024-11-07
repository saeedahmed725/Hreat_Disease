from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
from bson import ObjectId

# USER
class CreateUser(BaseModel):
    name: str
    surname: str
    email: str
    role: str = "user"
    password: str = Field(..., min_length=4),
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class GetUser(BaseModel):
    id: int = Field(default=None , alias="_id")
    name: str
    surname: str
    role: str
    email: str
    updated_at: datetime
    created_at: datetime      
    
       
    
class UpdateUser(BaseModel):
    name: str
    surname: str
    
class LoginUser(BaseModel):
    email: str
    password: str
    
class UpdateUserPass(BaseModel):
    old_password: str = Field(..., min_length=4)
    new_password: str = Field(..., min_length=4)
    
# Token
class Token(BaseModel):
    user_id: str   
    role : str
    exp: datetime
    
    @field_validator("user_id", mode="before")
    def validate_id(cls, value):
        if isinstance(value, ObjectId):
            return str(value)
        return value
 

    
    

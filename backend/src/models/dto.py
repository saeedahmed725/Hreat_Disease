from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

# USER
class CreateUser(BaseModel):
    name: str
    surname: str
    email: str
    password: str = Field(..., min_length=4)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)  # Automatically set the current UTC time
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow) #For 1 big letter, 1 small letter, 1 number, 1 special character and min 8 characters: pattern="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

class GetUser(BaseModel):
    name: str
    surname: str
    email: str
    updated_at: datetime
    created_at: datetime         
    


    @staticmethod
    def from_dict(data: dict) -> "GetUser":
        return GetUser(
            name=data.get("name"),
            surname=data.get("surname"),
            email=data.get("email"),
            updated_at=data.get("updated_at"),
            created_at=data.get("created_at"),
        )
    
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
    user_id: int
    exp: datetime
    
    

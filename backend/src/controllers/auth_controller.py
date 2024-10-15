from fastapi import APIRouter, HTTPException, status
from models import dto
from services import user_service

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/get_id/{id}", response_model=dto.GetUser, status_code=status.HTTP_200_OK)
async def get_id(id: str) -> dto.GetUser:
    user = await user_service.get_by_id(id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.post("/signup", response_model=dto.GetUser, status_code=status.HTTP_201_CREATED)
async def signup(signup_data: dto.CreateUser) -> dto.GetUser:
    existing_user = await user_service.get_by_email(signup_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = await user_service.signup_user(signup_data)
    if new_user is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="User creation failed")
    return new_user

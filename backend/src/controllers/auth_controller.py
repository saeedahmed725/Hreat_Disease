from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from models import dto
from services import user_service , jwt_service
from utils import formating , dependencies 
from utils.formating import MongoIDConverter
from models import Users
from utils.bcrypt_hashing import HashLib
from constants import SESSION_TIME, COOKIES_KEY_NAME

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/signup", response_model=Users.User, status_code=status.HTTP_201_CREATED)
async def signup(user: dto.CreateUser) -> Users.User:
    email = formating.format_string(user.email)
    password = HashLib.hash(user.password)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email")
    if not user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
    
    existing_user = await user_service.get_by_email(email)
    
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    user = {
        "name": user.name,
        "surname": user.surname,
        "email": email,
        "role": Users.User.Role.USER,
        "password": password,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    return await user_service.create(
        user
    )



@router.post("/login", response_model=str , status_code=status.HTTP_200_OK)
async def login(dto: dto.LoginUser , res: Response):
    Now = datetime.now(timezone.utc)
    email = formating.format_string(dto.email)
    user = await user_service.get_by_email(email)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not HashLib.validate(dto.password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password")
    
    exp_date = Now + SESSION_TIME
    
    token = jwt_service.encode(user['_id'] , user['role'] , exp_date)
    
    res.set_cookie(COOKIES_KEY_NAME, token, expires=exp_date)
    
    return token


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(res: Response) -> JSONResponse:
    res.delete_cookie(COOKIES_KEY_NAME)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/validate" , response_model=dto.Token , status_code=status.HTTP_200_OK)
async def check_session(req:Request , res:Response):
    token = req.cookies.get(COOKIES_KEY_NAME)
    data = jwt_service.decode(token)
    if data is None:
        res.delete_cookie(COOKIES_KEY_NAME)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return data

@router.post("/password/update"  , status_code=204)
async def update_password(dto: dto.UpdateUserPass , user:dependencies.user_dependency):
    if dto.old_password == dto.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is the same")
    
    if HashLib.validate(dto.old_password, user['password']) is False:
        raise HTTPException(status_code=401, detail="Current password is incorrect")
    
    user_id =  MongoIDConverter.ensure_object_id(user['_id'])
    await user_service.update_password(user_id, dto.new_password)
    
    
@router.post("/password/reset" , status_code=204)
async def reset_password(dto: dto.UpdateUserPass , user:dependencies.user_dependency):
    user = await user_service.get_by_email(user['email'])
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user_id = MongoIDConverter.ensure_string(user['_id'])
    new_pass = await user_service.reset_password(user_id)
    print(f"User {user['email']} new password: {new_pass}")
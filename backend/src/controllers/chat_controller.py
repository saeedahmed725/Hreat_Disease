from fastapi import APIRouter , status , Request , HTTPException
from services.chat_service import ChatService
from models.dto import MessageResponse
from services import jwt_service
from constants import COOKIES_KEY_NAME
from models import Messages
from uuid import uuid4
 


router = APIRouter(
    tags=["Chat"],
)


@router.post("/create_chat_session" , response_model=Messages.ChatSession , status_code=status.HTTP_201_CREATED)
async def create_chat(chat: Messages.ChatSession , req:Request) -> Messages.ChatSession:
    token = req.cookies.get(COOKIES_KEY_NAME)
    data = jwt_service.decode(token)
    if data is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    chat_service = ChatService()
    return await chat_service.create_session( data.user_id , "Hello Chat")


@router.post("/send_message" , response_model=Messages.Messages , status_code=status.HTTP_201_CREATED)
async def send_message(message: Messages.MessageContent , req:Request) -> Messages.Messages:
    token = req.cookies.get(COOKIES_KEY_NAME)
    random_id = str(uuid4())
    data = jwt_service.decode(token)
    if data is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    chat_service = ChatService()
    session_id = f"${random_id + "-" + data.user_id}"
 
    return await chat_service.create_message( user_id=data.user_id , session_id=session_id , content=message , role="user" , metadata={
        'user_id':data.user_id,
        'session_id':session_id
    })
    
    
@router.post("/send_message/{session_id}" , response_model=Messages.Messages , status_code=status.HTTP_201_CREATED)
async def send_message(session_id:str , message: Messages.MessageContent , req:Request) -> MessageResponse:
    token = req.cookies.get(COOKIES_KEY_NAME)
    data = jwt_service.decode(token)
    if data is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    chat_service = ChatService()
    return await chat_service.create_message( user_id=data.user_id , session_id=session_id , content=message , role="user" , metadata={
        'user_id':data.user_id,
        'session_id':session_id
    })
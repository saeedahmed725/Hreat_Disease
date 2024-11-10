from datetime import datetime
from typing import List, Optional
from models.dto import ChatSession, Messages
from repos.chat_repository import ChatRepository, MessageRepository

class ChatService:
    def __init__(self):
        self.chat_repo = ChatRepository()
        self.message_repo = MessageRepository()
    
    async def create_session(
        self,
        user_id: str,
        title: Optional[str] = None
    ) -> ChatSession:
        return await self.chat_repo.create_session(
            user_id=user_id,
            title=title or "Untitled Session"
        )
    
    async def create_message(
        self,
        session_id: str,
        user_id: str,
        content: str,
        role: str,
        metadata: Optional[dict] = None
    ) -> Messages:
        message_data = {
            "session_id": session_id,
            "user_id": user_id,
            "role": role,
            "content": {
                "text": content,
                "metadata": metadata or {}
            },
            "is_visible": True,
            "metadata": {}
        }
        return await self.message_repo.create_message(message_data)
    
    async def get_chat_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Messages]:
        return await self.message_repo.get_chat_history(session_id, limit)
    
    async def reset_session(self, session_id: str) -> None:
        await self.message_repo.delete_session_messages(session_id)
        await self.chat_repo.delete(session_id)
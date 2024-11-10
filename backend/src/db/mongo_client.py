from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from constants import DB_CONNECTION_STRING

class MongoDBClient:
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect(cls):
        """Initialize database connection"""
        if cls.client is None:
            cls.client = AsyncIOMotorClient(DB_CONNECTION_STRING)
            
    @classmethod
    async def close(cls):
        """Close database connection"""
        if cls.client is not None:
            await cls.client.close()
            cls.client = None
    
    @classmethod
    def get_db(cls):
        """Get database instance"""
        if cls.client is None:
            raise Exception("Database not initialized")
        return cls.client["Quran"]
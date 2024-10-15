from fastapi import Depends, FastAPI
from pymongo import MongoClient
from controllers import auth_controller
from utils import startup
from constants import DB_CONNECTION_STRING

app = FastAPI(lifespan=startup.lifespan)

app.include_router(auth_controller.router)  

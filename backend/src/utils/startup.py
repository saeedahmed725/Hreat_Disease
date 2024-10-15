from fastapi import FastAPI
from pymongo import MongoClient
from constants import DB_CONNECTION_STRING, COLLECTION_NAME
from contextlib import asynccontextmanager

if not DB_CONNECTION_STRING:
    raise Exception("DB connection string not provided")

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = MongoClient(DB_CONNECTION_STRING)
    database = client.get_default_database()

    # Ping the database to check the connection
    pong = database.command("ping")
    
    if int(pong["ok"]) != 1:
        client.close()
        raise Exception("Cluster connection is not okay!")

    # Store the database and collection in the app state
    app.state.database = database
    app.state.quran_collection_user = database.get_collection(COLLECTION_NAME)
    
    yield  # This allows the application to run
    
    client.close()

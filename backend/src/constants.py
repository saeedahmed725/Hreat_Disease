from datetime import timedelta
from os import getenv
import dotenv

dotenv.load_dotenv()

DB_CONNECTION_STRING = getenv("MONGODB_URI")
COOKIES_KEY_NAME = "session_token"
SESSION_TIME = timedelta(days=30)
HASH_SALT = getenv("HASH_SALT", "qeqweasdshfhsfewfsdif")
COLLECTION_NAME = "Quran_Backend"
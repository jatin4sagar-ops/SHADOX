# =============================================================
# SHADOX — db/db.py
# MongoDB connection and collection exports.
# =============================================================

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Connection settings
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "shadox_db"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)

    # Test connection
    client.admin.command("ping")

    print("[SHADOX] Connected to MongoDB successfully.")

except ConnectionFailure:
    print("[SHADOX] ERROR: Could not connect to MongoDB.")
    client = None

except ServerSelectionTimeoutError:
    print("[SHADOX] ERROR: MongoDB server timed out.")
    client = None

# Database
db = client[DB_NAME] if client is not None else None

users_col = db["users"] if db is not None else None
messages_col = db["messages"] if db is not None else None

# Create unique index
if users_col is not None:
    users_col.create_index("college_id", unique=True)
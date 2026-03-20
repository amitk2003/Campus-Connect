from pymongo import MongoClient
from config import Config

def get_db():
    try:
        client = MongoClient(Config.MONGO_URI)
        db = client.get_database()
        print("✅ Connected to DB:", db.name)
        return db
    except Exception as e:
        print("❌ DB Connection Error:", e)

db = get_db()
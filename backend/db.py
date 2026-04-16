from pymongo import MongoClient
from config import Config

client = None
db = None

try:
    client = MongoClient(Config.MONGO_URI)
    db = client["OnlineMarketplace"]
    print("✅ MongoDB connected")
except Exception as e:
    print("❌ DB Connection Error:", e)

def get_db():
    return db
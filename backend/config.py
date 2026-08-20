import os
from dotenv import load_dotenv

load_dotenv()

print("SECRET_KEY:", os.getenv("SECRET_KEY"))
print("MONGO_URI:", os.getenv("MONGO_URI"))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    print("SECRET_KEY:", os.getenv("SECRET_KEY"))
    print("MONGO_URI:", os.getenv("MONGO_URI"))

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    MONGO_URI = os.getenv('MONGO_URI')
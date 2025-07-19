from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

#connection to url
MONGO_URL = os.getenv("MONGODB_URL")

#client is used to access database collections and methods by async methods
client = AsyncIOMotorClient(MONGO_URL)
db = client["ecoomerce"]

product_collection = db["products"]
order_collection = db["orders"]

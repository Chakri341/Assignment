import os
from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient

def get_mongo_client():
   mongo_url = os.environ.get("MONGO_URL")
   if not mongo_url:
      raise ValueError("MONGO_URL environment variable is not set.")
   return MongoClient(mongo_url);


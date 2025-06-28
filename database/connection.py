import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load .env from the current directory (same as this file)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

def get_database():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("MONGO_DB", "iot_project")
   
    if not mongo_uri or not db_name:
        raise ValueError("MONGO_URI or MONGO_DB not found in .env file")

    client = MongoClient(mongo_uri)
    return client[db_name]

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            connection_url = os.environ.get("MONGO_CONNECTION_URL")
            cls._instance.client = MongoClient(connection_url)
            print("MongoDB connection established!")
        return cls._instance

    def get_client(self):
        return self.client
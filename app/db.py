from functools import lru_cache
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


@lru_cache
def get_db():
    uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")

    if not uri:
        raise RuntimeError("MONGO_URI environment variable is required")

    if not db_name:
        raise RuntimeError("DB_NAME environment variable is required")

    client = MongoClient(uri)

    return client[db_name]


def get_people_collection():
    return get_db()["people"]
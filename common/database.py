import urllib.parse
import pymongo as pymongo
from typing import Dict
import os

class Database:
    # Uniform Resource Identifier
    # URI = "mongodb://127.0.0.1:27017/pricing"
    DB_USER = urllib.parse.quote_plus(os.getenv('DB_USER'))
    PASSWORD = urllib.parse.quote_plus(os.getenv('PASSWORD'))
    SERVER_IP = os.getenv('SERVER_IP')

    URI = "mongodb://%s:%s@%s/pricing" % (DB_USER, PASSWORD, SERVER_IP)
    DATABASE = pymongo.MongoClient(URI)["pricing"]

    @staticmethod
    def insert(collection: str, data: Dict) -> None:
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def remove(collection: str, query: Dict) -> Dict:
        return Database.DATABASE[collection].remove(query)


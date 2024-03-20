import pymongo
from pymongo import MongoClient
from src.managers.configuration_manager import CONFIG


class MongoClient:
    def __init__(self) -> None:
        self.client = self._connect_client()

    def _connect_client(self) -> MongoClient:
        try:
            return pymongo.MongoClient(CONFIG.MONGO_CONNECTION_STRING)
        except Exception:
            raise Exception

    def get_db(self):
        return self.client.get_database("your_database")


MONGO_DB = MongoClient().get_db()

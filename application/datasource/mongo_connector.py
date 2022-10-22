import os

from os.path import dirname, join
from pymongo import MongoClient
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '../../.env')
load_dotenv(dotenv_path)


class MongoConnector:
    __MONGO_CONNECTION_STRING = os.environ.get("MONGO_CONNECTION_STRING")
    __client = None
    __db = None

    def __init__(self):
        self.__client = MongoClient(self.__MONGO_CONNECTION_STRING)
        self.__db = self.__client.database

    def get_database(self):
        return self.__db
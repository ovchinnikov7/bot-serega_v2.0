import os

from pymongo.collection import Collection
from pymongo.database import Database

from application.datasource.entity.user_data import User


class UserStatsRepository:
    __users_collection_name = os.environ.get('MONGO_USERS_COLLECTION_NAME')

    # users stats collection fields names
    __user_id_field = os.environ.get('USER_ID_FIELD_NAME')
    __stats_field = os.environ.get('USER_STATS_FIELD_NAME')
    __user_index = os.environ.get('USER_INDEX_NAME')

    __users_collection: Collection[User]

    def __init__(self, database: Database):
        self.__users_collection = database[self.__users_collection_name]

    def fuck_off_inc(self, user_id):
        self.__users_collection.update_one({self.__user_id_field: user_id}, {"$inc": {self.__stats_field: 1}}, upsert=True)

    def find_user(self, user_id):
        return self.__users_collection.find_one({self.__user_id_field: user_id})[self.__stats_field]

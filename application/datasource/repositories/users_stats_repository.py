import os

from aiogram import types
from pymongo.collection import Collection
from pymongo.database import Database

from application.datasource.entity.user_data import User


class UserStatsRepository:
    __users_collection_name = os.environ.get('MONGO_USERS_COLLECTION_NAME')

    # users stats collection fields names
    __user_id_field = os.environ.get('USER_ID_FIELD_NAME')
    __user_first_name_field = os.environ.get('USER_FIRST_NAME_FIELD_NAME')
    __user_last_name_field = os.environ.get('USER_LAST_NAME_FIELD_NAME')
    __user_username_field = os.environ.get('USER_USERNAME_FIELD_NAME')
    __user_chat_id_field = os.environ.get('USER_CHAT_ID_FIELD_NAME')
    __stats_field = os.environ.get('USER_STATS_FIELD_NAME')
    __user_index = os.environ.get('USER_INDEX_NAME')

    __users_collection: Collection[User]

    def __init__(self, database: Database):
        self.__users_collection = database[self.__users_collection_name]

    def fuck_off_inc(self, user_id):
        self.__users_collection.update_one({self.__user_id_field: str(user_id)}, {"$inc": {self.__stats_field: 1}}, upsert=True)

    def get_user_stats(self, user_id):
        return self.__users_collection.find_one({self.__user_id_field: str(user_id)})[self.__stats_field]

    def is_user_exist(self, user_id):
        user = self.__users_collection.find_one({self.__user_id_field: str(user_id)})
        return user != None

    def user_start(self, message: types.Message):
        return self.__users_collection.update_one(
        {
            self.__user_id_field: str(message.from_user.id)},
            self.get_user_json_from_message(message),
            upsert=True
        )

        # self.__users_collection.update_one({self.__user_id_field: user_id}, {"$inc": {self.__stats_field: 1}}, upsert=True)
    def get_user_json_from_message(self, message: types.Message):
        return {
            '$set': {
                     self.__user_first_name_field:   message.from_user.first_name,
                     self.__user_last_name_field:    message.from_user.last_name,
                     self.__user_username_field:     message.from_user.username},
            '$addToSet': {self.__user_chat_id_field: message.chat.id},
            "$inc": {self.__stats_field: 1}
        }

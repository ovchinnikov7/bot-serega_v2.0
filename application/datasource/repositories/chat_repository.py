import os

from pymongo.collection import Collection
from pymongo.database import Database
from datetime import time


from application.datasource.entity.chat_data import ChatEntity


class ChatRepository:
    __chat_collection_name = os.environ.get('MONGO_CHAT_COLLECTION_NAME')

    __chat_id_field        = os.environ.get('CHAT_ID_FIELD_NAME')
    __chat_next_time_field = os.environ.get('CHAT_NEXT_TIME_FIELD_NAME')
    __chat_flag_field      = os.environ.get('CHAT_ENABLE_FLAG_FIELD_NAME')

    __chats_collection: Collection[ChatEntity]

    def __init__(self, database: Database):
        self.__chats_collection = database[self.__chat_collection_name]

    def add_chat(self, chat_id: str):
        next_time: time
        self.__chats_collection.update_one(
            {self.__chat_id_field: str(chat_id)},
            {'$set': {self.__chat_next_time_field: next_time,
                      self.__chat_flag_field: True}}
        )

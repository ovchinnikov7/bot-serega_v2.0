import os

from pymongo import MongoClient
from pymongo.database import Database

__database_name = os.environ.get('MONGO_DATABASE_NAME')
__connection_string = os.environ.get('MONGO_CONNECTION_STRING')

__users_collection_name = os.environ.get('MONGO_USERS_COLLECTION_NAME')
__jokes_collection_name = os.environ.get('MONGO_JOKES_COLLECTION_NAME')
__words_collection_name = os.environ.get('MONGO_JOKE_TRIGGERS_COLLECTION_NAME')
__foul_lang_collection_name = os.environ.get('MONGO_FOUL_LANGUAGE_COLLECTION_NAME')
__answer_collection_name = os.environ.get('MONGO_ANSWERS_COLLECTION_NAME')

# jokes collection fields names
__jokes_hash_field = os.environ.get('JOKES_HASH_FIELD_NAME')
__jokes_text_field = os.environ.get('JOKES_TEXT_FIELD_NAME')
__jokes_hash_index = os.environ.get('JOKES_HASH_INDEX_NAME')

# users stats collection fields names
__user_id_field = os.environ.get('USER_ID_FIELD_NAME')
__stats_field = os.environ.get('USER_STATS_FIELD_NAME')
__user_index = os.environ.get('USER_INDEX_NAME')

# dictionary collection fields names
__grop_field = os.environ.get('GROUP_FIELD_NAME')
__triggers_field = os.environ.get('TRIGGERS_FIELD_NAME')
__jokes_grope = os.environ.get('JOKE_TRIGGER_GROPE')
__greetings_grope = os.environ.get('GREETINGS_TRIGGER_GROPE')

# answers collection fields names
__answer_hash_field = os.environ.get('ANSWER_HASH_FIELD_NAME')
__answer_text_field = os.environ.get('ANSWER_TEXT_FIELD_NAME')
__answer_hash_index = os.environ.get('ANSWER_INDEX_NAME')

__data_base_connection: Database
__mongo_client: MongoClient


def init_db():
    mongo_client = MongoClient(__connection_string)

    if __database_name not in mongo_client.list_database_names():
        print(f'Warn! DataBase <{__database_name}> does not exist!')
        return

    bot_serega_db_connection = mongo_client.get_database(__database_name)

    users_collection = bot_serega_db_connection[__users_collection_name]
    jokes_collection = bot_serega_db_connection[__jokes_collection_name]
    answers_collection = bot_serega_db_connection[__answer_collection_name]
    words_collection = bot_serega_db_connection[__words_collection_name]

    users_collection.create_index([(__user_id_field, 1)], name=__user_index, unique=True)
    jokes_collection.create_index([(__jokes_hash_field, 1)], name=__jokes_hash_index, unique=True)
    # answers_collection.create_index([(__answer_hash_field, 1)], name=__answer_hash_index, unique=True)

    global __data_base_connection, __mongo_client
    __mongo_client = mongo_client
    __data_base_connection = bot_serega_db_connection


def get_mongo_connection():
    global __data_base_connection
    return __data_base_connection


def get_mongo_client():
    global __mongo_client
    return __mongo_client


# TODO: DELETE
def get_datas(db: Database, client: MongoClient):
    print(f'collections => {db.list_collection_names()}')
    print(f'databases => {client.list_database_names()}')

import hashlib
import os
import random

from pymongo.collection import Collection

from application.datasource.entity.joke_data import Joke


class JokesRepository:
    __jokes_collection_name = os.environ.get('MONGO_JOKES_COLLECTION_NAME')

    # jokes collection fields names
    __hash_field = os.environ.get('JOKES_HASH_FIELD_NAME')
    __text_field = os.environ.get('JOKES_TEXT_FIELD_NAME')
    __hash_index = os.environ.get('JOKES_HASH_INDEX_NAME')

    __jokes_collection: Collection[Joke]

    def __init__(self, mongo_connector):
        self.__jokes_collection = mongo_connector[self.__jokes_collection_name]

    def get_random_joke(self):
        dock_count = self.__jokes_collection.count_documents({})
        random_number = random.randint(0, dock_count)
        joke_text = self.__jokes_collection.find().limit(-1).skip(random_number).next()
        return joke_text[self.__text_field]

    def insert_jokes_dataset(self, jokes_list):
        for joke in jokes_list:
            try:
                self.__jokes_collection.insert(self.joke_to_json(joke))
            except Exception as ex:
                print(ex)
                print(joke)
                continue

    def joke_to_json(self, text: str):
        hash_id = calculate_hash(text)
        return {self.__hash_field: hash_id, self.__text_field: text}


def calculate_hash(text: str):
    return int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16)

# self.__jokes_collection.insert_many(jokes_list)

import os

from pymongo.collection import Collection

from application.datasource.entity.joke_data import Joke
from application.datasource.repositories.repo_utils import check_not_empty, calculate_hash


class JokesRepository:
    __jokes_collection_name = os.environ.get('MONGO_JOKES_COLLECTION_NAME')

    __hash_field = os.environ.get('JOKES_HASH_FIELD_NAME')
    __text_field = os.environ.get('JOKES_TEXT_FIELD_NAME')
    __hash_index = os.environ.get('JOKES_HASH_INDEX_NAME')

    __jokes_collection: Collection[Joke]

    def __init__(self, mongo_connector):
        self.__jokes_collection = mongo_connector[self.__jokes_collection_name]

    def get_random_joke(self):
        if check_not_empty(self.__jokes_collection):
            joke = self.__jokes_collection.aggregate([{"$sample": {'size': 1}}]).next()
            return joke.get(self.__text_field)
        return "Хуй с маслом"

    def insert_jokes_dataset(self, jokes_list: [str]):
        for joke in jokes_list:
            try:
                hash_id = str(calculate_hash(joke))
                joke_filter = self.get_joke_uniq_filter(hash_id)
                joke_json = self.joke_to_json(hash_id, joke)
                self.__jokes_collection.update_one(joke_filter, {"$setOnInsert": joke_json}, upsert=True)
            except Exception as ex:
                print(ex)
                print(joke)
                continue

    def joke_to_json(self, hash_id: str, text: str):
        return {self.__hash_field: hash_id, self.__text_field: text}

    def get_joke_uniq_filter(self, hash_id: str):
        return {self.__hash_field: hash_id}

# self.__jokes_collection.insert_many(jokes_list)

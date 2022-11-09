import os
import re
from re import Pattern

from pymongo.collection import Collection

from application.datasource.entity.words_data import Words
from application.datasource.repositories.repo_utils import check_not_empty, calculate_hash


class WordsRepository:
    __words_collection_name: str
    __answer_collection_name: str

    # dictionary collcetion fields names
    __grop_field: str
    __words_field: str
    __jokes_trig_grope: str
    __greetings_trig_grope: str
    __foul_lang_trig_grope: str
    __foul_lang_grope: str

    __answer_hash_field: str
    __answer_text_field: str

    __words_collection: Collection[Words]
    __answer_collection: Collection[Words]

    def __init__(self, mongo_connection):
        # collections names
        self.__words_collection_name = os.environ.get('MONGO_JOKE_TRIGGERS_COLLECTION_NAME')
        self.__answer_collection_name = os.environ.get('MONGO_ANSWERS_COLLECTION_NAME')

        # words fields
        self.__grop_field = os.environ.get('GROUP_FIELD_NAME')
        self.__words_field = os.environ.get('WORDS_COLLECTION_FIELD_NAME')

        # words groups
        self.__jokes_trig_grope = os.environ.get('JOKE_TRIGGER_GROPE')
        self.__greetings_trig_grope = os.environ.get('GREETINGS_TRIGGER_GROPE')
        self.__foul_lang_trig_grope = os.environ.get('FOUL_LANGUAGE_TRIGGER_GROPE')
        self.__foul_lang_grope = os.environ.get('FOUL_LANGUAGE_GROPE')

        # answers fields
        self.__answer_hash_field = os.environ.get('ANSWER_HASH_FIELD_NAME')
        self.__answer_text_field = os.environ.get('ANSWER_TEXT_FIELD_NAME')

        # init collections
        self.__words_collection = mongo_connection[self.__words_collection_name]
        self.__answer_collection = mongo_connection[self.__answer_collection_name]

    def get_joke_triggers(self) -> list:
        return self.__words_collection.find_one({self.__grop_field: self.__jokes_trig_grope}).get(self.__words_field)

    def get_greeting_triggers(self) -> list:
        return self.__words_collection.find_one({self.__grop_field: self.__greetings_trig_grope}, {self.__words_field: 1}).get(self.__words_field)

    def get_foul_lang_triggers(self) -> [Pattern]:
        words = self.__words_collection.find_one({self.__grop_field: self.__foul_lang_trig_grope}, {self.__words_field: 1}).get(self.__words_field)
        patterns = [re.compile(word) for word in words]
        return patterns

    def get_foul_lang_words(self) -> list:
        return self.__words_collection.find_one({self.__grop_field: self.__foul_lang_grope}, {self.__words_field: 1}).get(self.__words_field)

    def get_foul_answer(self) -> str:
        if check_not_empty(self.__answer_collection):
            joke = self.__answer_collection.aggregate([{"$sample": {'size': 1}}]).next()
            return joke.get(self.__answer_text_field)
        return 'Ты просто хуй с маслом'

    def update_joke_triggers(self, data: list):
        json_data = self.words_data_to_document(self.__jokes_grope, data)
        self.__words_collection.update_one(
            {self.__grop_field: self.__jokes_grope},
            json_data,
            upsert=True
        )

    def update_greetings_triggers(self, data: list):
        json_data = self.words_data_to_document(self.__greetings_grope, data)
        self.__words_collection.update_one(
            {self.__grop_field: self.__greetings_grope},
            json_data,
            upsert=True
        )

    def update_foul_lang_triggers(self, data: list):
        json_data = self.words_data_to_document(self.__foul_lang_trig_grope, data)
        self.__words_collection.update_one(
            {self.__grop_field: self.__foul_lang_trig_grope},
            json_data,
            upsert=True
        )

    def update_foul_lang(self, data: list):
        json_data = self.words_data_to_document(self.__foul_lang_grope, data)
        self.__words_collection.update_one(
            {self.__grop_field: self.__foul_lang_grope},
            json_data,
            upsert=True
        )

    def update_foul_answers(self, data: list):
        for answer in data:
            try:
                hash_id = str(calculate_hash(answer))
                answer_filter = self.get_answer_uniq_filter(hash_id)
                ansver_json = self.answer_data_to_document(
                        hash_id,
                        answer
                    )
                self.__answer_collection.update_one(
                    answer_filter,
                    ansver_json,
                    upsert=True
                )
            except Exception as ex:
                print(ex)
                print(answer)
                continue

    def get_answer_uniq_filter(self, hash_id: str):
        return {self.__answer_hash_field: hash_id}


    def words_data_to_document(self, words_group: str, data: list):
        return {'$set': {self.__grop_field: words_group}, '$addToSet': {self.__words_field: {'$each': data}}}

    def answer_data_to_document(self, hash_id: str, text: str):
        return {self.__answer_hash_field: hash_id, self.__answer_text_field: text}

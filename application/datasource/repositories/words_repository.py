import os

from pymongo.collection import Collection

from application.datasource.entity.words_data import Words


class WordsRepository:
    __words_collection_name = os.environ.get('MONGO_JOKE_TRIGGERS_COLLECTION_NAME')
    __foul_lang_collection_name = os.environ.get('MONGO_FOUL_LANGUAGE_COLLECTION_NAME')

    # dictionary collcetion fields names
    __grop_field = os.environ.get('GROUP_FIELD_NAME')
    __triggers_field = os.environ.get('TRIGGERS_FIELD_NAME')
    __jokes_grope = os.environ.get('JOKE_TRIGGER_GROPE')
    __greetings_grope = os.environ.get('GREETINGS_TRIGGER_GROPE')

    __trigger_words_collection: Collection[Words]
    __foul_lang_collection: Collection[Words]

    def __init__(self, mongo_connection):
        self.__trigger_words_collection = mongo_connection[self.__words_collection_name]
        self.__foul_lang_collection = mongo_connection[self.__foul_lang_collection_name]

    def get_joke_triggers(self) -> list:
        return self.__trigger_words_collection.find({self.__grop_field: self.__jokes_grope})[self.__triggers_field]
        # triggers = self.__joke_trigger_collection.find()
        # return triggers[self.__foul_lang_collection_name]

    def update_joke_triggers(self, data: list):
        json_data = data_to_document(self.__jokes_grope, data)
        self.__trigger_words_collection.update_one(
            {self.__grop_field: self.__jokes_grope},
            json_data,
            upsert=True
        )

    def update_greetings_triggers(self, data: list):
        json_data = data_to_document(self.__greetings_grope, data)
        self.__trigger_words_collection.update_one(
            {self.__grop_field: self.__greetings_grope},
            json_data,
            upsert=True
        )


def data_to_document(words_group: str, data: list):
    return {"$addToSet": {words_group: {"$each": data}}}
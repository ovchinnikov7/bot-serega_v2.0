from application.datasource.migrations.init_mongo_database import *
from application.datasource.repositories.users_stats_repository import UserStatsRepository
from application.datasource.repositories.jokes_repository import JokesRepository
from application.datasource.repositories.words_repository import WordsRepository
from pymongo.database import Database


class MongoRepositories:
    __connection: Database

    __jokes_repository: JokesRepository
    __users_repository: UserStatsRepository
    __words_repository: WordsRepository

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance.__init_repositories()
        return cls._instance

    def __init_repositories(self):
        init_db()
        self.__connection = get_mongo_connection()

        self.__users_repository = UserStatsRepository(self.__connection)
        self.__jokes_repository = JokesRepository(self.__connection)
        self.__words_repository = WordsRepository(self.__connection)

    def get_users_repository(self):
        return self.__users_repository

    def get_jokes_repository(self):
        return self.__jokes_repository

    def get_words_repository(self):
        return self.__words_repository

from application.datasource.mongo_connector import MongoConnector
from application.datasource.users_stats_repository import UserStatsRepository

def setup_data_source():
    mongo_connector = MongoConnector()
    return UserStatsRepository(mongo_connector)
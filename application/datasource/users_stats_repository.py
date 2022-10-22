import os

users = os.environ.get('MONGO_COLLECTION_NAME')


class UserStatsRepository:
    __mongo_db = None

    def __init__(self, mongo_connector):
        self.__mongo_db = mongo_connector.get_database()

    async def fuck_off_inc(self, user_id):
        self.__mongo_db.users.update_one({"user_id": user_id}, {"$inc": {"user_stat": 1}}, upsert=True)
        return "Success"

    async def find_user(self, user_id):
        user_data = self.__mongo_db.users.find_one({"user_id": user_id})['user_stat']
        return user_data

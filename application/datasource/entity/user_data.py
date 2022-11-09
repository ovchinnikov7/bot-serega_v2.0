from typing import TypedDict
from aiogram import types


class User(TypedDict):
    user_id: str
    first_name: str
    last_name: str
    username: str
    chat_id: str
    stats: int

    @staticmethod
    def of(message: types.Message):
        user = User()
        user.user_id        = message.message_id
        user.first_name     = message.from_user.first_name
        user.last_name      = message.from_user.last_name
        user.username       = message.from_user.username
        user.chat_id        = message.chat.id
        user.stats = 0

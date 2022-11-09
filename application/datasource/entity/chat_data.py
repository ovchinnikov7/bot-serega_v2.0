from datetime import time
from typing import TypedDict


class ChatEntity(TypedDict):
    chat_id: str
    next_time: time
    flag: bool

import hashlib
import random
from datetime import time
from enum import Enum

from pymongo.collection import Collection

__morning = 10
__evening = 22


def check_not_empty(collection:Collection):
    if collection.count_documents({}) > 0:
        return True
    return False


def calculate_hash(text: str):
    return int(hashlib.md5(text.encode('utf-8')).hexdigest(), 16)


def get_next_time(old_time: time):
    now = time.strftime()
    print(now)
    if old_time is None:
        return


def get_random_hour(current_time: time):
    global __morning, __evening
    rand_num = random.randint(2, 10)
    next_hour = current_time.hour + rand_num
    if next_hour > __morning and next_hour < __evening:
        return time(hour=next_hour)
    else:
        random_minute = random.randint(3, 59)
        return time(hour=__morning, minute=random_minute)



class DictionaryGrope(Enum):
    GREETINGS_TRIG_GROPE = 1
    JOKES_TRIG_GROPE = 2
    FOUL_LANG_TRIG_GROPE = 3
    FOUL_LANG_GROPE = 4
    DEFAULT = -1

    @staticmethod
    def get_grope(command: str):
        if command.find('add_jokes_trig') != -1:
            return DictionaryGrope.JOKES_GROPE
        elif command.find('add_greet_trig') != -1:
            return DictionaryGrope.GREETINGS_GROPE
        elif command.find('add_foul_trig') != -1:
            return DictionaryGrope.FOUL_LANG_TRIG_GROPE
        elif command.find('add_foul_trig') != -1:
            return DictionaryGrope.FOUL_LANG_GROPE
        return DictionaryGrope.DEFAULT

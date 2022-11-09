import os

from application.dataset_api.parse_utils import ParseUtils
from application.datasource.repositories.repo_utils import DictionaryGrope
from application.configuration import *

__tmp_storage_path: str
__parse_utils: ParseUtils


def init_data_handler(parse_utils):
    global __tmp_storage_path, __parse_utils
    __tmp_storage_path = os.environ.get('FILE_TMP_DESTINATION')
    __parse_utils = parse_utils


async def handle_jokes_registry(file_name, download_file_callback=None):
    if download_file_callback == None: return
    global __tmp_storage_path

    destination = f'{__tmp_storage_path}/{file_name}'
    try:
        await download_file_callback(destination)
        file_str = read_file(destination)
        await __parse_utils.parse_html_jokes(file_str)
    finally:
        if os.path.exists(destination):
            os.remove(destination)


async def handle_answer_registry(file_name, download_file_callback=None):
    if download_file_callback == None: return
    global __tmp_storage_path

    destination = f'{__tmp_storage_path}/{file_name}'
    try:
        await download_file_callback(destination)
        file_str = read_file(destination)
        __parse_utils.add_foul_answers(file_str)
    finally:
        if os.path.exists(destination):
            os.remove(destination)


async def handle_words(filename, download_file_callback=None, grope=DictionaryGrope.DEFAULT, upd_callback=None):
    if download_file_callback == None\
             or grope == DictionaryGrope.DEFAULT:
        return

    global __tmp_storage_path
    destination = f'{__tmp_storage_path}/{filename}'
    try:
        await download_file_callback(destination)
        file_str = read_file(destination)
        match grope:
            case DictionaryGrope.GREETINGS_TRIG_GROPE:
                __parse_utils.add_greetings_trig_words(file_str)

            case DictionaryGrope.JOKES_TRIG_GROPE:
                __parse_utils.add_jokes_trig_words(file_str)

            case DictionaryGrope.FOUL_LANG_TRIG_GROPE:
                __parse_utils.add_foul_lang_trig_words(file_str)

            case DictionaryGrope.FOUL_LANG_GROPE:
                __parse_utils.add_foul_lang_words(file_str)
    finally:
        if upd_callback is not None: upd_callback()
        if os.path.exists(destination):
            os.remove(destination)


def save_file(file):
    tmp_file = open(__tmp_storage_path, 'w', encoding='UTF-8')
    tmp_file.write(file)
    tmp_file.close()

def read_file(file_name):
    f = open(file_name, 'r', encoding='UTF-8')
    file_data = f.read()
    f.close()
    return file_data

from bs4 import BeautifulSoup
import re

from application.datasource.repositories.jokes_repository import JokesRepository
from application.datasource.repositories.words_repository import WordsRepository

required_file_extension = '.html'


class ParseUtils:
    __jokes_repository: JokesRepository
    __words_repository: WordsRepository

    def __init__(self, jokes_repository, __words_repository):
        self.__jokes_repository = jokes_repository
        self.__words_repository = __words_repository

    # async def parse_html_jokes(self, file):
    #     if is_supported_file_extension(file):
    #         file_data = read_file(f'application/temp_data/{file}')
    #         soup = BeautifulSoup(file_data, 'html.parser')
    #         jokes = [tag.text for tag in soup.findAll('div', {"class": "text"})]
    #         jokes_parsed = []
    #
    #         for joke in jokes:
    #
    #             tmp = re.sub('[^ ](-|—|-|–)', ' —', joke)
    #             tmp = tmp.strip()
    #
    #             if len(tmp) > 10 and tmp.find('http') == -1:
    #                 jokes_parsed.append(compile_json(tmp))
    #
    #         await self.__jokes_repository.insert_jokes_dataset(jokes_parsed)
    #         return
    #     else:
    #         return 'unsupported file extension'

    async def parse_html_jokes(self, file: str):
        soup = BeautifulSoup(file, 'html.parser')
        jokes = [tag.text for tag in soup.findAll('div', {"class": "text"})]
        beautified_jokes = beautify_jokes(jokes)

        await self.__jokes_repository.insert_jokes_dataset(beautified_jokes)
        return

    def add_greetings_triggers(self, file: str):
        trigger_words = beautify_triggers(file)
        self.__words_repository.update_greetings_triggers(trigger_words)

    def add_joke_triggers(self, file: str):
        trigger_words = beautify_triggers(file)
        self.__words_repository.update_greetings_triggers(trigger_words)


def beautify_jokes(jokes: list):
    jokes_parsed = []
    for joke in jokes:
        tmp = re.sub('[^ ](-|—|-|–)', ' —', joke)
        tmp = re.sub('(-|—|-|–)[^ ]', '— ', tmp)
        tmp = tmp.strip()
        if len(tmp) > 10 and tmp.find('http') == -1:
            jokes_parsed.append(compile_json(tmp))
    return jokes_parsed


def beautify_triggers(words: str):
    split_lines = words.split('\n')
    result = []
    for word in split_lines:
        tmp = word.strip()
        if tmp != "":
            result.append(tmp)
    return result


def read_file(file_name):
    f = open(file_name, 'r', encoding='UTF-8')
    file_data = f.read()
    f.close()
    return file_data


def compile_json(text: str):
    return {"text": text}

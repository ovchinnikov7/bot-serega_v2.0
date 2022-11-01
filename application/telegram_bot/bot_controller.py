import os

import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ContentType
from aiogram.utils import executor
# from aiogram.dispatcher import Dispatcher, filters

from telebot.apihelper import get_file

from application.dataset_api.parse_utils import ParseUtils
from application.datasource.repositories.users_stats_repository import UserStatsRepository
from application.datasource.repositories.jokes_repository import JokesRepository
from application.telegram_bot.message_utils import get_user_first_name, get_user_id, get_word_form

__bot_token = users = os.environ.get('API_TOKEN')
__update_jokes_token = os.environ.get('UPDATE_JOKES_TOKEN')


__bot = Bot(token=__bot_token)
dp = Dispatcher(__bot)
__joke_repository: JokesRepository
__users_repository: UserStatsRepository
__parse_utils: ParseUtils

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

joke_trigers = ['анек', 'fytr', 'anek']

def init_bot_handlers(jokes_repository,
                      users_repository,
                      parse_utils):
    global __joke_repository, __users_repository, __parse_utils
    __joke_repository = jokes_repository
    __users_repository = users_repository
    __parse_utils = parse_utils

# @dp.message_handler(lambda msg: msg.text.lower() in joke_trigers)
@dp.message_handler(lambda msg: any(word in msg.text.lower() for word in joke_trigers))
async def message_handler(message: types.Message):
    joke = __joke_repository.get_random_joke()
    await message.answer(joke)


@dp.message_handler(CommandStart())
async def message_handler(message: types.Message):
    user_name = get_user_first_name(message)
    user_id = get_user_id(message)
    user_stats = __users_repository.find_user(user_id)
    await message.reply(f'{user_name} сходил нахуй {user_stats} {get_word_form(user_stats)}')


# @dp.message_handler(filters.Text(contains=['add_new_jokes'], ignore_case=True), content_types=ContentType.DOCUMENT)
@dp.message_handler(commands=['add_new_jokes'], commands_ignore_caption=False, content_types=ContentType.DOCUMENT)
async def add_new_jokes(message: types.Message):
    message_text = get_message_text(message)
    if not have_privilege(message_text, __update_jokes_token):
        await message.answer(invalid_token_message())
        return
    else:
        if is_supported_file_extension(message.document.file_name):
            file = get_file(message.document.file_id).download()
            await __parse_utils.parse_html_jokes(file)
            await message.answer('все путем')
            return
    await message.answer(invalid_token_message())
    return



def is_supported_file_extension(file_name):
    extension = os.path.splitext(file_name)[1]
    if file_name.find(extension):
        return True
    return False

    # else:
        # file_id = message.document.file_id
        #
        # file = get_file(file_id).download()

        # await message.answer(answer)

    # answer: str
    # if not have_privilege(message.text, __update_jokes_token):
    #     answer = invalid_token_message()
    # else:

    # print("ABOBA работает?")
    # print(file)

    # global __update_joks_token
    # text = message.text
    # if __update_joks_token in text:


    #     await message.answer('Начинается обработка');
    #     file = get_file(message.document).download()
    #     await message.answer('Реестр успешно обработан!');
    #
    # print(message)
    # await message.answer("Привет")

    # await message.answer("есть пробитие")
    # file = get_file(message.document).download()
    # print(f'file = {file:>10}')
    # print(f'file name = {message.document.file_name:>10}')
    # with open("custom/file.doc", 'wb') as f:
    #     context.bot.get_file(update.message.document).download(out=f)

@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    try:
        raise exception
    except Exception as e:
        logger.exception("Cause exception {e} in update {update}", e=e, update=update)
        # sentry_sdk.capture_exception(e)
    return True


def invalid_token_message():
    return "Твой батя пидор, сынок..."

def run_bot():
    executor.start_polling(dp)

def have_privilege(text: str, token: str):
    if text.find(token) != -1:
        return True
    return False

def get_message_text(message: types.Message):
    if message.text is not None:
        return message.text
    if message.html_text is not None:
        return message.html_text
    if message.md_text is not None:
        return message.md_text
    return ""

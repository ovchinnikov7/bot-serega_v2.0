import os

import logging

import asyncio
import random
from os.path import join, dirname

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import ContentType
from aiogram.utils import executor
from dotenv import load_dotenv

from application.configuration import *

from application.dataset_api.data_handler import handle_jokes_registry, handle_words, handle_answer_registry
from application.datasource.repositories.repo_utils import DictionaryGrope
from application.datasource.repositories.users_stats_repository import UserStatsRepository
from application.datasource.repositories.jokes_repository import JokesRepository
from application.datasource.repositories.words_repository import WordsRepository
from application.telegram_bot.bot_utils import get_user_first_name, get_user_id, get_word_form, get_probability, \
    get_reply_username

__bot_token = users = os.environ.get('API_TOKEN')
__update_jokes_token = os.environ.get('UPDATE_JOKES_TOKEN')

__bot = Bot(token=__bot_token)
__my_names: ()
dp = Dispatcher(__bot)
__joke_repository: JokesRepository
__users_repository: UserStatsRepository
__words_repository: WordsRepository

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

__greetings_triggers: [str]
__jokes_triggers: [str]
__foul_lang_triggers: [str]
__foul_language: [str]


def init_bot_handlers(jokes_repository,
                      users_repository,
                      words_repository):
    global __bot, \
        __my_names, \
        __joke_repository, \
        __users_repository, \
        __words_repository, \
        __greetings_triggers, \
        __jokes_triggers, \
        __foul_lang_triggers, \
        __foul_language

    asyncio.ensure_future(init_my_name())

    # get repositories
    __joke_repository = jokes_repository
    __users_repository = users_repository
    __words_repository = words_repository

    # initialize dictionaries
    update_words()


@dp.message_handler(lambda msg:
                    any(word in msg.text.lower()
                        for word in __jokes_triggers))
async def message_handler(message: types.Message):
    is_foul_land = is_foul_lang(get_message_text(message).lower())

    if is_foul_land and get_probability():
        await message.answer('А пососать не завернуть? Грубиян Пиздарваныч')
        return
    elif is_foul_land:
        await message.answer(fuck_user(message))
        return
    joke = __joke_repository.get_random_joke()
    await message.answer(joke)
    return


@dp.message_handler(lambda msg: any(word in msg.text.lower() for word in __my_names)
                              | any(word in get_reply_username(msg) for word in __my_names))
async def message_handler(message: types.Message):
    text = get_message_text(message).lower()

    if is_foul_lang(text):
        answer = __words_repository.get_foul_answer()
        await message.answer(answer)
    elif is_greetings(text) and get_probability():
        await message.reply('Здаров чупакабрик!')
    else:
        await message.answer(fuck_user(message))


@dp.message_handler(CommandStart())
async def message_handler(message: types.Message):
    await __users_repository.user_start(message)
    insult = random.choice(__foul_language).title()
    await message.reply(f'Привет! {insult} {get_user_first_name(message)}')


@dp.message_handler(commands=['stats'])
async def message_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = get_user_first_name(message)
    insult = random.choice(__foul_language).title()
    if __users_repository.is_user_exist(user_id):
        user_stats = __users_repository.get_user_stats(user_id)
        await message.answer(f'Кста! {insult} {user_name} сходил нахуй {user_stats} {get_word_form(user_stats)}')
    else:
        __users_repository.fuck_off_inc(user_id)
        await message.answer(f'Пошел нахуй, {insult} {user_name}!')

# @dp.message_handler(CommandStart())
# async def message_handler(message: types.Message):
#     user_name = get_user_first_name(message)
#     user_id = get_user_id(message)
#     insult = random.choice(__foul_language).title()
#     if __users_repository.is_user_exist(user_id):
#         user_stats = __users_repository.get_user_stats(user_id)
#         await message.answer(f'Кста! {insult} {user_name} сходил нахуй {user_stats} {get_word_form(user_stats)}')
#     else:
#         __users_repository.fuck_off_inc(user_id)
#         await message.answer(f'Пошел нахуй, {insult} {user_name}!')

@dp.message_handler(commands=['add_new_jokes'],
                    commands_ignore_caption=False,
                    content_types=ContentType.DOCUMENT)
async def add_new_jokes(message: types.Message):
    message_text = get_message_text(message)
    if not have_privilege(message_text, __update_jokes_token):
        await message.answer('Твой батя пидор, сынок...')
        return
    else:
        if is_supported_file_extension(message.document.file_name):
            asyncio.ensure_future(handle_jokes_registry(
                message.document.file_name,
                message.document.download # <- callback that download file
            ))
            await message.answer('Я попробую')
            return
        await message.answer('Хуйню скинул, чел...')

@dp.message_handler(commands=['add_new_answer'],
                    commands_ignore_caption=False,
                    content_types=ContentType.DOCUMENT)
async def add_new_jokes(message: types.Message):
    message_text = get_message_text(message)
    if not have_privilege(message_text, __update_jokes_token):
        await message.answer('Твой батя пидор, сынок...')
        return
    else:
        if is_supported_file_extension(message.document.file_name):
            asyncio.ensure_future(handle_answer_registry(
                message.document.file_name,
                message.document.download # <- callback that download file
            ))
            await message.answer('Я попробую')
            return
        await message.answer('Хуйню скинул, чел...')

@dp.message_handler(commands=['add_jokes_trig', 'add_greet_trig', 'add_foul_lang_trig', 'add_foul_trig'],
                    commands_ignore_caption=False,
                    content_types=ContentType.DOCUMENT)
async def add_new_words(message: types.Message):
    message_text = get_message_text(message)
    if not have_privilege(message_text, __update_jokes_token):
        await message.answer('Твой батя пидор, сынок...')
        return
    grope = DictionaryGrope.get_grope(message.caption)
    asyncio.ensure_future(handle_words(
        message.document.file_name,
        message.document.download,  # <- callback that download file
        grope,
        upd_callback=update_words
    ))
    await message.answer('Я попробую')


def is_supported_file_extension(file_name):
    extension = os.path.splitext(file_name)[1]
    if file_name.find(extension):
        return True
    return False



# @dp.message_handler(commands=['help'])
# async def get_chat_members(message: types.Message):
#     # chat = await __bot.get_chat_member('*', message.chat.id)
    # chat = await __bot.get_chat(message.chat.id)
    # await __bot.send_message(message.chat.id, 'Пишли все нахуй!')
    # aiogram.methods.get_chat_member.GetChatMember(message.chat.id)
    # chat_members = __bot.get_chat_members(message.chat.id)


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    try:
        raise exception
    except Exception as e:
        logger.exception("Cause exception {e} in update {update}", e=e, update=update)
        # sentry_sdk.capture_exception(e)
    return True


async def init_my_name():
    global __bot, __my_names
    me = await __bot.get_me()
    __my_names = (me.first_name.lower(), me.username.lower())


def is_greetings(text: str):
    for word in __greetings_triggers:
        if text.find(word) != -1:
            return True
    return False


def is_foul_lang(text: str):
    for word in __foul_lang_triggers:
        if word.search(text) != None:
            return True
    return False


def fuck_user(message: types.Message) -> str:
    user_name = get_user_first_name(message)
    user_id = get_user_id(message)
    insult = random.choice(__foul_language).title()
    __users_repository.fuck_off_inc(user_id)
    return f'Пошел нахуй, {insult} {user_name}!'


def update_words():
    global __greetings_triggers, __jokes_triggers, __foul_lang_triggers, __foul_language
    __greetings_triggers = __words_repository.get_greeting_triggers()
    __jokes_triggers = __words_repository.get_joke_triggers()
    __foul_lang_triggers = __words_repository.get_foul_lang_triggers()
    __foul_language = __words_repository.get_foul_lang_words()


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

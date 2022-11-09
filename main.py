from application.dataset_api.data_handler import init_data_handler
from application.dataset_api.parse_utils import ParseUtils
from application.datasource.repositories.repositories import MongoRepositories
from application.telegram_bot.bot_controller import init_bot_handlers, run_bot


def main():
    # Init datasource
    repositories = MongoRepositories.instance()

    pars_utils = ParseUtils(
        repositories.get_jokes_repository(),
        repositories.get_words_repository()
    )
    init_data_handler(pars_utils)
    # await pars_utils.parse_html_jokes('messages.html')
    # pars_utils.add_triggers()

    # get_file_extension('messages.html')

    # Init bot controller, setup repositories
    init_bot_handlers(
        repositories.get_jokes_repository(),
        repositories.get_users_repository(),
        repositories.get_words_repository()
    )

    # Start bot
    run_bot()


if __name__ == "__main__":
    main()

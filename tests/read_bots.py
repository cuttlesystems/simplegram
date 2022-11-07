from b_logic.bot_api import BotApi
from cuttle_builder.bot_generator import BotGenerator

SUITE_ADDR = 'http://127.0.0.1:8000/'
USERNAME = 'test'
PASSWORD = '1'

BOT_ID = 2

# BOT_ID = 95


if __name__ == '__main__':
    bot_api = BotApi(SUITE_ADDR)
    bot_api.authentication(USERNAME, PASSWORD)

    bot = bot_api.get_bot_by_id(BOT_ID)

    bot = BotGenerator(bot_api, bot)
    bot.create_bot()
    # print(bot)
    # messages = bot_api.get_messages(bot)
    # for message in messages:
    #     print('    ', message)
    #     variants = bot_api.get_variants(message)
    #     for variant in variants:
    #         print('    ' * 2, variant)

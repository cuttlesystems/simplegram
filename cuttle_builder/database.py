from b_logic.bot_api import BotApi


SUITE_ADDR = 'http://127.0.0.1:8000/'
USERNAME = 'test'
PASSWORD = '1'

BOT_ID = 2

if __name__ == '__main__':
    bot_api = BotApi(SUITE_ADDR)
    bot_api.authentication(USERNAME, PASSWORD)

    bot = bot_api.get_bot_by_id(BOT_ID)
    messages = bot_api.get_messages(bot)
    for message in messages:
        print(message.id)
        variants = bot_api.get_variants(message)
        for variant in variants:
            print('    ' * 2, variant)
        break
from api.bot_api import BotApi


SUITE_ADDR = 'http://127.0.0.1:8000/'
USERNAME = 'test_user'
PASSWORD = '123'


if __name__ == '__main__':
    bot_api = BotApi(SUITE_ADDR)
    bot_api.authentication('test_user', '123')

    bots = bot_api.get_bots()
    for bot in bots:
        print(bot)
        messages = bot_api.get_messages(bot)
        for message in messages:
            print('    ', message)
            variants = bot_api.get_variants(message)
            for variant in variants:
                print('    ' * 2, variant)

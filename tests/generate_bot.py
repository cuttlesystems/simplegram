from b_logic.bot_api import BotApi
from cuttle_builder.bot_generator import BotGenerator
from cuttle_builder.bot_generator_db import BotGeneratorDb
from tests.connection_settings import ConnectionSettings


if __name__ == '__main__':
    settings = ConnectionSettings()
    bot_api = BotApi(settings.site_addr)
    bot_api.authentication(settings.username, settings.password)

    bot = bot_api.get_bot_by_id(settings.bot_id)

    bot = BotGeneratorDb(bot_api, bot)
    bot.create_bot()

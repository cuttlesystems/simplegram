from pathlib import Path

from b_logic.bot_api.bot_api_by_requests import BotApi
from cuttle_builder.bot_generator_db import BotGeneratorDb
from app_tests.connection_settings import ConnectionSettings


if __name__ == '__main__':
    settings = ConnectionSettings()
    bot_api = BotApi(settings.site_addr)
    bot_api.authentication(settings.username, settings.password)

    bot = bot_api.get_bot_by_id(settings.bot_id)

    bot_dir = str(Path(__file__).parent / f'bot_{bot.id}')
    bot_generator = BotGeneratorDb(bot_api, bot, bot_dir)
    bot_generator.create_bot()

    print(f'Сгенерирован исходный код бота с номером {bot.id}')

from pathlib import Path

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from app_tests.connection_settings import ConnectionSettings
from cuttle_builder.bot_generator_mini_app import BotGeneratorMiniApp

if __name__ == '__main__':
    settings = ConnectionSettings()
    bot_api = BotApiByRequests(settings.site_addr)
    bot_api.authentication(settings.username, settings.password)

    bot = bot_api.get_bot_by_id(settings.bot_id)

    bot_dir = str(Path(__file__).parent / f'bot_{bot.id}')
    with BotGeneratorMiniApp(bot_api, bot, bot_dir) as bot_generator:
        bot_generator.create_bot()

    print(f'Сгенерирован исходный код бота с номером {bot.id}')
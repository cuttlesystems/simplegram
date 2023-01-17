from pathlib import Path

from b_logic.bot_api.i_bot_api import IBotApi
from b_logic.data_objects import BotDescription
from backend.bot_django_project.bot_constructor.log_configs import logger_django
from cuttle_builder.bot_generator import BotGenerator


class BotGeneratorDb(BotGenerator):
    def __init__(self, bot_api: IBotApi, bot: BotDescription, bot_dir: str):
        assert isinstance(bot_api, IBotApi)
        assert isinstance(bot, BotDescription)

        commands = bot_api.get_commands(bot)
        messages = bot_api.get_messages(bot)

        bot_logs_file_path = self._get_bot_logs_file_path(bot, bot_dir)
        # соберем варианты, принадлежащие всем сообщениям в один список
        all_variants = []
        for mes in messages:
            message_variants = bot_api.get_variants(mes)
            all_variants.extend(message_variants)
        print(bot.start_message_id)
        super().__init__(messages, all_variants, commands, bot, bot_dir)

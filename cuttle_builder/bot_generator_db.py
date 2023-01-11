from b_logic.bot_api.i_bot_api import IBotApi
from b_logic.data_objects import BotDescription
from cuttle_builder.bot_generator import BotGenerator
from bot_constructor.settings import BOTS_LOG_DIR
import logging

logger = logging.getLogger('django')


class BotGeneratorDb(BotGenerator):
    def __init__(self, bot_api: IBotApi, bot: BotDescription, bot_dir: str):
        assert isinstance(bot_api, IBotApi)
        assert isinstance(bot, BotDescription)

        commands = bot_api.get_commands(bot)
        messages = bot_api.get_messages(bot)

        bot_logs_dir = self.get_bot_logs_path(bot)
        # соберем варианты, принадлежащие всем сообщениям в один список
        all_variants = []
        for mes in messages:
            message_variants = bot_api.get_variants(mes)
            all_variants.extend(message_variants)
        print(bot.start_message_id)
        super().__init__(messages, all_variants, commands, bot, bot_dir, bot_logs_dir)

    def get_bot_logs_path(self, bot: BotDescription) -> str:
        """
        Получает полный путь к файлу для хранения логов бота.

        Args:
            bot (BotDescription): экземпляр BotDescription

        Returns (str): Полный путь к файлу логов бота.

        """
        assert isinstance(bot, BotDescription)
        bot_log_path = BOTS_LOG_DIR / f'bot_{bot.id}.log'
        logger.info(f'Bot logs path: {bot_log_path}')
        return str(bot_log_path)

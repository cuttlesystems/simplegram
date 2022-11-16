from pathlib import Path

from b_logic.bot_api import BotApi
from b_logic.data_objects import BotDescription
from cuttle_builder.bot_generator import BotGenerator


class BotGeneratorDb(BotGenerator):
    def __init__(self, bot_api: BotApi, bot: BotDescription):
        assert isinstance(bot_api, BotApi)
        assert isinstance(bot, BotDescription)

        messages = bot_api.get_messages(bot)

        # соберем варианты, принадлежащие всем сообщениям в один список
        all_variants = []
        for mes in messages:
            message_variants = bot_api.get_variants(mes)
            all_variants.extend(message_variants)

        bot_dir = str(Path(__file__).parent.parent / f'bot_{bot.id}')
        super().__init__(messages, all_variants, bot.start_message_id, bot.id, bot.bot_token, bot_dir)

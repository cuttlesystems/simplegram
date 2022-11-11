from b_logic.bot_api import BotApi
from b_logic.data_objects import BotDescription
from cuttle_builder.bot_generator import BotGenerator


class BotGeneratorDb(BotGenerator):
    def __init__(self, bot_api: BotApi, bot: BotDescription):
        messages = bot_api.get_messages(bot)
        all_vars = []
        for mes in messages:
            var = bot_api.get_variants(mes)
            all_vars.extend(var)

        super().__init__(messages, all_vars, bot.start_message_id, bot.id)

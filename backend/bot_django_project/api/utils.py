from .exceptions import InvalidBotTokenWhenGenerateBot

from bots.models import Bot


def check_bot_token_when_generate_bot(bot: Bot) -> None:
    """
    Проверка, что токен бота не пустой.

    Args:
        bot (Bot): экземпляр бота

    Raises:
        InvalidBotTokenWhenGenerateBot
    """
    assert isinstance(bot, Bot)
    if not bot.token:
        raise InvalidBotTokenWhenGenerateBot()

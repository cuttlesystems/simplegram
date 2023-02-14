from django.utils.autoreload import file_changed, autoreload_started

from api.exceptions import InvalidBotTokenWhenGenerateBot
from bots.models import Bot
from bots.started_bots_manage.restart_bot_manage import stop_all_running_bots_before_autoreload, start_all_launched_bots


# Сигнал file_changed испускается при обнаружении изменений в коде на запущенном сервере
# После сигнала file_changed следует перезагрузка сервера
file_changed.connect(stop_all_running_bots_before_autoreload)
autoreload_started.connect(start_all_launched_bots)


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

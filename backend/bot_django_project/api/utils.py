from pathlib import Path

from api.exceptions import InvalidBotTokenWhenGenerateBot
from b_logic.bot_processes_manager import BotProcessesManagerSingle
from b_logic.bot_runner import BotRunner
from bots.models import Bot
from django.utils.autoreload import file_changed


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


def stop_all_running_bots_before_autoreload(sender, **kwargs) -> None:
    """
    Остановка всех запущенных ботов при перезапуске сервера.

    Args:
        sender: Отправитель сигнала. Обязательный аргумент.
        **kwargs: Произвольные аргументы. Обязательный аргумент.
        (https://docs.djangoproject.com/en/4.1/topics/signals/#receiver-functions)
    """
    print('before autoreload')
    process_manager = BotProcessesManagerSingle()
    all_running_processes = process_manager.get_all_processes_info()
    if len(all_running_processes) > 0:
        for process in all_running_processes.values():
            process.bot_runner.stop()


# Сигнал file_changed испускается при обнаружении изменений в коде на запущенном сервере
# После сигнала file_changed следует перезагрузка сервера
file_changed.connect(stop_all_running_bots_before_autoreload)


def create_dir_if_it_doesnt_exist(directory: Path) -> None:
    """
    Создает директорию если её не существует

    Args:
        directory (Path): путь к директории

    """
    directory.mkdir(exist_ok=True)

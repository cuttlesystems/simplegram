from pathlib import Path

from b_logic.bot_processes_manager import BotProcessesManagerSingle
from bot_constructor.log_configs import logger_django
from bot_constructor.settings import BOTS_DIR
from b_logic.bot_runner import BotRunner
from bots.started_bots_manage.started_bots_storage_manager import StartedBotsStorageManager
from process_manager_utils.notification_sender_to_bot_manager import NotificationSenderToBotManager


def get_bot_dir(bot_id: int) -> Path:
    assert isinstance(bot_id, int)
    bot_dir = BOTS_DIR / f'bot_{bot_id}'
    return bot_dir


def stop_bot_if_it_run(bot_id: int):
    assert isinstance(bot_id, int)
    bot_process_manager = BotProcessesManagerSingle()
    already_started_bot = bot_process_manager.get_process_info(bot_id)
    if already_started_bot is not None:
        already_started_bot.bot_runner.stop()
        bot_process_manager.remove(bot_id)


def stop_all_running_bots_before_autoreload(sender, **kwargs) -> None:
    """
    Остановка всех запущенных ботов при перезапуске сервера.

    Args:
        sender: Отправитель сигнала. Обязательный аргумент.
        **kwargs: Произвольные аргументы. Обязательный аргумент.
        (https://docs.djangoproject.com/en/4.1/topics/signals/#receiver-functions)
    """
    logger_django.info_logging('Before autoreload.')
    process_manager = BotProcessesManagerSingle()
    all_running_processes = process_manager.get_all_processes_info()
    all_running_bots_list = [bot.bot_id for bot in all_running_processes.values() if not bot.is_terminated]
    logger_django.info_logging(f'Running bots: {all_running_bots_list}')
    if len(all_running_processes) > 0:
        for process in all_running_processes.values():
            process.bot_runner.stop()
    started_bots_storage_manager = StartedBotsStorageManager()
    started_bots_storage_manager.save_data(all_running_bots_list)


def start_all_launched_bots(sender, **kwargs) -> None:
    """
    Запуск всех остановленных перед autoreload ботов.
    Args:
        sender: Отправитель сигнала. Обязательный аргумент.
        **kwargs: Произвольные аргументы. Обязательный аргумент.
    """
    logger_django.info_logging('After autoreload.')
    started_bots_storage_manager = StartedBotsStorageManager()
    started_bots_list = started_bots_storage_manager.load_data()
    if started_bots_list is not None and len(started_bots_list) > 0:
        logger_django.info_logging(f'Bots need to start: {started_bots_list}')
        for bot_id in started_bots_list:
            bot_dir = get_bot_dir(bot_id)
            stop_bot_if_it_run(bot_id)
            notification_sender_to_manager = NotificationSenderToBotManager()
            runner = BotRunner(bot_dir, notification_sender_to_manager)
            process_id = runner.start()
            if process_id is not None:
                bot_process_manager = BotProcessesManagerSingle()
                bot_process_manager.register(bot_id, runner)
                notification_sender_to_manager.set_process_manager(bot_process_manager)
            logger_django.info_logging(f'Bot {bot_id} started after server reload. Process: {process_id}')
    else:
        logger_django.info_logging(f'No bots need to start.')

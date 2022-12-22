from pathlib import Path
from datetime import datetime

from git import Repo

from .exceptions import InvalidBotTokenWhenGenerateBot
from bots.models import Bot

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
UTC_6 = 21600


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


def get_info_about_last_commit() -> str:
    """
    Выводит информацию о последнем коммите из ветки main

    Returns:
        str: Информация о последнем коммите
    """
    repo = Repo(ROOT_DIR)
    latest_commit = repo.rev_parse('origin/main')
    hash = (str(latest_commit))[:7]
    author = latest_commit.author
    date_of_commit = datetime.utcfromtimestamp(latest_commit.committed_date + UTC_6).strftime('%Y-%m-%d %H:%M:%S')
    return f'Latest commit: {hash}, Author: {author}, Date: {date_of_commit}'

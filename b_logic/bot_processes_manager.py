from dataclasses import dataclass
from typing import Dict, Optional

from b_logic.bot_runner import BotRunner
from common_utils.singlethon import SingletonBase


@dataclass
class BotProcessInfo:
    bot_id: int
    bot_runner: BotRunner


class BotProcessesManagerSingle(metaclass=SingletonBase):
    """
    Синглтон для хранения данных о запущенных ботах
    (информация о идентификаторе процесса)
    """

    def __init__(self):
        self._processes: Dict[int, BotProcessInfo] = {}

    def register(self, bot_id: int, bot_runner: BotRunner) -> None:
        assert bot_id not in self._processes
        assert isinstance(bot_runner, BotRunner)
        process_info = BotProcessInfo(
            bot_id=bot_id,
            bot_runner=bot_runner
        )
        self._processes[bot_id] = process_info

    def get_process_info(self, bot_id: int) -> Optional[BotProcessInfo]:
        return self._processes.get(bot_id)

    def get_all_processes_info(self) -> Dict[int, BotProcessInfo]:
        return self._processes

    def remove(self, bot_id: int) -> None:
        assert bot_id in self._processes
        del self._processes[bot_id]

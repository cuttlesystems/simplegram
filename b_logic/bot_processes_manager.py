from dataclasses import dataclass
from typing import Dict, Optional, List

from b_logic.bot_runner import BotRunner
from common_utils.singlethon import SingletonBase


@dataclass
class BotProcessInfo:
    bot_id: int
    bot_runner: BotRunner
    is_terminated: bool


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
            bot_runner=bot_runner,
            is_terminated=False
        )
        self._processes[bot_id] = process_info

    def get_process_info(self, bot_id: int) -> Optional[BotProcessInfo]:
        return self._processes.get(bot_id)

    def get_all_processes_info(self) -> Dict[int, BotProcessInfo]:
        return self._processes

    def get_all_running_bots_id_list(self) -> List[int]:
        return [bot.bot_id for bot in self._processes.values() if not bot.is_terminated]

    def remove(self, bot_id: int) -> None:
        assert bot_id in self._processes
        if bot_id in self._processes:
            del self._processes[bot_id]

    def find_bot_id_by_process_id(self, process_id: int):
        for bot_id, process_info in self._processes.items():
            if process_info.bot_runner.process_id == process_id:
                return bot_id

    def mark_process_as_error(self, bot_id: int):
        current_procerss_info = self._processes[bot_id]
        current_procerss_info.is_terminated = True
        self._processes[bot_id] = current_procerss_info

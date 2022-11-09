from dataclasses import dataclass
from typing import Dict, Optional
from utils.singlethon import SingletonBase


@dataclass
class BotProcessInfo:
    bot_id: int
    process_id: int


class BotProcessesManager(metaclass=SingletonBase):
    def __init__(self):
        self._processes: Dict[int, BotProcessInfo] = {}

    def register(self, bot_id: int, process_id: int):
        assert bot_id not in self._processes
        process_info = BotProcessInfo(
            bot_id=bot_id,
            process_id=process_id
        )
        self._processes[bot_id] = process_info

    def get_process_info(self, bot_id: int) -> Optional[BotProcessInfo]:
        return self._processes.get(bot_id)

    def remove(self, bot_id: int):
        assert bot_id in self._processes
        del self._processes[bot_id]

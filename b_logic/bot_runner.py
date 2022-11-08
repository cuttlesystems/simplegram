import subprocess
import sys
from pathlib import Path
from typing import Optional
# import psutil


class BotRunner:
    def __init__(self, bot_directory: Path):
        assert isinstance(bot_directory, Path)
        self._bot_directory = bot_directory

    def start(self) -> Optional[int]:
        result = None
        if self._bot_directory.exists():
            bot_py_executable = self._bot_directory / 'app.py'
            if bot_py_executable.exists():
                bot_process = subprocess.Popen([sys.executable, bot_py_executable])
                result = bot_process.pid
        return result

    def stop(self, process_id: int):
        # process = psutil.Process(process_id)
        # print(process.name())
        pass

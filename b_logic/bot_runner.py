import subprocess
import sys
from pathlib import Path
from typing import Optional
import psutil


class BotRunner:
    def __init__(self, bot_directory: Optional[Path]):
        assert isinstance(bot_directory, Path) or bot_directory is None
        self._bot_directory = bot_directory

    def start(self) -> Optional[int]:
        result = None
        if self._bot_directory.exists():
            bot_py_executable = self._bot_directory / 'app.py'
            if bot_py_executable.exists():
                bot_process = subprocess.Popen([sys.executable, bot_py_executable])
                result = bot_process.pid
        return result

    def stop(self, process_id: int) -> bool:
        result = False
        try:
            process = psutil.Process(process_id)
            print(process.name(), process.cmdline())
            process_name = process.name()
            if '.' in process_name:
                only_name = process_name.split('.')[0]
            else:
                only_name = process_name
            only_name = only_name.lower()
            if only_name in ['python', 'python3']:
                print(f'kill bot with pid: {process_id}')
                process.kill()
                result = True
            else:
                print('Invalid process id. It is not a python process')
        except psutil.NoSuchProcess:
            print('Can not found process')
        return result

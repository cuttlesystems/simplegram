import subprocess
import sys
import time
from io import TextIOWrapper, BufferedReader
from pathlib import Path
from threading import Thread
from typing import Optional
import psutil


class BotRunner:
    def __init__(self, bot_directory: Optional[Path]):
        assert isinstance(bot_directory, Path) or bot_directory is None
        self._bot_directory = bot_directory
        self._stdout_thread: Optional[Thread] = None

    def start(self) -> Optional[int]:
        result = None
        self._stop_pipe()
        if self._bot_directory.exists():
            bot_py_executable = self._bot_directory / 'app.py'
            if bot_py_executable.exists():
                bot_process = subprocess.Popen(
                    [sys.executable, bot_py_executable],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    # bufsize=1,
                    # universal_newlines=True
                )
                self._stdout_thread = Thread(target=self._reader, args=[bot_process.stdout])
                self._stdout_thread.start()
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
                self._stop_pipe()
                result = True
            else:
                print('Invalid process id. It is not a python process')
        except psutil.NoSuchProcess:
            print('Can not found process')
        return result

    def _stop_pipe(self):
        if self._stdout_thread is not None:
            self._stdout_thread.join()
            self._stdout_thread = None

    def _reader(self, pipe: BufferedReader):
        assert isinstance(pipe, BufferedReader)
        print('reader start')
        with pipe:
            for line in iter(pipe.readline, b''):
                print(line)
                # time.sleep(0.5)
                # queue.put((pipe, line))
        print('reader end')


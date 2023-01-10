import subprocess
import sys
import time
import typing
from io import TextIOWrapper, BufferedReader, FileIO
from pathlib import Path
from threading import Thread
from typing import Optional
import psutil


class BotRunner:
    _MAX_LOG_LEN_LINES = 300

    def __init__(self, bot_directory: Optional[Path]):
        assert isinstance(bot_directory, Path) or bot_directory is None
        self._bot_directory = bot_directory
        self._stdout_thread: Optional[Thread] = None
        self._stderr_thread: Optional[Thread] = None
        self._process_id: Optional[int] = None

        self._bot_stdout_log: typing.List[str] = []
        self._bot_stderr_log: typing.List[str] = []

    def get_bot_stdout(self) -> typing.List[str]:
        return self._bot_stdout_log

    def get_bot_stderr(self) -> typing.List[str]:
        return self._bot_stderr_log

    @property
    def process_id(self) -> Optional[int]:
        return self._process_id

    def start(self) -> Optional[int]:
        result = None
        self._bot_stdout_log = []
        self._bot_stderr_log = []
        self._stop_pipe()
        if self._bot_directory.exists():
            bot_py_executable = self._bot_directory / 'app.py'
            if bot_py_executable.exists():
                bot_process = subprocess.Popen(
                    [sys.executable, bot_py_executable],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=1,
                    universal_newlines=True
                )
                self._process_id = bot_process.pid
                self._stdout_thread = Thread(target=self._reader_stdout, args=[bot_process.stdout])
                self._stderr_thread = Thread(target=self._reader_stderr, args=[bot_process.stderr])

                self._stdout_thread.start()
                self._stderr_thread.start()
                result = self._process_id
        return result

    def stop(self) -> bool:
        result = False
        if self._process_id is not None:
            try:
                process = psutil.Process(self._process_id)
                print(process.name(), process.cmdline())
                process_name = process.name()
                if '.' in process_name:
                    only_name = process_name.split('.')[0]
                else:
                    only_name = process_name
                only_name = only_name.lower()
                if only_name in ['python', 'python3']:
                    print(f'kill bot with pid: {self._process_id}')
                    process.kill()
                    self._stop_pipe()
                    result = True
                else:
                    print('Invalid process id. It is not a python process')
            except psutil.NoSuchProcess:
                print('Can not found process')
        else:
            print('This bot is not started')
        return result

    def _stop_pipe(self):
        if self._stdout_thread is not None:
            self._stdout_thread.join()
            self._stdout_thread = None
        if self._stderr_thread is not None:
            self._stderr_thread.join()
            self._stderr_thread = None

    def _add_stdout_line(self, line: str):
        self._bot_stdout_log.append(line)
        if len(self._bot_stdout_log) > self._MAX_LOG_LEN_LINES:
            self._bot_stdout_log = self._bot_stderr_log[-self._MAX_LOG_LEN_LINES:]

    def _add_stderr_line(self, line: str):
        self._bot_stderr_log.append(line)
        if len(self._bot_stderr_log) > self._MAX_LOG_LEN_LINES:
            self._bot_stderr_log = self._bot_stderr_log[-self._MAX_LOG_LEN_LINES:]

    def _reader_stdout(self, pipe: TextIOWrapper):
        assert isinstance(pipe, TextIOWrapper)
        print('reader stdout start: ', type(pipe))
        with pipe:
            # for line in iter(pipe.readline, b''):
            #     print('out: ', line)
            line = 'line'
            while line != '':
                line = pipe.readline()
                if line != '':
                    self._add_stdout_line(line)
                    print('bot out: ', line.rstrip())

        print('reader stdout end')

    def _reader_stderr(self, pipe: TextIOWrapper):
        assert isinstance(pipe, TextIOWrapper)
        print('reader stderr start: ', type(pipe))

        with pipe:
            # for line in iter(pipe.readline, b''):
            #     print('err: ', line)
            line = 'line'
            while line != '':
                line = pipe.readline()
                if line != '':
                    self._add_stderr_line(line)
                    print('bot err: ', line.rstrip())

        print('reader stderr end')


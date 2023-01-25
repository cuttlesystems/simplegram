import os
import platform
import sys
from enum import Enum

import venv
from pathlib import Path
import shutil
import pip
from typing import Optional
from subprocess import run


class OsClass(Enum):
    LINUX_CLASS = 'linux_class'
    WINDOWS_CLASS = 'windows_class'


def define_os() -> OsClass:
    current_os = platform.system()
    if current_os == "Linux" or current_os == 'Darwin':
        result = OsClass.LINUX_CLASS
    elif current_os == "Windows":
        result = OsClass.WINDOWS_CLASS
    else:
        raise NotImplementedError(f'Unsupported os: {current_os}')
    return result


def get_venv_python_path(venv_dir: Path) -> Path:
    assert isinstance(venv_dir, Path)
    current_os = define_os()
    if current_os == OsClass.WINDOWS_CLASS:
        result = venv_dir / 'Scripts' / 'python.exe'
    elif current_os == OsClass.LINUX_CLASS:
        result = venv_dir / 'bin' / 'python3'
    else:
        raise NotImplementedError('Unsupported os')
    return result


if __name__ == '__main__':
    print(f'Current OS: ', define_os())
    test_venv_dir = Path('.') / 'test_venv'

    # if test_venv_dir.exists():
    #     shutil.rmtree(test_venv_dir)

    test_venv_dir.mkdir(exist_ok=True)

    # venv_dir = os.path.join(os.path.expanduser("~"), "test_venv")
    if not test_venv_dir.exists():
        venv.create(test_venv_dir, with_pip=True)

    print(sys.executable)

    # D:\Git Repos\tg_bot_constructor\deploy\build_desktop\test_venv\Scripts\python.exe - m pip\  install - -upgrade pip
    run([get_venv_python_path(test_venv_dir), '-m', 'pip', 'install', '--upgrade', 'pip'])
    run([get_venv_python_path(test_venv_dir), '-m', 'pip', 'install', '-r', 'requirements.txt'])

    exit(0)


    # def get_application_data_dir() -> Path:
    #     path: Optional[Path] = None
    #     result: Optional[Path] = None
    #     current_os = platform.system()
    #     if current_os == "Linux" or current_os == 'Darwin':
    #         path = Path.home()
    #         result = path / '.cuttle_systems' / 'bot_constructor'
    #     elif current_os == "Windows":
    #         path = Path(os.getenv('APPDATA'))
    #         result = path / 'cuttle_systems' / 'bot_constructor'
    #     else:
    #         raise NotImplementedError(f'Unsupported os: {current_os}')
    #     return result

    # if [ ! -d ./$GH_REPO/mini_app/venv/ ]
    #     then
    #         python3 -m venv ./$GH_REPO/mini_app/venv
    # source ./$GH_REPO/mini_app/venv/bin/activate


    current_os = platform.system()
    os.path.exists('./venv/')
    print(current_os)
    # if current_os == "Linux" or current_os == 'Darwin':
    #     if not os.path.exists('./venv/'):
    #         python3 -m venv . / venv
    #     source . / venv / bin / activate
    # elif current_os == "Windows":
    #     if [ ! -d . / venv / ]:
    #         python - m venv . / venv
    #     source . / venv / Scripts / activate
    #
    #     python - m venv venv_
    # else:
    #     raise NotImplementedError(f'Unsupported os: {current_os}')
    # return result
    #
    # Создание виртуальных сред выполняется путем выполнения pyvenvскрипта:
    #
    # pyvenv /path/to/new/virtual/environment
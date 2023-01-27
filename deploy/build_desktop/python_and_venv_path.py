# модуль, необходимый для выполнения скрипта 'build_executable.py' с использованием файла 'start_constructor.spec'

import platform
from enum import Enum
from pathlib import Path


class OsClass(Enum):
    LINUX_CLASS = 'linux_class'
    WINDOWS_CLASS = 'windows_class'


def get_script_dir() -> Path:
    """
    функция получения родительской директории запускаемого скрипта
    """
    return Path(__file__).parent



def get_current_os() -> OsClass:
    """
    функция получения операционной системы, в которой выполняется запуск
    """
    current_os = platform.system()
    if current_os == "Linux" or current_os == 'Darwin':
        result = OsClass.LINUX_CLASS
    elif current_os == "Windows":
        result = OsClass.WINDOWS_CLASS
    else:
        raise NotImplementedError(f'Unsupported os: {current_os}')
    return result


def get_venv_python_path(venv_dir: Path) -> Path:
    """
    функция определения пути к исполняемому файлу python в виртуальном окружении
    в зависимости от типа операционной системы
    """
    assert isinstance(venv_dir, Path)
    current_os = get_current_os()
    if current_os == OsClass.WINDOWS_CLASS:
        result = venv_dir / 'Scripts' / 'python.exe'
    elif current_os == OsClass.LINUX_CLASS:
        result = venv_dir / 'bin' / 'python3'
    else:
        raise NotImplementedError('Unsupported os')
    return result


def get_building_dir():
    """
    функция получения необходимой для создания исполняемого файла приложения 'simple_gram' директории
    в зависимости от типа операционной системы
    """
    current_os = get_current_os()
    if current_os == OsClass.WINDOWS_CLASS:
        result = get_script_dir() / 'windows'
    elif current_os == OsClass.LINUX_CLASS:
        result = get_script_dir() / 'linux'
    else:
        raise NotImplementedError('Unsupported os')
    return result

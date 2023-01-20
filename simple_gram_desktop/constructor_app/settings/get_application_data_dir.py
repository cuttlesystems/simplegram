import os
import sys
from typing import Optional
from pathlib import Path
import platform


def get_application_data_dir() -> Path:
    path: Optional[Path] = None
    result: Optional[Path] = None
    current_os = platform.system()
    if current_os == "Linux" or current_os == 'Darwin':
        path = Path.home()
        result = path / '.cuttle_systems' / 'bot_constructor'
    elif current_os == "Windows":
        path = Path(os.getenv('APPDATA'))
        result = path / 'cuttle_systems' / 'bot_constructor'
    else:
        raise NotImplementedError(f'Unsupported os: {current_os}')
    return result


def is_run_from_source() -> bool:
    return not getattr(sys, 'frozen', False)


def get_application_executable_dir() -> Path:
    if is_run_from_source():
        path = Path(__file__).parent.parent.parent
    else:
        path = Path(sys.executable).parent

    return path

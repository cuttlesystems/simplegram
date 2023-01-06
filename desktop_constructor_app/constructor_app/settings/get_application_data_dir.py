import os
from typing import Optional
from pathlib import Path
import platform


def get_application_data_dir() -> Path:
    path: Optional[Path] = None
    result: Optional[Path] = None
    current_os = platform.system()
    if current_os == "Linux":
        path = Path.home()
        result = path / '.cuttle_systems' / 'bot_constructor'
    elif current_os == "Windows":
        path = Path(os.getenv('APPDATA'))
        result = path / 'cuttle_systems' / 'bot_constructor'
    else:
        raise NotImplementedError(f'Unsupported os: {current_os}')
    return result


def get_application_executable_dir() -> Path:
    # todo: это для случая исполняемого файла скорее всего не будет работать,
    #  нужно будет проверить и рассмотреть этот случай
    return Path(__file__).parent.parent.parent.parent

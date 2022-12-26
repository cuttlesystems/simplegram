import os
from pathlib import Path
import platform


def get_application_data_dir() -> Path:
    path: Path = None
    current_os = platform.system()
    result: Path = None
    if current_os == "Linux":
        path = Path.home()
        result = path / '.cuttle_systems' / 'bot_constructor'
    elif current_os == "Windows":
        path = Path(os.getenv('APPDATA'))
        result = path / 'cuttle_systems' / 'bot_constructor'
    return result

import os
from pathlib import Path
import platform


def get_application_data_dir() -> Path:
    path: Path = None
    current_os = platform.system()
    if current_os == "Linux":
        path = Path('/var/lib')
    elif current_os == "Windows":
        path = Path(os.getenv('APPDATA'))

    return path / 'cuttle_systems' / 'bot_constructor'

import os
from pathlib import Path


def get_application_data_dir() -> Path:
    return Path(os.getenv('APPDATA')) / 'cuttle_systems' / 'bot_constructor'

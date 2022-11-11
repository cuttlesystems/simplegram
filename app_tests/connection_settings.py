import json
from pathlib import Path
from typing import Optional


class ConnectionSettings:
    def __init__(self, filename: Optional[str] = None):
        if filename is None:
            filename = str(Path(__file__).parent / 'connection_settings.json')
        if not Path(filename).exists():
            raise Exception(
                f'Создайте себе персональный файл с настройками {filename} по'
                ' примеру из connection_settings_template.json')
        with open(filename, 'r') as settings_file:
            settings_dict = json.load(settings_file)
        self._site_addr: str = settings_dict['suite_addr']
        self._username: str = settings_dict['username']
        self._password: str = settings_dict['password']
        self._bot_id: Optional[int] = settings_dict['bot_id']

    @property
    def site_addr(self) -> str:
        return self._site_addr

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def bot_id(self) -> Optional[int]:
        return self._bot_id

import json
from pathlib import Path


class ConnectionSettings:
    def __init__(self, filename: str):
        if not Path(filename).exists():
            raise Exception(
                'Создайте себе персональный файл с настройками connection_settings.json по'
                ' примеру из connection_settings_template.json')
        with open(filename, 'r') as settings_file:
            settings_dict = json.load(settings_file)
        self._site_addr = settings_dict['suite_addr']
        self._username = settings_dict['username']
        self._password = settings_dict['password']
        self._bot_id: int = settings_dict['bot_id']

    @property
    def site_addr(self):
        return self._site_addr

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def bot_id(self):
        return self._bot_id

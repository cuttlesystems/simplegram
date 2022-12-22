import base64
import json
import os
from pathlib import Path

from cryptography.fernet import Fernet

from desktop_constructor_app.constructor_app.utils.application_settings import get_application_data_dir
from desktop_constructor_app.data_objects import Settings


class ApplicationSettings:

    def __init__(self, path_to_storage, key):
        print(key)
        self.fernet = Fernet(key)
        self.path_to_storage: Path = path_to_storage

    def read_settings(self):
        settings_path = self._get_application_settings_path()
        if not settings_path.exists():
            return Settings()
        with open(settings_path) as file:
            data = json.load(file)
            settings = self._dict_to_settings(data)
            return settings

    def write_settings(self, settings: Settings):
        self._create_settings_dir_if_not_exist()
        settings_path = self._get_application_settings_path()
        data = self._settings_to_dict(settings)
        with open(settings_path, 'w+') as outfile:
            json.dump(data, outfile, indent=4)

    def _get_application_settings_path(self):
        settings_path = self.path_to_storage / 'data.json'
        return settings_path

    def _create_settings_dir_if_not_exist(self):
        # создаем path_to_storage если не существует
        if not self.path_to_storage.exists():
            self.path_to_storage.mkdir(exist_ok=True, parents=True)

    def _settings_to_dict(self, settings: Settings):
        encrypted_password = self.fernet.encrypt(settings.password.encode('utf-8'))
        data = {
            'address': settings.address,
            'name': settings.name,
            'password': base64.b64encode(encrypted_password).decode('utf-8')}
        return data

    def _dict_to_settings(self, data: dict):
        coded_bytes = base64.b64decode(data['password'])
        print(coded_bytes)
        settings = Settings()
        settings.address = data['address']
        settings.name = data['name']
        settings.password = self.fernet.decrypt(coded_bytes).decode('utf-8')
        return settings

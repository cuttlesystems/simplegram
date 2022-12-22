import base64
import json
from pathlib import Path

from cryptography.fernet import Fernet

from desktop_constructor_app.data_objects import Settings


class ApplicationSettings:

    def __init__(self, path_to_storage: Path, key: bytes):
        assert isinstance(path_to_storage, Path)
        assert isinstance(key, bytes)
        self._fernet = Fernet(key)
        self._path_to_storage: Path = path_to_storage

    def read_settings(self) -> Settings:
        settings_path = self._get_application_settings_path()
        settings = Settings()
        if settings_path.exists():
            with open(settings_path) as file:
                data = json.load(file)
                settings = self._dict_to_settings(data)
        return settings

    def write_settings(self, settings: Settings) -> None:
        assert isinstance(settings, Settings)
        self._create_settings_dir_if_not_exist()
        settings_path = self._get_application_settings_path()
        data = self._settings_to_dict(settings)
        with open(settings_path, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def _get_application_settings_path(self) -> Path:
        settings_path = self._path_to_storage / 'data.json'
        return settings_path

    def _create_settings_dir_if_not_exist(self) -> None:
        # создаем path_to_storage если не существует
        if not self._path_to_storage.exists():
            self._path_to_storage.mkdir(exist_ok=True, parents=True)

    def _encrypt(self, password: str):
        encrypted_password_bytes = self._fernet.encrypt(password.encode('utf-8'))
        encrypted_password_str = base64.b64encode(encrypted_password_bytes).decode('utf-8')
        return encrypted_password_str

    def _settings_to_dict(self, settings: Settings) -> dict:
        assert isinstance(settings, Settings)
        encrypted_password = self._encrypt(settings.password)
        data = {
            'address': settings.address,
            'name': settings.name,
            'password': encrypted_password
        }
        return data

    def _decrypt(self, encrypted_password):
        encrypted_password_bytes = base64.b64decode(encrypted_password)
        password = self._fernet.decrypt(encrypted_password_bytes).decode('utf-8')
        return password

    def _dict_to_settings(self, data: dict) -> Settings:
        assert isinstance(data, dict)
        password = self._decrypt(data['password'])
        settings = Settings()
        settings.address = data['address']
        settings.name = data['name']
        settings.password = password
        return settings

# if __name__ == '__main__':
#     app = ApplicationSettings(get_application_data_dir(), b'OCbAwQH4JA9ID-5gJB4nvk4UbNwpHx4wNT5O5VNKcGI=')
#     app.write_settings(Settings(
#         name='admin',
#         password='admin',
#         address='localhost'
#     ))
#     print('start')

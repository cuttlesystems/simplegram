import base64
import json
from pathlib import Path
from typing import Optional

from cryptography.fernet import Fernet

from constructor_app.settings.login_settings import LoginSettings


class LoginSettingsManager:
    def __init__(self, path_to_storage: Path, key: bytes):
        assert isinstance(path_to_storage, Path)
        assert isinstance(key, bytes)
        self._fernet = Fernet(key)
        self._path_to_storage: Path = path_to_storage

    def read_settings(self) -> LoginSettings:
        settings_path = self._get_application_settings_path()
        settings = LoginSettings()
        if settings_path.exists():
            with open(settings_path) as file:
                data = json.load(file)
                settings = self._dict_to_settings(data)
        return settings

    def write_settings(self, settings: LoginSettings) -> None:
        assert isinstance(settings, LoginSettings)
        self._create_settings_dir_if_not_exist()
        settings_path = self._get_application_settings_path()
        data = self._settings_to_dict(settings)
        with open(settings_path, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def _get_application_settings_path(self) -> Path:
        settings_path = self._path_to_storage / 'login_form_settings.json'
        return settings_path

    def _create_settings_dir_if_not_exist(self) -> None:
        # создаем path_to_storage если не существует
        if not self._path_to_storage.exists():
            self._path_to_storage.mkdir(exist_ok=True, parents=True)

    def _encrypt(self, password: Optional[str]) -> str:
        if password is not None:
            encrypted_password_bytes = self._fernet.encrypt(password.encode('utf-8'))
            encrypted_password_str = base64.b64encode(encrypted_password_bytes).decode('utf-8')
        else:
            encrypted_password_str = None
        return encrypted_password_str

    def _settings_to_dict(self, settings: LoginSettings) -> dict:
        assert isinstance(settings, LoginSettings)
        encrypted_password = self._encrypt(settings.password)
        data = {
            'address': settings.address,
            'name': settings.name,
            'password': encrypted_password,
            'save_password': settings.save_password
        }
        return data

    def _decrypt(self, encrypted_password: Optional[str]) -> str:
        if encrypted_password is not None:
            encrypted_password_bytes = base64.b64decode(encrypted_password)
            password = self._fernet.decrypt(encrypted_password_bytes).decode('utf-8')
        else:
            password = None
        return password

    def _dict_to_settings(self, data: dict) -> LoginSettings:
        assert isinstance(data, dict)
        password = self._decrypt(data['password'])
        settings = LoginSettings()
        settings.address = data['address']
        settings.name = data['name']
        settings.password = password
        settings.save_password = data.get('save_password', True)
        return settings


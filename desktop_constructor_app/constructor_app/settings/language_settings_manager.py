import json
from pathlib import Path

from desktop_constructor_app.constructor_app.settings.get_application_data_dir import get_application_data_dir
from desktop_constructor_app.constructor_app.settings.language_settings import LanguageSettings
from desktop_constructor_app.constructor_app.settings.languages_enum import LanguagesEnum


class LanguageSettingsManager:
    def __init__(self):
        self._path_to_storage: Path = get_application_data_dir()

    def read_settings(self) -> LanguageSettings:
        settings_path = self._get_application_settings_path()
        settings = LanguageSettings()
        if settings_path.exists():
            with open(settings_path) as file:
                data = json.load(file)
                settings = self._dict_to_settings(data)
        return settings

    def write_settings(self, settings: LanguageSettings) -> None:
        assert isinstance(settings, LanguageSettings)
        self._create_settings_dir_if_not_exist()
        settings_path = self._get_application_settings_path()
        data = self._settings_to_dict(settings)
        with open(settings_path, 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def _get_application_settings_path(self) -> Path:
        settings_path = self._path_to_storage / 'language_settings.json'
        return settings_path

    def _create_settings_dir_if_not_exist(self) -> None:
        # создаем path_to_storage если не существует
        if not self._path_to_storage.exists():
            self._path_to_storage.mkdir(exist_ok=True, parents=True)

    def _settings_to_dict(self, settings: LanguageSettings) -> dict:
        assert isinstance(settings, LanguageSettings)
        data = {
            'language': settings.language.value,
        }
        return data

    def _dict_to_settings(self, data: dict) -> LanguageSettings:
        assert isinstance(data, dict)
        settings = LanguageSettings()
        settings.language = LanguagesEnum(data['language'])
        return settings


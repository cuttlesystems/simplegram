import typing
from pathlib import Path

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication

from constructor_app.settings.get_application_data_dir import get_application_executable_dir
from constructor_app.settings.language_settings_manager import LanguageSettingsManager
from constructor_app.settings.languages_enum import LanguagesEnum


class LanguageException(Exception):
    pass


class LanguageManager:
    """
    Класс для настройки языка Qt приложения
    """

    def __init__(self):
        self._languages = [language for language in LanguagesEnum]

        # важно, чтобы объект переводчика хранился в классе, чтобы время жизни переменной переводчика
        # было: все время работы приложения
        self._translator: typing.Optional[QTranslator] = None

    def check(self) -> None:
        files = [self._get_language_file(language) for language in self._languages]
        for file in files:
            if not file.exists():
                raise LanguageException(f'Can not found translation file: {file}')

    def configure_language_by_settings(self, app: QApplication) -> None:
        assert isinstance(app, QApplication)
        settings_manager = LanguageSettingsManager()
        language_settings = settings_manager.read_settings()
        self._translator = QTranslator()
        self._translator.load(str(self._get_language_file(language_settings.language)))
        app.installTranslator(self._translator)

    def _get_language_file(self, language: LanguagesEnum) -> Path:
        assert isinstance(language, LanguagesEnum)
        language_code = language.value
        return (
            get_application_executable_dir() / 'desktop_constructor_app' /
            'constructor_app' / 'translations' / f'bot_constructor_{language_code}.qm'
        )

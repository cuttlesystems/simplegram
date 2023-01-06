from pathlib import Path

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication

from desktop_constructor_app.constructor_app.settings.language_settings_manager import LanguageSettingsManager
from desktop_constructor_app.constructor_app.settings.languages_enum import LanguagesEnum


class LanguageException(Exception):
    pass


class LanguageManager:
    def __init__(self):
        self._languages = [language for language in LanguagesEnum]

    def check(self):
        files = [self._get_language_file(language) for language in self._languages]
        for file in files:
            if not file.exists():
                raise LanguageException(f'Can not found translation file: {file}')

    def configure_language_by_settings(self, app: QApplication):
        assert isinstance(app, QApplication)
        settings_manager = LanguageSettingsManager()
        language_settings = settings_manager.read_settings()
        translator = QTranslator()
        translator.load(str(self._get_language_file(language_settings.language)))
        app.installTranslator(translator)

    def _get_language_file(self, language: LanguagesEnum) -> Path:
        assert isinstance(language, LanguagesEnum)
        language_code = language.value
        return (
            Path('desktop_constructor_app') /
            'constructor_app' / 'translations' / f'bot_constructor_{language_code}.qm'
        )

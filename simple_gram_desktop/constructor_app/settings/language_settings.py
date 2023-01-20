import dataclasses

from constructor_app.settings.languages_enum import LanguagesEnum


@dataclasses.dataclass
class LanguageSettings:
    language: LanguagesEnum = LanguagesEnum.ENGLISH

import dataclasses

from constructor_app.settings.languages_enum import LanguagesEnum


@dataclasses.dataclass(slots=True)
class LanguageSettings:
    language: LanguagesEnum = LanguagesEnum.ENGLISH

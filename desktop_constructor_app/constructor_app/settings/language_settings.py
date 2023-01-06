import dataclasses

from desktop_constructor_app.constructor_app.utils.language_manager import LanguagesEnum


@dataclasses.dataclass
class LanguageSettings:
    language: LanguagesEnum = LanguagesEnum.ENGLISH

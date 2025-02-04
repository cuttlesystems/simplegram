import sys
from PySide6.QtWidgets import QApplication
from utils.compile_resources import compile_all_resources


if __name__ == "__main__":
    # сначала нужно скомпилировать все ресурсы
    compile_all_resources()

    # и только потом есть уверенность, что импорты (которые могут быть на ui_*.py) пройдут правильно
    import constructor_app.rc_bot_icons
    from constructor_app.utils.application_style import print_available_styles
    from constructor_app.settings.language_manager import LanguageManager
    from constructor_app.windows_manager import WindowsManager

    print_available_styles()

    app = QApplication(sys.argv)

    language_manager = LanguageManager()
    language_manager.check()
    language_manager.configure_language_by_settings(app)

    # ссылаемся на модуль, чтобы он не удалился при автоматическом рефакторинге
    _rc_module = constructor_app.rc_bot_icons

    windows_manager = WindowsManager()
    windows_manager.start()
    sys.exit(app.exec())

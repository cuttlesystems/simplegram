from PySide6.QtWidgets import QApplication
import constructor_app.rc_bot_icons
from constructor_app.utils.application_style import print_available_styles
from constructor_app.settings.language_manager import LanguageManager
from constructor_app.windows_manager import WindowsManager
from utils.compile_resources import compile_all_resources
import sys


if __name__ == "__main__":
    print_available_styles()
    compile_all_resources()

    app = QApplication(sys.argv)

    language_manager = LanguageManager()
    language_manager.check()
    language_manager.configure_language_by_settings(app)

    # ссылаемся на модуль, чтобы он не удалился при автоматическом рефакторинге
    _rc_module = constructor_app.rc_bot_icons

    windows_manager = WindowsManager()
    windows_manager.start()
    sys.exit(app.exec())

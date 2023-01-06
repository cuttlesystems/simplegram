import sys
from pathlib import Path

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication
import desktop_constructor_app.constructor_app.rc_bot_icons
from desktop_constructor_app.constructor_app.utils.application_style import print_available_styles
from desktop_constructor_app.constructor_app.windows_manager import WindowsManager


if __name__ == "__main__":
    print_available_styles()

    app = QApplication(sys.argv)
    translator = QTranslator()
    translator.load(str(Path('desktop_constructor_app') / 'bot_constructor_ru.qm'))
    app.installTranslator(translator)

    # ссылаемся на модуль, чтобы он не удалился при автоматическом рефакторинге
    _rc_module = desktop_constructor_app.constructor_app.rc_bot_icons

    windows_manager = WindowsManager()
    windows_manager.start()
    sys.exit(app.exec())

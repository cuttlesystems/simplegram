import sys
from PySide6.QtWidgets import QApplication
from desktop_constructor_app.constructor_app.windows_manager import WindowsManager
import desktop_constructor_app.constructor_app.rc_bot_icons


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ссылаемся на модуль, чтобы он не удалился при автоматическом рефакторинге
    _rc_module = desktop_constructor_app.constructor_app.rc_bot_icons

    windows_manager = WindowsManager()
    windows_manager.start()
    sys.exit(app.exec())

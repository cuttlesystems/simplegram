import sys

from PySide6.QtWidgets import QApplication
import constructor_app.rc_bot_icons
from constructor_app.utils.application_style import print_available_styles
from constructor_app.settings.language_manager import LanguageManager
from constructor_app.widgets.client_widget import ClientWidget
from constructor_app.windows_manager import WindowsManager


if __name__ == "__main__":
    print_available_styles()

    app = QApplication(sys.argv)

    language_manager = LanguageManager()
    language_manager.check()
    language_manager.configure_language_by_settings(app)

    # ссылаемся на модуль, чтобы он не удалился при автоматическом рефакторинге
    _rc_module = constructor_app.rc_bot_icons

    client_widget = ClientWidget()
    client_widget.show()
    sys.exit(app.exec())

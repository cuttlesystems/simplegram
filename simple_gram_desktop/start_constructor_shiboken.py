import sys

from PySide6.QtWidgets import QApplication
from utils.compile_resources import compile_all_resources

def main():
    compile_all_resources()

    # и потом можно выполнить импорты, поскольку они могут появиться после компиляции
    import constructor_app.rc_bot_icons
    from constructor_app.settings.language_manager import LanguageManager
    from constructor_app.utils.application_style import print_available_styles
    from constructor_app.widgets.client_widget import ClientWidget

    print_available_styles()

    app = QApplication(sys.argv)

    language_manager = LanguageManager()
    language_manager.check()
    language_manager.configure_language_by_settings(app)

    # ссылаемся на модуль, чтобы он не удалился при автоматическом рефакторинге
    _rc_module = constructor_app.rc_bot_icons

    client_widget = ClientWidget()
    currentExitCode = -11231351

    while currentExitCode == client_widget.EXIT_CODE_REBOOT:
        client_widget.show()
        currentExitCode = app.exec()
        return currentExitCode


if __name__ == "__main__":
    main()

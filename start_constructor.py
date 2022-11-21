import sys

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication

from b_logic.bot_api import BotApi
from b_logic.data_objects import BotDescription
from desktop_constructor_app.constructor_app.bot_editor_form import BotEditorForm
from desktop_constructor_app.constructor_app.login_form import LoginForm


class WindowsManager(QObject):
    def __init__(self):
        super().__init__()
        self._login_form = LoginForm(None, bot_api)
        self._bot_editor_form = BotEditorForm(None)

        self._login_form.open_bot_signal.connect(self._on_open_bot)
        self._bot_editor_form.close_bot.connect(self._on_close_bot)

        self._login_form.show()

    def show_login(self):
        self._login_form.show()

    def _on_open_bot(self, bot: BotDescription):
        print('open bot', bot)
        self._bot_editor_form.set_bot(bot)
        self._login_form.hide()
        self._bot_editor_form.show()

    def _on_close_bot(self):
        print('close bot')
        self._bot_editor_form.hide()
        self._login_form.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot_api = BotApi()
    windows_manager = WindowsManager()
    windows_manager.show_login()

    sys.exit(app.exec())

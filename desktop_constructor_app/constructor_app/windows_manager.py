from PySide6.QtCore import QObject

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from b_logic.data_objects import BotDescription
from desktop_constructor_app.constructor_app.widgets.bot_editor_form import BotEditorForm
from desktop_constructor_app.constructor_app.widgets.login_form import LoginForm


class WindowsManager(QObject):
    def __init__(self):
        super().__init__()
        bot_api = BotApiByRequests()
        self._login_form = LoginForm(None, bot_api)
        self._bot_editor_form = BotEditorForm(None, bot_api)

        self._login_form.open_bot_signal.connect(self._on_open_bot)
        self._bot_editor_form.close_bot.connect(self._on_close_bot)

        self._login_form.show()

    def start(self) -> None:
        self._login_form.show()

    def _on_open_bot(self, bot: BotDescription):
        print('open bot', bot)
        self._bot_editor_form.set_bot(bot)
        self._login_form.hide()
        self._bot_editor_form.show()

    def _on_close_bot(self):
        print('close bot')
        self._bot_editor_form.hide()
        self._login_form.login_to_server()
        self._login_form.show()

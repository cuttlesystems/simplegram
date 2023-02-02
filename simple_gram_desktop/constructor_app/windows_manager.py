from PySide6.QtCore import QObject

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from b_logic.data_objects import BotDescription
from constructor_app.widgets.bot_editor.bot_editor_form import BotEditorForm
from constructor_app.widgets.login_form import LoginForm
from constructor_app.widgets.sign_up_form import SignUpForm
from network.bot_api_by_request_extended import BotApiByRequestsProxy


class WindowsManager(QObject):
    def __init__(self):
        super().__init__()
        bot_api = BotApiByRequestsProxy()
        self._login_form = LoginForm(None, bot_api)
        self._bot_editor_form = BotEditorForm(None, bot_api)
        self._sign_up_form = SignUpForm(None, bot_api)

        self._login_form.open_bot_signal.connect(self._on_open_bot)
        self._login_form.sign_up_signal.connect(self._on_login_form_sign_up)
        self._bot_editor_form.close_bot.connect(self._on_close_bot)
        self._sign_up_form.sign_up_success_signal.connect(self._on_success_sign_up)
        self._sign_up_form.sign_up_close_signal.connect(self._on_close_sign_up)
        self._sign_up_form.sign_up_server_address_error_signal.connect(self._on_server_address_error)

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

    def _on_login_form_sign_up(self, server_addr):
        print('sign up')
        self._login_form.hide()
        self._sign_up_form.server_addr = server_addr
        self._sign_up_form.show()

    def _on_success_sign_up(self):
        print('success sign up')
        self._sign_up_form.hide()
        self._login_form.show()

    def _on_close_sign_up(self):
        print('closed sign up')
        self._login_form.show()

    def _on_server_address_error(self):
        print('fill in server address')
        self._sign_up_form.hide()
        self._login_form.show()

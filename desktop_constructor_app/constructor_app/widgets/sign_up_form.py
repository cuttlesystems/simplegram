# This Python file uses the following encoding: utf-8
import typing
from enum import Enum

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QPixmap, QCloseEvent
from PySide6.QtWidgets import QWidget, QLineEdit, QMessageBox, QListWidgetItem, QPushButton
from six import b

from b_logic.bot_api.bot_api_by_requests import BotApiByRequests
from b_logic.bot_api.i_bot_api import BotApiException
from desktop_constructor_app.constructor_app.widgets.ui_sign_up_form import Ui_SignUpForm

SERVER_URL: str = 'http://127.0.0.1:8000/'


class SignUpForm(QWidget):
    """
    Окно регистрации.
    """

    sign_up_success_signal = Signal()
    sign_up_close_signal = Signal()

    def __init__(self, parent: typing.Optional[QWidget], bot_api: BotApiByRequests):
        super().__init__(parent)
        self._bot_api = bot_api
        self._ui = Ui_SignUpForm()
        self._ui.setupUi(self)
        self._ui.sign_up_user_button.clicked.connect(self._on_sing_up_form_sign_up)

    def _on_sing_up_form_sign_up(self, checked):
        username: QLineEdit = self._ui.username_line_edit
        email: QLineEdit = self._ui.email_line_edit
        password: QLineEdit = self._ui.password_line_edit

        for field in (username, email, password):
            if not field.text():
                error = QMessageBox()
                error.warning(self, 'Error', f'It is necessary to fill in the field {field.objectName()}')

        try:
            self._bot_api.set_suite(SERVER_URL)
            self._bot_api.sign_up(
                username=username.text(),
                email=email.text(),
                password=password.text()
            )
            QMessageBox.information(self, 'Success', f'User {username.text()} created successfully')
            self.sign_up_success_signal.emit()
        except BotApiException as bot_api_exception:
            QMessageBox.critical(self, 'Error', str(bot_api_exception))

    def closeEvent(self, event: QCloseEvent) -> None:
        self.sign_up_close_signal.emit()
        event.accept()
